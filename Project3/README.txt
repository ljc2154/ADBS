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
	Then, for each of the first 10,000 main dictionary keys (city blocks), we wrote its subdictionary keys (permit types) to a line of INTEGRATED-DATASET.csv.
	We made the decision not to incorporate unknown block numbers (all 0s) and unknown permit types (N/A or INCORRECT LICENSE) in our INTEGRATED-DATASET.csv.
	Sometimes, different data was entered to denote the same permit type
	(ie, FOOD SERVICE EST. and FOOD SERVICE ESTAB. or FULL TERM MFV PERMIT and FOOD VENDOR LICENSE)
	We did our best to unify such instances under one permit type.
	Additionally, we chose to disclude permits for PLUMBING and EQUIPMENT WORK from our data set as nearly all blocks with buildings require plumbing work or equipment work (ie, tweaking the boiler).
	This means that any block with a building-related permit will also have a plumbing related permit and most likely an equipment work permit.
	This would then create a large amount of uninteresting association rules with PLUMBING or EQUIPMENT work on the RHS and some combination of building-related permits on the LHS.
	We chose to only take the first 10,000 market baskets because we found them to be a fair representation of all market baskets and the run time was significantly longer of our program when we include all 300,000 market baskets.


	(c) what makes your choice of INTEGRATED-DATASET file interesting (in other words, justify your choice of NYC Open Data data set(s)).
	We think the choice of different permit types granted by block would be interesting and potentially useful to city officials and possibly related businesses.
	How likely is a block that had a FULL DEMOLITION to also have a NEW BUILDING permit?
	If it is highly likely, city officials might be inclined to offer a packaged FULL DEMOLITION/NEW BUILDING permit in an effort to sell/issue more permits and thus bring more money into the city.
	Alternatively, if it is unlikely, it could spark discussions between analysts at city hall as to why knocked down buildings aren't being replaced by new ones.
	Perhaps it would even be helpful for someone getting a food cart permit to know how succesfull food carts are on a block with a food establishment (if association rules are any measure of success).


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
python associationRuleMining.py INTEGRATED-DATASET.csv .042 .55

Before divulging into the association rules we found interesting, I wanted to explain a common permit type, EQUIPMENT.
In NYC, an EQUIPMENT permit is required to use Heating, Ventilation, Air Conditioning, or Refrigeration equipoment while on a construction job.
Thus, the association rule "[FULL DEMOLITION] => [EQUIPMENT] (Conf: 93.8%, Supp: 9.0000%)" makes perfect sense:
When tackling the full demolition of a building in NYC with its hot summers and cold winters, it would make sense for workers on a block to require some form of equipment use permit at some point of the demolition process.

Interesting Association Rule 1: [SIGN] => [EQUIPMENT] (Conf: 74.5%, Supp: 4.3500%)
If city hall officials learned of how likely a block requiring a sign is to require an equipment use permit, it may be profitable for the city to sell a SIGN + EQUIPMENT permit.

Interesting Association Rule 2: [FOOD SERVICE EST., ALTERATION] => [EQUIPMENT] (Conf: 66.8%, Supp: 4.4400%)
What interests me most about this association rule is that there is no ALTERATION => EQUIPMENT or FOOD SERVICE EST. => EQUIPMENT association rules above the minimum confidence level.
Does this imply that restaurants are likely to bring in the necessary equipment to stay open while alterations are happening to its building? 

Interesting Association Rule 3:[FULL DEMOLITION] => [NEW BUILDING] (Conf: 57.0%, Supp: 5.4700%)
There are a few points of interest with this association rule.
First, observe that NEW BUILDING => FULL DEMOLITION is not in example-run.txt and thus did not exceed our minimum confidence.
This is because this association rule has a confidence lower than 40%.
This would mean that the vast majority of new buildings going up aren't going up in place of torn down buildings.
However, association rule 3 leads us to believe that most buildings being torn down ARE being replaced by a new building.
I think the combination of these findings are interesting.
Should we be alarmed by the possible increased amount of land being used for buildings?

g)     Any additional information that you consider significant.
