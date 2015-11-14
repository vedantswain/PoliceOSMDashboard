import os
import pymongo
from os.path import isfile, join

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def getStateCount(data):
	state_pg_count={
		'Andaman and Nicobar Islands':0,
		'Andhra Pradesh':0,
		'Arunachal Pradesh':0,
		'Assam':0,
		'Bihar':0,
		'Chandigarh':0,
		'Chhattisgarh':0,
		'Dadra and Nagar Haveli':0,
		'Daman and Diu':0,
		'Delhi':0,
		'Goa':0,
		'Gujarat':0,
		'Haryana':0,
		'Himachal Pradesh':0,
		'Jammu and Kashmir':0,
		'Jharkhand':0,
		'Karnataka':0,
		'Kerala':0,
		'Lakshadweep':0,
		'Madhya Pradesh':0,
		'Maharashtra':0,
		'Manipur':0,
		'Meghalaya':0,
		'Mizoram':0,
		'Nagaland':0,
		'Orissa':0,
		'Puducherry':0,
		'Punjab':0,
		'Rajasthan':0,
		'Sikkim':0,
		'Tamil Nadu':0,
		'Telangana':0,
		'Tripura':0,
		'Uttar Pradesh':0,
		'Uttarakhand':0,
		'West Bengal':0,
	}

	stateDataArray=[['State','No. of Pages']]

	for ht_dat in data:
		state=ht_dat['state'].encode('utf8')
		if state != "":
			state_pg_count[state]+=1

	for key in state_pg_count:
		pg_datum=[key,state_pg_count[key]]
		stateDataArray.append(pg_datum)

	return stateDataArray

def getAllHandles():
	client = pymongo.MongoClient()
	db = client.FBPoliceData
	page_info=db.page_names.find()
	All_handles={}
	for pi in page_info:
		j=db.page_fields.find_one({"page":pi["page"]})
		if j is None:
			continue
		if "id" in j.keys():
			All_handles[pi["page"]]=[pi["name"],pi["handle"],j["id"]]
	return All_handles

def getId(handle):
	handle=handle.encode('utf8')
	All_handles=getAllHandles()
	return All_handles[handle][2]

def getTitle(handle,platform):
	handle=handle.encode('utf8')
	All_handles=getAllHandles()
	return (All_handles[handle][0],All_handles[handle][1])

def getComparisons(handle,platform):
	handle=handle.encode('utf8')
	All_handles=getAllHandles()
	handles=All_handles
	# print All_handles.keys()
	output_handles={}
	for key in handles.keys():
		if key!=handle:
			output_handles[key]=handles[key];

	if platform=="twitter":
		return getTwitterTitles(handles)
	return sortHandles(output_handles)

def getKeywords(keyword):
	keywords=["worried","why","want","need","how can","where","fear","trouble","notice of","issue"]
	keywords.remove(keyword)
	return keywords

def getTwitterTitles(handles):
	output_handles={}
	for key in handles.keys():
		if handles[key][1]!="":
			output_handles[key]=handles[key];
	return sortHandles(output_handles)

def sortHandles(handles_dict):
	handles_list=[]
	for key in handles_dict.keys():
		datum={}
		datum["key"]=key
		datum["name"]=handles_dict[key][0]
		datum["tw_handle"]=handles_dict[key][1]
		datum["fb_id"]=handles_dict[key][2]
		handles_list.append(datum)

	sorted_handles_list = sorted(handles_list, key=lambda k: k['name'])

	return sorted_handles_list