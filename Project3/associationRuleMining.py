import os.path # for isfile() function
import csv # for csv reader
import sys # to exit
from sets import Set # to check subset

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
csvfile = open(integrated_dataset, 'rb')
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
listofLs.append(newL)
for item in masterItemset:
	tempList = []
	tempList.append(item)
	listofLs[0].append(tempList)

while len(listofLs[-1]) > 0:
	lastL = listofLs[-1]
	# generate C_k
	c = []
	cCount = []
	for itemSet in lastL:
		for item in masterItemset:
			newSet = itemSet
			if item not in newSet:
				newSet.append(item)
				c.append(newSet)
				cCount.append(0)

	# traverse transactions (rows of csv)
	for row in datasetreader:
		for i in xrange(len(c)):
			if Set(c[i]).issubset(Set(row)):
				cCount[i] += 1
	
	# Generate L_k
	newL = []
	for i in xrange(len(c)):
		if cCount[i]/rows > min_sup:
			newL.append(c[i])

	# Append L_k
	listofLs.append(newL)

# Create master list of itemsets
masterL = []
for l_k in listofLs:
	for itemSet in l_k:
		print itemSet
		masterL.append(itemSet)
