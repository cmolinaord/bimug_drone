import sys
import sensor
import mat4py
import numpy as np
from datetime import datetime

# Read the arguments given to load the raw data file
if len(sys.argv) == 1:
	print("ERROR: You must give me the a filename which contains the raw data")
	exit()
filename = sys.argv[1]

# Begin parsing data file
print("Parsing file:", filename)
f = open(filename, 'r')
line = f.readline().rstrip('\n')
line_n = 1 # Line number counter

# Global time initialization
miliseconds = [0,0]
Ntime = 0 # Number of 10s passed
time = 0 # Real global time in seconds after bootloading

# Initializing output data
# GPSPOS
gpspos_time = np.zeros([1,1])
utc 		= np.zeros([1,1])
AV 			= np.zeros([1,1])
lat 		= np.zeros([1,1])
NS			= np.zeros([1,1])
lon 		= np.zeros([1,1])
EW			= np.zeros([1,1])
knots 		= np.zeros([1,1])
track 		= np.zeros([1,1])
date 		= np.zeros([1,1])
# GPSFIX
gpsfix_time = np.zeros([1,1])
numsat 		= np.zeros([1,1])
dop 		= np.zeros([1,1])
gps_alt 	= np.zeros([1,1])
# ATMOSPHERIC
atm_time 	= np.zeros([1,1])
temp 		= np.zeros([1,1])
pressure	= np.zeros([1,1])
baro_alt	= np.zeros([1,1])
# HEADING
head_time 	= np.zeros([1,1])
heading 	= np.zeros([1,3])
# ACCELERATION
acc_time 	= np.zeros([1,1])
acceleration= np.zeros([1,3])
# CALIBRATION
cal_time 	= np.zeros([1,1])
calibration = np.zeros([1,4])
# BUTTONS
button_time	= np.zeros([1,1])
buttons 	= np.zeros([1,4])

while line:
	# Skipping (and printing) header lines
	if not line.startswith('$'):
		print("       ",line)
		line = f.readline().rstrip('\n')
		line_n += 1
		continue

	# WARING if data is not consistent with valid format
	if line[1] is not 'S':
		print("\nWARNING, line %i: Found a line starting with something different from '$S#' (Skipping line):" % line_n)
		print("         ",line)
		print("         Make sure the file is correct data from a flight using BIMUG system")
		line_n += 1
		line = f.readline().rstrip('\n')
		continue

	# Starting operations in current valid data line
	data = sensor.parse(line)
	mode = int(data[0][2])
	# Global time computation (since system start-up)
	# Take into account that data[-1] gives time in miliseconds and it's reset every 10s
	miliseconds[1] = int(data[-1])
	if miliseconds[1] < miliseconds[0]:
		Ntime += 1
	time = 10*Ntime + 1e-3*miliseconds[1]
	miliseconds[0] = miliseconds[1]

	print("Line %i: type $S%i, time = %3.3f" % (line_n, mode, time))

	if mode is 1:
		# GPSPOS
		# Preprocces
		if gpsfix:
			gpstime = str.split(data[1],'.')[0] # Use only integer part of time (always is measured at excat seconds)
			utc_time = datetime.strptime(data[9] + gpstime, '%d%m%y%H%M%S')
			latitude	= sensor.coordinates(data[3])
			longitude 	= sensor.coordinates(data[5])
			# Maybe it would be needed to skip empty values of data resulting from incorrect datasum sentences
			gpspos_time = np.concatenate((gpspos_time, 	[[time]] )) # Warning with the 10 second reset
			utc 		= np.concatenate((utc, 			[[ utc_time ]] ))
			AV 			= np.concatenate((AV, 			[[ data[2] ]] ))
			lat 		= np.concatenate((lat, 			[[ latitude ]] ))
			NS			= np.concatenate((NS, 			[[ data[4] ]] ))
			lon 		= np.concatenate((lon, 			[[ longitude ]] ))
			EW			= np.concatenate((EW, 			[[ data[6] ]] ))
			knots 		= np.concatenate((knots, 		[[ float(data[7]) ]] ))
			track 		= np.concatenate((track, 		[[ float(data[8]) ]] ))
		else:
			print("WARNING: GPS not fixed (time = %3.3f)" % time)

	elif mode is 2:
		# GPSFIX
		gpsfix = bool(int(data[1]))
		if gpsfix:
			gpsfix_time = np.concatenate((gpsfix_time, 	[[time]] ))
			numsat 		= np.concatenate((numsat, 		[[ int(data[2]) ]] ))
			dop 		= np.concatenate((dop, 			[[ float(data[3]) ]] ))
			gps_alt 	= np.concatenate((gps_alt, 		[[ float(data[4]) ]] ))
		else:
			print("WARNING: GPS not fixed (time = %3.3f)" % time)


	elif mode is 3:
		# ATMOSPHERIC sensors
		atm_time 	= np.concatenate((atm_time, 	[[time]] ))
		temp 		= np.concatenate((temp,			[[ float(data[1]) ]] ))
		pressure	= np.concatenate((pressure,		[[ float(data[2]) ]] ))
		baro_alt	= np.concatenate((baro_alt,		[[ float(data[3]) ]] ))

	elif mode is 4:
		# HEADING
		head_time 	= np.concatenate((head_time,	[[time]] ))
		x = float(data[1])
		y = float(data[2])
		z = float(data[3])
		head = [x,y,z]
		heading 	= np.concatenate((heading, 		[ head ] ))

	elif mode is 5:
		# ACCELERATION
		acc_time 	= np.concatenate((acc_time,		[[time]] ))
		accel = [float(data[1]), float(data[2]), float(data[3])]
		acceleration= np.concatenate((acceleration, [ accel ] ))

	elif mode is 6:
		# CALIBRATION STATUS
		cal_time 	= np.concatenate((cal_time, 	[[time]] ))
		cal = [bool(data[1]), bool(data[2]), bool(data[3]), bool(data[3])]
		calibration = np.concatenate((calibration, 	[ cal ] ))

	elif mode is 7:
		# PRESSED BUTTONS
		button_time	= np.concatenate((button_time, 	[[time]] ))
		but = [bool(data[1]), bool(data[2]), bool(data[3]), bool(data[3])]
		buttons 	= np.concatenate((buttons, 		[ but ]))

	else:
		# NOT VALID MODE
		print("\nWARNING, line %i: Not valid mode found (Skipping line):" % line_n)
		print("         ",line)
		line = f.readline().rstrip('\n')
		line_n += 1
		continue

	# Finished operations in the current line and going to the next line
	line = f.readline().rstrip('\n')
	line_n += 1
# Finished file reading and closing file
f.close()
