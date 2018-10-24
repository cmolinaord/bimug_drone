import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import process_data as pd
import numpy as np
from numpy import pi, sin, cos, deg2rad

mpl.rcParams['legend.fontsize'] = 10

comment = "f1"

time, alt0 = pd.resample(comment, 3, 'baro_alt', 2*60, 4*60, 0.5)
alt0 = np.average(alt0)

dt = 0.5
t0 = 800
tf = 920

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
ax1.axis('equal')
ax1.legend()
ax1.grid()

# Figre 2 (path in 3D)
max_range = np.array([lon.max()-lon.min(), lat.max()-lat.min(), alt.max()-alt.min()]).max() / 2.0

mid_x = (lon.max() + lon.min()) * 0.5
mid_y = (lat.max() + lat.min()) * 0.5
mid_z = (alt.max() + alt.min()) * 0.5

# Figure 2 (Path in 3D)
fig2 = plt.figure()
ax2 = fig2.gca(projection='3d')
ax2.plot(lon, lat, alt, '-r', label='Flight path')
ax2.plot(lon_v, lat_v, alt_v, 'ob')
ax2.set_xlim(mid_x - max_range, mid_x + max_range)
ax2.set_ylim(mid_y - max_range, mid_y + max_range)
ax2.set_zlim(mid_z - max_range, mid_z + max_range)
#ax2.quiver(lon_v, lat_v, alt_v, X, Y, 0 )
ax2.legend()

# Figure 3 (glide angle)

dt = 0.5
t0 = 800
tf = 920

t, speed = 	pd.resample(comment, 1, 'knots', t0, tf, dt)
T, Speed = 	pd.resample(comment, 1, 'knots', t0, tf, DT)
t, alt 	=	pd.resample(comment, 3, 'baro_alt', t0, tf, dt)
T, Alt 	=	pd.resample(comment, 3, 'baro_alt', t0, tf, DT)
alt = alt - alt0

fig3, (ax31, ax32) = plt.subplots(2,1)
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

plt.show()
