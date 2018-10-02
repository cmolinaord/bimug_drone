def checksum(str):
	c = int('',16)
	for s in str:
		c = c ^ s
	return c
