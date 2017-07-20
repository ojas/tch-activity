import os
from flask import Flask, request, Response, jsonify
import json

API_KEYS = os.environ.get('API_KEYS', '').split(',') 

app = Flask(__name__)

def add_cors(request, resp):
    headers = {
        'Access-Control-Allow-Origin': '*', #request.environ.get('HTTP_HOST', '*'),
        'Access-Control-Request-Method:' : 'GET',
        'Access-Control-Allow-Headers': 'Host, Origin, X-Requested-With, Content-Type, Accept, apikey',
    }
    for k, v in headers.items():
        resp.headers[k] = v

@app.route("/")
def hello():
    return "no peeking"

@app.route("/data/<id>", methods=['POST', 'GET'])
def data_endpoint(id):

    id = id.replace('/', '-').replace('.', '-')

    filename = 'data/%s.json' % id

    if request.method == 'POST':
        if request.headers.get('api-key') not in API_KEYS:
            return Response(json.dumps({'message' : 'access denied'}), status=403, mimetype='application/json', )

        o = request.json

        with open(filename, 'w') as f:
            json.dump(o, f)

    with open(filename, 'r') as f:
        o = json.load(f)

    resp = Response(json.dumps(o), status=200, mimetype='application/json', )
    add_cors(request, resp)
    return resp
