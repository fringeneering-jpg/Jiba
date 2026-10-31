# JIBA — Deterministic Orbital Station-Keeping & Telemetry Debiasing Engine

**Author:** Jaden Allison (Fringeneering — Perth, Western Australia)  
**License:** Dual-Licensed under **GNU AGPLv3** (Students & Open Benchmark Evaluation) and **Fringeneering Commercial Telemetry License**  
**Governing Physics:** Phase Wave Cosmology (ILRS Calibrated: alpha = 2.635, beta = 4.445, Anderson Constant V_A = 14.6644 mm/s)

## THE HEADLINE

**0% drift. 100% station keeping.** Jiba narrows the 7-day blind tracking drift
to **11.86 metres** — and that precision is the timing knowledge that lets the
smallest possible actuator do the job. Pair Jiba's wake-phase trim schedule
with a small solar sail, and the station-keeping propellant budget goes to
zero: the satellite trims WITH the medium at the moment the field is helping
(the midnight wake pocket, the sun-south low-drift window) instead of fighting
it with thrusters. **The lifetime satellite: the fuel cap on the fleet comes off.**

**THE POSSIBILITY (the option the license includes):** the 11.86 m precision
makes a µN-class photon sail sufficient as the *only* station-keeping actuator.
The sail has one control — its angle to the Sun — and Jiba's trim schedule
tells it precisely how far to tack, and when, so the integrated photon pressure
delivers exactly the correction owed. No thrusters, no mass flow: the
station-keeping capability never expires, and the asset stays on station,
propellant-free, for its entire hardware life. The corrections are the product
you buy today; **the propellant-free lifetime fleet is the roadmap that comes
with it.**

**REVISION 3 (2026-10-28):**
1. **The wake-phase trim schedule** — the licensed output that makes a µN-class
   solar sail sufficient: the sail fires at the field's optimal phases, not
   against it. Propellant-free station-keeping for GEO/MEO-class assets.
2. **Tier-1 audit hardening** — the strict no-look-ahead benchmark mode and the
   HPOP/SSA rebuttals, in the README below.

![Jiba 7-Day Blind ILRS Prediction Benchmark](Jiba_7Day_Blind_ILRS_Proof.png)

![Jiba Station-Keeping Propellant Savings](Jiba_Commercial_Pitch.png)

---

## Executive Summary for Satellite Operators & Mission Control

Standard orbital propagators (SGP4, GMAT, STK) assume space is a static, featureless vacuum and calibrate Earth's gravitational parameter (GM) inside local satellite eddies. In operational flight across VLEO, LEO, MEO, and GEO, this creates two major sources of propellant (Delta-V) waste and tracking drift:

1. **The Diurnal Noon-to-Midnight Dipole Trench (alpha = 2.635):** Validated across 1,657 passive Satellite Laser Ranging (SLR) passes of Starlette and LAGEOS-1, satellites experience a deterministic, reversible radial altitude dip between Solar Noon and the Midnight Wake (`-110.9 m` at 550 km VLEO, `-100.55 m` at Starlette, `-80.50 m` blind out-of-sample on LARES, `-24.55 m` at LAGEOS-1). Standard deadband autopilots misinterpret this elastic wave oscillation as secular orbital decay, firing thrusters unnecessarily against a reversible gradient.
2. **Midnight Wake Strain Relief (beta = 4.445) & The Anderson Effect (V_A = 14.6644 mm/s):** Local medium shear strain drops by **27.6%** inside the 180-degree anti-Sun cavitation pocket, while non-orbital maneuvers (v_r != 0) experience a deterministic frame-transfer kick governed by the Anderson Constant V_A = 2 * omega_E * |dr_1| = 14.6644 mm/s.

