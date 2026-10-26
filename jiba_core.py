# -*- coding: utf-8 -*-
"""
jiba_core.py — JIBA COMMERCIAL ORBITAL STATION-KEEPING & TELEMETRY DEBIASING KERNEL
Copyright (c) 2026 Jaden Allison (Fringeneering). Dual Licensed: AGPLv3 / Commercial License.
Physics Core: Phase Wave Cosmology (ILRS alpha = 2.635, beta = 4.445, Anderson V_A = 14.6644 mm/s)
"""
import numpy as np

class JibaStationKeepingEngine:
    def __init__(self, deadband_m=45.0):
        # Locked Geodetic & PWC Constants (Zero Fitted Parameters)
        self.R_EARTH_KM    = 6378.137
        self.GM_APP_REF    = 3.986004418e14     # m^3/s^2
        self.OMEGA_EARTH   = 7.2921150e-5       # rad/s
        self.C0_MS         = 299792458.0
        self.H0_SEC        = 2.39607e-18        # s^-1
        self.A_ENTROPY     = 8.9297e-10         # m/s^2 (c0 * H0 * (1 + drho_geom))
        
        # ILRS Starlette & LAGEOS-1 Calibration Anchors
        self.R1_KM         = 7190.137
        self.R2_M          = 12278137.0
        self.DR1_M         = 100.55             # Starlette Noon-Wake dipole amplitude (m)
        self.GAMMA1_SEC    = 1.746e-9           # Starlette radial strain rate (s^-1)
        self.ALPHA         = 2.635              # Wake-Noon dipole exponent
        self.BETA          = 4.445              # Radial shear strain exponent
        self.V_ANDERSON_MS = 2.0 * self.OMEGA_EARTH * self.DR1_M  # 14.6644 mm/s
        
        # Unmasked True 1/r^2 Earth GM
        self.GM_TRUE       = self.GM_APP_REF - self.A_ENTROPY * (self.R2_M ** 2)
        self.deadband_m    = deadband_m

    def evaluate_telemetry(self, alt_km, sun_angle_deg, raw_radial_offset_m, v_radial_ms=0.0):
        """
        Takes raw satellite sensor telemetry and returns:
          - debiased_secular_offset_m : True orbital drift after stripping the elastic Noon-Wake wave
          - std_thruster_cmd          : What a dumb standard autopilot would do
          - jiba_thruster_cmd         : What Jiba commands (saving fuel & waiting for Midnight Wake)
          - wake_impedance_factor     : Local strain multiplier (drops by 27.6% at Midnight = 180 deg)
          - anderson_dv_corr_mms      : Non-orbital Anderson Effect maneuver correction (mm/s)
        """
        r_km = self.R_EARTH_KM + alt_km
        r_m  = r_km * 1000.0
        cos_sun = np.cos(np.radians(sun_angle_deg))

        # 1. Elastic Noon-to-Midnight Wave Offset (alpha = 2.635):
        #    Positive (+cos_sun) at Noon (0 deg), Negative (-cos_sun) at Midnight (180 deg)
        elastic_wave_m = 0.5 * self.DR1_M * ((self.R1_KM / r_km) ** self.ALPHA) * cos_sun

        # 2. Strip elastic wave from raw sensor reading to get TRUE secular orbital decay:
        debiased_offset_m = raw_radial_offset_m - elastic_wave_m

        # 3. Local Strain Impedance Relief in the Midnight Wake (beta = 4.445):
        #    Drops from 1.000 at Noon (0 deg) down to 0.724 (-27.6%) at Midnight (180 deg)
        wake_impedance = 1.0 - 0.138 * (1.0 - cos_sun)
        in_midnight_pocket = (sun_angle_deg >= 135.0 and sun_angle_deg <= 225.0)

        # 4. Anderson Effect Non-Orbital Maneuver Correction (when v_radial != 0):
        v_circ_ms = np.sqrt(self.GM_TRUE / r_m)
        anderson_corr_mms = (self.V_ANDERSON_MS * 1000.0) * (v_radial_ms / v_circ_ms) * ((self.R1_KM / r_km) ** self.BETA)

        # 5. Compare Standard Autopilot vs. Jiba Smart Controller:
        std_cmd = "FIRE THRUSTER (WASTED)" if abs(raw_radial_offset_m) > self.deadband_m else "HOLD"

        if abs(debiased_offset_m) <= self.deadband_m:
            jiba_cmd = "HOLD (SURFING WAVE)"
        else:
            if in_midnight_pocket:
                jiba_cmd = "FIRE IN WAKE (-27.6% STRAIN)"
            else:
                jiba_cmd = "WAIT FOR MIDNIGHT POCKET"

        return {
            "elastic_wave_m": elastic_wave_m,
            "debiased_offset_m": debiased_offset_m,
            "wake_impedance": wake_impedance,
            "anderson_corr_mms": anderson_corr_mms,
            "std_cmd": std_cmd,
            "jiba_cmd": jiba_cmd
        }
