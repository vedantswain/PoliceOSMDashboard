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

def chart_line(ydata,xdata,filename):
	output_file = open(filename, 'w')
	type = 'lineChart'
	chart = lineChart(name=type, x_is_date=True, color_category='category20c', height=450, width=900)
	chart.set_containerheader("\n\n<h2>" + type + "</h2>\n\n")
	chart.add_serie(y=ydata, x=xdata)
	chart.buildcontent()
	# print chart.htmlcontent
	# output_file.write(chart.htmlcontent)
	return chart.htmlcontent

def parseData(all_data,filename):
	html_data={}
	file_path=os.path.join(BASE_DIR, 'data/')
	tweet_time={}
	retweet_time={}
	# print all_data[0].keys()
	for data in all_data:
		# print data['created_at']
		dt = parser.parse(data['created_at'])
		dt=dt+timedelta(hours=5,minutes=30)
		time_label=str(dt).split(":")[0]
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

	tweet_time=collections.OrderedDict(sorted(tweet_time.items()))
	add=0
	for key in tweet_time.keys():
		tweet_time[key]=tweet_time[key]+add
		add=tweet_time[key]
	xtick_labels=[tm.mktime(datetime.strptime(time, "%Y-%m-%d %H").timetuple())*1000 for time in tweet_time.keys()]
	# plot_line(x=range(len(tweet_time.values())),y=tweet_time.values(),x_label="Time",y_label="No. of Posts",xtick_labels=xtick_labels,title=filename)
	# print tweet_time
	html_data['tweets']=chart_line(tweet_time.values(),xtick_labels,filename=file_path+"tweet_cdf.html")

	retweet_time=collections.OrderedDict(sorted(retweet_time.items()))
	add=0
	for key in retweet_time.keys():
		retweet_time[key]=retweet_time[key]+add
		add=retweet_time[key]
	xtick_labels=[tm.mktime(datetime.strptime(time, "%Y-%m-%d %H").timetuple())*1000 for time in retweet_time.keys()]
	# plot_line(x=range(len(retweet_time.values())),y=retweet_time.values(),x_label="Time",y_label="No. of Posts",xtick_labels=xtick_labels,title=filename)
	# print retweet_time
	html_data['retweets']=chart_line(retweet_time.values(),xtick_labels,filename=file_path+"retweet_cdf.html")

	return html_data

if __name__=="__main__":
	filename="gujarat riot_search.json"
	data=fileParser(filename)
	# print data
	parseData(data,filename)

	filename="karnataka bandh_search.json"
	data=fileParser(filename)
	# print data
	parseData(data,filename)