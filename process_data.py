import csv
#import str

with open('example_output.txt', 'r') as f:
	reader = csv.reader(f)
	for row in reader:
		mode = row[0]
		if mode.startswith('$'):
			print(row)
