import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import process_data as pd
import numpy as np
from numpy import pi, sin, cos, deg2rad

mpl.rcParams['legend.fontsize'] = 10

comment = "f2"

time, alt0 = pd.resample(comment, 3, 'baro_alt', 2*60, 4*60, 0.5)
alt0 = np.average(alt0)

dt = 0.5
t0 = 530
tf = 660

dt = 0.5
t, lat = pd.resample(comment, 1, 'lat', t0, tf, dt)
t, lon = pd.resample(comment, 1, 'lon', t0, tf, dt)
t, alt = pd.resample(comment, 3, 'baro_alt', t0, tf, dt)
t, h = pd.resample(comment, 4, 'x', t0, tf, dt)
alt = alt - alt0
lat = pd.deg2meters(lat) - pd.deg2meters(lat[0])
lon = pd.deg2meters(lon) - pd.deg2meters(lon[0])
x = pd.deg2meters(cos(h))
y = pd.deg2meters(sin(h))

DT = 10
T, lat_v = 	pd.resample(comment, 1, 'lat', t0, tf, DT)
T, lon_v = 	pd.resample(comment, 1, 'lon', t0, tf, DT)
T, alt_v = 	pd.resample(comment, 3, 'baro_alt', t0, tf, DT)
T, head = pd.resample(comment, 4, 'x', t0, tf, DT)
alt_v = alt_v - alt0
head = deg2rad(head)
lat_v = pd.deg2meters(lat_v) - pd.deg2meters(lat_v[0])
lon_v = pd.deg2meters(lon_v) - pd.deg2meters(lon_v[0])
X = pd.deg2meters(cos(head))
Y = pd.deg2meters(sin(head))

# Figure 1 (Path in 2D)
#fig1, (ax1, ax2) = plt.subplots(1,2)
fig1 = plt.figure()
ax1 = fig1.gca()
ax1.plot(lon, lat, '-b', label='path')
ax1.quiver(lon, lat, x, y, label='heading')
ax1.set_xlabel('longitude (deg)')
ax1.set_ylabel('latitude (deg)')
ax1.legend()

# Figre 2 (path in 3D)
fig2 = plt.figure()
ax2 = fig2.gca(projection='3d')
ax2.plot(lon, lat, alt, '-r', label='Flight path')
ax2.plot(lon_v, lat_v, alt_v, 'ob')
#ax2.quiver(lon_v, lat_v, alt_v, X, Y, 0 )
ax2.legend()

# Figure 3 (glide angle)

dt = 0.5
t0 = 530
tf = 660

t, speed = 	pd.resample(comment, 1, 'knots', t0, tf, dt)
T, Speed = 	pd.resample(comment, 1, 'knots', t0, tf, DT)
t, alt 	=	pd.resample(comment, 3, 'baro_alt', t0, tf, dt)
T, Alt 	=	pd.resample(comment, 3, 'baro_alt', t0, tf, DT)

fig3 = plt.figure()
ax31 = fig3.gca()
ax31.plot(t, speed, '.-b')
ax31.plot(T, Speed, 'or')
ax31.set_xlabel('Time (s)')
ax31.set_ylabel('Speed (knots)')
ax32 = ax31.twinx()
ax32.plot(t, alt, '-b')
ax32.plot(T, Alt, 'or')
ax32.set_ylabel('Alt (m)')

plt.show()


# Glode angle calculation
t0 = 587
tf = 594
t1, speed1 = pd.resample(comment, 1, 'knots', t0, tf, dt)
speed1 = pd.knots2ms(speed1)
avg_speed = np.average(speed1)

t1, alt = pd.resample(comment, 3, 'baro_alt', t0, tf, dt)
A = np.vstack([t1, np.ones(len(t1))]).T
vv, c = np.linalg.lstsq(A, alt, rcond=None)[0]

print("\nFirst period of gliding descending")
print("  -  -  -  -  -  -  -  -  -  -  -  -")
print("From %3.1fs to %3.1fs" % (t0, tf))
print("From %3.2fm to %3.2fm of altitude" % (t0*vv + c, tf*vv + c))
print("Mean horizontal velocity = %2.3f m/s" % avg_speed)
print("Mean vertical velocity = %2.3f m/s" % vv)
print("Glide ratio = %2.2f" % (-avg_speed / vv))

t0 = 600
tf = 625
t1, speed1 = pd.resample(comment, 1, 'knots', t0, tf, dt)
speed1 = pd.knots2ms(speed1)
avg_speed = np.average(speed1)

t1, alt = pd.resample(comment, 3, 'baro_alt', t0, tf, dt)
A = np.vstack([t1, np.ones(len(t1))]).T
vv, c = np.linalg.lstsq(A, alt, rcond=None)[0]

print("\nSecond period of gliding descending")
print("  -  -  -  -  -  -  -  -  -  -  -  -")
print("From %3.1fs to %3.1fs" % (t0, tf))
print("From %3.2fm to %3.2fm of altitude" % (t0*vv + c, tf*vv + c))
print("Mean horizontal velocity = %2.3f m/s" % avg_speed)
print("Mean vertical velocity = %2.3f m/s" % vv)
print("Glide ratio = %2.2f" % (-avg_speed / vv))
