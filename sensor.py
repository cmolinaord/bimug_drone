modes = {
	1: "GPS POS",
	2: "GPS FIX",
	3: "ATMOSPHERIC",
	4: "HEADING",
	5: "ACCELERATION",
	6: "CALIBRATION",
	7: "BUTTONS"
}

def gpspos(line):
	# GPSPOS
	# Study if parse it manually or instead, use the pynmea2 library
	print("This would parse GPSPOS data")
	print("And return [gpspos_time, gpspos...]")
	gpspos_time = 0
	gpspos = 0
	return gpspos_time
	return gpspos

def gpsfix(line):
	# GPSFIX
	# Study if parse it manually or instead, use the pynmea2 library
	print("This would parse GPSFIX data")
	print("And return [gpsfix_time, gpsfix...]")
	gpsfix_time = 0
	gpsfix = 0
	return gpsfix_time
	return gpsfix

def atmospheric(line):
	# ATMOSPHERIC
	print("This would parse ATMOSPHERIC data")
	print("And return [atm_time, temp, pressure, bar_altitude]")
	return
	return

def heading(line):
	# HEADING
	print("This would parse HEADING data")
	print("And return [head_time, heading]")
	return
	return

def acceleration(line):
	# ACCELERATION
	print("This would parse ")
	print("And return [acc_time, acceleration]")
	return
	return

def calibration(line):
	# CALIBRATION
	print("This would parse ")
	print("And return [cal_time, calibration]")
	return
	return

def buttons(line):
	# BUTTONS
	print("This would parse ")
	print("And return [button_time, buttons]")
	return
	return
