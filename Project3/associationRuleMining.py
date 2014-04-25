import os.path # for isfile() function
import csv # for csv reader
import sys # to exit
from sets import Set # to check subset
import os # for system
import copy

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
print 'Generating Master List of Items'
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
print 'Running A Priori Algorithm'
listofLs = []
# set L_0
newL = []
tempL = []
tempL.append('')
newL.append((Set(tempL), 0.0))
listofLs.append(newL)

while len(listofLs[-1]) > 0:
	if listofLs[-1][0][0] == Set(['']):
		print 'Generating Frequent Itemsets of Size 1'
	else:
		print 'Generating Frequent Itemsets of length ' + str(len(listofLs[-1][0][0])+1)
	lastL = listofLs[-1]

	# generate C_k
	c = []
	cCount = []
	for itemSet in lastL:
		for item in masterItemset:
			newSet = copy.deepcopy(itemSet[0])
			if item not in newSet:
				# Check if we are generating L_1
				if '' in newSet:
					newSet = Set([])
				newSet.add(item)
				if newSet not in c:
					c.append(newSet)
					cCount.append(0)

	# traverse transactions (rows of csv)
	with open(integrated_dataset, 'rb') as csvfile:
		datasetreader = csv.reader(csvfile, quotechar='|')
		for row in datasetreader:
			for i in xrange(len(c)):
				if c[i].issubset(Set(row)):
					cCount[i] += 1
	
	# Generate L_k
	newL = []
	for i in xrange(len(c)):
		if float(cCount[i])/rows > min_sup:
			newL.append((c[i], float(cCount[i])/rows))

	# Append L_k
	listofLs.append(newL)

# Create master list of frequent itemsets
frequentItemSets = []
for l_k in listofLs:
	for itemSet in l_k:
		if '' not in itemSet[0]:
			frequentItemSets.append(itemSet)

# Write itemsets to output file in order of decreasing support
os.system('rm -f output.txt')
output = open('output.txt', 'w')
output.write('==Frequent itemsets (min_sup={0:.0f}%)\n'.format(min_sup * 100))
for itemSet in sorted(frequentItemSets, key=lambda x: -x[1]):
	output.write(str(list(itemSet[0])).replace('\'', ''))
	output.write(', {0:.4f}%\n'.format(itemSet[1] * 100))

# Create list of tuples for association rules (set1, set2, confidence)
print 'Generating Association Rules'
associationRules = []
# Traverse each possible LHS U RHS (called A)
for setA in frequentItemSets:
	# Traverse each possible LHS (called B)
	for setB in frequentItemSets:
		# Check if setB is a subset of setA and not equal to setA
		if setB[0] != setA[0] and setB[0].issubset(setA[0]):
			# Check if confidence of LHS => RHS is sufficient
			conf = setA[1]/setB[1]
			if conf > min_conf:
				# Generate new association rule and add it to list
				rhs = setA[0].difference(setB[0])
				# We only want association rules with 1 item on RHS
				if len(rhs) == 1:
					assocRule = (setB[0], rhs, conf, setA[1])
					associationRules.append(assocRule)

# Write high confidence association rules to output file
# in order of decreasing confidence
output.write('\n==High-confidence association rules (min_conf={0:.0f}%)\n'.format(min_conf * 100))
for assocRule in sorted(associationRules, key=lambda x: -x[2]):
	output.write(str(list(assocRule[0])).replace('\'', ''))
	output.write(' => ')
	output.write(str(list(assocRule[1])).replace('\'', ''))
	output.write(' (Conf: {0:.1f}%, '.format(assocRule[2] * 100))
	output.write('Supp: {0:.4f}%)\n'.format(assocRule[3] * 100))

