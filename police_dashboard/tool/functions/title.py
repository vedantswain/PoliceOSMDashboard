import os
from os.path import isfile, join

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def getTitle(handle,platform):
	twitter_titles={"BlrCityPolice":"Bangaluru City Police",
					"CPBlr":"Commissioner of Police, Bangaluru City",
					"addlcptraffic":"Additional Commissioner of Police - Traffic, Bengaluru City"}
	if platform=="twitter":
		return twitter_titles[handle]
	return ""

def getComparisons(handle,platform):
	twitter_titles=allTwitterTitles()
	if platform=="twitter":
		twitter_titles.remove(handle)
		return twitter_titles
	return []

def getKeywords(keyword):
	keywords=["worried","why","want","need"]
	keywords.remove(keyword)
	return keywords

def allTwitterTitles():
	mypath=os.path.join(BASE_DIR, 'data/')
	onlyfiles = [ f for f in os.listdir(mypath) if isfile(join(mypath,f)) ]
	handles=[]
	for fl in onlyfiles:
		if '.json' in fl  and 'tweets_' in fl:
			handles.append(fl[7:-5])

	return handles