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

def onlySpecificLine(data,name,handle,only):
	div='<div id="graph'+'_'+name+'_'+only+'" style="height:300px;width:960px;"></div>\n'
	script='<script>\nvar data = [\n'

	for key in data.keys():
		# print data[key].keys()
		# break
		date=tm.strftime('%Y-%m-%d', tm.localtime(key))
		script+='{date:"'+date+'", "'+only+'": '+str(data[key][only])+'},\n' 
    
	script=script[:-2]
	script+='\n];\n'
	# script+='function callRender'+'_'+name+'_'+only+'(){\n'
	script+='renderGraph(data,"graph'+'_'+name+'_'+only+'","#collapse_'+only+'")\n'
	# script+='}\n'
	script+='</script>'

	return div+script

def chartD3Line(data,name,handle):
	fb=['posts','likes','comments']
	tw=['tweets','retweets','favs']

	if name =='fb':
		osn=fb ### for now
	else:
		osn=tw

	div='<div id="graph'+'_'+name+'" style="height:500px;width:960px;"></div>\n'
	script='<script>\nvar data = [\n'

	for key in data.keys():
		date=tm.strftime('%Y-%m-%d', tm.localtime(key))
		script+='{date:"'+date+'", "'+handle+' '+osn[0]+'": '+str(data[key][osn[0]])+', "'+handle+' '+osn[1]+'": '+str(data[key][osn[1]])+', "'+handle+' '+osn[2]+'": '+str(data[key][osn[2]])+'},\n' 
    
	script=script[:-2]
	script+='\n];\nrenderGraph(data,"graph'+'_'+name+'","")\n</script>'

	return div+script 

def chartD3LineVS(data1,data2,name,handle1,handle2):

	fb=['posts','likes','comments']
	tw=['tweets','retweets','favs']

	if name =='facebook':
		osn=fb ### for now
	else:
		osn=tw

	data=mergeData(data1,data2,osn) ### merges both dictionaries into a single one to ensure dates are correct

	div='<div id="graph'+'_'+name+'" style="height:500px;width:960px;"></div>\n'
	script='<script>\nvar data = [\n'

	for key in data.keys():
		date=tm.strftime('%Y-%m-%d', tm.localtime(key))
		script+='{date:"'+date+'", "'+handle1+' '+osn[0]+'": '+str(data[key][osn[0]+'_1'])+', "'+handle1+' '+osn[1]+'": '+str(data[key][osn[1]+'_1'])+', "'+handle1+' '+osn[2]+'": '+str(data[key][osn[2]+'_1'])
		script+=', "'+handle2+' '+osn[0]+'": '+str(data[key][osn[0]+'_2'])+', "'+handle2+' '+osn[1]+'": '+str(data[key][osn[1]+'_2'])+', "'+handle2+' '+osn[2]+'": '+str(data[key][osn[2]+'_2'])+'},\n' 
    
	script=script[:-2]
	script+='\n];\nrenderGraph(data,"graph'+'_'+name+'","")\n</script>'

	return div+script 

def wordTree(text_array,name,word,kind="norm"):
	inject=""

	extra2=""

	new_text_arr=[]

	for text in text_array:
		if word in text:
			new_text_arr.append(text)

	text_array=new_text_arr

	if len(text_array)>25:
		random.shuffle(text_array)
		text_array=text_array[:25]

	if kind=='ajax':
		function_call="drawChart(data,'"+name+"','"+word+"')"
	else:
		function_call="google.setOnLoadCallback(drawChart(data,'"+name+"','"+word+"'))"
		if "twitter" in name:
			extra2="var container = document.getElementById('menu1');"
			extra2+="google.visualization.events.addListener(chart, 'ready', function () {"
			extra2+="container.className = container.className.replace( /(?:^|\s)active(?!\S)/g , '' );});"
			function_call=""

	inject+='<div id="'+name+'" style="width: 800px; height: 300px;"></div>'
	inject+='<script type="text/javascript">\n'

	data='data=[\n'
	data+="['Phrases'],\n"
	
	for text in text_array:
		if "connect.facebook.net" in text:
			# print "skipping\n"+text
			continue
		data+='["'+text+'"],\n'

	data+="];\n"
	
	inject+=data
	inject+=function_call+';\n'

	inject+="</script>"

	return inject

def wordCloud(text_array,name,keyword=""):
	return wordCloudN(text_array,name,keyword)
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

def wordCloudN(text_array,name,keyword=""):
	new_text_arr=[]
	if keyword is not "":
		keyword=keyword.split(" ")[0]
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

	# image_mask = os.path.join(BASE_DIR, 'static/tool/img/nebula.png')
	# coloring = imread(image_mask)
	
	wordcloud = WordCloud(stopwords=STOPWORDS,background_color="white",ranks_only=True,max_words=100).generate(cloud_text)
	# filename=os.path.join(BASE_DIR, 'static/tool/img/'+name+'.png')

	# image_colors = ImageColorGenerator(coloring)
	# wordcloud.recolor(color_func=image_colors)
	# wordcloud.to_file(filename)
	# data_uri = open(filename, 'rb').read().encode('base64').replace('\n', '')

	# img_tag = '<img src="data:image/png;base64,{0}" style="height:400px;">'.format(data_uri)
	
	layout=wordcloud.layout_
	words_freqs=[]
	count=1
	for lo in layout:
		entry={}
		entry['word']=lo[0][0].encode('utf8')
		entry['size']=lo[1]
		words_freqs.append(entry)

	inject=''
	inject+='<script type="text/javascript">\n'
	inject+='var freq_list='+str(words_freqs)+';\n'
	inject+='renderCloud(freq_list,"#'+name+'");\n'
	inject+='</script>'
	# print words_colours
	list_html=""
	cap=51
	if cap>len(words_freqs):
		cap=len(words_freqs)

	for i in range(1,cap):
		list_html+='<li class="list-group-item" ><a class="cloud-key-'+name+'" href="#" >'
		list_html+="#"+str(i)+" "+words_freqs[i]['word']+'</a></li>'

	return (inject,list_html)

