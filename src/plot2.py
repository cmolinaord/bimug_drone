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
h = deg2rad(h)
x = pd.deg2meters(cos(h))
y = pd.deg2meters(sin(h))

DT = 10
T, lat_v = 	pd.resample(comment, 1, 'lat', t0, tf, DT)
T, lon_v = 	pd.resample(comment, 1, 'lon', t0, tf, DT)
T, alt_v = 	pd.resample(comment, 3, 'baro_alt', t0, tf, DT)
T, head = pd.resample(comment, 4, 'x', t0, tf, DT)
alt_v = alt_v - alt0
headrad = deg2rad(head)
lat_v = pd.deg2meters(lat_v) - pd.deg2meters(lat_v[0])
lon_v = pd.deg2meters(lon_v) - pd.deg2meters(lon_v[0])
X = pd.deg2meters(cos(headrad))
Y = pd.deg2meters(sin(headrad))

# Figure 1 (Path in 2D)
#fig1, (ax1, ax2) = plt.subplots(1,2)
fig1 = plt.figure()
fig1.suptitle("2d path")
ax1 = fig1.gca()
ax1.plot(lon, lat, '-b', label='path')
ax1.quiver(lon, lat, x, y, label='heading')
ax1.set_xlabel('longitude (m)')
ax1.set_ylabel('latitude (m)')
ax1.axis('equal')
ax1.legend()
ax1.grid()


# Figre 2 (path in 3D)
fig2 = plt.figure()
fig2.suptitle("3d path")
ax2 = fig2.gca(projection='3d')
ax2.plot(lon, lat, alt, '-r', label='Flight path')
ax2.plot(lon_v, lat_v, alt_v, 'ob', label='10s steps')
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
alt = alt - alt0

fig3, (ax31, ax32) = plt.subplots(2,1)
fig3.suptitle("Altitude vs speed")
ax31.plot(t, speed, '.-b', label='Speed')
#ax31.plot(T, Speed, 'or')
ax31.set_ylabel('Speed (knots)')
ax31.legend()
ax31.grid()

ax32.plot(t, alt, '+-r', label='Altitude')
#ax32.plot(T, Alt, 'or')
ax32.set_xlabel('Time (s)')
ax32.set_ylabel('Alt (m)')
ax32.legend()
ax32.grid()



# Glode angle calculation
t0 = 587
tf = 594
t1, speed1 = pd.resample(comment, 1, 'knots', t0, tf, dt)
speed1 = pd.knots2ms(speed1)
avg_speed = np.average(speed1)

t1, alt = pd.resample(comment, 3, 'baro_alt', t0, tf, dt)
A = np.vstack([t1, np.ones(len(t1))]).T
vv, c = np.linalg.lstsq(A, alt, rcond=None)[0]

ax31.plot([t0, t0], [0, 1.1*max(speed)], '--g')
ax31.plot([tf, tf], [0, 1.1*max(speed)], '--g')
ax32.plot([t0, t0], [0, 150], '--g')
ax32.plot([tf, tf], [0, 150], '--g')

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

ax31.plot([t0, t0], [0, max(speed)], '--b')
ax31.plot([tf, tf], [0, max(speed)], '--b')
ax32.plot([t0, t0], [0, 150], '--b')
ax32.plot([tf, tf], [0, 150], '--b')

print("\nSecond period of gliding descending")
print("  -  -  -  -  -  -  -  -  -  -  -  -")
print("From %3.1fs to %3.1fs" % (t0, tf))
print("From %3.2fm to %3.2fm of altitude" % (t0*vv + c, tf*vv + c))
print("Mean horizontal velocity = %2.3f m/s" % avg_speed)
print("Mean vertical velocity = %2.3f m/s" % vv)
print("Glide ratio = %2.2f" % (-avg_speed / vv))



plt.show()