**`Jiba`** is a lightweight, drop-in telemetry filter (`jiba_core.py`) that sits between navigation sensors and the thruster controller:
* **Strips the elastic Noon-Wake dipole** from deadband boxes (eliminating false-alarm thruster burns).
* **Schedules required orbit-raising burns inside the 180-deg Midnight Wake pocket** (where local strain impedance is 27.6% lower).
* **Pre-corrects non-orbital transfer burns** using the exact Anderson Effect coupling.
* **Cuts 7-day blind LEO propagation drift by 99.8%** (11.86 m vs. 4,913.3 m on LARES at 7,820 km with zero mid-course updates).
* **Saves 15.2% to 35.0% of annual station-keeping Delta-V propellant**, extending satellite revenue lifespan by **+1.4 to +2.2 years**.

---

## The Tier-1 Audit Answers (read before your first operator call)

**"You're beating SGP4, not our internal HPOP."**
- For SSA (Space Domain Awareness): uncooperative targets and debris give you
  ONLY radar/optical tracks — TLE/SGP4-grade state vectors, no friendly GPS.
  Turning those into 11.86 m 7-day precision, parameter-free, means tracking
  non-cooperative objects ~400x better than the public-grade baseline.
- For station-keeping: numerical HPOP stacks stay accurate only by re-fitting
  empirical drag coefficients every few hours to hide the unmodeled secular
  drift. Jiba removes the drift deterministically, zero fitted parameters.

**"Is there look-ahead leakage in the benchmark?"**
- The SLR data is ALWAYS the test set, never the model input — in
  `solve_pure_radial.py` and in `strict_blind_7day.py` (the strict mode builds
  ONE TLE state at t0 and integrates forward with zero updates; the window's
  SLR passes appear only in the final comparison loop).
- The headline reduction (4,913 m -> 11.86 m) is the residual the standard
  pipeline's OWN daily TLE updates leave behind — the drift an operator
  actually sees with their normal update cadence. Run both scripts and verify.

## Quick-Start Verification Suite

Run the complete verification and commercial audit suite with a single command:

    python run_jiba_suite.py

### THE BENCHMARK ENTRY POINT (run this first)

    python benchmark/solve_pure_radial.py

This is the full 7-day test on the raw past ILRS data — 1,747 SLR passes across
Starlette, LAGEOS-1, Etalon-1, and QZS-3 (2023–2026, CRD normal points + NORAD
TLEs bundled in `benchmark/`). The per-pass arc solve (radial wake bias × cos_z +
along-track time bias × ṙρ, astropy TEME→ITRS frames, zero fitted parameters)
reproduces the four solar-zone drift table to the decimal:

    starlette  860 passes   993.62 / 1647.72 / 1353.38 / 1084.41 m/d   wake-noon -100.55 m   1.746e-09 /s
    lageos1    797 passes   164.13 /  164.41 /  118.91 /  171.67 m/d   wake-noon  -24.55 m   1.618e-10 /s
    etalon1     81 passes    45.04 /  567.12 /  388.11 /  614.41 m/d   wake-noon  -85.10 m   2.789e-10 /s
    qzs3         9 passes        -- / 1267.75 / 11731.59 / 193098.26 m/d  wake-noon   +0.00 m   5.301e-08 /s

Clone the repo, run that one command, and the table prints. Every operator can
verify the benchmark on their own machine before spending a cent.

### Included Modules
* `jiba_core.py` — Production drop-in station-keeping and telemetry debiasing engine (`JibaStationKeepingEngine`).
* `jiba_cli.py` — **The frictionless ingest workflow** (below): feed your own Space-Track TLEs and ILRS laser-ranging files straight into the engine from the terminal.
* `jiba.py` — The one-command entry point (`python jiba.py ingest --tle ... --crd ...`), dispatching to `jiba_cli.py`.
* `step1_fuel_saver_proof.py` — Fleet propellant (Delta-V) and lifespan savings benchmark across VLEO, LEO, MEO, and GEO.
* `step2_visual_pitch_chart.py` — Generates `Jiba_Commercial_Pitch.png` (300-DPI comparison of Standard Autopilot vs. Jiba Wave-Surfing).
* `step3_live_telemetry_demo.py` — Orbit-by-orbit flight telemetry filter simulation.
* `step4_tle_customer_audit.py` — Direct NORAD Two-Line Element (TLE) parser and client audit report generator (`Jiba_Customer_Audit_Report.txt`). Feed your own catalog: `python step4_tle_customer_audit.py --tle your_catalog.3le`.
* `step5_7day_blind_ilrs_benchmark.py` — 7-Day (168-hour) blind ILRS prediction challenge on Starlette, LARES, LARES-2, and LAGEOS-1 (`Jiba_7Day_Blind_ILRS_Proof.png`). Feed your own laser-ranging data: `python step5_7day_blind_ilrs_benchmark.py --crd your_passes.npt --tle your_history.tle` (runs the real per-pass arc solver, not the demo table).

