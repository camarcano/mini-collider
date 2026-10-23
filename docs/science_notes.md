# Science notes for the grown-ups

Everything in the model, the slides, and the simulation, with what is really
going on behind it. This is the crib sheet for the question you will get at the
stand that the kids' script does not cover.

Numbers are for the LHC in its current Run 3 configuration, and are rounded.
Where a figure is approximate, it says so.

---

## 1. The real machine, in numbers

| Quantity | Value |
|---|---|
| Machine | Large Hadron Collider, at CERN, near Geneva (straddles the France–Switzerland border) |
| Circumference | 26.7 km (≈27 km), in a tunnel roughly 100 m underground |
| Beam particles | protons (also heavy ions in part of each year) |
| Injection energy | 450 GeV per proton |
| Top beam energy | 6.8 TeV per proton (Run 3) |
| Speed at top energy | 99.9999991 % of the speed of light |
| Revolutions | ≈11,245 laps per second |
| Temperature | 1.9 K (−271 °C), colder than the 2.7 K of deep space |
| Main bending magnets | 1,232 superconducting dipole magnets, up to 8.33 tesla |
| RF accelerating system | 400 MHz superconducting cavities |
| Collisions at a detector | of order a billion proton–proton collisions per second |
| Major detectors | ATLAS, CMS, ALICE, LHCb |
| Biggest detector | ATLAS — about 45 m long, 25 m across, roughly 7,000 tonnes |

Two facts worth having in your pocket at a stand:

- **Almost all of the speed is gained before the big ring.** A proton entering
  the LHC at 450 GeV is already at 99.9998 % of light speed. The 27 km ring is
  not really making it *faster* in any way you could see — it is making it
  *hotter*, in the sense of packing in far more energy. This is why our
  simulation shows the percentage barely moving while the energy climbs a lot,
  and it is a genuinely good thing to point at.
- **The web was invented at CERN**, by Tim Berners-Lee in 1989, so that
  physicists could share results. Nice one for a school audience.

---

## 2. How the machine actually works

**Injection.** Protons are stripped from hydrogen gas, then passed through a
ladder of four accelerators (LINAC → booster → Proton Synchrotron → SPS) before
they enter the LHC. At the entrance to the LHC, fast **kicker magnets** switch on
for a couple of microseconds and snap the beam onto the ring. Our electromagnet
gates are a direct — if much slower — copy of this.

**Bending (dipoles).** A charged particle moving in a magnetic field feels a
force at right angles to its motion, `F = qvB`. That sideways force is what bends
the beam into a circle. Setting `qvB = mv²/r` gives the key accelerator
relationship:

```
p = q B r        momentum = charge × field × radius
```

So for a fixed ring radius, **the field you need is proportional to the momentum
you want**. That single line is why the LHC needed superconducting magnets, why
it is 27 km long instead of 27 m, and it is exactly what the simulation's magnet
meter is showing. Turn the magnet slider down at full energy and the beam leaves
the ring — in real life that is called **beam loss**, and the machine dumps the
beam rather than let it hit the magnet.

**Focusing (quadrupoles).** Dipoles steer; quadrupoles squeeze. A beam is a cloud
of particles that drift apart, so focusing magnets pinch it back together tens of
thousands of times a second. Our model does not show focusing; worth mentioning
if someone asks "is it just one big magnet?"

**Acceleration (RF cavities).** The cavities are resonant boxes holding an
oscillating electric field at 400 MHz. A proton that arrives at the right moment
rides the crest of the wave and gains energy. Particles that arrive late get
pulled back, which has the useful side effect of holding the beam together in
tight **bunches** rather than a smooth smear. The individual kick is small, but
the protons pass a cavity 11,245 times a second, and that is how you climb from
450 GeV to 6.8 TeV over about twenty minutes.

**Crossing and collision.** The two counter-rotating beams share the tunnel in
separate pipes and are crossed at four interaction points. Beams are bunched, and
bunches pass through each other about every 25 nanoseconds. The protons are so
small and the space between them is so vast that only about 1 in 10⁹ crossing
protons actually interacts — hence the machine runs for months to collect
enough events.

