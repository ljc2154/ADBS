import csv
from collections import defaultdict		# to initialize dictionary values to 0
import os

os.system("rm -f INTEGRATED-DATASET.csv")

source = open("newCSV.csv","rb")
rdr= csv.reader( source )

blocks = defaultdict(dict)
for row in rdr:
	if row[1] != '0000000000' and row[0] != 'N/A' and row[0] != 'INCORRECT LICENSE':
		blocks[row[1]][row[0]] = 1

output = open('INTEGRATED-DATASET.csv', 'w')
for block in blocks:
	counter = 1
	for permit in blocks[block]:
		if counter == 1:
			output.write(permit)
			counter=counter+1
		else:
			output.write(','+permit)
			counter=counter+1
	# write new line
	output.write('\n')
output.close()