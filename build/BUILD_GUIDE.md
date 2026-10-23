# The Colliderscope — build guide

A table-top particle collider that two steel balls race around and crash into
each other in front of a "detector". Built from clear tubing, a board, two
homemade electromagnets, and a buzzer.

**Works offline, costs about £45, builds in an afternoon, and it is designed so
that a Year 4 child can run it themselves at a stand.**

---

## 1. What it demonstrates

| Part of our model | Real machine | Honest? |
|---|---|---|
| Clear plastic tube | the beam pipe that protons travel through | ✅ directly comparable |
| Steel ball bearing | a proton (tiny, but our ball is tiny too) | ✅ |
| Two mirrored tracks, launched at the same moment | two counter-rotating beams | ✅ |
| The long sweeping curve | the ring — the beam is bent round by magnets | ✅ |
| Electromagnet "gate" holding each ball at the start | the **kicker / injection magnets** that drop the beam into the ring | ✅ this is real: LHC beams are injected by fast kicker magnets |
| The slope / the launch speed | the **RF cavities** that give the beam its energy | 🔶 simplified — in the real machine the kick is repeated every lap |
| Beads knocked out of the detector cup | new particles made out of the crash energy | ✅ E = mc², and it is the point of the whole machine |
| The buzzer firing at the moment of impact | the detector's trigger signal | ✅ |
| Balls that jump out of the cup | particles escaping the detector, e.g. neutrinos | ✅ use it — it's a great line |

Things our model deliberately does **not** show (say so if anyone asks — it
makes you sound like a scientist): the balls roll, protons don't roll; our balls
slow down, the real beam gets topped up every lap; our crash is a mechanical
bounce, the real one converts energy into matter.

---

## 2. Time, cost, difficulty

| | |
|---|---|
| Build time | 4–6 hours spread over one weekend (glue needs to cool) |
| Cost | ~£35–55 (see `parts_list.md`) |
| Difficulty | **Level 1 build is easy** — cutting, taping, winding wire, gluing |
| Adult jobs | hot glue gun, wire stripping, cutting tubing |
| Kid jobs | winding coils, testing with balls, sticking down cable clips, decorating, labelling, timing the launches |

Build the **Level 1** machine first. Add Level 2 and 3 only if you are enjoying it.

---

## 3. The design in one picture

```
        TOP OF BOARD  (raised on a wedge — the "injection point")
        ┌───────────────────────────────────────────────┐
        │  ⬤ ← ball A              ball B → ⬤          │   ← electromagnet
        │  [coil A]                  [coil B]           │     gates hold them
        │   ╲                          ╱                │
        │    ╲  ← tube A sweep        ╱  ← tube B sweep │   each tube sweeps
        │     ╲                      ╱                  │   round the middle,
        │      ╲                    ╱                   │   getting faster
        │        ╲                ╱                     │
        │          ╲            ╱                       │
        │            ╲        ╱                         │
        │              ▼    ▼                           │
        │            ╔══════╗                           │
        │            ║ DET.  ║  ← clear cup, beads       │   the crash!
        │            ╚══════╝     inside, + buzzer      │
        └───────────────────────────────────────────────┘
        BOTTOM OF BOARD (lowest edge)

        board tilted by a wedge:  15–22°
```

Two identical, mirrored tubes. One launch button fires **both** electromagnet
gates at the same instant, so both balls arrive at the centre together and
**CLACK** — beads spray out, the buzzer rings.

**Why two mirrored tracks instead of one ring?** Two reasons. First, in a real
collider the two beams really do travel in opposite directions and meet at a
crossing point — so this is truer to the physics than a single ring with one
ball. Second, it is reliable: gravity does the accelerating, so it works on the
hundredth go exactly like the first.

---

## 4. Parts you need

Full shopping list with quantities and prices: **`parts_list.md`.**
Safety notes: **`SAFETY.md`** — read before you start.

---

## 5. Build steps

> **Golden rule of this build: dry-fit everything with masking tape and test it
> with a ball BEFORE you glue. Tape is cheap; a stalled ball at the fair is not.**

### Step 1 — The board (30 min)
1. Cut MDF or plywood to **80 × 60 cm**. Sand the edges.
2. Stand it up on a wedge at the back so it tilts **15–22°**. A door wedge, a
   folded block of wood, or a stack of books all work. Screw a small batten
   across the bottom front edge so tubes and balls can't roll off the table.
