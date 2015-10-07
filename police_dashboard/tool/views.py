import os
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from functions.json_parser import fileParser
from functions.graphing import parseData,chartLine,chartVS
from functions.title import getTitle,getComparisons

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def index(request):
    return HttpResponse("Hello, world. You're at the tool index.")

def dashboard(request,handle):
	template = loader.get_template('tool/basic.html')
	
	filename = os.path.join(BASE_DIR, 'tool/data/tweets_'+handle+'.json')
	data = fileParser(filename)

	series = parseData(data,filename)
	graph = chartLine(series,"graph 1")

	comparisonList=getComparisons(handle=handle,platform="twitter")
	comp_div_twitter=""
	for comp in comparisonList:
		comp_div_twitter=comp_div_twitter+'<li><a class="compare-to-graph1-twitter" href="#">@'+comp+'</a></li>'
	
	context = RequestContext(request, {
	    'dashboard_name': getTitle(handle=handle,platform="twitter")+" Dashboard",
	    'compare_to': "Compare to",
	    'graph_tweets':graph,
	    'graph_retweets':"graph",
	    'twitter_handle':handle,
	    'compare_to_graph1_twitter':comp_div_twitter,
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