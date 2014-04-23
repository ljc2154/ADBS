import os.path # for isfile() function
import csv # for csv reader
import sys # to exit
from sets import Set # to check subset
import os # for system

# Make sure script utilized correctly with command line arguments
usageStr = "Usage error: Format must be python associationRuleMining.py <INTEGRATED-DATASET.csv> <Minimum Support> <Minimum Confidence>\n"
usageStr += " or make ARGS=\" <INTEGRATED-DATASET.csv> <Minimum Support> <Minimum Confidence>\"\n"
usageStr += " or python associationRuleMining.py <INTEGRATED-DATASET.csv> <Minimum Support> <Minimum Confidence>\n"
usageStr += " or make ARGS=\" <INTEGRATED-DATASET.csv> <Minimum Support> <Minimum Confidence>\""
if len(sys.argv) != 4:
	sys.exit(usageStr)

# Check that INTEGRATED-DATASET exists
integrated_dataset = sys.argv[1]
if os.path.isfile(integrated_dataset) == False:
	sys.exit(usageStr)

# Check minimum support and minimum confidence are valid
try:
	min_sup = float(sys.argv[2])
except ValueError:
	sys.exit(usageStr)
if min_sup < 0 or min_sup > 1:
	sys.exit(usageStr)
try:
	min_conf = float(sys.argv[3])
except ValueError:
	sys.exit(usageStr)
if min_conf < 0 or min_conf > 1:
	sys.exit(usageStr)


# Compute Frequent Itemsets

# Generate master list of all possible items
masterItemset = []
rows = 0
with open(integrated_dataset, 'rb') as csvfile:
		datasetreader = csv.reader(csvfile, quotechar='|')
		for row in datasetreader:
			rows += 1
			for i in row:
				if i not in masterItemset:
					masterItemset.append(i)

# A Priori Algorithm
listofLs = []
# set L_1
newL = []
tempL = []
tempL.append('')
newL.append((tempL, 0.0))
# for item in masterItemset:
# 	tempList = []
# 	tempList.append(item)
# 	newL.append(tempList)
listofLs.append(newL)

while len(listofLs[-1]) > 0:
	lastL = listofLs[-1]

	# generate C_k
	c = []
	cCount = []
	for itemSet in lastL:
		for item in masterItemset:
			newSet = itemSet[0][:]
			if item not in newSet:
				# Check if we are generating L_1
				if '' in newSet:
					newSet = []
				newSet.append(item)
				c.append(newSet)
				cCount.append(0)

	# traverse transactions (rows of csv)
	with open(integrated_dataset, 'rb') as csvfile:
		datasetreader = csv.reader(csvfile, quotechar='|')
		for row in datasetreader:
			for i in xrange(len(c)):
				if Set(c[i]).issubset(Set(row)):
					cCount[i] += 1
	
	# Generate L_k
	newL = []
	for i in xrange(len(c)):
		if float(cCount[i])/rows > min_sup:
			newL.append((c[i], float(cCount[i])/rows))

	# Append L_k
	listofLs.append(newL)

# Create master list of itemsets
masterL = []
for l_k in listofLs:
	for itemSet in l_k:
		if '' not in itemSet[0]:
			masterL.append(itemSet)

# Sort masterL by support
os.system('rm -f output.txt')
output = open('output.txt', 'w')
output.write('Frequent Item Sets\n')
for itemSet in sorted(masterL, key=lambda x: -x[1]):
	output.write(str(itemSet[0]))
	output.write(', {0:.4f}%\n'.format(itemSet[1] * 100))
