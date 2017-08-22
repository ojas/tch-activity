import os
from flask import Flask, request, Response, jsonify, send_from_directory, render_template, abort
import pytz
import json
from datetime import datetime

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

def open_info(hours):
    import calendar
    import time
    from datetime import datetime

    mins_in_day = 24 * 60;
    mins_in_week = mins_in_day * 7

    def get_minute_value(time_str):
        time_str = time_str.strip().upper().replace(' ', '')
        if time_str:
            t = time.strptime(time_str, "%I:%M%p")
            return 60 * t.tm_hour + t.tm_min
        return None

    def get_open_times():
        open_times = []
        for day_of_week, biz_hours in enumerate(hours):
            day_open = get_minute_value(biz_hours['Open'])
            day_close = get_minute_value(biz_hours['Close'])
            if day_open is not None and day_close is not None:
                if day_close < day_open:
                    day_close += mins_in_day
                open_times.append([
                    (mins_in_day * day_of_week + day_open) % mins_in_week,
                    (mins_in_day * day_of_week + day_close) % mins_in_week,
                    biz_hours
                    ])
        return open_times

    def within(val, nmin, nmax):
        if nmax<nmin:
            return val >= nmin or val <= nmax
        return val >= nmin and val <= nmax

    austin_time = datetime.now(tz=pytz.timezone('America/Chicago'))
    day_of_week_name = calendar.day_name[austin_time.weekday()]


    the_day = None
    for day_hour in hours:
        if day_of_week_name == day_hour['Day']:
            the_day = day_hour
            break

    open_times = get_open_times()
    # Note: austin_time.weekday() means 0 = Monday
    # We need to convert to 0 = Sunday hence the (austin_time.weekday()+1) % 7
    week_time = (mins_in_day * ((austin_time.weekday()+1) % 7) + 60 * austin_time.hour + austin_time.minute) % mins_in_week

    open_now = False
    next_open_time = None

    for day_open, day_close, day_open_info in open_times:
#        print(day_open, day_close, day_open_info)
        if next_open_time is None and day_open >= week_time:
            next_open_time = day_open_info
        if within(week_time, day_open, day_close):
            open_now = True

    if next_open_time is None:
        next_open_time = open_times[0][2]

    if next_open_time['Day'] == day_of_week_name:
        next_open_time['Day'] = 'Today'
    return open_now, next_open_time

def simplify_time(s):
    s = s.replace(' PM', 'p')
    s = s.replace(' AM', 'a')
    s = s.replace(':00', '')
    return s

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
    austin_time = datetime.now(tz=pytz.timezone('America/Chicago'))

    hours = obj_data('north-austin-hours')
    is_open_now, next_open_time = open_info(hours)
    return "%s\n\n<br>%s<br>%s" % (austin_time, is_open_now, next_open_time)

    return "%s" % austin_time


@app.route("/hero-text")
def hero_text():
    id = request.args.get('id')
    font_size = request.args.get('font-size', '10')
    try:
        font_size = int(font_size)
    except ValueError:
        pass

    text = obj_data('%s' % id)

    return render_template('hero.html',
        font_size=font_size,
        text=text,
        )
@app.route("/activity-text")
def activity():
    location = request.args.get('location')
    font_size = request.args.get('font-size', '10')
    try:
        font_size = int(font_size)
    except ValueError:
        pass

    activity = obj_data('%s' % location)
    hours = obj_data('%s-hours' % location)

    austin_time = datetime.now(tz=pytz.timezone('America/Chicago'))

    is_open_now, next_open_time = open_info(hours)
    next_open_time['Open'] = simplify_time(next_open_time['Open'])
    next_open_time['Close'] = simplify_time(next_open_time['Close'])

    return render_template('activity.html',
        activity=activity,
        hours=hours,
        is_open_now=is_open_now,
        next_open_time=next_open_time,
        font_size=font_size,
        )

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

@app.route("/admin")
def admin():
    api_key = request.args.get('api-key')
    return render_template('admin.html',
        api_key=api_key
        )
