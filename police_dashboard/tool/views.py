import os
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from functions.json_parser import fileParser
from functions.graphing import parseData,chartLine,chartVS,wordTree,parseText,wordCloud
from functions.title import getTitle,getComparisons,getKeywords,allTwitterTitles

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def index(request):
    return HttpResponse("Hello, world. You're at the tool index.")

def dashboard(request,handle):
	template = loader.get_template('tool/basic.html')

	filename = os.path.join(BASE_DIR, 'tool/data/tweets_'+handle+'.json')
	data = fileParser(filename)

	series = parseData(data,filename)
	graph = chartLine(series,"graph 1")

	# print "GRAPH HERE"
	# print graph

	comparisonList=getComparisons(handle=handle,platform="twitter")
	comp_div_twitter1=""
	pick_div=""
	for comp in comparisonList:
		comp_div_twitter1=comp_div_twitter1+'<li><a class="compare-to-graph1-twitter" href="#">@'+comp+'</a></li>'
		pick_div=pick_div+'<li><a class="pick-account" href="../'+comp+'/">@'+comp+'</a></li>'

	word="why"
	keyList=getKeywords(keyword=word)
	key_div_twitter1=""
	for key in keyList:
		key_div_twitter1=key_div_twitter1+'<li><a class="victimzn-key-twitter" href="#">'+key+'</a></li>'

	text_array=parseText(data)
	tree=wordTree(text_array=text_array,name="wordtree_twitter",word=word)

	if len(text_array)>0:
		(cloud,cloud_list)=wordCloud(text_array=text_array,name="wordcloud_twitter")
	else:
		cloud=""
		cloud_list=[]

	context = RequestContext(request, {
	    'dashboard_name': handle+" Dashboard",
	    'pick_account':pick_div,
	    'graph_tweets':graph,
	    'graph_tree_twitter':tree,
	    'twitter_handle':handle,
	    'compare_to_graph1_twitter':comp_div_twitter1,
	    'victimisation_twitter':key_div_twitter1,
	    'victim_current_key_twitter':word,
	    'wordcloud_twitter':cloud,
	    'wordcloud_twitter_list':cloud_list
	})

	return HttpResponse(template.render(context))

def load_name(request):
    context = RequestContext(request)
    name=""
    if request.method == 'GET':
        name = request.GET['comp_handle_name']

    return HttpResponse("Comparing to "+name)

def graph1_twitter_comp(request):
	context =RequestContext(request)
	handle=""
	if request.method == 'GET':
		handle = request.GET['handle_name']
		filename1 = os.path.join(BASE_DIR, 'tool/data/tweets_'+handle+'.json')
		data1 = fileParser(filename1)
		series1 = parseData(data1,filename1)
		series1['name']="@"+handle

		comp_handle = request.GET['comp_handle_name']
		filename2 = os.path.join(BASE_DIR, 'tool/data/tweets_'+comp_handle[1:]+'.json')
		data2 = fileParser(filename2)
		series2 = parseData(data2,filename2)
		series2['name']="@"+comp_handle[1:]
		
		graph = chartVS(series1,series2,"graph 1")
		# print graph
	return HttpResponse(graph)

def victimzn_tree(request):
	context =RequestContext(request)
	handle=""
	if request.method == 'GET':
		platform=request.GET['platform']
		handle = request.GET['handle_name']
		filename = os.path.join(BASE_DIR, 'tool/data/tweets_'+handle+'.json')
		data = fileParser(filename)
		
		word = request.GET['keyword']
		text_array=parseText(data)
		tree=wordTree(text_array=text_array,name="wordtree_"+platform,word=word,kind="ajax")

	return HttpResponse(tree)