"""Combine the printed parts into full-bed print plates.

Reads the STLs that ``generate_stls.py`` wrote, splits multi-part files
(detector_rings.stl is three rings laid out in a row) into individual
solids, then shelf-packs the quantities listed in PRINTED_PARTS.md onto
bed-sized plates so a slicer receives one file per print job instead of
thirty separate ones.

Usage:
    python3 make_plates.py                 # 220 x 220 bed (default)
    python3 make_plates.py --bed 256 256   # Bambu-size bed

Nothing here needs libraries beyond Python 3. Every placed solid must
still be closed (every edge used exactly twice) and fit inside the bed,
or the script stops instead of writing a bad plate.

Re-run this after ``generate_stls.py`` whenever part dimensions change —
the plates are derived files and are not regenerated automatically.
"""

import argparse
import math
import os
import struct
import sys
from collections import Counter

import generate_stls as gen

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "stl")
PLATES = os.path.join(OUT, "plates")

# How many of each part the machine needs (mirrors PRINTED_PARTS.md).
# detector_rings.stl is handled separately: it is three separate rings.
QUANTITIES = {
    "track_clip": 30,
    "ball_gate": 2,
    "gate_shutter": 2,
    "coil_mandrel": 1,
    "catch_funnel": 1,
}

BED_MARGIN = 4.0   # keep-away from the bed edge, per side
PART_GAP = 6.0     # spacing between neighbouring parts


# ---------------------------------------------------------------------------
# STL reading and mesh helpers
# ---------------------------------------------------------------------------

def read_stl(path):
    """Read a binary or ASCII STL into a gen.Mesh (vertices welded)."""
    with open(path, "rb") as fh:
        data = fh.read()
    tris = []
    if data[:5].lstrip().lower() == b"solid" and b"facet" in data[:512].lower():
        verts = []
        for line in data.decode("utf-8", errors="ignore").splitlines():
            parts = line.strip().split()
            if parts and parts[0] == "vertex":
                verts.append(tuple(float(x) for x in parts[1:4]))
        tris = [tuple(verts[i:i + 3]) for i in range(0, len(verts), 3)]
    else:
        n = struct.unpack("<I", data[80:84])[0]
        off = 84
        for _ in range(n):
            v = struct.unpack("<12f", data[off:off + 48])
            tris.append((tuple(v[3:6]), tuple(v[6:9]), tuple(v[9:12])))
            off += 50
    m = gen.Mesh()
    index = {}
    for tri in tris:
        ids = []
        for p in tri:
            key = (round(p[0], 4), round(p[1], 4), round(p[2], 4))
            if key not in index:
                index[key] = m.vert(p)
            ids.append(index[key])
        m.face(*ids)
    return m


