import requests
import json
from urllib import urlencode
from json_parser import updateBulkSentimentRecord


def getSentiment(posts):

	print 'datadsfasfafsdfas'
	api_url = 'http://www.sentiment140.com/api/bulkClassifyJson?'+urlencode({'appid': 'yatharth.sharma@gmail.com'})

	payload  = {'data': []}
	for data in posts:
		payload['data'].append({
							'localid': str(data['localid']),
							'text': str(data['message'].encode('utf-8'))
						})
	r = requests.post(api_url, data = json.dumps(payload))
	results = r.json()



	updateBulkSentimentRecord(results)





