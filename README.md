# JIBA — Deterministic Orbital Station-Keeping & Telemetry Debiasing Engine

**Author:** Jaden Allison (Fringeneering — Perth, Western Australia)  
**License:** Dual-Licensed under **GNU AGPLv3** (Students & Open Benchmark Evaluation) and **Fringeneering Commercial Telemetry License**  
**Governing Physics:** Phase Wave Cosmology (ILRS Calibrated: alpha = 2.635, beta = 4.445, Anderson Constant V_A = 14.6644 mm/s)

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

* **Contact:** Jaden Allison — Fringeneering (Western Australia)
* **GitHub:** https://github.com/fringeneering-jpg/Jiba
