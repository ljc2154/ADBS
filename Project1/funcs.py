import urllib2
import base64
import json
from collections import defaultdict		# to initialize dictionary values to 0
from math import log # for log for idf

# stopWords list obtained from http://norm.al/2009/04/14/list-of-english-stop-words/
stopWords = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'you', 'you\'ll', 'your']

# Queries bing api with given accountKey and query
# returns list of documents (dictionaries)
def queryBing(query, bingUrl, accountKey):
	# Query bing api and receive response
	accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
	headers = {'Authorization': 'Basic ' + accountKeyEnc}
	req = urllib2.Request(bingUrl, headers = headers)
	response = urllib2.urlopen(req)

	# content contains the xml/json response from Bing. 
	content = response.read()
	results = json.loads(content)

	# return the list of the results stored as dictionaries
	return results['d']['results']

# Get relevance feedback on list of docs from user,
# store in 'relevant' key of dictionary doc
# return updated docs
def displayResultsAndStoreFeedback(docs):
	print "Total no of results : " + str(len(docs))
	print "Bing Search Results:"
	print "======================"

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
			docs[i]['relevant'] = 'Y'
		else:
			docs[i]['relevant'] = 'N'
	return docs

# Returns the number of relevant documents
def getRelevantCount(docs):
	relevantCount = 0
	for i in xrange(len(docs)):
		if docs[i]['relevant'] is 'Y':
			relevantCount = relevantCount + 1
	return relevantCount

# Returns true if desired precision of relevant documents reached.
# Returns false otherwise
def precisionReached(docs, precision):
	relevantCount = getRelevantCount(docs)
	nonrelevantCount = len(docs) - relevantCount
	currentPrecision = float(relevantCount) / len(docs)
	print "Precision " + str(currentPrecision)
	if (currentPrecision >= precision):
		print "Desired precision reached, done"
		return True
	else:
		print "Still below the desired precision of " + str(precision)
		return False

# Returns a string with the non-ASCII chars removed from s
def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

# Removes unnecessary characters from a string s
def removeChars(s):
	s = s.replace('.', '')
	s = s.replace(',', '')
	s = s.replace('&', '')
	s = s.replace('\'', '')
	s = s.replace('!', '')
	s = s.replace('\"', '')
	s = s.replace('?', '')
	s = s.replace('@', '')
	s = removeNonAscii(s)
	return s

# Removes any characters we deem unnecessary for our indexing
#		from the title and description of a document doc.
def removeUnnecessaryCharacters(doc):
	# From description
	doc['Description'] = removeChars(doc['Description'])
	# From title
	doc['Title'] = removeChars(doc['Title'])

	# Make lowercase
	doc['Description'] = doc['Description'].lower()
	doc['Title'] = doc['Title'].lower()

	return doc

# Returns a list of terms compiled from the dictionary doc's
# 'Description' and 'Title' keys
def generateTermsList(doc):
	terms = doc['Description'].split()
	terms = terms + doc['Title'].split()
	return terms

# For a given list of documents (dictionaries), this function calculates
# the document frequency of a given term and stores it at index 10
# of the array that the term maps to in the df dictionary.
# Note: this function only depends on the number of documents, so we
# only need take docCt instead of the entire list of dictionaries
def calculateDF(df, docCt):
	for key in df:
		count = 0
		for i in xrange(docCt):
			count = count + df[key][i]
		df[key][10] = count
	return df

# For each term in each doc, this function applies the term's inverse
# document frequency to the term's score
def applyDFtoTermScore(docs, df):
	for i in xrange(len(docs)):
		for key in docs[i]['scores']:
			docs[i]['scores'][key] = docs[i]['scores'][key] * log(10./df[key][10])
	return docs

# Returns two dictionaries that map terms to scores.
# Relevant maps terms to the cumulative term scores from all relevant docs
# Nonrelevant does the same with nonrelevant docs
def generateRelNonRelDicts(docs):
	relevant = defaultdict(int)
	nonrelevant = defaultdict(int)
	for i in xrange(len(docs)):
		if docs[i]['relevant'] == 'Y':
			for key in docs[i]['scores']:
				relevant[key] = relevant[key] + docs[i]['scores'][key]
		else:
			for key in docs[i]['scores']:
				nonrelevant[key] = nonrelevant[key] + docs[i]['scores'][key]
	return relevant, nonrelevant

# Merge term scores from relevant and nonrelevant dictionaries into
# 1 dictionary using the Rocchio algorithm
def generateMasterDict(relevant, nonrelevant, docs, queryTerms):
	# determine number of relevant docs
	relevantCount = getRelevantCount(docs)

	master = defaultdict(int)
	# note that we disregard terms unique to non-relevant documents
	for key in relevant:
		# no coefficients at this time
		master[key] = .75*relevant[key]/relevantCount
		master[key] = master[key] - .15*nonrelevant[key]/(len(docs)-relevantCount)
		notYetATerm = True
		# Make sure key is not already a query term
		for term in queryTerms:
			if key == term.lower():
				notYetATerm = False

	# Increment score of previous query terms by some constant
	for term in queryTerms:
		master[term.lower()] = master[term.lower()] + 1/len(queryTerms)
	return master

# returns the keys with the two highest scores not yet in queryTerms
def getNewQueryTerms(master, queryTerms):
	max1Score = 0
	max2Score = 0
	max1Term = ""
	max2Term = ""

	for key in master:
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

	return max1Term, max2Term