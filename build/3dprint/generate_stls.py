#!/usr/bin/env python3
"""Generate the Colliderscope's 3D-printable parts as STL files.

Pure Python, no dependencies. Change the PARAMETERS below, then run:

    python3 generate_stls.py

Every part here is either a straight extrusion of a flat outline or a solid
of revolution, so all of them print lying flat on the bed with no supports
and no brim. That is a design constraint, not an accident: it means a school
printer and a first-time operator can produce them.

Why each part exists is in PRINTED_PARTS.md, next to this script.
"""

import math
import os
import struct
from collections import Counter

# --------------------------------------------------------------------------
# PARAMETERS - the only numbers you should need to change
# --------------------------------------------------------------------------

TUBE_OD = 21.0        # outside diameter of your clear tubing (mm). MEASURE IT.
TUBE_ID = 16.0        # inside diameter of the tubing (mm)
BALL_D = 14.0         # steel ball diameter (mm)
SQUEEZE = 0.30        # how much tighter than the tube the clip grips (mm per side)
CLEAR = 0.30          # sliding clearance for loose-fitting parts (mm per side)
SEG = 72              # facets on a full circle - leave alone

WALL = 3.0            # general wall thickness (mm)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stl")


# --------------------------------------------------------------------------
# Mesh plumbing
# --------------------------------------------------------------------------

class Mesh:
    """Indexed triangle soup. Vertices are shared, so the manifold check works."""

    def __init__(self):
        self.v = []
        self.f = []

    def vert(self, p):
        self.v.append((float(p[0]), float(p[1]), float(p[2])))
        return len(self.v) - 1

    def face(self, a, b, c):
        self.f.append((a, b, c))

    def add(self, other, offset=(0.0, 0.0, 0.0)):
        """Union by overlap: slicers merge two closed shells that intersect."""
        base = len(self.v)
        for p in other.v:
            self.vert((p[0] + offset[0], p[1] + offset[1], p[2] + offset[2]))
        for a, b, c in other.f:
            self.face(base + a, base + b, base + c)
        return self


def map_verts(m, fn):
    for i, p in enumerate(m.v):
        m.v[i] = fn(p)
    return m


def translate(m, dx=0.0, dy=0.0, dz=0.0):
    return map_verts(m, lambda p: (p[0] + dx, p[1] + dy, p[2] + dz))


def rotate_x(m, deg):
    t = math.radians(deg)
    c, s = math.cos(t), math.sin(t)
    return map_verts(m, lambda p: (p[0], c * p[1] - s * p[2], s * p[1] + c * p[2]))


def rotate_y(m, deg):
    t = math.radians(deg)
    c, s = math.cos(t), math.sin(t)
    return map_verts(m, lambda p: (c * p[0] + s * p[2], p[1], -s * p[0] + c * p[2]))


def rotate_z(m, deg):
    t = math.radians(deg)
    c, s = math.cos(t), math.sin(t)
    return map_verts(m, lambda p: (c * p[0] - s * p[1], s * p[0] + c * p[1], p[2]))


# --------------------------------------------------------------------------
# Two solids are all the project needs
# --------------------------------------------------------------------------

def triangulate(poly):
    """Ear clipping. The outlines used here are simple, so this is enough."""
    n = len(poly)
    idx = list(range(n))
    tris = []

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def in_tri(p, a, b, c):
        d1, d2, d3 = cross(a, b, p), cross(b, c, p), cross(c, a, p)
        return (d1 >= -1e-9) and (d2 >= -1e-9) and (d3 >= -1e-9)

    if sum(cross(poly[i], poly[(i + 1) % n], poly[(i + 2) % n]) for i in range(n)) < 0:
        idx.reverse()

    guard = 0
    while len(idx) > 3 and guard < 20000:
        guard += 1
        for k in range(len(idx)):
            i0, i1, i2 = idx[k - 1], idx[k], idx[(k + 1) % len(idx)]
            a, b, c = poly[i0], poly[i1], poly[i2]
            if cross(a, b, c) <= 1e-9:
                continue
            if any(in_tri(poly[j], a, b, c)
                   for j in idx if j not in (i0, i1, i2)):
                continue
            tris.append((i0, i1, i2))
            idx.pop(k)
            break
    if len(idx) == 3:
        tris.append(tuple(idx))
    return tris


def prism(poly, thickness):
    """Extrude a closed 2-D outline (list of (x, y)) along +Z."""
    m = Mesh()
    n = len(poly)
    bottom = [m.vert((x, y, 0.0)) for x, y in poly]
    top = [m.vert((x, y, thickness)) for x, y in poly]
    for a, b, c in triangulate(poly):
        m.face(bottom[a], bottom[c], bottom[b])
        m.face(top[a], top[b], top[c])
    for i in range(n):
        j = (i + 1) % n
        m.face(bottom[i], bottom[j], top[j])
        m.face(bottom[i], top[j], top[i])
    return m