3. Kids' job: cover the board in lining paper and draw the collider logo on it —
   two spirals and a starburst in the middle. It hides the MDF and makes it look
   like a real machine.

**Tilt test before anything else:** put a steel ball at the top corner and time it
rolling to the bottom. You want **2–4 seconds**. Faster than that and the crash
will be violent; slower and it may stall. Adjust the wedge now, not later.

### Step 2 — Draw the two beam pipes (15 min)
Use `layout_template.html` — print it and copy the grid onto the board square by
square (each square is 10 cm). Or draw it yourself:

1. With a pencil, mark a spot on the centre line, about **8–10 cm up from the
   bottom edge**. That is the **detector** — the lowest point of the whole run,
   so that everything descends into it.
2. From the **top-left corner**, draw a sweeping curve that runs down the board,
   bows outward to the left edge, and curls back in to the detector. **The curve
   must always be going downhill or sideways — never back up the board.** About
   three-quarters of a turn is perfect: it reads as "going round the ring".
3. Now **mirror** it exactly on the right-hand side. The template has a dotted
   fold line down the middle — that symmetry is not decoration. Identical tracks
   are what makes the two balls arrive together.
4. Drop a ball on each line and let it roll. If it stalls anywhere, rub the line
   out and make that section straighter or steeper. **Do not move on until both
   balls roll the whole way and arrive within half a second of each other.**

### Step 3 — Lay the tubing (45 min)
1. Uncoil the clear tubing and leave it in a warm room for an hour — it uncurls
   and stops fighting you.
2. Cut two lengths to match your two drawn lines, plus 15 cm spare at each end.
   **Adult job** — sharp scissors or a hobby knife, straight cut.
3. Tape each tube along its line with masking tape. Leave the top 15 cm of each
   tube sticking out past the top edge of the board — this is the **injection
   point**, where the ball waits.
4. Drop a ball in the top of tube A. Watch the whole run. Then tube B. Then both.
   Adjust tape positions until both runs are smooth and quiet.
5. Only now: replace the masking tape with **cable clips** (or dabs of hot glue)
   every 15–20 cm. Leave the last 20 cm before the detector un-clipped so you can
   still nudge the final aim.

> Tip: the last 10 cm before the cup should point **downwards into** the cup, so
> the ball lands in it and not across the room.

### Step 4 — The electromagnet gates (1 hour, the best bit)
Each gate is a coil of wire wound straight onto the outside of the clear tube.
Energised, it drags the steel ball up into its centre and **holds** it at the top
of the track. Press the button, the power cuts, and the ball drops — exactly like
a real injection kicker magnet.

1. Tape a starting tab of masking tape on the tube, sticky side out, about 20 cm
   down from the top end.
2. **Kid job:** wind insulated copper wire around the tube, on the spot, keeping
   the turns side by side and neat. **200 turns.** Count in tens and keep a
   tally. Leave 25 cm of wire free at each end.
3. Wrap a layer of tape over the coil so it cannot unwind. Repeat for the second
   gate — **same direction, same number of turns**.
4. Strip 1 cm of insulation off the four wire ends (**adult job**).
5. Wire one coil to its own battery pack and push button:
   `battery + → button → coil → battery −`. Do not solder anything — twist the
   wires together tightly and cover each joint with tape, or use a choc-block
   connector.
6. **Test hold:** tilt the board, put a ball just above the coil, press and hold
   the button. The ball should pull up into the coil and stay there when you
   gently wiggle the board.
7. **Test release:** let go of the button. The ball must drop **immediately**.
   *If the ball stays stuck for a moment*, the coil is holding too well — take
   off 40 turns, or nudge the board. *If it never pulls in*, add 40 turns or
   check the battery.
8. Glue or tape each coil firmly to the tube, then wire both gates to **one**
   button so a single press fires both balls together.

> Physics note worth saying out loud: a real accelerator's kicker magnets are
> switched on and off in a few millionths of a second to inject the beam. Ours
> take a few hundredths — but it is the same idea.

### Step 5 — The detector (30 min)
1. Cut the bottom 8 cm off a clear plastic bottle, or use a small clear cup.
2. **Kid job:** pour in a layer of small coloured beads, about 1 cm deep.
3. Fix the cup to the board dead centre of where the two tubes meet, slightly
   sunken into a hole or held in a ring of hot glue so it cannot move.
4. Decorate a paper collar around it: **ATLAS-style detector** — draw the layers
   (inner tracker, calorimeter, muon chambers) as coloured bands. Great talking
   point, and the real detector really is built in concentric layers.

