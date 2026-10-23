---
# Pages: an explicit permalink keeps README out of the way of index.md,
# which the readme-index plugin would otherwise claim or drop.
layout: default
title: Start here
permalink: /start-here/
---

# MiniCollider 🎡⚛️

A school project: **build a tiny model of a particle collider, present it, and
run a computer simulation of it.** Made for STEM week by three Year 4 children
and one grown-up.

Everything here works **offline** — open the files, they just run. No installs,
no internet, no accounts.

```
mini-collider/
├── README.md                  ← you are here
├── build/                     the physical model
│   ├── BUILD_GUIDE.md            START HERE — how to build the board
│   ├── parts_list.md             shopping list, ~£48
│   ├── SAFETY.md                 read before you build
│   └── layout_template.html      print at 100% → board plan + labels
├── presentation/
│   ├── index.html                14 slides — arrows to move, F for fullscreen
│   └── KIDS_SCRIPT.md            who says what, and the questions to expect
├── simulation/
│   └── index.html                the collider, live — double-click to run
└── docs/
    └── science_notes.md          the real physics behind every part
```

---

## Start here

1. **Read `build/BUILD_GUIDE.md`.** It is the plan for the whole project, and it
   includes a five-minute stand routine at the end.
2. **Buy the parts** from `build/parts_list.md`. Nothing is specialist; one
   online order plus a trip to a hardware shop covers it.
3. **Build Level 1 only, first.** It is a weekend, and it is what you will
   actually take to the fair. Levels 2–5 are optional extras.
4. **Practise the presentation** with `presentation/KIDS_SCRIPT.md`.
5. **Put `simulation/index.html` on the laptop** you will take, and try it
   full-screen before the day.

---

## The three things we made

### 1. The model — "The Colliderscope"

A tilted board with two mirrored clear-plastic beam pipes. Two steel ball
bearings — our protons — are held at the top by two **electromagnets the children
wound themselves** (200 turns of copper wire each). One button releases both at
exactly the same moment, both balls race down in opposite directions, and they
crash in a clear detector cup in the middle. Coloured beads spray out — those are
the **new particles**, made out of the energy of the crash, and a buzzer rings.

The electromagnets are not decoration. Kicker magnets releasing the beam into the
ring is how the real machine starts, and `p = qBr` — the reason a faster beam
needs stronger magnets — is the real equation hiding behind the whole project.

### 2. The presentation

Fourteen slides, written for an 8-year-old to deliver, with a script split
between three speakers. Keyboard arrows to move, `F` for fullscreen, and
`Ctrl/Cmd+P` prints it as a PDF — one slide per page — if you would rather have
paper.

### 3. The simulation

A live collider in the browser. Two beams circulate in opposite directions past
bending magnets and RF cavities, and you can:

- **charge the beam up** and watch the energy climb from 450 GeV to 7 TeV;
- **turn the magnets down** and watch the beam fly off the ring — real beam loss;
- **press COLLIDE NOW** and see new particles spray out, including neutrinos that
  escape unseen;
- flip on **Real LHC numbers** to see the speed hit 99.9999991 % of light speed.

It also shows the honest, counter-intuitive bit: the energy climbs enormously
while the percentage-of-light-speed figure barely moves. That is not a bug in our
simulation — that is relativity, and it is the best question-killer at the stand.

---

## If you only have one evening

Do this:

1. Print `build/layout_template.html` (both pages).
2. Get one 3 m length of 16 mm clear tubing, two 14 mm steel balls, a board, a
   bag of beads, and a buzzer-and-battery kit.
3. Build the two tracks and the cup. Skip the electromagnets — launch the balls
   with your fingers.
4. Open `simulation/index.html` on a laptop.

You will have a working demonstration for about £20. The electromagnets are the
part worth coming back for, because they turn a marble run into an accelerator.

---

## What the children are actually learning

- **Matter is made of particles, and particles are made of smaller particles.**
- **A force at right angles to motion bends a path** — the single most useful
  piece of physics in the project, and the reason magnets steer beams.
- **Energy can become matter** (E = mc²), which is why colliders find new
  particles.
- **Models are not the real thing, and that is fine** — knowing which parts of
  your model are honest is a scientific skill in itself.
- **Engineering is iteration.** The board is built with masking tape first and
  glue last, because the first version will be wrong and that is normal.

There is a much longer version of all of this in `docs/science_notes.md`, written
for the grown-up who has to answer the questions.
