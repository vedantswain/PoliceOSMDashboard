import os
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from functions.json_parser import fileParser
from functions.graphing import parseData,chartLine,chartD3Line,chartVS,chartD3LineVS,wordTree,parseText,wordCloud,getGraphData
from functions.title import getTitle,getComparisons,getKeywords,allTwitterTitles

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def index(request):
    return HttpResponse("Hello, world. You're at the tool index.")

def dashboard(request,handle):
	template = loader.get_template('tool/basic.html')

	filename = os.path.join(BASE_DIR, 'tool/data/tweets_'+handle+'.json')
	data = fileParser(filename)
	series = parseData(data,filename)
	graph_data_tw=getGraphData(series)

	filename = os.path.join(BASE_DIR, 'tool/data/tweets_'+handle+'.json')
	data = fileParser(filename)
	series = parseData(data,filename)
	graph_data_fb=getGraphData(series)
	
	d3graph_tw=chartD3Line(graph_data_tw,"tw",handle)
	d3graph_fb=chartD3Line(graph_data_fb,"fb",handle)

	# print "GRAPH HERE"
	# print d3graph

	comparisonList=getComparisons(handle=handle,platform="twitter")
	comp_div_twitter1=""
	comp_div_facebook1=""
	pick_div=""
	for comp in comparisonList:
		comp_div_twitter1=comp_div_twitter1+'<li><a class="compare-to-graph1-twitter" href="#">@'+comp+'</a></li>'
		comp_div_facebook1=comp_div_facebook1+'<li><a class="compare-to-graph1-facebook" href="#">@'+comp+'</a></li>'
		pick_div=pick_div+'<li><a class="pick-account" href="../'+comp+'/">@'+comp+'</a></li>'

	word="why"
	keyList=getKeywords(keyword=word)
	key_div_twitter1=""
	key_div_facebook1=""
	for key in keyList:
		key_div_twitter1=key_div_twitter1+'<li><a class="victimzn-key-twitter" href="#">'+key+'</a></li>'
		key_div_facebook1=key_div_facebook1+'<li><a class="victimzn-key-facebook" href="#">'+key+'</a></li>'

	text_array_tw=parseText(data)
	text_array_fb=parseText(data)
	tree_tw=wordTree(text_array=text_array_tw,name="wordtree_twitter",word=word)
	tree_fb=wordTree(text_array=text_array_tw,name="wordtree_facebook",word=word)

	if len(text_array_tw)>0:
		(cloud_tw,cloud_list_tw)=wordCloud(text_array=text_array_tw,name="wordcloud_twitter")
	else:
		cloud_tw=""
		cloud_list_tw=[]

	if len(text_array_fb)>0:
		(cloud_fb,cloud_list_fb)=wordCloud(text_array=text_array_fb,name="wordcloud_facebook")
	else:
		cloud_fb=""
		cloud_list_fb=[]

	context = RequestContext(request, {
	    'dashboard_name': handle+" Dashboard",
	    'pick_account':pick_div,
	    # 'graph_tweets':d3graph_tw,
	    'graph_facebook':d3graph_fb,
	    'graph_tree_twitter':tree_tw,
	    'graph_tree_facebook':tree_fb,
	    'twitter_handle':handle,
	    'facebook_handle':handle,
	    'compare_to_graph1_twitter':comp_div_twitter1,
	    'compare_to_graph1_facebook':comp_div_facebook1,
	    'victimisation_twitter':key_div_twitter1,
	    'victimisation_facebook':key_div_facebook1,
	    'victim_current_key_twitter':word,
	    'victim_current_key_facebook':word,
	    'wordcloud_twitter':cloud_tw,
	    'wordcloud_twitter_list':cloud_list_tw,
	    'wordcloud_facebook':cloud_fb,
	    'wordcloud_facebook_list':cloud_list_tw
	})

	return HttpResponse(template.render(context))

def load_name(request):
    context = RequestContext(request)
    name=""
    if request.method == 'GET':
        name = request.GET['comp_handle_name']

    return HttpResponse("Comparing to "+name)

def graph_comp(request):
	context =RequestContext(request)
	handle=""
	platform=request.GET['platform']
	if request.method == 'GET':
		handle = request.GET['handle_name']
		filename1 = os.path.join(BASE_DIR, 'tool/data/tweets_'+handle+'.json')
		data1 = fileParser(filename1)
		series1 = parseData(data1,filename1)
		graph_data1=getGraphData(series1)
		
		comp_handle = request.GET['comp_handle_name']
		filename2 = os.path.join(BASE_DIR, 'tool/data/tweets_'+comp_handle[1:]+'.json')
		data2 = fileParser(filename2)
		series2 = parseData(data2,filename2)
		graph_data2=getGraphData(series2)
		
		d3graph=chartD3LineVS(graph_data1,graph_data2,platform,handle,comp_handle)
		print d3graph
	return HttpResponse(d3graph)

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