def wordTreeActual(all_data,word,platform):
	inject=""

	extra2=""

	random.shuffle(all_data)

	actual_posts=[]
	if platform=="twitter":
		for data in all_data:
			actual_post={}
			text=data['text']
			if 'RT' in text:
				continue
			if word in text:
				actual_post['text']=text
				# actual_post['from']=data['screen_name']
				actual_post['link']="https://twitter.com/statuses/"+str(data['id'])
				actual_posts.append(actual_post)
	else:
		for data in all_data:
			actual_post={}
			if 'message' not in data.keys():
				continue
			text=data['message']
			if "connect.facebook.net" in text:
				# print "skipping\n"+text
				continue
			if word in text:
				actual_post['text']=text
				# actual_post['from']=data['screen_name']
				actual_post['link']='https://www.facebook.com/'+data['id']
				actual_posts.append(actual_post)

	return actual_posts

def parseText(all_data,platform):
	text_array=[]
	if platform=="twitter":
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
			# print final_text
			text_array.append(final_text)
	else:
		for data in all_data:
			if 'message' not in data.keys():
				continue
			text=data['message']
			if "connect.facebook.net" in text:
				# print "skipping\n"+text
				continue
			tweet_text=text.replace('\n', ' ').replace('\r', '')
			tweet_text=tweet_text.replace("'", "\'")
			tweet_text=tweet_text.replace('"', '\'')
			no_url_text=re.sub(r'https?:\/\/.*[\r\n]*', '', tweet_text, flags=re.MULTILINE)
			no_mention_text=re.sub(r'@\w+','',no_url_text,flags=re.MULTILINE)
			final_text=no_mention_text
			# print final_text
			text_array.append(final_text)
	return text_array

def parseFBData(all_data):
	html_data={}
	post_time={}
	like_time={}
	com_time={}
	# print all_data[0].keys()
	for data in all_data:
		datum={}
		# print data['created_at']
		dt = parser.parse(data['created_time'])
		dt=dt+timedelta(hours=5,minutes=30)
		time_label=str(dt).split(" ")[0]+" 12"

		if time_label not in post_time.keys():
			post_time[time_label]=1
		else:
			post_time[time_label]=post_time[time_label]+1

		if time_label not in like_time.keys():
			if 'totallikescount' in data.keys():
				like_time[time_label]=long(data['totallikescount'])
		else:
			if 'totallikecount' in data.keys():
				like_time[time_label]=like_time[time_label]+long(data['totallikescount'])

		if time_label not in com_time.keys():
			if 'totalcommentscount' in data.keys():
				com_time[time_label]=long(data['totalcommentscount'])
		else:
			if 'totalcommentscount' in data.keys():
				com_time[time_label]=com_time[time_label]+long(data['totalcommentscount'])

	series={}
	post_time=collections.OrderedDict(sorted(post_time.items()))
	xtick_labels=[tm.mktime(datetime.strptime(time, "%Y-%m-%d %H").timetuple())*1000 for time in post_time.keys()]
	series['posts']=[post_time.values(),xtick_labels]

	like_time=collections.OrderedDict(sorted(like_time.items()))
	xtick_labels=[tm.mktime(datetime.strptime(time, "%Y-%m-%d %H").timetuple())*1000 for time in like_time.keys()]
	series['likes']=[like_time.values(),xtick_labels]

	com_time=collections.OrderedDict(sorted(com_time.items()))
	xtick_labels=[tm.mktime(datetime.strptime(time, "%Y-%m-%d %H").timetuple())*1000 for time in com_time.keys()]
	series['comments']=[com_time.values(),xtick_labels]
	
	# html_data=chart_line(series,"graph_1")

	return series

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

def getGraphData(series,name):
	data={}

	fb=['posts','likes','comments']
	tw=['tweets','retweets','favs']

	if name =='facebook':
		osn=fb ### for now
	else:
		osn=tw

	i=0

	while i < len(series[osn[0]][0]):
		datum={osn[1]:0,osn[2]:0}
		datum[osn[0]]=series[osn[0]][0][i]
		data[series[osn[0]][1][i]/1000]=datum
		i+=1


	i=0
	while i < len(series[osn[1]][0]):
		data[series[osn[1]][1][i]/1000][osn[1]]=series[osn[1]][0][i]
		i+=1

	i=0
	while i < len(series[osn[2]][0]):
		data[series[osn[2]][1][i]/1000][osn[2]]=series[osn[2]][0][i]
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