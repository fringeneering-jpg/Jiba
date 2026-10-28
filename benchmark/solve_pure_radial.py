import os
import numpy as np
from datetime import datetime, timedelta, timezone
from sgp4.api import Satrec
from astropy.time import Time
from astropy.coordinates import TEME, ITRS, GCRS, CartesianRepresentation, get_sun
import astropy.units as u

BENCH_DIR = os.path.dirname(os.path.abspath(__file__))

C0 = 299792.458
R_E = 6378.137
AU_KM = 149597870.7
MPC_KM = 3.085677581e19
H0_SEC = 73.935 / MPC_KM  # 2.396e-18 s^-1

ILRS_STATIONS = {
    7090: np.array([-2389.0080,  5043.3320, -3078.5260]),  # Yarragadee, WA
    7825: np.array([-4467.0649,  2683.0349, -3667.0070]),  # Mt Stromlo, ACT
    7237: np.array([-2674.3870,  3757.1890,  4391.5080]),  # Changchun
    7821: np.array([-2830.7445,  4676.5800,  3275.0720]),  # Shanghai
    7249: np.array([-2148.7650,  4426.7590,  4044.5090]),  # Beijing
    7396: np.array([-2267.7490,  5009.3200,  3220.9670]),  # Wuhan
    7838: np.array([-3822.3880,  3699.3630,  3507.5730]),  # Simosato
    7358: np.array([-3526.3180,  4130.9850,  3221.0310]),  # Tanegashima
    7840: np.array([ 4033.4638,    23.6623,  4924.3050]),  # Herstmonceux
    7839: np.array([ 4194.4260,  1162.6940,  4647.2460]),  # Graz
    7810: np.array([ 4331.2830,   567.5490,  4633.1400]),  # Zimmerwald
    7105: np.array([ 1130.7190, -4831.3530,  3994.0870]),  # Greenbelt
    7941: np.array([ 4641.9510,  1393.0570,  4133.2800]),  # Matera
    8834: np.array([ 4075.5770,   931.7850,  4801.5830]),  # Wettzell
    7841: np.array([ 3800.6400,   882.0780,  5028.7910]),  # Potsdam
    7845: np.array([ 4581.6920,   556.1600,  4389.3550]),  # Grasse
    7110: np.array([-2386.2790, -4802.3540,  3444.8830]),  # Monument Peak
    7119: np.array([-5466.0650, -2404.2690,  2242.1990]),  # Haleakala
    7501: np.array([ 5085.4420,  2668.2630, -2768.6970]),  # Hartebeesthoek
}

SHELLS = [
    ("starlette", R_E + 812.0),
    ("lageos1",   R_E + 5900.0),
    ("etalon1",   R_E + 19120.0),
    ("qzs3",      R_E + 35786.0),
]

def load_tles(sat_name):
    fn = os.path.join(BENCH_DIR, f"{sat_name}_historical.tle")
    if not os.path.exists(fn): return []
    with open(fn, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]
    return [Satrec.twoline2rv(lines[i], lines[i+1])
            for i in range(len(lines)-1) if lines[i].startswith('1 ') and lines[i+1].startswith('2 ')]

def parse_passes(sat_name):
    fn = os.path.join(BENCH_DIR, f"{sat_name}_master_slr.npt")
    if not os.path.exists(fn): return []
    passes, curr = [], []
    st, dt_b, start_sec = None, None, 0.0
    with open(fn, 'r', errors='ignore') as f:
        for line in f:
            p = line.strip().split()
            if not p: continue
            rt = p[0].lower()
            if rt == 'h2' and len(p) >= 3:
                if len(curr) >= 4: passes.append(curr)
                curr = []
                try: st = int(p[2])
                except ValueError: st = None
            elif rt == 'h4' and len(p) >= 8:
                try:
                    dt_b = datetime(int(p[2]), int(p[3]), int(p[4]), tzinfo=timezone.utc)
                    start_sec = int(p[5]) * 3600 + int(p[6]) * 60 + float(p[7])
                except ValueError: dt_b = None
            elif rt == '11' and st in ILRS_STATIONS and dt_b:
                try:
                    sec = float(p[1])
                    if sec < start_sec - 43200.0: sec += 86400.0
                    curr.append((dt_b + timedelta(seconds=sec), st, 0.5 * C0 * float(p[2])))
                except (ValueError, IndexError): continue
    if len(curr) >= 4: passes.append(curr)
    return passes

