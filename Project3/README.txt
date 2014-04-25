a)	Your name and your partner's name;
Louis Croce ljc2154
Kevin Mangan kmm2256

b)	A list of all the files that you are submitting;
README.txt: this file
INTEGRATED-DATASET.csv: our single file consisting of market basket type rows of permit types requested for a given block

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
	(ie, FOOD SERVICE EST. and FOOD SERVICE ESTAB. or EQUIPMENT and EQUIPMENT WORK)
	We did our best to unify such instances under one permit type.


	(c) what makes your choice of INTEGRATED-DATASET file interesting (in other words, justify your choice of NYC Open Data data set(s)).
	We think the choice of different permit types granted by block would be interesting and potentially useful to city officials and related businesses.
	How likely is a block that required equipment work to need plumbing done?
	How likely are cigarrette shops to be located on blocks with barber shops?
	Perhaps it would even be helpful for someone opening up a laundry business to see how correlated they are with beauty parlors on the same block.


c)     A clear description of how to run your program (note that your project
must compile/run under Linux in your CS account)
1. Widen your shell window to fit 130 characters across
2. Change to project directory if not already there (ljc2154-proj2)
3. Run the python script in one of the 4 following ways:
	a) python knowledgegraph.py -key <Freebase API key> -q <query> -t <infobox|question>
	b) make ARGS="-key <Freebase API key> -q <query> -t <infobox|question>"
	c) python knowledgegraph.py -key <Freebase API key> -f <file of queries> -t <infobox|question>
	d) make ARGS=" -key <Freebase API key> -f <file of queries> -t <infobox|question>"
	note: order of args in each example doesn't matter as long as preceded by correct flag


d)      A clear description of the internal design of your project, including listing the mapping that you used to map from Freebase properties to the entity properties of interest that you return

We chose to implement the project using the Python programming language.

FUNCTIONS
To avoid code duplication, we wrote functions that appear at the beginning
of the script.

DATA STRUCTURES
In this project, we made extensive use of Python's dictionary data type as
	well as Python's list data type.
For Part 1, our main data structure is the infobox dictionary.
	The infobox dictionary maps the type of entity for our project (person, author, etc. )
		to usually sub-dictionary but sometimes a list of properties of interest
		that correspond to that type of entity.
	If the type key maps to a sub-dictionary, the property of interest usually maps
		to a list of corresponding properties for the entity.  The corresponding properties
		can be strings, or sometimes dictionaries or lists of sub-properties of
		interest (coaches, players, etc.)
	If the type key maps to a list (actor), the list contains dictionaries corresponding
		to films.  The keys of the dictionary map to lists of properties corresponding to
		films (keys are 'character' and 'film')
For Part 2, our main data structure is the creators dictionary.
	The creators dictionary maps a creators name to a list of the creator's works.
	The creator's works are stored as tuples in the list.
	The tuple consist of the as_a type (Author/Business Person) and a list of the names
	of the work (there will most likely be just 1).

STRUCTURE OF CODE
First we determine that the user ran the script with the correct number/type
	of arguments.
Second we determine if the user is interested in an infobox or answering a question
	from the -t flag.
If the user is interested in an infobox, then for each query given, we fill out
	the infobox dictionary to the best of our ability using the mappings in MAPPING
	and output an infobox.
If the user is interested in answering a question, then for each question given
	we fill out the creators dictionary to the best of our ability using the mappings
	in MAPPING and output the results.

MAPPING - PART1
Entity Type-Property-Freebase Entity Type-Freebase Property
	Comments
Person-Name-/people/person-/people/object/name
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	the value.  Although it is improbable there would be more than one, we are
	not penalized for inefficiency and it is possible for there to be more than
	one value in Freebase so we store and print them all.
Person-Birthday-/people/person-/people/person/date_of_birth
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	the value.  Although it is improbable there would be more than one, we are
	not penalized for inefficiency and it is possible for there to be more than
	one value in Freebase so we store and print them all.
Person-Place of Birth-/people/person-/people/person/place
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	the value.  Although it is improbable there would be more than one, we are
	not penalized for inefficiency and it is possible for there to be more than
	one value in Freebase so we store and print them all.
Person-Deathdate-/people/person-/people/deceased_person/date_of_death
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	the value.  Although it is improbable there would be more than one, we are
	not penalized for inefficiency and it is possible for there to be more than
	one value in Freebase so we store and print them all.
Person-Deathplace-/people/person-/people/deceased_person/place_of_death
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	the value.  Although it is improbable there would be more than one, we are
	not penalized for inefficiency and it is possible for there to be more than
	one value in Freebase so we store and print them all.
