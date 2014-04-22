import os.path # for isfile() function
import csv # for csv reader

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
if min_sup < 0 or min_sup > 1
	sys.exit(usageStr)
try:
	min_conf = float(sys.argv[3])
except ValueError:
	sys.exit(usageStr)
if min_conf < 0 or min_conf > 1
	sys.exit(usageStr)


# Compute Frequent Itemsets
