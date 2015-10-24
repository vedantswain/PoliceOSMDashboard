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

def getDashed(content):
	replace_str="var datum = data_graph_1;"
	script_added="for (var i = 0; i < data_graph_1.length; i++) {"
	script_added+="if (data_graph_1[i]['key'].indexOf('Tweets')> -1){"
	script_added+="data_graph_1[i].classed='dashed';}}\n"
	script_added+=replace_str
	content=content.replace(replace_str,script_added)
	return content

def chartD3Line(data,name,handle):
	fb=['posts','likes','comments']
	tw=['tweets','retweets','favs']

	if name =='fb':
		osn=tw ### for now
	else:
		osn=tw

	div='<div id="graph'+'_'+name+'"></div>\n'
	script='<script>\nvar data = [\n'

	for key in data.keys():
		date=tm.strftime('%Y-%m-%d', tm.localtime(key))
		script+='{date:"'+date+'", "'+handle+' '+osn[0]+'": '+str(data[key][osn[0]])+', "'+handle+' '+osn[1]+'": '+str(data[key][osn[1]])+', "'+handle+' '+osn[2]+'": '+str(data[key][osn[2]])+'},\n' 
    
	script=script[:-2]
	script+='\n];\nrenderGraph(data,"#graph'+'_'+name+'")\n</script>'

	return div+script 

def chartD3LineVS(data1,data2,name,handle1,handle2):
	handle2=handle2[1:]

	fb=['posts','likes','comments']
	tw=['tweets','retweets','favs']

	if name =='facebook':
		osn=tw ### for now
	else:
		osn=tw

	data=mergeData(data1,data2,osn) ### merges both dictionaries into a single one to ensure dates are correct

	div='<div id="graph'+'_'+name+'"></div>\n'
	script='<script>\nvar data = [\n'

	for key in data.keys():
		date=tm.strftime('%Y-%m-%d', tm.localtime(key))
		script+='{date:"'+date+'", "'+handle1+' '+osn[0]+'": '+str(data[key][osn[0]+'_1'])+', "'+handle1+' '+osn[1]+'": '+str(data[key][osn[1]+'_1'])+', "'+handle1+' '+osn[2]+'": '+str(data[key][osn[2]+'_1'])
		script+=', "'+handle2+' '+osn[0]+'": '+str(data[key][osn[0]+'_2'])+', "'+handle2+' '+osn[1]+'": '+str(data[key][osn[1]+'_2'])+', "'+handle2+' '+osn[2]+'": '+str(data[key][osn[2]+'_2'])+'},\n' 
    
	script=script[:-2]
	script+='\n];\nrenderGraph(data,"#graph'+'_'+name+'")\n</script>'

	return div+script 

def wordTree(text_array,name,word,kind="norm"):
	inject=""

	extra2=""

	if kind=='ajax':
		function_call="drawChart()"
	else:
		function_call="google.setOnLoadCallback(drawChart)"
		if "twitter" in name:
			extra2="var container = document.getElementById('menu1');"
			extra2+="google.visualization.events.addListener(chart, 'ready', function () {"
			extra2+="container.className = container.className.replace( /(?:^|\s)active(?!\S)/g , '' );});"

	inject+='<div id="'+name+'" style="width: 800px; height: 300px;"></div>'
	inject+='<script type="text/javascript">'+function_call+';'
	inject+='function drawChart() {var data = google.visualization.arrayToDataTable(['
	inject+="['Phrases'],"
	
	for text in text_array:
		inject+='["'+text+'"],'

	inject+="]);var options = {wordtree: {format: 'implicit',"
	inject+="word: '"+word+"'}"
	inject+="};"
	inject+='console.log("loading graph");'
	inject+="var chart = new google.visualization.WordTree(document.getElementById('"+name+"'));"
	inject+=extra2
	inject+="chart.draw(data, options);}</script>"

	return inject

