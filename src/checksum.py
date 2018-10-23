def checksum(str):
	c = 0
	for s in str:
		c = c ^ ord(s)
	return hex(c)
