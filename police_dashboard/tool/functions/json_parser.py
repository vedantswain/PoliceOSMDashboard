import json

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

if __name__=='__main__':
	# ### returns dictionary for given json file
	print fileParser("Bhubaneswar school_pagesearch_data.json")