def revolve(profile, seg=SEG):
    """Revolve a 2-D (r, z) profile about the Z axis.

    Two cases:
      * solid of revolution - an open polyline whose first and last points
        sit on the axis (r == 0);
      * ring / shell - a closed loop (first point == last point), none of
        which touch the axis.
    """
    m = Mesh()
    pts = profile[:]
    loop = abs(pts[0][0] - pts[-1][0]) < 1e-9 and abs(pts[0][1] - pts[-1][1]) < 1e-9
    if loop:
        pts = pts[:-1]
    n = len(pts)

    rings = []
    for r, z in pts:
        if abs(r) < 1e-9:
            rings.append([m.vert((0.0, 0.0, z))])
        else:
            rings.append([m.vert((r * math.cos(2 * math.pi * k / seg),
                                  r * math.sin(2 * math.pi * k / seg), z))
                          for k in range(seg)])

    for i in range(n):
        j = (i + 1) % n if loop else i + 1
        if j >= n:
            continue
        a_ring, b_ring = rings[i], rings[j]
        if len(a_ring) == 1 and len(b_ring) == 1:
            continue
        if len(a_ring) == 1:
            p = a_ring[0]
            for k in range(seg):
                m.face(p, b_ring[k], b_ring[(k + 1) % seg])
        elif len(b_ring) == 1:
            p = b_ring[0]
            for k in range(seg):
                m.face(a_ring[k], p, a_ring[(k + 1) % seg])
        else:
            for k in range(seg):
                k2 = (k + 1) % seg
                m.face(a_ring[k], b_ring[k], b_ring[k2])
                m.face(a_ring[k], b_ring[k2], a_ring[k2])
    return m


# --------------------------------------------------------------------------
# Sanity checks - these run before anything is written
# --------------------------------------------------------------------------

def signed_volume(m):
    total = 0.0
    for a, b, c in m.f:
        p, q, r = m.v[a], m.v[b], m.v[c]
        total += (p[0] * (q[1] * r[2] - q[2] * r[1])
                  - p[1] * (q[0] * r[2] - q[2] * r[0])
                  + p[2] * (q[0] * r[1] - q[1] * r[0]))
    return total / 6.0


def fix_orientation(m):
    """Make every face wind outwards, whatever I got wrong above."""
    if signed_volume(m) < 0:
        m.f = [(a, c, b) for a, b, c in m.f]


def check_manifold(name, parts):
    """Every edge must be used exactly twice, once in each direction.

    Parts are checked individually, before they are combined: the combined
    solid is a union of overlapping shells, which slicers handle fine but
    which is not edge-manifold by this test.
    """
    for sub in parts:
        seen = Counter()
        for a, b, c in sub.f:
            for u, v in ((a, b), (b, c), (c, a)):
                seen[(min(u, v), max(u, v))] += 1
        bad = [e for e, n in seen.items() if n != 2]
        if bad:
            raise SystemExit(f"{name}: {len(bad)} non-manifold edges, e.g. {bad[:3]}")


def bbox(m):
    xs = [p[0] for p in m.v]
    ys = [p[1] for p in m.v]
    zs = [p[2] for p in m.v]
    return (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))


def write_stl(name, m):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name + ".stl")
    with open(path, "wb") as fh:
        fh.write(b" " * 80)
        fh.write(struct.pack("<I", len(m.f)))
        for a, b, c in m.f:
            p, q, r = m.v[a], m.v[b], m.v[c]
            ux, uy, uz = q[0] - p[0], q[1] - p[1], q[2] - p[2]
            vx, vy, vz = r[0] - p[0], r[1] - p[1], r[2] - p[2]
            nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
            ln = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
            fh.write(struct.pack("<12fH", nx / ln, ny / ln, nz / ln,
                                 *p, *q, *r, 0))
    return path


def write_zip(paths):
    """Bundle every STL into one file, so the whole set is a single download."""
    import zipfile
    path = os.path.join(OUT, "colliderscope_parts.zip")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in paths:
            z.write(p, os.path.basename(p))
    return path


# --------------------------------------------------------------------------
# The parts
# --------------------------------------------------------------------------

def arc(cx, cy, r, a0, a1, n):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * k / n)))
            for k in range(n + 1)]


def part_track_clip():
    """Saddle clip holding the tube to the board. Tape or glue the foot down."""
    r_in = TUBE_OD / 2 - SQUEEZE       # grips the tube slightly
    r_out = r_in + WALL
    length, base_t = 22.0, 3.0

    # Arch: half-annulus drawn in the X-Y plane, extruded along Z, then
    # rotated so the extrusion runs along the tube (X).
    profile = arc(0, 0, r_out, 0, 180, 32) + arc(0, 0, r_in, 180, 0, 32)
    arch = prism(profile, length)
    arch = map_verts(arch, lambda p: (p[2], p[0], p[1]))   # (u,v,w) -> (w,u,v)

    foot = prism([(-2, -r_out - 2), (length + 2, -r_out - 2),
                  (length + 2, r_out + 2), (-2, r_out + 2)], base_t)
    m = Mesh()
    m.add(foot)
    m.add(arch, offset=(0, 0, base_t - 0.4))   # sink slightly: clean union
    return [m]