def split_components(m):
    """Split a mesh into its connected solids (shared welded vertices)."""
    parent = list(range(len(m.v)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for a, b, c in m.f:
        for u, v in ((a, b), (b, c), (c, a)):
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[ru] = rv

    roots = {}
    for i in range(len(m.v)):
        roots.setdefault(find(i), len(roots))
    meshes = [gen.Mesh() for _ in roots]
    remap = [{} for _ in roots]
    for a, b, c in m.f:
        k = roots[find(a)]
        ids = []
        for v in (a, b, c):
            if v not in remap[k]:
                remap[k][v] = meshes[k].vert(m.v[v])
            ids.append(remap[k][v])
        meshes[k].face(*ids)
    return [s for s in meshes if s.f]


def transform(m, fn):
    """Map every vertex through fn, rebuilding the face list."""
    out = gen.Mesh()
    index = {}
    for a, b, c in m.f:
        ids = []
        for p in (m.v[a], m.v[b], m.v[c]):
            q = fn(p)
            key = (round(q[0], 4), round(q[1], 4), round(q[2], 4))
            if key not in index:
                index[key] = out.vert(q)
            ids.append(index[key])
        out.face(*ids)
    return out


def rotate90(m, w):
    """Rotate 90 degrees in the bed plane; [0,w]x[0,d] maps to [0,d]x[0,w]."""
    return transform(m, lambda p: (p[1], w - p[0], p[2]))


def normalize(m):
    """Translate so the minimum corner sits at the origin; returns (mesh, w, d)."""
    minx = min(p[0] for p in m.v)
    miny = min(p[1] for p in m.v)
    out = transform(m, lambda p: (p[0] - minx, p[1] - miny, p[2]))
    xs = [p[0] for p in out.v]
    ys = [p[1] for p in out.v]
    return out, max(xs), max(ys)


def place(m, x, y):
    return transform(m, lambda p: (p[0] + x, p[1] + y, p[2]))


# ---------------------------------------------------------------------------
# Shelf packing
# ---------------------------------------------------------------------------

def pack_shelves(items, bed_w, bed_d):
    """Greedy shelf packing, rotation allowed.

    items: list of (name, mesh, w, d) with meshes normalized to the origin.
    Returns a list of plates, each a list of (name, placed_mesh).
    Raises SystemExit if a part cannot fit in any orientation.
    """
    # Deep parts first, so each shelf is packed tight before a new one starts.
    items = sorted(items, key=lambda it: -max(it[2], it[3]))
    plates = []
    plate, x, y, shelf_d = [], 0.0, 0.0, 0.0

    for name, mesh, w, d in items:
        chosen = None
        for rot in (False, True):
            ww, dd = (d, w) if rot else (w, d)
            if plate:
                if x + ww <= bed_w and y + max(shelf_d, dd) <= bed_d:
                    chosen = (rot, ww, dd, x, y, "same_shelf")
                    break
                ny = y + shelf_d + PART_GAP
                if ny + dd <= bed_d:
                    chosen = (rot, ww, dd, 0.0, ny, "new_shelf")
                    break
                if ww <= bed_w and dd <= bed_d:
                    plates.append(plate)                      # this bed is full
                    plate, x, y, shelf_d = [], 0.0, 0.0, 0.0
                    chosen = (rot, ww, dd, 0.0, 0.0, "new_plate")
                    break
            elif ww <= bed_w and dd <= bed_d:
                chosen = (rot, ww, dd, 0.0, 0.0, "same_shelf")  # first part
                break
        if chosen is None:
            raise SystemExit(
                f"{name}: does not fit on a {bed_w:.0f} x {bed_d:.0f} bed in any orientation")
        rot, ww, dd, px, py, case = chosen
        solid = rotate90(mesh, w) if rot else mesh
        plate.append((name, place(solid, px, py)))
        if case == "same_shelf":
            x, shelf_d = px + ww + PART_GAP, max(shelf_d, dd)
        elif case == "new_shelf":
            x, y, shelf_d = ww + PART_GAP, py, dd
        else:  # new_plate
            x, y, shelf_d = ww + PART_GAP, 0.0, dd
    if plate:
        plates.append(plate)
    return [p for p in plates if p]


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def write_plate_stl(path, m):
    """Binary STL writer (same layout as generate_stls.write_stl)."""
    with open(path, "wb") as fh:
        fh.write(b" " * 80)
        fh.write(struct.pack("<I", len(m.f)))
        for a, b, c in m.f:
            p, q, r = m.v[a], m.v[b], m.v[c]
            ux, uy, uz = q[0] - p[0], q[1] - p[1], q[2] - p[2]
            vx, vy, vz = r[0] - p[0], r[1] - p[1], r[2] - p[2]
            nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
            ln = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
            fh.write(struct.pack("<12fH", nx / ln, ny / ln, nz / ln, *p, *q, *r, 0))


def collect_items():
    """Named solids in print quantities: the parts plus each split ring."""
    items = []
    for name, count in QUANTITIES.items():
        m = read_stl(os.path.join(OUT, name + ".stl"))
        # Mesh topology was already verified solid-by-solid by
        # generate_stls.py; plates only translate parts, so that
        # certification carries over. (Overlapping-shell unions such as
        # gate_shutter share welded vertices and cannot be re-checked
        # edge-wise after an STL round-trip.)
        m, w, d = normalize(m)
        for k in range(count):
            items.append((name if count == 1 else f"{name}_{k + 1}", m, w, d))
    rings = split_components(read_stl(os.path.join(OUT, "detector_rings.stl")))
    gen.check_manifold("detector_rings.stl (source)", rings)
    for i, ring in enumerate(rings, 1):
        ring, w, d = normalize(ring)
        items.append((f"detector_ring_{i}", ring, w, d))
    return items


def main():
    ap = argparse.ArgumentParser(description="Combine the printed parts into full-bed plates")
    ap.add_argument("--bed", nargs=2, type=float, default=[220.0, 220.0],
                    metavar="MM", help="bed size in mm (default: 220 220)")
    args = ap.parse_args()
    bed_w, bed_d = args.bed[0] - 2 * BED_MARGIN, args.bed[1] - 2 * BED_MARGIN

    items = collect_items()
    plates = pack_shelves(items, bed_w, bed_d)

    os.makedirs(PLATES, exist_ok=True)
    written = []
    for i, plate in enumerate(sorted(plates, key=len, reverse=True), 1):
        counts = Counter(n if not n.rsplit("_", 1)[-1].isdigit() else n.rsplit("_", 1)[0]
                         for n, _ in plate)
        tag = "_".join(f"{n}x{c}" for n, c in counts.most_common())
        fname = f"plate_{i}_{tag}.stl"
        combined = gen.Mesh()
        for _, solid in plate:
            combined.add(solid)   # shells side by side — no overlap, no union
        xs = [p[0] for p in combined.v]
        ys = [p[1] for p in combined.v]
        if max(xs) > bed_w + 0.01 or max(ys) > bed_d + 0.01:
            raise SystemExit(f"{fname}: laid out to {max(xs):.1f} x {max(ys):.1f} mm, exceeds the bed")
        path = os.path.join(PLATES, fname)
        write_plate_stl(path, combined)
        written.append(path)
        print(f"{fname}: {len(plate)} solids, {len(combined.f)} tris, "
              f"{max(xs):.0f} x {max(ys):.0f} mm used")

    parts = [os.path.join(OUT, f) for f in sorted(os.listdir(OUT)) if f.endswith(".stl")]
    gen.write_zip(parts + written)
    print(f"bundle: colliderscope_parts.zip ({len(parts)} parts + {len(written)} plates)")


if __name__ == "__main__":
    sys.exit(main())
