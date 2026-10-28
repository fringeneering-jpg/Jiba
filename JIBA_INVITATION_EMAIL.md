# THE JIBA INVITATION — final email copy (send-ready)

**Subject:** Free station-keeping benchmark — beat your current 7-day drift, or don't. It costs nothing to find out.

---

To the flight-dynamics team,

We've published a deterministic orbital station-keeping and telemetry-debiasing
engine — **Jiba** — and we're inviting your team to run a zero-cost comparison
against your current station-keeping, on your own telemetry.

**The claim, and the receipts:**

On our own past ILRS laser-ranging data — 1,747 SLR passes across four orbital
regimes, 2023–2026, raw CRD normal points — the standard propagator accumulates
993–1,648 m/day of unmodeled drift at LEO (Starlette), 119–172 m/day at MEO
(LAGEOS-1), while Jiba's correction removes the radial wake and strain to the
noise floor. On the blind LEO target (LARES, 7,820 km) the 7-day propagation
error falls from **4,913.3 m to 11.86 m — a 99.8% reduction, zero fitted
parameters, zero mid-course updates.**

**Run it yourself in one command:**

```
git clone https://github.com/fringeneering-jpg/Jiba
cd Jiba
python benchmark/solve_pure_radial.py
```

The benchmark data is bundled in the repo. The table prints on your machine in
under a minute — every number above, reproduced from the raw files. Then run
`python run_jiba_suite.py` for the full commercial audit (propellant savings,
TLE customer audit, the 7-day blind ILRS chart).

**The offer:** the AGPL build is free for students and free for enterprise
benchmarking. If the comparison holds on your telemetry, the commercial
station-keeping outputs are licensed under terms in the repo's prospectus —
first credible bidder takes the worldwide license.

The comparison is the pitch. Run it.

**Jaden Allison — Fringeneering** · fringeneering@gmail.com · Perth, Western Australia
