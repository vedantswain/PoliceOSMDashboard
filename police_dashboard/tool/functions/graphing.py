import os
from json_parser import fileParser
from dateutil import parser
from datetime import datetime, timedelta
import collections
import matplotlib.pyplot as plt
import numpy as np
from nvd3 import lineChart
import time as tm

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def chartLine(series_data,name):
	name = name
	chart = lineChart(name=name, x_is_date=True, color_category='category20c', height=300, width=800, x_axis_format="%m/%d/%y",use_interactive_guideline=True)
	# chart.set_containerheader("\n\n<h2>" + type + "</h2>\n\n")
	chart.add_serie(name='Tweets',y=series_data['tweets'][0], x=series_data['tweets'][1])
	chart.add_serie(name='Retweets',y=series_data['retweets'][0], x=series_data['retweets'][1])
	chart.add_serie(name='Favourites',y=series_data['favs'][0], x=series_data['favs'][1])
	chart.buildcontent()
	# print chart.htmlcontent
	# output_file.write(chart.htmlcontent)
	return chart.htmlcontent

def parseData(all_data,filename):
	html_data={}
	file_path=os.path.join(BASE_DIR, 'data/')
	tweet_time={}
	retweet_time={}
	fav_time={}
	# print all_data[0].keys()
	for data in all_data:
		# print data['created_at']
		dt = parser.parse(data['created_at'])
		dt=dt+timedelta(hours=5,minutes=30)
		time_label=str(dt).split(" ")[0]+" 12"
		if time_label not in tweet_time.keys():
			tweet_time[time_label]=1
		else:
			tweet_time[time_label]=tweet_time[time_label]+1

		if time_label not in retweet_time.keys():
			if 'retweet_count' in data.keys():
				retweet_time[time_label]=data['retweet_count']
		else:
			if 'retweet_count' in data.keys():
				retweet_time[time_label]=retweet_time[time_label]+data['retweet_count']

		if time_label not in fav_time.keys():
			if 'favorite_count' in data.keys():
				fav_time[time_label]=data['favorite_count']
		else:
			if 'favorite_count' in data.keys():
				fav_time[time_label]=fav_time[time_label]+data['favorite_count']

	series={}
	tweet_time=collections.OrderedDict(sorted(tweet_time.items()))
	# add=0
	# for key in tweet_time.keys():
	# 	tweet_time[key]=tweet_time[key]+add
	# 	add=tweet_time[key]
	xtick_labels=[tm.mktime(datetime.strptime(time, "%Y-%m-%d %H").timetuple())*1000 for time in tweet_time.keys()]
	# plot_line(x=range(len(tweet_time.values())),y=tweet_time.values(),x_label="Time",y_label="No. of Posts",xtick_labels=xtick_labels,title=filename)
	# print tweet_time
	# html_data['tweets']=chart_line(tweet_time.values(),xtick_labels,filename=file_path+"tweet_cdf.html")
	series['tweets']=[tweet_time.values(),xtick_labels]

	retweet_time=collections.OrderedDict(sorted(retweet_time.items()))
	# add=0
	# for key in retweet_time.keys():
	# 	retweet_time[key]=retweet_time[key]+add
	# 	add=retweet_time[key]
	xtick_labels=[tm.mktime(datetime.strptime(time, "%Y-%m-%d %H").timetuple())*1000 for time in retweet_time.keys()]
	# plot_line(x=range(len(retweet_time.values())),y=retweet_time.values(),x_label="Time",y_label="No. of Posts",xtick_labels=xtick_labels,title=filename)
	# print retweet_time
	series['retweets']=[retweet_time.values(),xtick_labels]

	fav_time=collections.OrderedDict(sorted(fav_time.items()))
	# add=0
	# for key in retweet_time.keys():
	# 	retweet_time[key]=retweet_time[key]+add
	# 	add=retweet_time[key]
	xtick_labels=[tm.mktime(datetime.strptime(time, "%Y-%m-%d %H").timetuple())*1000 for time in fav_time.keys()]
	# plot_line(x=range(len(retweet_time.values())),y=retweet_time.values(),x_label="Time",y_label="No. of Posts",xtick_labels=xtick_labels,title=filename)
	# print retweet_time
	series['favs']=[fav_time.values(),xtick_labels]
	
	# html_data=chart_line(series,"graph_1")

	return series

if __name__=="__main__":
	filename="gujarat riot_search.json"
	data=fileParser(filename)
	# print data
	parseData(data,filename)

	filename="karnataka bandh_search.json"
	data=fileParser(filename)
	# print data
	parseData(data,filename)