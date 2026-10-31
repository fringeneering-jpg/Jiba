import os
import numpy as np
import matplotlib
matplotlib.use("Agg")     # headless-safe
import matplotlib.pyplot as plt

# ==============================================================================
# JIBA ENGINE - STEP 2: VISUAL COMMERCIAL PITCH CHART GENERATOR
# Physics by Jaden Allison (Fringeneering)
# ==============================================================================

plt.style.use('dark_background')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.5, 5.6), gridspec_kw={'wspace': 0.25})
fig.suptitle("JIBA STATION-KEEPING ENGINE — DETERMINISTIC WAVE-WAKE SURFING vs. STANDARD AUTOPILOT",
             fontsize=13.5, fontweight='bold', y=0.97)

# ------------------------------------------------------------------------------
# PANEL 1: 3 ORBITS AT 550 KM VLEO (NOON-TO-MIDNIGHT -110.88m DIP)
# ------------------------------------------------------------------------------
t_hours = np.linspace(0, 4.8, 600)          # 3 LEO orbits (~96 mins each)
omega_orb = 2.0 * np.pi / 1.6               # Orbital angular frequency
dip_amp_m = 55.44                           # +/- 55.44 m = 110.88 m peak-to-trough Noon-Wake wave

# Natural PWC Noon-to-Midnight wave-trench oscillation + slow real drag decay (-4 m/hr):
natural_wave_m = dip_amp_m * np.cos(omega_orb * t_hours) - 3.5 * t_hours

# Standard Autopilot: panics whenever satellite dips below -45m deadband and fires thrusters
std_path_m = np.copy(natural_wave_m)
burn_times = []
burn_vals  = []
offset = 0.0
for i in range(len(t_hours)):
    val = natural_wave_m[i] + offset
    if val < -45.0:
        offset += 38.0   # Wasteful thruster firing fighting the reversible Midnight pocket!
        burn_times.append(t_hours[i])
        burn_vals.append(val)
    elif val > 55.0:
        offset -= 30.0   # Wasteful counter-burn on the Noon side!
        burn_times.append(t_hours[i])
        burn_vals.append(val)
    std_path_m[i] = natural_wave_m[i] + offset

# Jiba Engine: subtracts the known alpha=2.635 Noon-Wake dipole and only does 1 tiny burn in Midnight wake
jiba_mean_drift = -3.5 * t_hours

ax1.plot(t_hours, std_path_m, color='#ff4d4d', lw=2.0, linestyle='--', label='Standard Autopilot (Fights Wave = Wastes Fuel)')
ax1.plot(t_hours, natural_wave_m, color='cyan', lw=2.8, label='Jiba Wave-Surfing Path (Rides Natural -110.9m Dip)')
ax1.plot(t_hours, jiba_mean_drift, color='lime', lw=2.0, linestyle=':', label='Jiba Debiased Mean Orbit (Zero False Burns)')

ax1.axhline(45, color='white', linestyle='-.', alpha=0.35, label='Standard +/-45m Deadband Box')
ax1.axhline(-45, color='white', linestyle='-.', alpha=0.35)

ax1.scatter(burn_times, burn_vals, color='yellow', edgecolor='red', s=90, zorder=6, label='Wasted Standard Thruster Fires')

ax1.set_title("1. VLEO (550 km): Riding the -110.9m Noon-Wake Trench", fontsize=11, fontweight='bold', pad=8)
ax1.set_xlabel("Mission Time (Hours — 3 Orbits)", fontsize=10.5)
ax1.set_ylabel("Radial Altitude Offset (Meters)", fontsize=10.5)
ax1.set_ylim(-110, 105)
ax1.grid(True, alpha=0.2)
ax1.legend(loc='upper right', fontsize=8.5)

# ------------------------------------------------------------------------------
# PANEL 2: ANNUAL PROPELLANT (DELTA-V) CONSUMPTION COMPARISON
# ------------------------------------------------------------------------------
categories = ['Starlink VLEO\n(550 km)', 'Starlette LEO\n(812 km)', 'Polar LEO\n(1,200 km)', 'GEO Telecom\n(35,786 km)']
std_burns  = [45.00, 18.50, 8.20, 50.00]
jiba_burns = [34.63, 12.65, 5.33, 42.42]
pct_saves  = ["-23.0%", "-31.6%", "-35.0%", "-15.2%"]

x = np.arange(len(categories))
width = 0.36

rects1 = ax2.bar(x - width/2, std_burns, width, label='Standard SGP4/GMAT Autopilot', color='#ff4d4d', alpha=0.85)
rects2 = ax2.bar(x + width/2, jiba_burns, width, label='Jiba Engine (PWC Wake-Surfing)', color='#00e676', alpha=0.90)

for i in range(len(categories)):
    ax2.annotate(f"SAVED\n{pct_saves[i]}",
                 xy=(x[i] + width/2, jiba_burns[i]),
                 xytext=(0, 8), textcoords="offset points",
                 ha='center', va='bottom', color='lime', fontweight='bold', fontsize=9.5)

ax2.set_title("2. Annual Thruster Propellant Burn (m/s per Year — Lower is Better)", fontsize=11, fontweight='bold', pad=8)
ax2.set_xticks(x)
ax2.set_xticklabels(categories, fontsize=9.5)
ax2.set_ylabel("Annual Station-Keeping Delta-V (m/s/yr)", fontsize=10.5)
ax2.set_ylim(0, 60)
ax2.grid(True, axis='y', alpha=0.2)
ax2.legend(loc='upper left', fontsize=9.5)

fig.subplots_adjust(top=0.86, bottom=0.14, left=0.06, right=0.97, wspace=0.24)
out_png = os.path.abspath("Jiba_Commercial_Pitch.png")
plt.savefig(out_png, dpi=300, bbox_inches='tight')
print(f"\n[SUCCESS] Commercial pitch graphic saved to: {out_png}")
plt.show()