def wordCloud(text_array,name,keyword=""):
	new_text_arr=[]
	if keyword is not "":
		keyword=keyword.split(" ")[1]
	for text in text_array:
		if keyword in text:
			new_text_arr.append(text)

	text_array=new_text_arr

	cloud_text=""
	for text in text_array:
		cloud_text+=text+" "

	m_stopwords=['police','traffic','sir']

	for word in m_stopwords:
		STOPWORDS.add(word)

	image_mask = os.path.join(BASE_DIR, 'static/tool/img/nebula.png')
	coloring = imread(image_mask)
	
	wordcloud = WordCloud(stopwords=STOPWORDS,background_color="white",mask=coloring,ranks_only=True,max_words=50).generate(cloud_text)
	filename=os.path.join(BASE_DIR, 'static/tool/img/'+name+'.png')

	image_colors = ImageColorGenerator(coloring)
	wordcloud.recolor(color_func=image_colors)
	wordcloud.to_file(filename)
	data_uri = open(filename, 'rb').read().encode('base64').replace('\n', '')

	img_tag = '<img src="data:image/png;base64,{0}" style="height:400px;">'.format(data_uri)
	
	layout=wordcloud.layout_
	words_colours={}
	count=1
	for lo in layout:
		entry={}
		entry['word']=lo[0][0]
		color=lo[len(lo)-1]
		color=color[4:]
		color=color[:-1]
		color_split=color.split(',')
		color_num=[int(x) for x in color_split]
		color_hex='#%02x%02x%02x' % tuple(color_num)
		# print color_num
		entry['color']=color_hex
		words_colours[count]=entry
		count+=1

	# print words_colours
	list_html=""
	cap=51
	if cap>len(words_colours):
		cap=len(words_colours)

	for i in range(1,cap):
		list_html+='<li class="list-group-item" ><a class="cloud-key-'+name+'" href="#" style="color:'+words_colours[i]['color']+'">'
		list_html+="#"+str(i)+" "+words_colours[i]['word']+'</a></li>'

	return (img_tag,list_html)


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
		datum={}
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

def getGraphData(series):
	data={}
	i=0
	while i < len(series['tweets'][0]):
		datum={'retweets':0,'favs':0}
		datum['tweets']=series['tweets'][0][i]
		data[series['tweets'][1][i]/1000]=datum
		i+=1


	i=0
	while i < len(series['retweets'][0]):
		data[series['retweets'][1][i]/1000]['retweets']=series['retweets'][0][i]
		i+=1

	i=0
	while i < len(series['favs'][0]):
		data[series['favs'][1][i]/1000]['favs']=series['favs'][0][i]
		i+=1

	data=collections.OrderedDict(sorted(data.items()))
	return data

def mergeData(data1,data2,osn):
	data={}
	for key in data1.keys():
		datum={}
		datum[osn[0]+'_1']=data1[key][osn[0]]
		datum[osn[1]+'_1']=data1[key][osn[1]]
		datum[osn[2]+'_1']=data1[key][osn[2]]
		datum[osn[0]+'_2']=0
		datum[osn[1]+'_2']=0
		datum[osn[2]+'_2']=0

		data[key]=datum

	for key in data2.keys():
		if key in data1.keys():
			data[key][osn[0]+'_2']=data2[key][osn[0]]
			data[key][osn[1]+'_2']=data2[key][osn[1]]
			data[key][osn[2]+'_2']=data2[key][osn[2]]
		else:
			datum={}
			datum[osn[0]+'_2']=data2[key][osn[0]]
			datum[osn[1]+'_2']=data2[key][osn[1]]
			datum[osn[2]+'_2']=data2[key][osn[2]]
			datum[osn[0]+'_1']=0
			datum[osn[1]+'_1']=0
			datum[osn[2]+'_1']=0

			data[key]=datum

	# print data
	data=collections.OrderedDict(sorted(data.items()))
	return data


if __name__=="__main__":
	filename="gujarat riot_search.json"
	data=fileParser(filename)
	# print data
	parseData(data,filename)

	filename="karnataka bandh_search.json"
	data=fileParser(filename)
	# print data
	parseData(data,filename)