def solve_pure_radial_passes(sat_name, r_orb_km):
    tles = load_tles(sat_name)
    passes = parse_passes(sat_name)
    if not tles or not passes: return None
    tle_jds = np.array([s.jdsatepoch + s.jdsatepochF for s in tles])

    # Sample up to 600 full multi-point passes per satellite
    step = max(1, len(passes) // 600)
    sampled_passes = passes[::step]

    pass_dts, pass_rad_bias_m, pass_dt_days = [], [], []
    pass_r_teme = []

    for ps in sampled_passes:
        mid_dt, st_id, _ = ps[len(ps)//2]
        t_jd_mid = mid_dt.timestamp() / 86400.0 + 2440587.5
        idx = np.argmin(np.abs(tle_jds - t_jd_mid))
        dt_days = abs(tle_jds[idx] - t_jd_mid)
        if dt_days > 2.5 or dt_days < 0.01: continue

        dts = [pt[0] for pt in ps]
        slr_kms = np.array([pt[2] for pt in ps])
        r_temes, v_temes = [], []
        ok = True
        for dt_pt in dts:
            jd = dt_pt.timestamp() / 86400.0 + 2440587.5
            e, r_t, v_t = tles[idx].sgp4(np.floor(jd), jd - np.floor(jd))
            if e != 0: ok = False; break
            r_temes.append(r_t)
            v_temes.append(v_t)
        if not ok: continue

        t_vec = Time(dts, scale='utc')
        teme_c = TEME(CartesianRepresentation(np.array(r_temes).T * u.km), obstime=t_vec)
        itrs_c = teme_c.transform_to(ITRS(obstime=t_vec))
        r_itrs = np.vstack([itrs_c.cartesian.x.to(u.km).value,
                            itrs_c.cartesian.y.to(u.km).value,
                            itrs_c.cartesian.z.to(u.km).value]).T

        st_pos = ILRS_STATIONS[st_id]
        los_vec = r_itrs - st_pos
        pred_km = np.linalg.norm(los_vec, axis=1)
        los_unit = los_vec / pred_km[:, None]

        # Range rate d(rho)/dt along pass
        t_sec = np.array([(d - dts[0]).total_seconds() for d in dts])
        if t_sec[-1] < 10.0: continue
        drho_dt = np.gradient(pred_km, t_sec) * 1000.0  # m/s

        # Raw slant residual in meters
        y_res = (slr_kms - pred_km) * 1000.0
        if np.max(np.abs(y_res)) > 5000.0: continue

        # Radial unit vector vs Line-of-sight unit vector
        r_unit = r_itrs / np.linalg.norm(r_itrs, axis=1, keepdims=True)
        cos_z = np.sum(los_unit * r_unit, axis=1)

        # 2-parameter least squares per pass: y_res = Radial_Bias * cos_z + Time_Bias * drho_dt
        A = np.vstack([cos_z, drho_dt]).T
        sol, _, _, _ = np.linalg.lstsq(A, y_res, rcond=None)
        radial_bias_m = sol[0]  # True radial offset with along-track clock error stripped!

        pass_dts.append(mid_dt)
        pass_rad_bias_m.append(radial_bias_m)
        pass_dt_days.append(dt_days)
        pass_r_teme.append(r_temes[len(ps)//2])

    if not pass_dts: return None

    t_mid_vec = Time(pass_dts, scale='utc')
    teme_mid = TEME(CartesianRepresentation(np.array(pass_r_teme).T * u.km), obstime=t_mid_vec)
    gcrs_mid = teme_mid.transform_to(GCRS(obstime=t_mid_vec))
    r_sat = np.vstack([gcrs_mid.cartesian.x.to(u.km).value,
                       gcrs_mid.cartesian.y.to(u.km).value,
                       gcrs_mid.cartesian.z.to(u.km).value]).T
    sun = get_sun(t_mid_vec)
    r_sun = np.vstack([sun.cartesian.x.to(u.km).value,
                       sun.cartesian.y.to(u.km).value,
                       sun.cartesian.z.to(u.km).value]).T

    u_sat = r_sat / np.linalg.norm(r_sat, axis=1, keepdims=True)
    u_sun = r_sun / np.linalg.norm(r_sun, axis=1, keepdims=True)
    cos_theta = np.sum(u_sat * u_sun, axis=1)
    cross_z = u_sun[:, 0] * u_sat[:, 1] - u_sun[:, 1] * u_sat[:, 0]

    rad_arr = np.array(pass_rad_bias_m)
    rate_m_d = np.abs(rad_arr) / np.array(pass_dt_days)

    noon = cos_theta >= 0.5
    mid  = cos_theta <= -0.5
    dusk = (cos_theta > -0.5) & (cos_theta < 0.5) & (cross_z >= 0)
    dawn = (cos_theta > -0.5) & (cos_theta < 0.5) & (cross_z < 0)

    def fmt(a): return f"{np.median(a):7.2f} m/d" if len(a) > 0 else "    --     "
    wake_noon_m = (np.median(rad_arr[mid]) - np.median(rad_arr[noon])) if (np.any(mid) and np.any(noon)) else 0.0
    min_bin = rate_m_d[dawn] if np.any(dawn) else rate_m_d[mid]
    strain_s = (np.median(min_bin) / (r_orb_km * 1000.0)) / 86400.0 if len(min_bin) > 0 else 0.0

    return len(rad_arr), fmt(rate_m_d[noon]), fmt(rate_m_d[dusk]), fmt(rate_m_d[mid]), fmt(rate_m_d[dawn]), wake_noon_m, strain_s

if __name__ == '__main__':
    print("=" * 110)
    print("ALONG-TRACK DEBIASED PURE RADIAL SOLVER (SGP4 Clock Jitter Stripped via Pass Least-Squares)")
    print("=" * 110)
    print(f"{'Satellite':<10} | {'Passes':>6} | {'1.Noon(Peak)':>12} | {'2.Dusk(Cool)':>12} | {'3.Midnight':>12} | {'4.PreDawn(Min)':>14} | {'Wake-Noon (m)':>14} | {'Pure Strain/s':>14}")
    print("-" * 110)
    for sat, r_km in SHELLS:
        res = solve_pure_radial_passes(sat, r_km)
        if res:
            n_p, n_s, d_s, m_s, pd_s, wn_m, st_s = res
            print(f"{sat:<10} | {n_p:6d} | {n_s:>12} | {d_s:>12} | {m_s:>12} | {pd_s:>14} | {wn_m:+12.2f} m | {st_s:12.3e}/s")
    print("=" * 110)
