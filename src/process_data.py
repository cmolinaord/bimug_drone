import csv
import numpy as np
from numpy import pi, sqrt
import sensor

R_Earth = 6378100 # Meters

def resample(comment, mode, column, t0, tf, dt):
	# This function resamples the recorded data from t0 to tf with a
	# step of dt (in seconds) for the given sensor and column
	# giving as output, the new resampled time, and the corresponding data measurements

	time = []
	y = []
	index = sensor.modes[mode]['data'].index(column)

	filename = 'output_data/' + comment + '_S' + str(mode) + "_" + sensor.modes[mode]['name'] + ".csv"
	csvfile = open(filename, 'r')
	reader = csv.reader(csvfile, delimiter='\t')
	for row in reader:
		if not len(row) == 1:
			time.append(float(row[0]))
			y.append(float(row[index]))
	time_new = np.arange(t0, tf, dt)
	y_new = np.interp(time_new, time, y)
	return time_new, y_new


def deg2meters(d):
	# This function gives the distance in meters over the Earth surface
	# given an angle in degrees measured from the center of the Earth
	m = d * (2 * pi) / 360 * R_Earth
	return m

def dist(A, B):
	# Give distance between coordinates A and B in meters
	# A and B must be given in degrees
	d = sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2 )
	d = deg2meters(d)
	return d

def knots2ms(kn):
	# Converse knots to m/s
	return kn * 0.51444

def export_kml_path(comment, t0, tf, dt=2, altitude=False):
	# Export a KML file with the flight path corresponding to "comment"
	# to be visualized in Google Earth
	# Times given in minutes

	time, alt0 = resample(comment, 3, 'baro_alt', 2*60, 4*60, 0.5)
	alt0 = np.average(alt0)

	t0 = 60 * t0
	tf = 60 * tf

	time, lat = resample(comment, 1, 'lat', t0, tf, dt)
	time, lon = resample(comment, 1, 'lon', t0, tf, dt)
	if altitude:
		time, alt = resample(comment, 3, 'baro_alt', t0, tf, dt)
	alt = alt - alt0

	for i in range(len(time)):
		print('%2.5f,%2.5f,%1.3f' % (lon[i], lat[i], alt[i]) )
