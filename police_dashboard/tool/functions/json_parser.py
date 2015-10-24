import json
from tool.models import NPostsdatanew
from title import getId

def fileParser(file_name):
	data = []
	with open(file_name) as f:
	    for line in f:
	        data.append(json.loads(line))
	return data

def fileParser_json(file_name):
	data = []
	with open(file_name) as f:
	    for line in f:
	        data.append(line)
	return data

def getData(handle):
	data = []
	handle_id=getId(handle)
	for p in NPostsdatanew.objects.raw("select * from N_Postsdatanew where pageid='"+handle+"' && fromid!='"+handle_id+"'"):
		# print p.__dict__
		# print type(p)
		data.append(p.__dict__)
	return data

if __name__=='__main__':
	# ### returns dictionary for given json file
	print fileParser("Bhubaneswar school_pagesearch_data.json")
