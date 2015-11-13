import json
from tool.models import NPostsdatanew
from title import getId

def fileParser(file_name):
	data = []
	try:
		with open(file_name) as f:
		    for line in f:
		        data.append(json.loads(line))
	except IOError:
		print "Twitter file: "+file_name+" doesn't exist"
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

def getDataAll():
	data = []
	for p in NPostsdatanew.objects.raw("select * from N_Postsdatanew where sentiment=-1"):
		# print p.__dict__
		# print type(p)
		data.append(p.__dict__)
	return data


def getUniqueDataSentiment(handle):
	data = []
	handle_id=getId(handle)
	for p in NPostsdatanew.objects.raw("select * from N_Postsdatanew where pageid='"+handle+"' && sentiment=-1"):
		# print p.__dict__
		# print type(p)
		data.append(p.__dict__)
	return data

def updateBulkSentimentRecord(results):

	for data in results['data']:
		NPostsdatanew_edit = NPostsdatanew.objects.get(localid=data['localid']) # object to update
		NPostsdatanew_edit.sentiment = data['polarity']
		NPostsdatanew_edit.save()

def getSentimentCount(handle):
		data = []
		data_dict = {}
		for p in NPostsdatanew.objects.raw("select localid,sentiment,count(sentiment) as sent_count from N_Postsdatanew where pageid='"+handle+"' GROUP BY sentiment"): # object to update
			if p.sentiment == 0:
				data_dict = {'label':'Negative' ,'value': int(p.sent_count)}
			elif p.sentiment == 2:
				data_dict = {'label':'Neutral' ,'value': int(p.sent_count)}
			elif p.sentiment == 4:
				data_dict = {'label':'Positive' ,'value': int(p.sent_count)}

			if p.sentiment != -1:
				data.append(data_dict)

		return data

def getSentimentData(handle,sent):
	data = []
	data_dict = {}

	if sent == 'Negative':
		sent_val = 0
	elif sent == 'Neutral':
		sent_val = 2
	elif sent == 'Positive':
		sent_val = 4

	# print sent_val
	try:
		for p in NPostsdatanew.objects.raw("select * from N_Postsdatanew where pageid='"+handle+"' and sentiment="+str(sent_val)): # object to update
			data.append(p.__dict__)
	except Exception,e:
		print e

	return data



if __name__=='__main__':
	# ### returns dictionary for given json file
	print fileParser("Bhubaneswar school_pagesearch_data.json")
