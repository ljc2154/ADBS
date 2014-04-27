a)	Your name and your partner's name;
Louis Croce ljc2154
Kevin Mangan kmm2256

b)	A list of all the files that you are submitting;
README.txt: this file
INTEGRATED-DATASET.csv: our single csv file containing our INTEGRATED-DATASET file.  Each row corresponds to a "market basket" of permit types granted for a given block in New York City over a duration of time.
Makefile: file containing steps to run our program
example-run.txt: a file with an interesting sample run of our program
associationRuleMining.py: python script containing program source code

c)	A detailed description explaining:
	(a) which NYC Open Data data set(s) you used to generate the INTEGRATED-DATASET file;
	In this assignment, we used the Multi Agency Permits data set from NYC Open Data:
	https://data.cityofnewyork.us/City-Government/Multi-Agency-Permits/xfyi-uyt5

	(b) what (high-level) procedure you used to map the original NYC Open Data data set(s) into your INTEGRATED-DATASET file;
	First we downloaded the data set in .csv format.
	We then created a smaller .csv consisting of the only columns we cared about from the data set (Permit_Type_Description and Borough_Block_Lot).
	We then used a python script that stored the information from the data set valuable to us in a dictionary.
	The dictionary mapped block numbers to sub-dictionaries that mapped different permit types to bits (1 if the block contained that permit type).
	Then, for each main dictionary key (city block), we wrote its subdictionary keys (permit types) to a line of INTEGRATED-DATASET.csv.
	We made the decision not to incorporate unknown block numbers (all 0s) and unknown permit types (N/A or INCORRECT LICENSE) in our INTEGRATED-DATASET.csv.
	Sometimes, different data was entered to denote the same permit type
	(ie, FOOD SERVICE EST. and FOOD SERVICE ESTAB. or FULL TERM MFV PERMIT and FOOD VENDOR LICENSE)
	We did our best to unify such instances under one permit type.


	(c) what makes your choice of INTEGRATED-DATASET file interesting (in other words, justify your choice of NYC Open Data data set(s)).
	We think the choice of different permit types granted by block would be interesting and potentially useful to city officials and related businesses.
	How likely is a block that required equipment work to need plumbing done?
	How likely are cigarrette shops to be located on blocks with barber shops?
	Perhaps it would even be helpful for someone opening up a laundry business to see how correlated they are with beauty parlors on the same block.


d)     A clear description of how to run your program (note that your project must compile/run under Linux in your CS account);
1. Change to project directory if not already there (ljc2154-proj3)
2. Run the python script in one of the 2 following ways:
	a) python associationRuleMining.py <INTEGRATED-DATASET.csv> <Minimum Support> <Minimum Confidence>
	b) make ARGS=" <INTEGRATED-DATASET.csv> <Minimum Support> <Minimum Confidence>"
	note: order of args important. minimum support and confidence must
		be between 0 and 1.


e)      A clear description of the internal design of your project; in particular, if you decided to implement variation(s) of the original a-priori algorithm (see above), you must explain precisely what variation(s) you have implemented and why.

We chose to implement the project using the Python programming language.
.

DATA STRUCTURES
In this project, we made extensive use of Python's list, Set, and tuple data types.
We maintain all possible items in a master list of strings.
We represented various item sets with the Set data type.
We then combined an itemset with its support as determined in the Apriori algorithm in a (Set, float) tuple.
In the Apriori algorithm, we maintain c, the list of candidate itemsets at a certain length, as a list of Sets.
We then maintain the related cCount array such that the count at index i of the cCount array corresponds to the count of the itemset at index i of c.
Also in the Apriori algorithm, we maintain each L_k, the list of frequent item sets of size k, as a list of (Set, float) tuples of storing each itemset and its support.
We then maintain all the L_ks in a listofLs list of lists such that listofLs[k] stores L_k.
We then go on to store association rules in a list of (Set, Set, float float) tuples corresponding to (LHS, RHS, confidence, support).


STRUCTURE OF CODE
Our script can be divided into 6 steps
1. Check that script was run with correct parameters
2. Generate master list of items
3. Run Apriori to generate master list of frequent itemsets with their supports.
4. Write frequent itemsets and their supports in decreasing order to output.txt
5. Use supports of frequent itemsets to generate association rules of sufficient confidence.
6. Write association rules and their confidences and supports to output.txt

VARIATIONS ON APRIORI
We used Apriori just as described in 2.1 of Fast Algorithms for Mining Association Rules without any variations.

f)      The command line specification of an interesting sample run (i.e., a min_sup, min_conf combination that produces interesting results). Briefly explain why the results are interesting.


g)     Any additional information that you consider significant.
Our INTEGRATED-DATASET.csv file consists of nearly 300,000 lines.
You may wish to only run it with a subset of the lines.
We've found almost identical results by creating a SMALL-INTEGRATED-DATASET.csv consisting of anywhere form 1,000 to 100,000 lines.
