import urllib2
import base64
import json
from collections import defaultdict		# to initialize dictionary values to 0
from math import log # for log for idf
import funcs

# Take input from user.  Note that account key is already hard coded
print "Precision: ",
precision = float(raw_input())
currentPrecision = -1.0
print "Query: ",
query = raw_input()
# queryTerms is a list of the terms from the query
queryTerms = query.split()

# stopWords list obtained from http://norm.al/2009/04/14/list-of-english-stop-words/
stopWords = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'you', 'you\'ll', 'your']

# Loop until we have achieved desired precision
# or we can no longer generate query terms
while (currentPrecision < precision):
	# Generate bing api parameters
	print "Parameters:"

	# By defualt, program uses this account key
	accountKey = 'NCei/F/B/mWf0X51305yv4IqAv8uuJKQ1Fx55SGzMqQ'
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
	docs = funcs.displayResultsAndGetFeedback(docs)


	# We update our users with a summary of their feedback
	print "======================"
	print "FEEDBACK SUMMARY"
	print "Query " + query.replace("+", " ")

	# Check precision
	if funcs.precisionReached(docs, precision):
		break

	# Begin indexing terms
	print "Indexing results",
	# Intialize idf dictionary to 0 for all documents
	idf = defaultdict(list)
	for i in xrange(len(docs)):
		# Initialize all term scores to 0 for document
		docs[i]['scores'] = defaultdict(int)

		# Remove unnecessary characters
		def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)
		# From description
		docs[i]['Description'] = docs[i]['Description'].replace('.', '')
		docs[i]['Description'] = docs[i]['Description'].replace(',', '')
		docs[i]['Description'] = docs[i]['Description'].replace('&', '')
		docs[i]['Description'] = docs[i]['Description'].replace('\'', '')
		docs[i]['Description'] = docs[i]['Description'].replace('!', '')
		docs[i]['Description'] = docs[i]['Description'].replace('\"', '')
		docs[i]['Description'] = docs[i]['Description'].replace('?', '')
		docs[i]['Description'] = docs[i]['Description'].replace('@', '')
		docs[i]['Description'] = removeNonAscii(docs[i]['Description'])
		# From title
		docs[i]['Title'] = docs[i]['Title'].replace('.', '')
		docs[i]['Title'] = docs[i]['Title'].replace(',', '')
		docs[i]['Title'] = docs[i]['Title'].replace('&', '')
		docs[i]['Title'] = docs[i]['Title'].replace('\'', '')
		docs[i]['Title'] = docs[i]['Title'].replace('!', '')
		docs[i]['Title'] = docs[i]['Title'].replace('\"', '')
		docs[i]['Title'] = docs[i]['Title'].replace('?', '')
		docs[i]['Title'] = docs[i]['Title'].replace('@', '')
		docs[i]['Title'] = removeNonAscii(docs[i]['Title'])

		# Make lowercase
		docs[i]['Description'] = docs[i]['Description'].lower()
		docs[i]['Title'] = docs[i]['Title'].lower()

		# terms is the list of words in the description and title
		terms = docs[i]['Description'].split()
		terms = terms + docs[i]['Title'].split()

		# wordCt represents the number of words in a given document
		wordCt = float(len(terms))

		# for each term in list, increment term's score for document
		for term in terms:
			# increment normalized term score
			docs[i]['scores'][term] = docs[i]['scores'][term] + 1/wordCt
			
			# initialize list if necessary
			if (len(idf[term]) is 0):
				idf[term] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

			# mark idf for this document
			idf[term][i] = 1

	# Calculate actual idfs
	print ".",
	for key in idf:
		count = 0
		for i in xrange(len(docs)):
			count = count + idf[key][i]
		idf[key][10] = count

	# Apply idf to document's term scores
	print ".",
	for i in xrange(len(docs)):
		for key in docs[i]['scores']:
			docs[i]['scores'][key] = docs[i]['scores'][key] * log(10./idf[key][10])


	# 2 dictionaries for relevant and nonrelevant
	print ".",
	relevant = defaultdict(int)
	nonrelevant = defaultdict(int)
	for i in xrange(len(docs)):
		if docs[i]['relevant'] == 'Y':
			for key in docs[i]['scores']:
				relevant[key] = relevant[key] + docs[i]['scores'][key]
		else:
			for key in docs[i]['scores']:
				nonrelevant[key] = nonrelevant[key] + docs[i]['scores'][key]


	# merge into master dictionary: subtract relvant from nonrelevant
	print ".",
	master = defaultdict(int)
	max1Score = 0
	max2Score = 0
	max1Term = ""
	max2Term = ""
	# note that we disregard terms unique to non-relevant documents
	for key in relevant:
		# no coefficients at this time
		master[key] = .75*relevant[key]/funcs.getRelevantCount(docs)
		master[key] = master[key] - .15*nonrelevant[key]/(1-funcs.getRelevantCount(docs))
		notYetATerm = True
		# Make sure key is not already a query term
		for term in queryTerms:
			if key == term.lower():
				notYetATerm = False

		# Check if key not a stop word has a high enough score to add to query
		if (notYetATerm):
			if (master[key] > max1Score and key not in stopWords):
				newMax2 = max1Score
				newMax2Term = max1Term
				max1Score = master[key]
				max1Term = key
				max2Score = newMax2
				max2Term = newMax2Term
			elif (master[key] > max2Score and key not in stopWords):
				max2Score = master[key]
				max2Term = key

	# Increment score of previous query terms by some constant
	for term in queryTerms:
		master[term.lower()] = master[term.lower()] + 1/len(queryTerms)

	# Add 2 highest scoring terms to query
	print "."
	print "Augmenting by " + max1Term + " " + max2Term
	if (max1Term != ""):
		queryTerms.append(max1Term)
		if (max2Term != ""):
			queryTerms.append(max2Term)
	else:
		# Halts on same conditions that cause sample program to halt
		print "Below desired precision, but can no longer augment the query"
		break

	# Sort query terms by master score
	def getScore(k): return master[k.lower()]
	queryTerms.sort(key=getScore, reverse=True)
	for term in queryTerms:
		print term + " " + str(master[term.lower()])
	print "bill" + " " + str(master["bill"])
