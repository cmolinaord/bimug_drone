import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np
import csv
import process_data as pd
from matplotlib import animation
import cv2

# Load and compute google_earth aerial_image
map = plt.imread("../img/aerial_image.png")
edge = np.zeros([2,2])
with open("../img/coordinates.txt") as f:
	reader = csv.reader(f)
	i = 0
	for row in reader:
		edge[i,:] = row
		i += 1

offset_x = 25e-5
offset_y = 10e-5
edge[:,0] = edge[:,0] - offset_y
edge[:,1] = edge[:,1] - offset_x

fig1 = plt.figure(figsize=(16,9))
ax1 = fig1.gca()
line, = ax1.plot([], [], '-y', label='path')

fig2 = plt.figure(figsize=(16,9))
ax2 = fig2.gca()

# Load and compute path
dt = 1
t0 = 800
tf = 920
# Flight name
comment = "f1"

def init():
	ax1.imshow(map, extent=(edge[0,1],edge[1,1],edge[0,0],edge[1,0]))
	return line,

# animation function.  This is called sequentially
def path(i):
	t, lat = pd.resample(comment, 1, 'lat', t0, i, dt)
	t, lon = pd.resample(comment, 1, 'lon', t0, i, dt)
	line.set_data(lon, lat)
	return line,

#anim.save('../flight_path/' + comment + '.mp4', fps=10, extra_args=['-vcodec', 'libx264'])



flight1_video = '/home/data/Videos/MASE/Aerolabs/cuts/1st_flight.mp4'

cap = cv2.VideoCapture(flight1_video)

frm = 0

while(cap.isOpened()):
	frm += 1
	if frm % 24 == 0:
		i = t0 + 1
	t, lat = pd.resample(comment, 1, 'lat', t0, i, dt)
	t, lon = pd.resample(comment, 1, 'lon', t0, i, dt)
	ax2.plot([], [], '-y', label='path')

	ret, frame = cap.read()
	cv2.imshow('frame',frame)
	#anim = animation.FuncAnimation(fig1, animate, init_func=init, frames=tf, interval=1, blit=True)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break


plt.show()

cap.release()
cv2.destroyAllWindows()