**The detector.** Concentric layers, each specialised, from the inside out:
a tracker (where did it go?), a calorimeter (how much energy did it dump?), and
muon chambers (what got all the way out?). Our beads-in-a-cup with a buzzer maps
to the calorimeter-plus-trigger idea: something happened, energy was deposited,
a signal was raised.

**After.** A beam that is no longer wanted is steered into the **beam dump**, a
7 m graphite block behind 8 m of steel and concrete, in a few microseconds.

---

## 3. What the crash actually produces

Energy is conserved, but rest mass is not. At these energies the protons'
**kinetic** energy is about 7,000 times their rest energy, and when they collide
that kinetic energy can become **new particles**:

- quarks and gluon sprays, seen as **hadron jets**;
- **muons** — heavy electrons that punch all the way through the detector;
- **electrons and photons**;
- **neutrinos**, which are invisible, and which show up only as "missing energy"
  in the account books. In our simulation the neutrino is drawn dashed and flies
  straight out — it is the one product the detector genuinely does not see.

And famously: in 2012 ATLAS and CMS found the **Higgs boson**, predicted in 1964,
completing the Standard Model. Our model produces a random assortment of
particles, which is honest — real collisions are random too, and the physics is
in the statistics of millions of them.

---

## 4. Where our model is honest, and where it is not

| Our model | Real machine | Verdict |
|---|---|---|
| Two tubes, two balls, opposite directions | two counter-rotating beams crossing at an interaction point | ✅ faithful |
| Electromagnet gate releases both balls | kicker magnets inject both beams | ✅ faithful in kind, slower by ~1000× |
| One slope gives all the energy at the start | RF cavities add a little energy on every lap | 🔶 simplified |
| Balls stop when they reach the cup | the beam is topped up every lap and circulates for hours | 🔶 simplified |
| A mechanical bounce | a collision that converts energy into new matter | 🔶 analogy — the *result* (new particles flying out) is right |
| Beads = new particles | particles of many types, mostly uncaught | ✅ good analogy |
| Buzzer = detector trigger | the detector's trigger system | ✅ good analogy |
| Balls roll, and slow down from friction | protons do not roll, and lose almost no energy in vacuum | 🔶 simplified |
| Magnet strength matters | `p = qBr` — this is exactly right | ✅ faithful, and the most educational part of the whole build |

If someone pushes you on the rolling-versus-flying point, the answer is: *our
model is a model. It keeps the two things that matter — two beams, opposite
directions, steered by magnets into a collision — and swaps the parts we cannot
build in a kitchen for the parts we can.*

---

## 5. The simulation's physics

`simulation/index.html` uses a deliberately simple but self-consistent model:

- Each proton carries an energy `E` in GeV, starting at the real injection value
  of 450 GeV and topping out at 7,000 GeV.
- Passing an RF cavity adds a kick proportional to the RF power slider. So the
  ramp-up rate is genuinely under the visitor's control.
- Speed shown is the real relativistic speed, `β = √(1 − (m/E_total)²)` with
  `m = 0.938 GeV`. At injection this is 99.9998 % and at 7 TeV it is
  99.9999991 % — which is why the display saturates while the energy keeps
  climbing. **That is the lesson, not a bug.**
- The visual lap speed is *not* the real speed (a real proton does 11,245 laps a
  second, which would be a blur). It is log-mapped onto the beam energy so that
  the audience can *see* the beam speed up. The real number is displayed next to
  it.
- **Magnet requirement is linear in beam energy**, straight from `p = qBr`.
  Below the requirement, protons leave the ring tangentially — which is the
  correct shape of a real beam loss, and the single most instructive interaction
  in the whole simulation.
- Collisions require a proton from each beam to arrive at the detector together,
  and even then only some of them interact — because in reality only ~1 in 10⁹
  does.
- Product particles are drawn from a weighted random set, always including at
  least one photon and one neutrino, so the "some things escape unseen" point
  always lands.

Open questions a bright Year 4 might ask, and honest answers:

- **"Why doesn't the percentage change?"** Because light speed is a speed limit,
  not a target. Almost all the extra energy makes the proton *heavier* with
  energy, not faster.
- **"What happens if you turn the magnets right down?"** The beam comes off.
  Real machines dump the beam on purpose before that can damage a magnet.
- **"Where does the new stuff come from?"** From the energy of the crash. It was
  not hiding inside the proton — it is made on the spot. That is E = mc².
