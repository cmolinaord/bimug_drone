# BIMUG_parser
# Aerospace laboratories 2018
# MASE - Master's degree in Space and Aeronautical Engineering
# Carlos Molina

import sys
import os
import csv
import sensor
from datetime import datetime

# Read the arguments given to load the raw data file
if len(sys.argv) == 1:
	print("ERROR: You must give me, at least, the a filename which contains the raw data")
	exit()
elif len(sys.argv) == 2:
	filename = sys.argv[1]
	comment = []
elif len(sys.argv) == 3:
	filename = sys.argv[1]
	comment  = sys.argv[2] # Comentary given to the function (ussually information of flight number)
else:
	print("ERROR: Too much argument given")
	print("       Maximum number of arguments is 2: filename and comment (optional)")
	exit()

# Ask the user to write a comment for the output data
if comment == []:
	print("WARNING: No comment introduced")
	print("         You may want to write a comment to help identifying the output CSV data files")
	print("         Try to write a enough descriptive comment for this flight")
	proceed = input("Do you want to proceed without comment? y/N: ")
	if not proceed == 'y':
		exit()
else:
	# Verify that comment don't start with a number
	if comment[0].isnumeric():
		print("ERROR: Second argument given starts with a number")
		print("       It should start with a non-numeric character")
		print("       This argument will be the first part of the output CSV files name")
		exit()

# Create output directory for the CSV exported data
output_data_root = "output_data"
if not os.path.exists(output_data_root):
	os.mkdir(output_data_root)

# CSV output file initialization
csv_separator = '\t'
# Open CSV files and write first line with the name of the columns
csv_file = []
for i in sensor.modes:
	csv_name = output_data_root + "/" + comment + "_S" + str(i) + "_" + sensor.modes[i]['name'] + ".csv"
	csv_file.append(open(csv_name, 'w'))
	csv_file[i-1].write('#') # Comment the first line as a comment starting with #
	writer = csv.writer(csv_file[i-1])
	writer.writerow(sensor.modes[i]['data'])

# Define function for write each line to CSV
def write_csv(csvfile, mode, vector, line_n):
	writer = csv.writer(csvfile[mode - 1], delimiter = csv_separator)
	writer.writerow(vector)
	line_n[mode - 1] += 1
	return line_n

# Begin parsing data file
print("Parsing file:", filename)
f = open(filename, 'r')
line = f.readline().rstrip('\n')
line_n = 1 # Line number counter
csv_line_n = [0] * len(sensor.modes) # Initialize number of lines for CSV files

# Global time initialization
miliseconds = [0,0] # Raw miliseconds given in the datafile [older, newer]
Ntime = 0 # Number of 10s passed
time = 0 # Real global time in seconds after bootloading