def part_coil_mandrel():
    """Chuck it in a drill: winds a 200-turn coil in about twenty seconds.

    The tubing slides over the cylinder, the wire winds round the tube, the
    coil slides off. The hex end goes in the drill chuck.
    """
    r_body = TUBE_ID / 2 - 0.2
    body = revolve([(0, 0), (r_body, 0), (r_body, 60), (0, 60)])

    across_corners = 6.35 / math.cos(math.radians(30))
    hexagon = [(across_corners / 2 * math.cos(math.radians(60 * k - 30)),
                across_corners / 2 * math.sin(math.radians(60 * k - 30)))
               for k in range(6)]
    shank = prism(hexagon, 30)

    m = Mesh()
    m.add(body)
    m.add(shank, offset=(0, 0, 60 - 6))        # overlap: clean union
    return [m]


def part_ball_gate():
    """Launch gate for one beam: the ball rests in the cradle, a shutter
    across its path holds it, and pulling the shutter out lets it go.

    Print two, rotate one through 180 degrees, and a single string tied
    between the two shutters releases both beams on one pull - the
    no-electronics stand-in for the electromagnet kickers.
    """
    r_cradle = TUBE_OD / 2 + CLEAR      # matches the tube end at the mouth
    r_ball = BALL_D / 2 + CLEAR
    h = r_cradle                        # cradle and ball centres at the top
    length, width = 44.0, 34.0
    slot_x0, slot_x1, slot_bot = 13.0, 13.0 + 3.6, h - 8.0
    groove_c = 26.0

    # Cross-section in the X-Z plane, extruded across Y. Both the cradle and
    # the ball groove open upwards, so there is no undercut and no support.
    # Starts at the bottom-left corner, which is where the cradle arc begins.
    pts = arc(0, h, r_cradle, -90, 0, 24)         # seat for the tube's mouth
    pts += [(slot_x0, h), (slot_x0, slot_bot),
            (slot_x1, slot_bot), (slot_x1, h)]    # shutter slot
    pts += arc(groove_c, h, r_ball, 180, 360, 24)  # ball cradle
    pts += [(length, h), (length, 0.0)]           # close along the bottom
    block = prism(pts, width)
    # The prism was built as (x, z, width); swap the last two into place.
    map_verts(block, lambda p: (p[0], p[2], p[1]))

    m = Mesh()
    m.add(block)
    return [m]


def part_gate_shutter():
    """The sliding shutter for the ball gate. Print two, tie a string between
    the two tabs, one pull fires both beams."""
    plate = prism([(0, 0), (2.6, 0), (2.6, 50), (0, 50)], 6.0)
    tab = prism([(0, 50), (2.6, 50), (2.6, 62), (0, 62)], 11.0)
    m = Mesh()
    m.add(plate)
    m.add(tab)
    return [m]


def part_catch_funnel():
    """A flared ring that sits over the detector cup: balls that bounce hit
    the slope and fall back in, and the beads stay put."""
    seat_r = 29.5        # grips the mouth of a 250 ml bottle; measure yours
    seat_h, wall, flare_h, top_r = 6.0, 2.5, 32.0, 55.0
    prof = [(seat_r, 0), (seat_r + wall, 0), (seat_r + wall, seat_h),
            (top_r, seat_h + flare_h), (top_r - wall, seat_h + flare_h),
            (seat_r, seat_h), (seat_r, 0)]
    return [revolve(prof)]


def part_detector_rings():
    """Three paintable rings: tracker, calorimeter, muon chambers - the real
    detector really is built in concentric layers."""
    rings = []
    for inner in (31.0, 39.0, 47.0):
        prof = [(inner, 0), (inner + 3, 0), (inner + 3, 12), (inner, 12), (inner, 0)]
        rings.append(revolve(prof))
    return rings


PARTS = [
    ("track_clip", part_track_clip, "grips the tube"),
    ("coil_mandrel", part_coil_mandrel, "drill-driven coil winder"),
    ("ball_gate", part_ball_gate, "launch gate, one per beam"),
    ("gate_shutter", part_gate_shutter, "slides out to fire"),
    ("catch_funnel", part_catch_funnel, "stops bounce-outs"),
    ("detector_rings", part_detector_rings, "tracker / calorimeter / muon"),
]


def main():
    written = []
    for name, builder, blurb in PARTS:
        subs = builder()
        for sub in subs:
            fix_orientation(sub)
        check_manifold(name, subs)
        m = Mesh()
        for i, sub in enumerate(subs):
            m.add(sub, offset=(0, 140.0 * i, 0))   # lay multi-part files side by side
        path = write_stl(name, m)
        written.append(path)
        x, y, z = bbox(m)
        print(f"{name:16s} {len(m.f):5d} tris  {x:6.1f} x {y:6.1f} x {z:5.1f} mm  "
              f"{signed_volume(m) / 1000:7.2f} cm3   {os.path.basename(path)}  ({blurb})")
    print(f"bundle: {os.path.basename(write_zip(written))}")


if __name__ == "__main__":
    main()
