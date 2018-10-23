import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np
import csv
import process_data as pd
from matplotlib import animation

# Load and compute google_earth aerial_image
map = plt.imread("img/aerial_image.png")
edge = np.zeros([2,2])
with open("img/coordinates.txt") as f:
	reader = csv.reader(f)
	i = 0
	for row in reader:
		edge[i,:] = row
		i += 1

offset_x = 25e-5
offset_y = 10e-5
edge[:,0] = edge[:,0] - offset_y
edge[:,1] = edge[:,1] - offset_x

fig = plt.figure(figsize=(16,9))
ax = fig.gca()
line, = ax.plot([], [], '-y', label='path')

# Load and compute path
dt = 1
t0 = 800
tf = 920
# Flight name
comment = "f1"

def init():
	ax.imshow(map, extent=(edge[0,1],edge[1,1],edge[0,0],edge[1,0]))
	return line,

# animation function.  This is called sequentially
def animate(i):
	tf = t0 + i
	t, lat = pd.resample(comment, 1, 'lat', t0, tf, dt)
	t, lon = pd.resample(comment, 1, 'lon', t0, tf, dt)
	line.set_data(lon, lat)
	return line,

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=tf-t0, interval=1, blit=True)
anim.save('flight_path/' + comment + '.mp4', fps=10, extra_args=['-vcodec', 'libx264'])
plt.show()
