import urllib2
import base64
import json
from collections import defaultdict		# to initialize dictionary values to 0
from math import log # for log for idf
import sys						# for argv

# Parse Input from command line
# accountkey = sys.argv[1]
# we will have to increment these arg indexes
precision = float(sys.argv[1])
currentPrecision = -1.0
query = sys.argv[2]
queryTerms = query.split()

# stopWords list obtained from http://norm.al/2009/04/14/list-of-english-stop-words/
stopWords = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'you', 'your']

# Loop until we have achieved desired precision
# or we can no longer generate query terms
while (currentPrecision < precision):
	# Generate bing api parameters
	print "Parameters:"

	# account key will eventually be taken from the command line
	accountKey = 'NCei/F/B/mWf0X51305yv4IqAv8uuJKQ1Fx55SGzMqQ'
	print "Client key\t= " + accountKey

	# Convert query to HTTP string
	query = queryTerms[0]
	for term in xrange(len(queryTerms)-1):
		query += ("+"+queryTerms[term+1])
	print "Query\t\t= " + query.replace("+", " ")

	# Output precision to user
	print "Precision\t= " + str(precision)

	# Create URL
	bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27' + query + '%27&$top=10&$format=json'
	print "URL: " + bingUrl

	# Query bing api and receive response
	accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
	headers = {'Authorization': 'Basic ' + accountKeyEnc}
	req = urllib2.Request(bingUrl, headers = headers)
	response = urllib2.urlopen(req)

	# content contains the xml/json response from Bing. 
	content = response.read()
	results = json.loads(content)

	# docs is a list of results stored as dictionaries
	docs = results['d']['results']
	print "Total no of results : " + str(len(docs))
	print "Bing Search Results:"
	print "======================"

	# Intialize idf dictionary to 0 for all documents
	idf = defaultdict(list)

	# Keep track of the number of relevant and irrelevant docs
	relevantCount = 0
	irrelevantCount = 0

	# traverse results
	for i in xrange(len(docs)):
		# Print the search result for the user
		print "Result", i+1
		print "["
		print " Title: " + docs[i]['Title']
		print " Description: " + docs[i]['Description']
		print " Url: " + docs[i]['Url']
		print "]\n"
		# Obtain relevance feedback and update rel/irrel info
		answer = "X"
		while answer is not "Y" and answer is not "N":
			print "Relevant (Y/N)?"
			answer = raw_input()
		if answer is "Y":
			relevantCount = relevantCount + 1
			docs[i]['relevant'] = 'Y'
		else:
			irrelevantCount = irrelevantCount + 1
			docs[i]['relevant'] = 'N'

		# Initialize all term scores to 0 for document
		docs[i]['scores'] = defaultdict(int)

		# Remove unnecessary characters
		docs[i]['Description'] = docs[i]['Description'].replace('.', '')
		docs[i]['Description'] = docs[i]['Description'].replace(',', '')
		docs[i]['Description'] = docs[i]['Description'].replace('&', '')
		# Make description all lowercase
		docs[i]['Description'] = docs[i]['Description'].lower()
		# terms is the list of words in a document
		terms = docs[i]['Description'].split()
		# wordCt represents the number of words in a given document
		wordCt = float(len(terms))

		#for each term slurped, increment term's score for document
		for term in terms:
			# increment normalized term score
			docs[i]['scores'][term] = (docs[i]['scores'][term] + 1)/wordCt
			
			# elongate list if necessary
			if (len(idf[term]) is 0):
				idf[term] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

			# mark idf for this document
			idf[term][i] = 1

	# We update our users with a summary of their feedback
	print "======================"
	print "FEEDBACK SUMMARY"
	print "Query " + query.replace("+", " ")

	# Check precision
	currentPrecision = float(relevantCount) / len(docs)
	print "Precision " + str(currentPrecision)
	if (currentPrecision >= precision):
		print "Desired precision reached, done"
		break
	else:
		print "Still below the desired precision of " + str(precision)

	# Apply idfs to term scores
	print "Indexing results",
	# Calculate actual idfs
	for key in idf:
		count = 0
		for i in xrange(10):
			count = count + idf[key][i]
		idf[key][10] = count

	# Apply idf to document's term scores
	print ".",
	for i in xrange(10):
		for key in docs[i]['scores']:
			docs[i]['scores'][key] = docs[i]['scores'][key] * log(10./idf[key][10])


	# 2 dictionaries for relevant and nonrelevant
	print ".",
	relevant = defaultdict(int)
	irrelevant = defaultdict(int)
	for i in xrange(10):
		if docs[i]['relevant'] == 'Y':
			for key in docs[i]['scores']:
				relevant[key] = relevant[key] + docs[i]['scores'][key]
		else:
			for key in docs[i]['scores']:
				irrelevant[key] = irrelevant[key] + docs[i]['scores'][key]


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
		master[key] = relevant[key]/relevantCount - irrelevant[key]/irrelevantCount
		notYetATerm = True
		# Make sure key is not already a query term
		for term in queryTerms:
			if key == term.lower():
				master[key] = 1.
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

	# Sort query terms by master score
	def getScore(k): return master[k.lower()]
	queryTerms.sort(key=getScore, reverse=True)
