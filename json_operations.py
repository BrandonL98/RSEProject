import json
from collections import OrderedDict

def writeToJSONFile(path, data):
	url = './' + path + '.json'
	with open(url, 'w') as fp:
		json.dump(data,fp, indent=4)

	# USAGE:
	# data = {}
	# data['james'] = 'visitor'

	# writeToJSONFile(data)

def readFromJSONFile(path):
	url = './' + path + '.json'
	with open(url) as json_file:
		record = json.load(json_file, object_pairs_hook=OrderedDict)
	
	return record