a)     Your name and your partner's name and Columbia UNI
Louis Croce ljc2154
Kevin Mangan kmm2256

b)     A list of all the files that you are submitting
README.txt: this file
relevance.py: python script containing program source code
Makefile: file containing steps to run program
transcript.txt: text file with test runs of our program from the 3 given
	test queries "snow leopard", "gates", and "columbia"

c)     A clear description of how to run your program (note that your project
must compile/run under Linux in your CS account)
1. Change to project directory (ljc2154-proj1)
2. Run program with command "make"
3. Enter desired precision following "Precision: " prompt.
4. Enter desired query following "Query: " prompt.
5. Program will query bing API and output (up to) 10 results one at a time.
	If the user thinks the result to be relevant, he/she should
		enter a "Y" after the "Relevant (Y/N)?" prompt.
	Else, the user should enter a "N" after the "Relevant (Y/N)?" prompt.
The program will update the query and the user will repeat step 5 until the
desired precision is reached or the query returns no relevant documents.

d)     A clear description of the internal design of your project
We chose to implement the project using the Python programming language.

STRUCTURE OF CODE
Our program runs our python script which consists of an initial information
	gathering stage followed by a while loop.
The while loop consists of four steps:
	1. query bing API and store results in the program
	2. output results one by one to user
		a) record relevance feedback
		b) score document's terms
	3. perform further indexing
		a) update document's term frequency information for term score
		b) apply idf to term score
		c) compile overall relevant/nonrelevant term scores
		d) compute master term scores using rocchio algorithm
	4. update query with top 2 term scores that aren't in query or stop words

DATA STRUCTURES
In this project, we made extensive use of Python's dictionary data type as
	well as Python's list data type.
We store the query terms as well as the stop words in lists
	(queryTerms and stopWords).
When the documents were returned from the bing query, they are converted from
	json to a list of dictionaries.
	We store this list of dictionaries in our own variable docs.
	The dictionaries in the list map to a document's 'Title', 'Description',
		and 'Url' as well as 'relevant' and 'scores' keys added by us.
	The dictionary's 'relevant' key maps to "Y" or "N" depending on the user's
		input for a given document's relevance.
	The dictionary's 'scores' key maps to another dictionary of terms that
		maps to a term's term score in that document.
Similar to a given document's 'scores' mapping, we implement relevant,
	nonrelevant, and master dictionaries mapping a term to a term score.
We also use a dictionary called "idf" that maps terms to a list of bits to
	measure the idf of a given term.
	Each index of the list corresponds to a different document.

e)     A detailed description of your query-modification method
We based our query-modification method on the Rocchio algorithm in
	correspondence with the scoring and term-weighting of the vector-space model
	described chapters 9 and 6 of the Introduction to Information Retrieval
	textbook respectively.
Our query-modification method can be divided into 4 major steps:
1. Document Term Score Compilation
	a) Scores for all terms intially initialized to 0
	b) Update the term score for each term in the title and description of a
		document with Normalized Term Frequency
		i) We do this for each document by incrementing each term's score by 1
			divided by the document's term count (1/wordCt) for each term in the
			document's term list.
	c) Update the term score for each term in title/description of document with
		Inverse Document Frequency
		i) We do this for each document by multiplying each term's score by
			log(docsReturned/idf).
2. Relevant/NonRelevant Term Score Compilation
	a) Scores for all terms intially initialized to 0 for both relevant and
		and nonrelevant dictionaries
	b) Generate relevant document term scores
		i) For every term in every relevant document, we increment the relevant
			dictionary's score for that term by the document's score for that term.
	c) Generate nonrelevant document term scores
		i) For every term in every relevant document, we increment the relevant
			dictionary's score for that term by the document's score for that term.
3. Master Term Score Compilation
	a) Scores for all terms intially initialized to 0 for master dictionary
	b) While keeping track of top 2 non-query term scores, compute master
		term score for terms in the relevant dictionary
		i) Set the term's score to the Rocchio normalized relevant term score by
			setting it to the relevant term score divided by the number of relevant
			documents all multiplied by the Rocchio Beta constant (we used .75).
		ii) Decrement the term's score by the Rocchio normalized nonrelevant term
			score by setting it to itself minus the nonrelevant term score divided
			by the number of nonrelevant documents all multiplied by the Rocchio
			Gamma constant (we used .15).
	c) Weight previous query terms higher
		i) Similar to how Rocchio uses an alpha constant multiplied by the query
			term score, we decided to increment the master scores by 1 divided
			by the number of terms in the previous query.
4. Query Generation
	a) Add terms with 2 highest master term scores to query.
	b) Sort query by master term score.

f)      Your Bing Search Account Key (so we can test your project)
Bing Search Account Key: NCei/F/B/mWf0X51305yv4IqAv8uuJKQ1Fx55SGzMqQ
Note: this key is hard-coded into our script

g)     Any additional information that you consider significant.