# Start reading raw input data line-by-line
#################################################
while line:
	# Skipping (and printing) header lines
	if not line.startswith('$'):
		print("       ",line)
		line = f.readline().rstrip('\n')
		line_n += 1
		continue

	# WARING if data is not consistent with valid format
	if line[1] is not 'S':
		print("WARNING, line %i: Found a line starting with something different from '$S#' (Skipping line):" % line_n)
		print("         ",line)
		print("         Make sure the file is correct data from a flight using BIMUG system")
		line_n += 1
		line = f.readline().rstrip('\n')
		continue

	# Starting operations in current valid data line
	#################################################
	data = sensor.parse(line)
	mode = int(data[0][2])

	# Global time computation (since system start-up)
	# Take into account that data[-1] gives time in miliseconds and it's reset every 10s

	if data[-1] == '': # If no time data recorded
		print("WARNING, line %i: No timestamp found" % line_n)
		line_n += 1
		line = f.readline().rstrip('\n')
		continue
	miliseconds[1] = int(data[-1]) # Store read data in newer
	if miliseconds[1] < miliseconds[0]:  # If new value is lower than the old one, we might have jumped to next 10s
		Ntime += 1
	# If not, do anything

	time = round(10*Ntime + 1e-3*miliseconds[1], 3) # Refresh time with last value (in seconds with 3 decimals)
	miliseconds[0] = miliseconds[1] # Update [older, newer] for the next line

	# Print progress
	if line_n % 5000 == 0:
		print("Line %i: %3.3fs" % (line_n, time))

	# Analyse line mode read
	if mode is 1:
		# GPSPOS
		# Just parse the data if GPS position is fixed
		# It is decided with $S2 lines, so if the $S1 line which corresponds
		# with the first $S2 fixed line, is written just before the $S2 line,
		# we'll lose this first (valid) $S1 data. Try to fix this bug

		if gpsfix:
			# Preprocces UTC date and coordinates
			gpstime = str.split(data[1],'.')[0] # Use only integer part of time (always is measured at exact seconds)
			utc = datetime.strptime(data[9] + gpstime, '%d%m%y%H%M%S')
			latitude	= sensor.coordinates(data[3])
			longitude 	= sensor.coordinates(data[5])

			write_vector = [
			time,			# gpspos_time
			utc,			# utc
			data[2],		# AV
			latitude,		# lat
			data[4],		# NS
			longitude,		# lon
			data[6],		# EW
			float(data[7]),	# knots
			float(data[8])	# track
			]

			csv_line_n = write_csv(csv_file, mode, write_vector, csv_line_n)

		else:
			print("WARNING: GPS not fixed (time = %3.3f)" % time)

	elif mode is 2:
		# GPSFIX
		gpsfix = bool(int(data[1])) # Changes the value of global gpsfix status (used for S1 and S2 lines)
		if gpsfix:

			write_vector = [
			time, 			# gpsfix_time
			int(data[2]),	# numsat
			float(data[3]),	# dop
			float(data[4])	# gps_alt
			]

			csv_line_n = write_csv(csv_file, mode, write_vector, csv_line_n)

		else:
			print("WARNING: GPS not fixed (time = %3.3f)" % time)

	elif mode is 3:
		# ATMOSPHERIC sensors
		write_vector = [
		time,			# atm_time
		float(data[1]),	# temp
		float(data[2]),	# pressure
		float(data[3]) 	# baro_alt
		]

		csv_line_n = write_csv(csv_file, mode, write_vector, csv_line_n)

	elif mode is 4:
		# HEADING
		write_vector = [
		time,			# time
		float(data[1]),	# x
		float(data[2]),	# y
		float(data[3])	# z
		]

		csv_line_n = write_csv(csv_file, mode, write_vector, csv_line_n)

	elif mode is 5:
		# ACCELERATION
		write_vector = [
		time,			# time
		float(data[1]),	# x
		float(data[2]),	# y
		float(data[3])	# z
		]

		csv_line_n = write_csv(csv_file, mode, write_vector, csv_line_n)

	elif mode is 6:
		# CALIBRATION STATUS
		write_vector = [
		time,			# time
		int(data[1]),	# sys
		int(data[2]),	# gyro
		int(data[3]),	# acc
		int(data[4])	# mag
		]

		csv_line_n = write_csv(csv_file, mode, write_vector, csv_line_n)

	elif mode is 7:
		# PRESSED BUTTONS
		write_vector = [
		time,			# time
		int(data[1]),	# sync
		int(data[2]),	# off
		int(data[3]),	# load
		int(data[4])	# save
		]

		csv_line_n = write_csv(csv_file, mode, write_vector, csv_line_n)

		# Get the index of the (first) data equal to 1 (button pressed)
		index_but = write_vector.index(1)
		print("Button %s pressed at time = %2.3fs" % (sensor.modes[mode]['data'][index_but], time))

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
print("\n...\nFinished parsing %i lines of raw data from %s" % (line_n, filename))
print("\tClosing %s..." % filename)
f.close()

print("\nTotal time recording: %4.3fs = %2.2f" % (time, time / 60))

# Close all CSV files
for i in sensor.modes:
	n = csv_line_n[i-1]
	print("%5i lines written in %s\t\tOne each %3.1fms (%3.1fHz)" % (n, csv_file[i-1].name, time/n*1e3, n/time))
	print("      ... closing CSV file")
	csv_file[i-1].close()