Person-Deathcause-/people/person-/people/deceased_person/cause_of_death
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	the value.
Person-Siblings-/people/person-/people/person/sibling_s (/people/sibling_relationship/sibling)
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	first val in 'values' field in the '/people/sibling_relationship/sibling' tag (if it existed) in the 'property' tag of value's property tag.
Person-Spouses-/people/person-/people/person/spouse_s (/people/marriage/spouse)
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	first val in 'values' field in the '/people/marriage/spouse' tag (if it existed) in the 'property' tag of value's property tag.
Person-Description-/people/person-/common/topic/description
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'value' tag associated with
	the value.
Author-Books-/book/author-/book/author/works_written
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	the value.
Author-Books About the Author-/book/author-/book/book_subject/works
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	the value.
Author-Influenced-/book/author-/influence/influence_node/influenced
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	the value.
Author-Influenced by-/book/author-/influence/influence_node/influenced_by
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	the value.
Actor-Films-/film/actor or /tv/actor-/film/actor/film
	If this freebase property was accessible, we proceeded as follows:
	For each value's property field in the 'values' field, for each val in the 'values'
	field of '/film/performance/character' and '/film/performance/film' we stored each
	name from the 'text' tag of the val for the possible characters/film names
	of the given film.  Although it is improbable there would be more than one
	film name, we are not penalized for inefficiency and it is possible for there
	to be more than one value in Freebase so we store and print them all.
BusinessPerson-Founded-/organization/organization_founder or /business/board_member-/organization/organization_founder/organizations_founded
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	the value.
BusinessPerson-BoardMember-/organization/organization_founder or /business/board_member-/business/board_member/organization_board_memberships
	If this freebase property was accessible, we proceeded as follows:
	For each value's property field in the 'values' field, for each val in the 'values'
	field of '/organization/organization_board_membership/organization', '/organization/organization_board_membership/title', '/organization/organization_board_membership/role', '/organization/organization_board_membership/from', and '/organization/organization_board_membership/to' we stored each
	name from the 'text' tag of the val for the possible subproperties
	of the given organization.  Although it is improbable there would be more than one
	organization name, from, etc., we are not penalized for inefficiency and it is possible for there
	to be more than one value in Freebase so we store and print them all.
BusinessPerson-Leadership-/organization/organization_founder or /business/board_member-/business/board_member/leadership_of
	If this freebase property was accessible, we proceeded as follows:
	For each value's property field in the 'values' field, for each val in the 'values'
	field of '/organization/leadership/organization', '/organization/leadership/title', '/organization/leadership/role', '/organization/leadership/from', and '/organization/leadership/to' we stored each
	name from the 'text' tag of the val for the possible subproperties
	of the given organization.  Although it is improbable there would be more than one
	organization name, from, etc., we are not penalized for inefficiency and it is possible for there
	to be more than one value in Freebase so we store and print them all.
League-Name-/sports/sports_league-/type/object/name
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	the value.  Although it is improbable there would be more than one, we are
	not penalized for inefficiency and it is possible for there to be more than
	one value in Freebase so we store and print them all.
League-Championship-/sports/sports_league-/sports/sports_league/championship
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	the value.  Although it is improbable there would be more than one, we are
	not penalized for inefficiency and it is possible for there to be more than
	one value in Freebase so we store and print them all.
League-Sport-/sports/sports_league-/sports/sports_league/sport
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	the value.  Although it is improbable there would be more than one, we are
	not penalized for inefficiency and it is possible for there to be more than
	one value in Freebase so we store and print them all.
League-Slogan-/sports/sports_league-/organization/organization/slogan
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	the value.  Although it is improbable there would be more than one, we are
	not penalized for inefficiency and it is possible for there to be more than
	one value in Freebase so we store and print them all.
League-OfficialWebsite-/sports/sports_league-/common/topic/official_website
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	the value.  Although it is improbable there would be more than one, we are
	not penalized for inefficiency and it is possible for there to be more than
	one value in Freebase so we store and print them all.
League-Description-/sports/sports_league-/common/topic/description
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'value' tag associated with
	the value.
League-Teams-/sports/sports_league-/sports/sports_league/teams
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	first val in 'values' field in the '/sports/sports_league_participation/team' tag (if it existed) in the 'property' tag of value's property tag.
Team-Name-/sports/sports_team or /sports/professional_sports_team-/type/object/name
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	the value.  Although it is improbable there would be more than one, we are
	not penalized for inefficiency and it is possible for there to be more than
	one value in Freebase so we store and print them all.
