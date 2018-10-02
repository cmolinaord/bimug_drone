#include <stdio.h>

int checksum(const char *s) {
	int c = 0;
	printf("c = %i = 0x%02x\n", c, c);
	while(*s)
		c ^= *s++;
		printf("s = %c = %i = 0x%02X\n", c, c, c);
	return c;
}

int main(int argc, char *argv[]) {
	char *str;
	if (argc >= 2)
		str = argv[1];
	else
		str = "GPRMC,092751.000,A,5321.6802,N,00630.3371,W,0.06,31.66,280511,,,A";

	printf("String: %s\nChecksum: 0x%04X\n", str, checksum(str));
	return 0;
}
