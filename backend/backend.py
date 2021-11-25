from flask import Flask
from flask import request
from flask import Response
from flask.json import jsonify
import torch

import json

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS, cross_origin
# app = Flask(__name__)
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('bert-base-nli-mean-tokens')

# Only for testing purposes
dummyresponse = {
    "labels": [
        {
            "index": "1",
            "labels": []
        },
        {
            "index": "3",
            "labels": [
                12,
                10,
                2
            ]
        },
        {
            "index": "5",
            "labels": []
        },
        {
            "index": "7",
            "labels": [
                6,
                13,
                14
            ]
        },
        {
            "index": "9",
            "labels": [
                18
            ]
        },
        {
            "index": "11",
            "labels": [
                2
            ]
        },
        {
            "index": "13",
            "labels": [
                7,
                9
            ]
        },
        {
            "index": "15",
            "labels": [
                21,
                5,
                3
            ]
        },
        {
            "index": "17",
            "labels": []
        },
        {
            "index": "19",
            "labels": [
                2,
                10
            ]
        },
        {
            "index": "21",
            "labels": [
                12,
                2,
                10
            ]
        },
        {
            "index": "23",
            "labels": []
        },
        {
            "index": "25",
            "labels": []
        },
        {
            "index": "27",
            "labels": []
        },
        {
            "index": "29",
            "labels": []
        },
        {
            "index": "31",
            "labels": [
                1,
                9,
                18
            ]
        },
        {
            "index": "33",
            "labels": [
                9,
                10,
                2
            ]
        },
        {
            "index": "35",
            "labels": [
                21,
                4,
                11
            ]
        },
        {
            "index": "37",
            "labels": [
                15
            ]
        },
        {
            "index": "39",
            "labels": [
                5,
                12
            ]
        },
        {
            "index": "41",
            "labels": [
                15
            ]
        },
        {
            "index": "43",
            "labels": [
                15
            ]
        },
        {
            "index": "45",
            "labels": []
        },
        {
            "index": "47",
            "labels": [
                0
            ]
        },
        {
            "index": "49",
            "labels": [
                2
            ]
        }
    ]
}

epDescHash = {
    0: 'Provide a dark UI color theme on devices with AMOLED screens.',
    1: 'Whenever an attempt to access a resource has failed, increase the interval of time waited before asking access to that same resource.',
    2: 'Avoid performing tasks that are not visible/valuable to the user and/or quickly become obsolete',
    3: 'Release resources or services as soon as possible',
    4: 'Open/start resources/services only when they are strictly necessary',
    5: 'Use push notifications to receive updates from resources, instead of actively querying resources',
    6: 'Provide an energy efficient mode in which user experience can drop for the sake of better energy usage',
    7: 'Have a different behavior when device is connected/disconnected to a power station, or has different battery levels',
    8: 'When transmitting data, reduce its size as much as possible',
    9: 'Delay or disable heavy data connections until the device is connected to a WiFi network',
    10: 'Avoid using intensive logging',
    11: 'Batch multiple operations instead of putting the device into an active state many times',
    12: 'Avoid performing unnecessary operations by using cache mechanisms',
    13: 'Increase time between syncs/sensor reads as much as possible',
    14: 'Allow users to enable/disable certain features in order to save energy',
    15: 'Let the user know if the app is doing any battery intensive operation',
    16: 'Collect or provide high accuracy data only when strictly necessary',
    17: 'Use data from low power sensors to infer whether new data needs to be collected from high power sensors',
    18: 'Kill abnormal tasks. Provide means of interrupting energy greedy operations',
    19: 'Whenever possible allow interaction without using the display',
    20: 'Graphics and animations are really important to improve user experience. However, they can also be battery intensive – use them with moderation',
    21: 'Perform tasks only when the user specifically asks'
}

list_of_eps = []
for ep in epDescHash:
  list_of_eps.append(epDescHash[ep])

ep_embeddings = model.encode(list_of_eps)

def label_issue(issue_title):
    labels = []
    cs  = cosine_similarity([model.encode(issue_title['text'])], ep_embeddings)[0]
    top3eps = np.argsort(cs)[-3:]
    for p in top3eps:
        if(cs[p] >= 0.55):
            labels.append(int(p))
    return labels

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origin": "*"}})
CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
# CORS(app, resources={r"*": {"origins": "*"}})

# @app.after_request
# def after_request(response):
#   response.headers.add('Access-Control-Allow-Origin', '*')
#   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#   response.headers.add('Access-Control-Allow-Credentials', 'true')
#   response.headers.add("Access-Control-Allow-Headers", "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers");

#   return response

@app.route("/", methods=["POST"])
@cross_origin()
def home():
    if not 'items' in request.json:
        return "no data"
    labels = []
    for issue in request.json['items']:
        labels.append({ 
            "index": issue['index'],
            "labels": label_issue(issue_title=issue)
            })
    return Response(json.dumps({
        "labels": labels
    }), mimetype='application/json')

    # return Response(json.dumps(dummyresponse, mimetype='application/json'))
    
if __name__ == "__main__":
    app.run(debug=True)