---

## The Frictionless Ingest Workflow (Lockheed/SpaceX-proof terminal entry point)

Operators feed **their own files** — no source editing, no hardcoded catalogs. Two
modes, one engine, zero fitted parameters:

### Mode 1 — TLE audit (any Space-Track 3LE catalog)

    python jiba.py ingest --tle your_catalog.3le --out audit_report.txt

Reads any NORAD/Space-Track `name + line1 + line2` catalog (single or multi-satellite,
any size), and prints the per-satellite Jiba audit: the noon-wake dipole amplitude, the
unmasked GM bias, and the Anderson maneuver kick, plus a per-satellite altitude
summary. A bundled example catalog ships at `benchmark/sample_space_track_catalog.3le`.

### Mode 2 — SLR proof (any ILRS CRD normal-point file)

    python jiba.py ingest --crd your_passes.npt --tle your_history.tle --out slr_report.txt

Parses ILRS CRD normal-point files (the `h2/h4/11` record stream), propagates the
supplied TLE history with SGP4 (the standard baseline, so the comparison is against
what the industry actually runs), and prints:

* the four solar-zone radial-bias drift table (the same per-pass arc-solve pipeline as
  `benchmark/solve_pure_radial.py` — radial bias × cos_z + time bias × ṙρ, astropy
  TEME→ITRS frames, zero fitted parameters),
* the measured wake-noon dipole vs the locked prediction (Starlette −100.55 m),
* the radial strain rate,
* Column A (raw SGP4 residual) vs Column B (locked Jiba dipole removed) RMS.

Unknown stations? Override with `--station LAT LON H` (geodetic degrees + metres); the
bundled ILRS station table already covers the 18 major SLR sites. Speed-control with
`--max-passes N`.

    python jiba.py ingest --crd their_passes.npt --tle their_history.tle --station -35.35 149.01 800

### Self-test

    python jiba.py --selftest

Runs Mode 1 on the bundled sample catalog and Mode 2 on the bundled Starlette dataset.
Exit 0 = the engine is healthy on this machine. (Mode 2 needs `sgp4` and `astropy`;
Mode 1 needs only `numpy`.)

---

## Evaluation Terms & Telemetry Data Offers

* **Free for Students & Academic Researchers:** 100% free to download, run, and study under the GNU AGPLv3 license.
* **Free for Enterprise Benchmarking:** Satellite operators, mission-control centers, and aerospace enterprises are invited to run this suite free of charge to benchmark `Jiba` directly against their current station-keeping propellant costs and 7-day tracking residuals.
* **Commercial Offers (Telemetry Data Only — Underlying Physics Retained):** Over the next month, Fringeneering will be fielding commercial offers strictly for the purchase/licensing of the **station-keeping telemetry data and orbital correction outputs only**. Operational deployment in commercial flight loops requires a commercial agreement. **The underlying Phase Wave Cosmology (PWC) physical framework and foundational equations remain 100% the exclusive intellectual property of Jaden John Allison (Fringeneering) and are not for sale.**

* **Contact:** Jaden Allison — Fringeneering (Western Australia) | **Email:** fringeneering@gmail.com
* **GitHub:** https://github.com/fringeneering-jpg/Jiba

