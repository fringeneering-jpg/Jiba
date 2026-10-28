# JIBA — Deterministic Orbital Station-Keeping & Telemetry Debiasing Engine

**Author:** Jaden Allison (Fringeneering — Perth, Western Australia)  
**License:** Dual-Licensed under **GNU AGPLv3** (Students & Open Benchmark Evaluation) and **Fringeneering Commercial Telemetry License**  
**Governing Physics:** Phase Wave Cosmology (ILRS Calibrated: alpha = 2.635, beta = 4.445, Anderson Constant V_A = 14.6644 mm/s)

**REVISION 2 (2026-10-28) — night-shift verified updates:**
1. **Pure GM (audit resolution (a)):** gravity is exactly 1/r² — the entropic term
   lives in the *telemetry* (the light-path secular drift), never in the force
   model. `GM_TRUE` = 398600.4415×10⁹ m³/s² (TT) with the IAU/IERS clock ladder
   (L_G, L_C, L_B) and the TDB value for DE440 ephemerides.
2. **Seasonal drift window (QZS-3 TLE audit, 3,624 epochs):** the natural
   mean-motion drift runs **~57×** larger in the sun-north months — Jiba now
   schedules correction burns in the sun-south window (Oct–Mar), the lowest
   possible thruster usage.
3. **Anderson amplitude regimes:** the relaxed dipole V_A = 14.6644 mm/s governs
   slow orbital station-keeping; the unrelaxed encounter wake carries the 19×
   fold (U_enc = 278.62 mm/s, s = 1/19) — flyby-class transfers only.

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
* `step1_fuel_saver_proof.py` — Fleet propellant (Delta-V) and lifespan savings benchmark across VLEO, LEO, MEO, and GEO.
* `step2_visual_pitch_chart.py` — Generates `Jiba_Commercial_Pitch.png` (300-DPI comparison of Standard Autopilot vs. Jiba Wave-Surfing).
* `step3_live_telemetry_demo.py` — Orbit-by-orbit flight telemetry filter simulation.
* `step4_tle_customer_audit.py` — Direct NORAD Two-Line Element (TLE) parser and client audit report generator (`Jiba_Customer_Audit_Report.txt`).
* `step5_7day_blind_ilrs_benchmark.py` — 7-Day (168-hour) blind ILRS prediction challenge on Starlette, LARES, LARES-2, and LAGEOS-1 (`Jiba_7Day_Blind_ILRS_Proof.png`).

---

## Evaluation Terms & Telemetry Data Offers

* **Free for Students & Academic Researchers:** 100% free to download, run, and study under the GNU AGPLv3 license.
* **Free for Enterprise Benchmarking:** Satellite operators, mission-control centers, and aerospace enterprises are invited to run this suite free of charge to benchmark `Jiba` directly against their current station-keeping propellant costs and 7-day tracking residuals.
* **Commercial Offers (Telemetry Data Only — Underlying Physics Retained):** Over the next month, Fringeneering will be fielding commercial offers strictly for the purchase/licensing of the **station-keeping telemetry data and orbital correction outputs only**. Operational deployment in commercial flight loops requires a commercial agreement. **The underlying Phase Wave Cosmology (PWC) physical framework and foundational equations remain 100% the exclusive intellectual property of Jaden John Allison (Fringeneering) and are not for sale.**

* **Contact:** Jaden Allison — Fringeneering (Western Australia) | **Email:** fringeneering@gmail.com
* **GitHub:** https://github.com/fringeneering-jpg/Jiba

