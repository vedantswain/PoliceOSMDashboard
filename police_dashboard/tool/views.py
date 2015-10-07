import os
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from functions.json_parser import fileParser
from functions.graphing import parseData,chartLine

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def index(request):
    return HttpResponse("Hello, world. You're at the tool index.")

def dashboard(request,handle):
	template = loader.get_template('tool/basic.html')
	
	filename = os.path.join(BASE_DIR, 'tool/data/tweets_BlrCityPolice.json')
	data = fileParser(filename)

	series = parseData(data,filename)
	graph = chartLine(series,"graph 1")

	context = RequestContext(request, {
	    'dashboard_name': handle+" dashboard",
	    'compare_to': "Compare to",
	    'graph_tweets':graph,
	    'graph_retweets':"graph",
	})

	return HttpResponse(template.render(context))

def load_name(request):
    context = RequestContext(request)
    name=""
    if request.method == 'GET':
        name = request.GET['handle_name']

    return HttpResponse(name)

