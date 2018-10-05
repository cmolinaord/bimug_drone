import sys
import sensor
import mat4py

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
	mode = int(line[2])
	print("Found a line of type $S%i" % mode)

	if mode is 1:
		# GPSPOS
		data = sensor.parse(line)
		gpspos_time = np.concatenate((gpspos_time, [[ data[-1] ]]))
		utc 		= np.concatenate((utc, [[ data[1] ]]))
#		AV 		= data[2]
#		lat 	= data[3]
#		NS		= data[4]
#		lon 	= data[5]
#		EW		= data[6]
#		knots 	= data[7]
#		track 	= data[8]
#		date 	= data[9]

	elif mode is 2:
		# GPSFIX
		#[gpsfix_time, gpsfix] = sensor.gpsfix(line)
		print("   ... working")
	elif mode is 3:
		# ATMOSPHERIC sensors
		#[atm_time, temp, pressure, bar_altitude] = sensor.atmospheric(line)
		print("   ... working")
	elif mode is 4:
		# HEADING
		#[head_time, heading] = sensor.heading(line)
		print("   ... working")
	elif mode is 5:
		# ACCELERATION
		#[acc_time, acceleration] = sensor.acceleration(line)
		print("   ... working")
	elif mode is 6:
		# CALIBRATION STATUS
		#[cal_time, calibration] = sensor.calibration(line)
		print("   ... working")
	elif mode is 7:
		# PRESSED BUTTONS
		#[button_time, buttons] = sensor.buttons(line)
		print("   ... working")
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