Team-Description-/sports/sports_team or /sports/professional_sports_team-/common/topic/description
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'value' tag associated with
	the value.
Team-Sport-/sports/sports_team or /sports/professional_sports_team-/sports/sports_team/sport
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	the value.  Although it is improbable there would be more than one, we are
	not penalized for inefficiency and it is possible for there to be more than
	one value in Freebase so we store and print them all.
Team-Arena-/sports/sports_team or /sports/professional_sports_team-/sports/sports_team/arena_stadium
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	the value.
Team-Championships-/sports/sports_team or /sports/professional_sports_team-/sports/sports_team/championships
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	the value.
Team-Founded-/sports/sports_team or /sports/professional_sports_team-/sports/sports_team/founded
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	the value.  Although it is improbable there would be more than one, we are
	not penalized for inefficiency and it is possible for there to be more than
	one value in Freebase so we store and print them all.
Team-Locations-/sports/sports_team or /sports/professional_sports_team-/sports/sports_team/location
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	the value.
Team-Leagues-/sports/sports_team or /sports/professional_sports_team-/sports/sports_team/league
	If this freebase property was accessible, we proceeded as follows:
	For each value in the 'values' field, we stored the 'text' tag associated with
	first val in 'values' field in the '/sports/sports_league_participation/league' tag (if it existed) in the 'property' tag of value's property tag.
Team-Coaches-/sports/sports_team or /sports/professional_sports_team-/sports/sports_team/coaches
	If this freebase property was accessible, we proceeded as follows:
	For each value's property field in the 'values' field, for each val in the 'values'
	field of '/sports/sports_team_coach_tenure/coach', '/sports/sports_team_coach_tenure/number', '/sports/sports_team_coach_tenure/from', '/sports/sports_team_coach_tenure/to', and '/sports/sports_team_coach_tenure/position' we stored each
	name from the 'text' tag of the val for the possible subproperties
	of the given organization.  Although it is improbable there would be more than one
	coach name, from, etc., we are not penalized for inefficiency and it is possible for there
	to be more than one value in Freebase so we store and print them all.
Team-Players-/sports/sports_team or /sports/professional_sports_team-/sports/sports_team/roster
	If this freebase property was accessible, we proceeded as follows:
	For each value's property field in the 'values' field, for each val in the 'values'
	field of '/sports/sports_team_roster/coach', '/sports/sports_team_roster/number', '/sports/sports_team_roster/from', '/sports/sports_team_roster/to', and '/sports/sports_team_roster/position' we stored each
	name from the 'text' tag of the val for the possible subproperties
	of the given organization.  Although it is improbable there would be more than one
	player name, from, etc., we are not penalized for inefficiency and it is possible for there
	to be more than one value in Freebase so we store and print them all.

MAPPING - PART 2
Creator Entity Type-Creation-Freebase Creator Type-Freebase Creation Property
	Query
	Comments
Author-Book-/book/author-/book/author/works_written
	[{"/book/author/works_written": [{"a:name": null,"name~=": "' + query + '"}],"id": null,"name": null,"type": "/book/author"}]
	Stored all possible names ('a:name' tag) for each creation even though most
	likely will have one name.
Founder-Organization-/organization/organization_founder-/organization/organization_founder/organizations_founded
	[{"/organization/organization_founder/organizations_founded": [{"a:name": null,"name~=": "' + query + '"}],"id": null,"name": null,"type": "/organization/organization_founder"}]
	Stored all possible names ('a:name' tag) for each creation even though most
	likely will have one name.

f)      Your Freebase API Key (so we can test your project) as well as the requests per second per user that you have set when you configured your Google project (see Freebase Basics section)
Freebase API Key: AIzaSyBsXEX0SMoWRYtQDRHWMHehGqmRiGRgQow
Note: this key is hard-coded into our script
Requests per second per user: 10.0

g)     Any additional information that you consider significant.
On many occasions, it would have made sense to only store the 'text' tag of the first
value (name, birthdate, deathdate, etc.).
We made the decision to store the 'text' for all possible values in many of those cases
because Freebase allows for multiple of them.
We knew we would not be penalized for inefficiency, so if we had the opportunity to
output more data provided by Freebase, we would do it.
In cases where there is only one value, only one value is stored and outputted, but
it is at times stored in a list.

Additionally, we made the choice to not output 'now' as the reference implementation
assumes for coaches and other properties' 'to' sub-property.
This is because just because Freebase doesn't have the 'to' data doesn't mean that the
coach is still coaching.  Freebase just may not have the 'to' information stored.

Although we require you to input some API key as a command line argument, the script
will ultimately use ours which is hardcoded into it.
