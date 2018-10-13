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

t0 = 7.6 # minutes
t0 = t0 * 60

tf = 11
tf = tf * 60

dt = 0.5
time, lat = pd.resample(comment, 1, 'lat', t0, tf, dt)
time, lon = pd.resample(comment, 1, 'lon', t0, tf, dt)
time, alt = pd.resample(comment, 3, 'baro_alt', t0, tf, dt)
time, h = pd.resample(comment, 4, 'z', t0, tf, dt)
alt = alt - alt0
lat = pd.deg2meters(lat) - pd.deg2meters(lat[0])
lon = pd.deg2meters(lon) - pd.deg2meters(lon[0])
x = pd.deg2meters(cos(h))
y = pd.deg2meters(sin(h))

DT = 4
t, lat_v = 	pd.resample(comment, 1, 'lat', t0, tf, DT)
t, lon_v = 	pd.resample(comment, 1, 'lon', t0, tf, DT)
t, alt_v = 	pd.resample(comment, 3, 'baro_alt', t0, tf, DT)
t, head = pd.resample(comment, 4, 'x', t0, tf, DT)
alt_v = alt_v - alt0
head = deg2rad(head)
lat_v = pd.deg2meters(lat_v) - pd.deg2meters(lat_v[0])
lon_v = pd.deg2meters(lon_v) - pd.deg2meters(lon_v[0])
X = pd.deg2meters(cos(head))
Y = pd.deg2meters(sin(head))

fig1, (ax1, ax2) = plt.subplots(1,2)
ax1.plot(lon, lat, '-b', label='path')
ax1.quiver(lon, lat, x, y, label='heading')
ax1.set_xlabel('longitude (deg)')
ax1.set_ylabel('latitude (deg)')
ax1.legend()

ax2.plot(time, alt, '.-r')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Altitude (m)')

fig2 = plt.figure()
ax21 = fig2.gca(projection='3d')
ax21.plot(lon, lat, alt, '-r', label='Flight path')
ax21.plot(lon_v, lat_v, alt_v, 'ob')
#ax21.quiver(lon_v, lat_v, alt_v, X, Y, 0 )
ax21.legend()

plt.show()
