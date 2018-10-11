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
	1: {
	'name': 'GPS_POS',
	'data': [
		'time',
		'utc',
		'AV',
		'lat',
		'NS',
		'lon',
		'EW',
		'knots',
		'track'
		]
	},
	2: {
	'name': 'GPS_FIX',
	'data': [
		'time',
		'date',
		'numsat',
		'dop',
		'gps_alt'
		]
	},
	3: {
	'name': 'ATMOSPHERIC',
	'data': [
		'time',
		'temp',
		'pressure',
		'baro_alt'
		]
	},
	4: {
	'name': 'HEADING',
	'data': [
		'time',
		'x',
		'y',
		'z'
		]
	},
	5: {
	'name': 'ACCELERATION',
	'data': [
		'time',
		'x',
		'y',
		'z'
		]
	},
	6: {
	'name': 'CALIBRATION',
	'data': [
		'time',
		'sys',
		'gyro',
		'acc',
		'mag'
		]
	},
	7: {
	'name': 'BUTTONS',
	'data': [
		'time',
		'sync',
		'off',
		'load',
		'save'
		]
	}
}
