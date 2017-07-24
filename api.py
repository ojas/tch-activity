import os
from flask import Flask, request, Response, jsonify, send_from_directory, render_template, abort
import pytz
import json

API_KEYS = os.environ.get('API_KEYS', '').split(',') 

app = Flask(__name__)

def obj_data(id, *args):
    id = id.replace('/', '-').replace('.', '-')
    filename = 'data/%s.json' % id

    if len(args):
        o = args[0]
        with open(filename, 'w') as f:
            json.dump(o, f)
    else:
        try:
            with open(filename, 'r') as f:
                o = json.load(f)
        except FileNotFoundError:
            abort(404) 
    return o

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

@app.route("/now")
def now():
    from datetime import datetime
    austin_time = datetime.now(tz=pytz.timezone('America/Chicago'))
    return "%s" % austin_time

@app.route("/button")
def button():
    from datetime import datetime
    austin_time = datetime.now(tz=pytz.timezone('America/Chicago'))
    print(austin_time)
    location = request.args.get('location')
    activity = obj_data('north-austin')
    hours = obj_data('north-austin-hours')

    # for tz in pytz.all_timezones:
    #     print(tz)

    # obj_data
    return render_template('button.html', activity=activity, hours=hours)


# @app.route('/static/<path:path>')
# def static(path):
#     return send_from_directory('static', path)

@app.route("/data/<id>", methods=['POST', 'GET'])
def data_endpoint(id):


    if request.method == 'POST':
        if request.headers.get('api-key') not in API_KEYS:
            return Response(json.dumps({'message' : 'access denied'}), status=403, mimetype='application/json', )

        o = request.json

        obj_data(id, o)

    o = obj_data(id)

    resp = Response(json.dumps(o), status=200, mimetype='application/json', )
    add_cors(request, resp)
    return resp
