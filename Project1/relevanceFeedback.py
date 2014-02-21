import urllib2
import base64
import json
from collections import defaultdict		# to initialize dictionary values to 0
from math import log # for log for df
import funcs

# Take input from user.  Note that account key is already hard coded
print "Precision: ",
precision = float(raw_input())
currentPrecision = -1.0
print "Query: ",
query = raw_input()
# queryTerms is a list of the terms from the query
queryTerms = query.split()

# roundAdded maps a query term to the round of relevance feedback it was added
roundAdded = defaultdict(int)
for term in queryTerms:
	roundAdded[term] = 1

# rnd is the current round of relevance feedback we are on
rnd = 1

# Loop until we have achieved desired precision
# or we can no longer generate query terms
while (currentPrecision < precision):
	# Generate bing api parameters
	print "Parameters:"

	# By defualt, program uses this account key
	accountKey = '9e0ZegIk++5Y9nY4guIsePsyEoKHw//0Cz9btJYlTAY'
	print "Client key\t= " + accountKey

	# Generate query and convert characters to html format
	query = queryTerms[0]
	for term in xrange(len(queryTerms)-1):
		query += (" "+queryTerms[term+1])
	print "Query\t\t= " + query
	query = query.replace(" ", "+")

	# Output precision to user
	print "Precision\t= " + str(precision)

	# Create URL
	bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27' + query + '%27&$top=10&$format=json'
	print "URL: " + bingUrl

	# Query bing api
	# docs is a list of results stored as dictionaries
	docs = funcs.queryBing(query, bingUrl, accountKey)

	# Display query results and obtain relevance feedback from user
	docs = funcs.displayResultsAndStoreFeedback(docs)


	# We update our users with a summary of their feedback
	print "======================"
	print "FEEDBACK SUMMARY"
	print "Query " + query.replace("+", " ")

	# Check precision
	if funcs.precisionReached(docs, precision):
		break

	# Begin indexing terms
	print "Indexing results",
	# Intialize df dictionary to 0 for all documents
	df = defaultdict(list)
	for i in xrange(len(docs)):
		# Initialize all term scores to 0 for document
		docs[i]['scores'] = defaultdict(int)

		# Remove unnecessary characters from doc's description and title
		docs[i] = funcs.removeUnnecessaryCharacters(docs[i])

		# terms is the list of words in the description and title of a document
		terms = funcs.generateTermsList(docs[i])

		# wordCt represents the number of words in a given document
		wordCt = float(len(terms))

		# Update a term's score in a document with the normalized term frequency
		# 	Also update the term's document frequency if necessary
		for term in terms:
			# increment normalized term score
			docs[i]['scores'][term] = docs[i]['scores'][term] + 1/wordCt
			
			# initialize list if necessary
			if (len(df[term]) is 0):
				df[term] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

			# mark df for this document
			df[term][i] = 1

	# Calculate actual dfs
	print ".",
	df = funcs.calculateDF(df, len(docs))

	# Apply df to document's term scores
	print ".",
	docs = funcs.applyDFtoTermScore(docs, df)

	# Generate 2 dictionaries for relevant and nonrelevant term score mappings
	print ".",
	relevant, nonrelevant = funcs.generateRelNonRelDicts(docs)

	# merge into master dictionary: apply Rocchio Algorithm
	print ".",
	master = funcs.generateMasterDict(relevant, nonrelevant, docs, queryTerms,
							roundAdded)

	# determine the two highest scoring terms not yet in query
	print ".",
	max1Term, max2Term = funcs.getNewQueryTerms(master, queryTerms)

	# Add 2 highest scoring terms to query
	print "."
	print "Augmenting by " + max1Term + " " + max2Term
	if (max1Term != ""):
		queryTerms.append(max1Term)
		roundAdded[max1Term] = rnd + 1
		if (max2Term != ""):
			queryTerms.append(max2Term)
			roundAdded[max2Term] = rnd + 1
	else:
		# Halts on same conditions that cause sample program to halt
		print "Below desired precision, but can no longer augment the query"
		break

	# Sort query terms by master score
	def getScore(k): return master[k.lower()]
	queryTerms.sort(key=getScore, reverse=True)

	# Increment feedback round
	rnd = rnd + 1
