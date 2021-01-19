import requests as req
import json
import os


DIR = os.path.dirname(__file__)
if not DIR:
	FILE_PATH = "Config.json"
else:
	FILE_PATH = DIR + "/Config.json"


with open(FILE_PATH, 'r') as readfile:
	json_dict = json.load(readfile)

id
class equipment():
    def __init__(self, name="", id="", key=None, tag=None, version=0):
        self.UniqueName =  name
		self.UniqueId =  
		self.key = key
		self.tag = tag
		self.version = 0
		self.json_dict = ""
		self.url= ""
		self.api_post_data = {}
		self.api_object = ""
