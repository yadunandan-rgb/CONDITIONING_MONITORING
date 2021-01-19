from flask import Flask
from flask import request
import json
import traceback
from waitress import serve
from flask import Flask, jsonify, request
import requests
import os


app = Flask(__name__)

# accelerometer horizont and vertical, fft horizontal, max rpm
# no of samples, sampling_frequency, 

DIR = os.path.dirname(__file__)
if not DIR:
	FILE_PATH = "Config1.json"
else:
	FILE_PATH = DIR + "/Config1.json"

with open(FILE_PATH, 'r') as readfile:
	json_dict = json.load(readfile)

inputs = [
    {
        "UniqueName" : "Main_tags",
        "UniqueId" : "U100",
        "Key" : "Horizontal",
        "Tags":["for_phase_accel_Horizon","fft_data"],
        "Version" : 0
    },
    {
        "UniqueName" : "Main_tags",
        "UniqueId" : "U100",
        "Key" : "Vertical",
        "Tags":["for_phase_accel_verti"],
        "Version" : 0
    }
]


@app.route("/tagsGet", methods=["GET"])
def get_tasks():
    metaDataApi = requests.post(json_dict['request_url'], json=json_dict['posting_data'])
    data = metaDataApi.text
    jsonData = []
    for post in data:
        jsonData.append(post)
    jsonData = jsonify(data)
    inputs.append(data)
    print(jsonData)  
    # return jsonData

    return jsonify({"inputs": inputs})

@app.route("/InputTags", methods=["POST"])
def create_task():
    # if not request.json or not "title" in request.json:
    #     abort(400)
    task = {
        # "id": tasks[-1]["id"] + 1,
        "UniqueName": request.json["UniqueName"],
        "UniqueId": request.json["UniqueId"],
        "Key": [],
        "Tag": [],
        "Version": 0
        # "description": request.json.get("description", ""),
        # "done": False
    }

    inputs.append(task)
    # tasks.append(request.get_json())
    return jsonify({"inputs": inputs})



serve(app, host='192.168.43.25', port=3000)










