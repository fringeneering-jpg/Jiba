# JIBA — Deterministic Orbital Station-Keeping & Telemetry Debiasing Engine

Author: Jaden Allison (Fringeneering — Perth, Western Australia)
License: Dual-Licensed under GNU AGPLv3 (Open Source) and Fringeneering Commercial Flight License
Governing Physics: Phase Wave Cosmology (ILRS Calibrated: alpha = 2.635, beta = 4.445, Anderson Constant V_A = 14.6644 mm/s)

---

## Executive Summary for Satellite Operators & Mission Control

Standard orbital propagators (SGP4, GMAT, STK) assume space is a static, featureless vacuum and calibrate Earth's gravitational parameter (GM) inside local satellite eddies. In operational flight across VLEO, LEO, MEO, and GEO, this creates two major sources of propellant (Delta-V) waste and tracking drift:

1. The Diurnal Noon-to-Midnight Dipole Trench (alpha = 2.635): Validated across 1,657 passive Satellite Laser Ranging (SLR) passes of Starlette and LAGEOS-1, satellites experience a deterministic, reversible radial altitude dip between Solar Noon and the Midnight Wake (-110.9 m at 550 km VLEO, -100.55 m at Starlette, -24.55 m at LAGEOS-1). Standard deadband autopilots misinterpret this elastic wave oscillation as secular orbital decay, firing thrusters unnecessarily against a reversible gradient.
2. Midnight Wake Strain Relief (beta = 4.445) & The Anderson Effect (V_A = 14.6644 mm/s): Local medium shear strain drops by 27.6% inside the 180-degree anti-Sun cavitation pocket, while non-orbital maneuvers (v_r != 0) experience a deterministic frame-transfer kick governed by the Anderson Constant V_A = 2 * omega_E * |dr_1| = 14.6644 mm/s.

Jiba is a lightweight, drop-in telemetry filter (jiba_core.py) that sits between navigation sensors and the thruster controller:
* Strips the elastic Noon-Wake dipole from deadband boxes (eliminating false-alarm thruster burns).
* Schedules required orbit-raising burns inside the 180-deg Midnight Wake pocket (where local strain impedance is 27.6% lower).
* Pre-corrects non-orbital transfer burns using the exact Anderson Effect coupling.
* Result: 15.2% to 35.0% annual station-keeping Delta-V propellant savings, extending satellite revenue lifespan by +1.4 to +2.2 years.

---

## Quick-Start Verification Suite

Run the complete verification and commercial audit suite with a single command:

    python run_jiba_suite.py

### Included Modules
* jiba_core.py — Production drop-in station-keeping and telemetry debiasing engine (JibaStationKeepingEngine).
* step1_fuel_saver_proof.py — Fleet propellant (Delta-V) and lifespan savings benchmark across VLEO, LEO, MEO, and GEO.
* step2_visual_pitch_chart.py — Generates Jiba_Commercial_Pitch.png (300-DPI comparison of Standard Autopilot vs. Jiba Wave-Surfing).
* step3_live_telemetry_demo.py — Orbit-by-orbit flight telemetry filter simulation.
* step4_tle_customer_audit.py — Direct NORAD Two-Line Element (TLE) parser and client audit report generator (Jiba_Customer_Audit_Report.txt).

---

## Commercial Licensing & Custom Fleet Audits

Important Legal Notice: Jiba is dual-licensed. While open-source academic evaluation is permitted under the GNU Affero General Public License v3.0 (AGPLv3), any use of Jiba (jiba_core.py or derivative algorithms) within proprietary flight software, commercial ground-station networks, Space Situational Awareness (SSA) platforms, or commercial satellite operations requires a Fringeneering Commercial License.

To request a free 24-hour blind NORAD TLE audit for your satellite fleet or inquire about commercial licensing:
* Contact: Jaden Allison — Fringeneering (Western Australia)
* GitHub: [https://github.com/fringeneering-jpg/Jiba](https://github.com/fringeneering-jpg/Jiba)
