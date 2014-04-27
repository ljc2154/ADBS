import csv
from collections import defaultdict		# to initialize dictionary values to 0
import os

os.system("rm -f newCSV.csv")

with open('Multi_Agency_Permits.csv',"rb") as source:
	rdr= csv.reader( source )
	with open("newCSV.csv","wb") as result:
		wtr= csv.writer( result )
		for r in rdr:
			wtr.writerow( (r[4], r[16]) )

os.system("rm -f INTEGRATED-DATASET.csv")

source = open("newCSV.csv","rb")
rdr= csv.reader( source )

blocks = defaultdict(dict)
for row in rdr:
	if row[1] != '0000000000' and row[1] != '' and row[0] != 'N/A' and row[0] != 'INCORRECT LICENSE' and row[0] != '':
		if row[0] == 'FOOD SERVICE EST.' or row[0] == 'FOOD SERVICE ESTAB' or row[0] == 'FOOD SERVICE ESTABL.' or row[0] == 'FOOD SERVICE ESTAB.':
			blocks[row[1]]['FOOD SERVICE EST.'] = 1
		elif row[0] == 'FULL TERM MFV PERMIT' or row[0] == 'FOOD VENDOR LICENSE':
			blocks[row[1]]['FOOD VENDOR LICENSE'] = 1
		else:
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