# -*- coding: utf-8 -*-
"""
jiba.py — JIBA UNIFIED INGEST CLI (ONE-COMMAND ENTRY POINT)

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

USAGE
-----
  python jiba.py ingest --tle <file.3le|.tle>                        # TLE audit
  python jiba.py ingest --crd <file.npt|.crd> --tle <file.tle>       # SLR proof
  python jiba.py ingest --tle <cat.3le> --crd <file.npt> \
         --tle <hist.tle> --out tracking_report.txt                  # unified report
  python jiba.py --selftest                                          # engine health

Thin dispatcher over jiba_cli.main(); the whole pipeline lives in jiba_cli.py.
"""
import sys

from jiba_cli import main

if __name__ == "__main__":
    sys.exit(main())
