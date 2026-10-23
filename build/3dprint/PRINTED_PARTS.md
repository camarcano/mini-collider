# 3D printed parts

Printing is **optional**. The machine works exactly as described in
`BUILD_GUIDE.md` with nothing printed at all — the parts list is written so
that a family with no printer can build the whole thing. If you do have a
printer, these six parts remove the three fiddliest jobs: gripping the tube,
winding the coils, and firing both beams at the same moment.

## The parts

| File | What it is | Print | Helps step |
|---|---|---|---|
| `stl/track_clip.stl` | Saddle clip that holds the tube to the board. Tape or glue the foot down. | ~30 | Step 3 |
| `stl/coil_mandrel.stl` | Slides inside the tube; the hex end chucks into a drill. Winds a 200-turn coil in twenty seconds instead of twenty minutes. | 1 | Step 4 |
| `stl/ball_gate.stl` | Launch gate for one beam: ball rests in the cradle, a shutter across its path holds it. | 2 | Step 5 |
| `stl/gate_shutter.stl` | The shutter that slides out to fire. Print two, tie a string between the two tabs, and **one pull fires both beams together**. | 2 | Step 5 |
| `stl/catch_funnel.stl` | Flared ring over the detector cup. Balls that bounce hit the slope and fall back in; the beads stay put. | 1 | Step 6 |
| `stl/detector_rings.stl` | Three rings the children paint: tracker, calorimeter, muon chambers. The real detector really is built in concentric layers. | 1 (all three in one file) | Step 6 |

The printed parts replace about **200 g of PLA — a few pounds of filament**.
Nothing here needs a large bed: the biggest single piece is 110 mm across.

## Print settings

These all print lying flat with **no supports and no brim** — that is a design
constraint, not a coincidence, because the parts were drawn as plain
extrusions and solids of revolution.

| Setting | Value |
|---|---|
| Material | PLA or PETG |
| Layer height | 0.2 mm |
| Perimeters (walls) | 3 |
| Infill | 15 % grid or gyroid |
| Supports | **off** |
| Brim | off (a brim helps only the mandrel, if your bed adhesion is poor) |

## The golden rule: print one, test it, then batch

**These parts have been generated and checked geometrically — closed,
manifold, printable orientation — but they have not been test-printed.** So
before you print thirty clips, print one and try it on your tube:

- **Clip too tight** (won't push on): regenerate with `SQUEEZE = 0.15`, or
  scale the STL to 102 % in your slicer.
- **Clip too loose** (tube slides about): `SQUEEZE = 0.5`, or scale to 98 %.
- **Ball gate**: the ball should sit in the cradle and be stopped by the
  shutter. If the shutter binds in its slot, `CLEAR = 0.4`.
- **Funnel**: measure the mouth of your cup or bottle. `seat_r` in the script
  is 29.5 mm for a 250 ml bottle; adjust to `your_cup_od / 2 + 0.5`.

## Changing the dimensions

Everything is parametric. Edit the block at the top of
[`generate_stls.py`](generate_stls.py), then run:

```
python3 generate_stls.py
```

It rewrites every STL in `stl/`. The numbers that matter:

| Parameter | Default | Meaning |
|---|---|---|
| `TUBE_OD` | 21.0 | **Measure your tube.** Flexible 16 mm ID PVC is commonly 21–22 mm outside, and the clips are the one part that must fit it |
| `TUBE_ID` | 16.0 | The mandrel slides inside this |
| `BALL_D` | 14.0 | Your steel balls |
| `SQUEEZE` | 0.30 | How much tighter than the tube the clip grips, per side |
| `CLEAR` | 0.30 | Sliding clearance for the shutter and the cradles, per side |

The script needs nothing but Python 3 — no CAD package, no libraries. Each
part is checked before it is written: the mesh must be closed (every edge
used exactly twice) and correctly wound, or the script stops instead of
writing a bad file.
