from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader


def index(request):
    return HttpResponse("Hello, world. You're at the tool index.")

def dashboard(request,handle):
	template = loader.get_template('tool/basic.html')
	context = RequestContext(request, {
	    'dashboard_name': handle+" dashboard",
	})
	return HttpResponse(template.render(context))