### Step 6 — The "we detected a collision!" buzzer (30 min)
Two options — build the first, keep the second as a fallback.

**Option A — impact switch (more like the real thing)**
1. Stick two strips of foil tape inside the cup, side by side, with a **2 mm
   gap** between them. Do not let them touch.
2. Wire: `battery + → buzzer → foil strip 1` and `battery − → foil strip 2`.
3. When the balls crash in, the beads and balls momentarily bridge the gap →
   buzz. Widen or narrow the gap until it fires every time but doesn't buzz on
   its own.

**Option B — the human detector (never fails, and is more fun)**
A big push button wired to the buzzer, sat next to the board. Whoever spots the
crash presses it. Announce loudly: *"The detector is a person who never blinks!"*

### Step 7 — Label everything (15 min, kids' job)
Print or hand-write labels and tape them on:
`INJECTION POINT` · `KICKER MAGNET` · `BEAM PIPE` · `BEAM A →` · `← BEAM B` ·
`DETECTOR` · `NEW PARTICLES`.

This is the single highest-value 15 minutes in the whole build. A visitor reads
the labels, the kids narrate, and the model explains itself.

### Step 8 — Dress rehearsal (20 min)
Run the whole thing 10 times in a row. Every time. If it works 10/10, you are
ready for the fair. If not, see the troubleshooting table below.

---

## 6. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Ball stalls part way | Board too shallow, or the curve climbs | Steeper wedge; straighten that bit of tube; shorten the track |
| Ball stops inside the coil after release | Coil holds too strongly (remanence) | Remove turns; move the coil 1 cm along the tube; tap the board |
| Ball never pulls into the coil | Too few turns, weak batteries, or a bad joint | Add turns; fresh batteries; re-twist the joints |
| Balls arrive at different times | Tracks not identical, or different friction | Re-check the mirror symmetry; rub a dry PTFE/graphite pencil along the slower tube |
| Ball bounces out of the cup | Too fast, or the cup is too shallow | Reduce the wedge slightly; use a deeper cup; pack the beads deeper |
| Buzzer never fires | Foil gap too wide | Narrow the gap; or press the human-detector button |
| Buzzer buzzes on its own | Foil gap too narrow | Widen the gap |
| Everything worked yesterday, nothing today | Flat batteries | Spare battery pack in the box. Seriously — bring spares. |

---

## 7. Optional upgrades

**Level 2 — add "steering magnets" (30 min).** Wind two more coils on large nails
and mount them beside the tube near the middle, wired to their own switch.
Flip the switch and the passing ball is tugged off line — a live demonstration
that **magnets steer charged particles**. Bonus: the same nail coil picks up
paperclips at the stand, so visitors can make the magnet work themselves.

**Level 3 — make it a real ring (2 hours).** Wind the tubing in a descending
spiral around the outside of a large plastic bucket, standing the bucket upright
in the middle of the board. Balls now do **three or four laps** instead of one
sweep, which looks much more like the pictures of the LHC. Keep the exit aimed
at the centre cup.

**Level 4 — automatic firing (a weekend, for the grown-ups).** A micro:bit or
Arduino, two cheap IR break-beam sensors at the detector, and a MOSFET driving
each gate: the machine then fires itself whenever the balls are loaded, and can
count collisions on screen. Only do this if a grown-up wants the electronics
project — the Level 1 button is better for Year 4 presenters, because *they* do
the firing.

**Level 5 — the standalone electromagnet table (30 min, huge hit at fairs).**
Nail, 1 m of wire, AA battery, a pile of paperclips, and a printed card:
*"Wind 50 turns. Connect the battery. How many clips can you pick up? Now try
25 turns. More turns = stronger magnet."* This turns your stand from a show into
an activity, and it is exactly the physics that makes the LHC's magnets work.

---

## 8. Running the stand (5-minute loop)

1. **Hook (30 s):** *"This is a model of the biggest machine humans ever built.
   It smashes tiny particles together to find out what everything is made of."*
2. **Show (60 s):** fire it twice. Let the beads fly. Ring the buzzer.
3. **Explain (90 s):** point at the labels, using the table in section 1.
4. **Computer (90 s):** open `simulation/index.html`, turn the magnets down so
   the beam flies off, then press **COLLIDE NOW**.
5. **Hands-on (60 s):** Level 5 paperclip table, or let a visitor press the
   launch button.

Keep a tally chart: *"Collisions so far: 214."* People queue for things with
numbers on them.
