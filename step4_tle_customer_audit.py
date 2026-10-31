# -*- coding: utf-8 -*-
"""
step4_tle_customer_audit.py — JIBA NORAD TLE READER & COMMERCIAL AUDIT GENERATOR

Copyright (c) 2026 Jaden Allison (Fringeneering). All Rights Reserved.

DUAL LICENSE:
  * GNU Affero General Public License v3.0 (AGPLv3) — free for students,
    academic research, and open benchmark evaluation only.
  * Fringeneering Commercial Telemetry License — required for any
    proprietary, commercial, or closed-source integration (flight software,
    ground-station control loops, SSA platforms, or any product that is not
    itself released under AGPLv3).

Integrating this file into a proprietary system without a commercial
agreement is PROHIBITED. Commercial Telemetry Inquiries:
Jaden Allison (Fringeneering) — fringeneering@gmail.com

WHAT THIS IS
------------
Reads any standard NASA/NORAD/Space-Track Two-Line Element (TLE) catalog and
outputs a complete PWC Station-Keeping, GM-Debiasing, and Anderson-Maneuver
Audit for a customer.

USAGE
-----
  python step4_tle_customer_audit.py --tle <file.3le|.tle> [--out report.txt]
      Feed YOUR OWN Space-Track 3LE catalog (name + line1 + line2 triples,
      or bare 2-line pairs). No editing of this script required.

  python step4_tle_customer_audit.py
      Without --tle, falls back to the bundled demonstration catalog so the
      step suite remains reproducible out of the box.
"""
import argparse
import os
import sys

import numpy as np

from jiba_core import JibaStationKeepingEngine
from jiba_cli import parse_norad_tle, read_tle_catalog

# Bundled demonstration catalog (used only when no --tle file is supplied):
DEMO_CATALOG = [
    (
        "ISS (ZARYA) - LEO Crew Station",
        "1 25544U 98067A   26299.50000000  .00016717  00000-0  10270-3 0  9991",
        "2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.49815532412345"
    ),
    (
        "STARLINK-30142 - Commercial VLEO",
        "1 57321U 23099A   26299.50000000  .00008512  00000-0  58210-4 0  9994",
        "2 57321  53.1582 112.8410 0001420  88.1204 272.0115 15.06412890145123"
    ),
    (
        "STARLETTE - ILRS Geodetic Anchor",
        "1 07646U 75010A   26299.50000000 -.00000045  00000-0  12340-4 0  9998",
        "2 07646  49.8225 184.2210 0205812 214.1120 144.3210 13.82274110987654"
    ),
    (
        "LAGEOS-1 - ILRS MEO Anchor",
        "1 08820U 76039A   26299.50000000 -.00000009  00000-0  00000+0 0  9992",
        "2 08820 109.8421  42.1950 0044510 198.4120 161.5890  6.38664642123456"
    ),
]


def run_audit(entries, engine, source, out_path):
    """Runs the per-satellite Jiba audit over a (name, line1, line2) catalog."""
    report_lines = []

    def log(line=""):
        print(line)
        report_lines.append(line)

    log("=" * 124)
    log("   JIBA COMMERCIAL ORBIT AUDIT — DIRECT NORAD TLE TELEMETRY & STATION-KEEPING ANALYSIS")
    log("   Prepared by: Jaden Allison (Fringeneering) | Engine: Jiba v0.1 (Dual License AGPLv3 / Commercial)")
    log("   Governing Physics: Phase Wave Cosmology (ILRS alpha=2.635, beta=4.445, Anderson Constant V_A=14.6644 mm/s)")
    log(f"   TLE Source     : {source} ({len(entries)} satellite(s))")
    log("=" * 124)
    log(f"{'Satellite Name (NORAD ID)':<34} | {'Alt (km)':>9} | {'Inc (deg)':>9} | {'Noon-Wake Dip':>14} | {'GM Bias (ppb)':>14} | {'Anderson Kick':>15}")
    log("-" * 124)

    for name, l1, l2 in entries:
        orb = parse_norad_tle(name, l1, l2)
        a_km = orb["a_km"]
        alt_km = orb["alt_km"]

        # Evaluate Noon (0 deg) vs Midnight (180 deg) wave dip and orbital eccentricity radial speed
        res_noon = engine.evaluate_telemetry(alt_km=alt_km, sun_angle_deg=0.0, raw_radial_offset_m=0.0)
        dip_p2p_m = -2.0 * res_noon["elastic_wave_m"]

        # Calculate max radial velocity from orbital eccentricity (v_r,max = e * v_circ) for Anderson Effect kick
        v_circ_ms = np.sqrt(engine.GM_TRUE / (a_km * 1000.0))
        v_rad_max = orb["ecc"] * v_circ_ms
        res_burn  = engine.evaluate_telemetry(alt_km=alt_km, sun_angle_deg=180.0, raw_radial_offset_m=0.0, v_radial_ms=v_rad_max)

        # Calculate unmasked GM entropic bias in parts-per-billion (ppb)
        g_local = engine.GM_TRUE / ((a_km * 1000.0) ** 2)
        gm_bias_ppb = (engine.A_ENTROPY / g_local) * 1e9

        sat_label = f"{orb['name'][:26]} (#{orb['sat_id']})"
        log(f"{sat_label:<34} | {alt_km:9.1f} | {orb['inc_deg']:8.2f}d | {dip_p2p_m:+12.2f} m | {gm_bias_ppb:+10.3f} ppb | {res_burn['anderson_corr_mms']:+10.4f} mm/s")

    log("-" * 124)
    log("KEY OPERATIONAL DELIVERABLES FOR SATELLITE OPERATOR:")
    log("  1. ZERO-FUEL WAVE SURFING : Strips the elastic Noon-to-Midnight dipole wave (alpha=2.635) from thruster deadbands.")
    log("  2. MIDNIGHT WAKE BURNS    : Schedules station-keeping maneuvers at 180-deg Solar Midnight (-27.6% strain impedance).")
    log("  3. ANDERSON BURN TARGETING: Pre-corrects non-orbital/eccentric maneuvers using V_A = 14.6644 mm/s (beta=4.445).")
    log("  4. UNMASKED 1/r^2 GRAVITY : Removes the altitude-dependent a_entropy*r^2 bias baked into standard IERS GM.")
    log("=" * 124)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

    print(f"\n[SUCCESS] Saved client-ready audit report to: {os.path.abspath(out_path)}\n")


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="step4_tle_customer_audit",
        description="JIBA NORAD TLE reader & commercial audit generator.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=("Examples:\n"
                "  python step4_tle_customer_audit.py --tle my_catalog.3le\n"
                "  python step4_tle_customer_audit.py --tle my_catalog.3le "
                "--out my_report.txt\n"))
    ap.add_argument("--tle", help="customer Space-Track 3LE catalog (.tle/.3le); "
                                  "when omitted the bundled demo catalog is used")
    ap.add_argument("--out", default="Jiba_Customer_Audit_Report.txt",
                    help="report output path (default: Jiba_Customer_Audit_Report.txt)")
    args = ap.parse_args(argv)

    engine = JibaStationKeepingEngine(deadband_m=45.0)

    if args.tle:
        entries = read_tle_catalog(args.tle)
        if not entries:
            print(f"[ERROR] No TLE entries parsed from: {args.tle} "
                  "(expected Space-Track 3LE '1 '/'2 ' line pairs, optionally "
                  "preceded by a satellite name line).")
            return 1
        source = args.tle
    else:
        entries = DEMO_CATALOG
        source = "BUNDLED DEMO CATALOG (no --tle supplied)"

    run_audit(entries, engine, source, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
