import os,re,random
from json_parser import fileParser
from dateutil import parser
from datetime import datetime, timedelta
import collections
import matplotlib.pyplot as plt
from scipy.misc import imread
import numpy as np
from nvd3 import lineChart
import time as tm
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def chartLine(series_data,name):
	name = name
	chart = lineChart(name=name, x_is_date=True, color_category='category20c', height=300, width=800, x_axis_format="%m/%d/%y",use_interactive_guideline=True)
	# chart.set_containerheader("\n\n<h2>" + type + "</h2>\n\n")
	kwargs1_1={"color":"#2574A9"}
	kwargs1_2={"color":"#3498DB"}
	kwargs1_3={"color":"#6BB9F0"}
	chart.add_serie(name='Tweets',y=series_data['tweets'][0], x=series_data['tweets'][1],**kwargs1_1)
	chart.add_serie(name='Retweets',y=series_data['retweets'][0], x=series_data['retweets'][1],**kwargs1_2)
	chart.add_serie(name='Favourites',y=series_data['favs'][0], x=series_data['favs'][1],**kwargs1_3)
	chart.buildcontent()
	# print chart.htmlcontent
	# output_file.write(chart.htmlcontent)
	return chart.htmlcontent

def chartVS(series_data1,series_data2,name):
	name = name
	chart = lineChart(name=name, x_is_date=True, color_category='category20c', height=300, width=800, x_axis_format="%m/%d/%y",use_interactive_guideline=True)
	# chart.set_containerheader("\n\n<h2>" + type + "</h2>\n\n")
	kwargs1_1={"color":"#2574A9"}
	kwargs1_2={"color":"#3498DB"}
	kwargs1_3={"color":"#6BB9F0"}
	chart.add_serie(name='Tweets '+series_data1['name'],y=series_data1['tweets'][0], x=series_data2['tweets'][1],**kwargs1_1)
	chart.add_serie(name='Retweets '+series_data1['name'],y=series_data1['retweets'][0], x=series_data2['retweets'][1],**kwargs1_2)
	chart.add_serie(name='Favourites '+series_data1['name'],y=series_data1['favs'][0], x=series_data2['favs'][1],**kwargs1_3)

	kwargs2_1={"color":"#D35400"}
	kwargs2_2={"color":"#F2784B"}
	kwargs2_3={"color":"#EB974E"}
	chart.add_serie(name='Tweets '+series_data2['name'],y=series_data2['tweets'][0], x=series_data2['tweets'][1],**kwargs2_1)
	chart.add_serie(name='Retweets '+series_data2['name'],y=series_data2['retweets'][0], x=series_data2['retweets'][1],**kwargs2_2)
	chart.add_serie(name='Favourites '+series_data2['name'],y=series_data2['favs'][0], x=series_data2['favs'][1],**kwargs2_3)
	
	chart.buildcontent()
	# print chart.htmlcontent
	# output_file.write(chart.htmlcontent)
	return chart.htmlcontent

def wordTree(text_array,name,word,kind="norm"):
	inject=""

	if kind=='ajax':
		function_call="drawChart()"
	else:
		function_call="google.setOnLoadCallback(drawChart)"

	inject+='<div id="'+name+'" style="width: 800px; height: 300px;"></div>'
	inject+='<script type="text/javascript">'+function_call+';'
	inject+='function drawChart() {var data = google.visualization.arrayToDataTable(['
	inject+="['Phrases'],"
	
	for text in text_array:
		inject+='["'+text+'"],'

	inject+="]);var options = {wordtree: {format: 'implicit',"
	inject+="word: '"+word+"'}};"
	inject+='console.log("loading graph");'
	inject+="var chart = new google.visualization.WordTree(document.getElementById('"+name+"'));"
	inject+="chart.draw(data, options);}</script>"

	return inject

def wordCloud(text_array,name):
	cloud_text=""
	for text in text_array:
		cloud_text+=text+" "

	m_stopwords=['police','traffic','sir']

	for word in m_stopwords:
		STOPWORDS.add(word)

	image_mask = os.path.join(BASE_DIR, 'static/tool/img/nebula.jpg')
	coloring = imread(image_mask)
	
	wordcloud = WordCloud(stopwords=STOPWORDS,background_color="white",mask=coloring).generate(cloud_text)
	filename=os.path.join(BASE_DIR, 'static/tool/img/'+name+'.png')

	image_colors = ImageColorGenerator(coloring)
	wordcloud.recolor(color_func=image_colors)
	wordcloud.to_file(filename)
	data_uri = open(filename, 'rb').read().encode('base64').replace('\n', '')
	img_tag = '<img src="data:image/png;base64,{0}" style="height:570px;width:570px">'.format(data_uri)
	return img_tag


def parseText(all_data):
	text_array=[]
	for data in all_data:
		text=data['text']
		if 'RT' in text:
			continue
		tweet_text=text.replace('\n', ' ').replace('\r', '')
		tweet_text=tweet_text.replace("'", "\'")
		tweet_text=tweet_text.replace('"', '\'')
		no_url_text=re.sub(r'https?:\/\/.*[\r\n]*', '', tweet_text, flags=re.MULTILINE)
		no_mention_text=re.sub(r'@\w+','',no_url_text,flags=re.MULTILINE)
		final_text=no_mention_text
		text_array.append(final_text)
	return text_array

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
	xtick_labels=[tm.mktime(datetime.strptime(time, "%Y-%m-%d %H").timetuple())*1000 for time in tweet_time.keys()]
	series['tweets']=[tweet_time.values(),xtick_labels]

	retweet_time=collections.OrderedDict(sorted(retweet_time.items()))
	xtick_labels=[tm.mktime(datetime.strptime(time, "%Y-%m-%d %H").timetuple())*1000 for time in retweet_time.keys()]
	series['retweets']=[retweet_time.values(),xtick_labels]

	fav_time=collections.OrderedDict(sorted(fav_time.items()))
	xtick_labels=[tm.mktime(datetime.strptime(time, "%Y-%m-%d %H").timetuple())*1000 for time in fav_time.keys()]
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