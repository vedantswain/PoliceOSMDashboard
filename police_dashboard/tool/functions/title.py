def getTitle(handle,platform):
	twitter_titles={"BlrCityPolice":"Bangaluru City Police",
					"CPBlr":"Commissioner of Police, Bangaluru City",
					"addlcptraffic":"Additional Commissioner of Police - Traffic, Bengaluru City"}
	if platform=="twitter":
		return twitter_titles[handle]
	return ""

def getComparisons(handle,platform):
	twitter_titles=["BlrCityPolice","addlcptraffic","CPBlr"]
	if platform=="twitter":
		twitter_titles.remove(handle)
		return twitter_titles
	return []