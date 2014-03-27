import json
import urllib
from collections import defaultdict		# to initialize dictionary values to 0

def setDictVals(ourList, properties, path):
	if (path in properties):
		for x in properties[path]['values']:
			ourList.append(x['text'])
		return ourList

api_key = 'AIzaSyBsXEX0SMoWRYtQDRHWMHehGqmRiGRgQow'
query = 'Bill Gates'
search_url = 'https://www.googleapis.com/freebase/v1/search'
topic_url = 'https://www.googleapis.com/freebase/v1/topic'
params = {
				'query': query,
				'key': api_key
}
url = search_url + '?' + urllib.urlencode(params)
response = json.loads(urllib.urlopen(url).read())
search_results = response['result']

infobox = defaultdict(dict)
for result in search_results:
		url = topic_url + result['mid'] + '?key=' + api_key
		topic_response = json.loads(urllib.urlopen(url).read())
		properties = topic_response['property']
		isActor = False
		isBusinessPerson = False
		for val in properties['/type/object/type']['values']:
			# Check if search result is a Person
			if (val['id'] == '/people/person'):
				person = defaultdict(list)
				person['name'] = setDictVals(person['name'], properties, '/type/object/name')
				person['birthday'] = setDictVals(person['birthday'], properties, '/people/person/date_of_birth')
				person['birthplace'] = setDictVals(person['birthplace'], properties, '/people/person/place_of_birth')
				person['deathdate'] = setDictVals(person['deathdate'], properties, '/people/deceased_person/date_of_death')
				person['deathplace'] = setDictVals(person['deathplace'], properties, '/people/deceased_person/place_of_death')
				person['deathcause'] = setDictVals(person['deathcause'], properties, '/people/deceased_person/cause_of_death')
				if ('/people/person/sibling_s' in properties):
					for sibling in properties['/people/person/sibling_s']['values']:
						if ('/people/sibling_relationship/sibling' in sibling['property']):
							person['siblings'].append(sibling['property']['/people/sibling_relationship/sibling']['values'][0]['text'])
				if ('/people/person/spouse_s' in properties):
					for spouse in properties['/people/person/spouse_s']['values']:
						if ('/people/marriage/spouse' in spouse['property']):
							person['spouses'].append(spouse['property']['/people/marriage/spouse']['values'][0]['text'])
				person['description'] = setDictVals(person['description'], properties, '/common/topic/description')	
				infobox['person'] = person

			# Check if search result is an Author
			elif (val['id'] == '/book/author'):
				author = defaultdict(list)
				author['books'] = setDictVals(author['books'], properties, '/book/author/works_written')
				author['booksonauth'] = setDictVals(author['booksonauth'], properties, '/book/book_subject/works')
				author['influenced'] = setDictVals(author['influenced'], properties, '/influence/influence_node/influenced')
				author['influencedby'] = setDictVals(author['influencedby'], properties, '/influence/influence_node/influenced_by')
				infobox['author'] = author

			# Check if search result is an Actor
			elif (not isActor and (val['id'] == '/film/actor' or val['id'] == 'tv/tv_actor')):
				isActor = True
				actor = defaultdict(str)
				if ('/film/actor/film' in properties):
					# map film to character
					for film in properties['/film/actor/film']['values']:
						actor[film['property']['/film/performance/film']['values'][0]['text']] = film['property']['/film/performance/character']['values'][0]['text']
				infobox['actor'] = actor

			# Check if search result is a BusinessPerson
			elif (not isBusinessPerson and (val['id'] == '/organization/organization_founder' or val['id'] == '/business/board_member')):
				isBusinessPerson = True
				bp = defaultdict(list)
				bp['founded'] = setDictVals(bp['founded'], properties, '/organization/organization_founder/organizations_founded')

				if ('/business/board_member/organization_board_memberships' in properties):
					for org in properties['/business/board_member/organization_board_memberships']['values']:
						a = defaultdict(str)
						if ('/organization/organization_board_membership/organization' in org['property']):
							a['organization'] = org['property']['/organization/organization_board_membership/organization']['values'][0]['text']
						bp['leadership'].append(a)		
				for d in bp['leadership']:
					print d['organization']
				infobox['businessperson'] = bp

		break