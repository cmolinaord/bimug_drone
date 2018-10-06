# Import regular expression python library
import re
from checksum import checksum

def check_data(line):
	# recorded checksum
	#cs = re.split('[*]|_',linea)[-2]
	# String to check
	#str = line.lstrip("$").split("*")[0]

	# Compare with string checksum
	#if cs == checksum(str):
	#	return True
	#else:
	#	return False
	return True

# Method to read any kind of line, separated with comma, asterisc and underscore
def parse(line):
	if check_data(line):
		data = re.split(',|[*]|_',line)
		return data

def coordinates(str):
	num = float(str)
	degree = int(num*0.01)
	coord = (num - degree * 100) / 60 + degree
	return coord

modes = {
	1: "GPS POS",
	2: "GPS FIX",
	3: "ATMOSPHERIC",
	4: "HEADING",
	5: "ACCELERATION",
	6: "CALIBRATION",
	7: "BUTTONS"
}
