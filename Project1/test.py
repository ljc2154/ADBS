import nltk   
from urllib import urlopen


url = "http://en.wikipedia.org/wiki/Bill_Gates"    
html = urlopen(url).read()    
raw = nltk.clean_html(html) 
raw = raw.replace('.', '')
raw = raw.replace(',', '')
raw = raw.replace('\"', '')
raw = raw.replace(':', '')
raw = raw.replace('/', '')
raw = raw.replace('&', '')
raw = raw.replace('|', '')
raw = raw.replace('^', '')
raw = raw.replace('\'', '')
raw = raw.replace(';', '')
raw = raw.replace('-', '')
raw = raw.replace('[', '')
raw = raw.replace(']', '')
raw = raw.replace(')', '')
raw = raw.replace('(', '')
raw = raw.replace('#', '')
raw = raw.replace('$', '')
raw = raw.replace('!', '')
raw = raw.split()
for word in raw:
	print(word)
