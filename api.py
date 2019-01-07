import os
from flask import Flask, request, Response, jsonify, send_from_directory, render_template, abort
import pytz
import json
from datetime import datetime
import calendar
import time

API_KEYS = os.environ.get('API_KEYS', '').split(',')
MINS_IN_DAY = 24 * 60;
MINS_IN_WEEK = MINS_IN_DAY * 7


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

def get_open_times(hours):

    def get_weektime(day_of_week, time_str):
        time_str = time_str.strip().upper().replace(' ', '')
        if time_str:
            t = time.strptime(time_str, "%I:%M%p")
            return (MINS_IN_DAY * day_of_week + 60 * t.tm_hour + t.tm_min) % MINS_IN_WEEK
        return None

    open_times = []

    last_open_time = None

    for day_of_week, biz_hours in enumerate(hours):
        day_open = get_weektime(day_of_week, biz_hours['Open'])
        day_close = get_weektime(day_of_week, biz_hours['Close'])

        if day_close is not None and day_open is not None and day_close < day_open:
            day_close += MINS_IN_DAY
            # or do we and two items? til mid


        # if day_open is not None and day_close is not None:
        if day_open is not None or day_close is not None:
            open_times.append([day_open, day_close, biz_hours, ''])

    l = len(open_times)

    for idx, item in enumerate(open_times):
        prev_item = open_times[(idx-1)%l]
        next_item = open_times[(idx+1)%l]

        # there's an open event and no close event from yday
        if item[0] is not None and prev_item[1] is None:
            # there's a close time for today...
            if item[1] is not None:
                prev_item[1] = item[1]
                # print('closing 1', item[2])
                # item[2] = None
                item[3] = '🚫 closing time exists, prev %s' % prev_item
            else:
                # otherwise, today's open event is extraneous
                item[3] = '🚫 extraneous'
                # item[2] = None

        # if item[1] is None:
        #     if next_item[1] is not None:
        #         item[1] = next_item[1]
        #         # next_item[2] = None
        #     else:
        #         item[1] = next_item[0] # better than nothing?

    # pprint(open_times)

    # open_times = [o for o in open_times if o[2] is not None]
        # if item[0] is None:
        #     item[0] = prev_item[0] # midnight prior?
        #     # find next closing time
        #
        # print('x', item, prev_item)

    # sun_ot, sat_ot = open_times[0], open_times[6]
    # for day_of_week in range(6, -1, -1):
    #
    #     print(day_of_week)

    return open_times

class BusinessHours:
    def __init__(self, hours):
        def get_weektime(day_of_week, time_str):
            time_str = time_str.strip().upper().replace(' ', '')
            if time_str:
                t = time.strptime(time_str, "%I:%M%p")
                return (MINS_IN_DAY * day_of_week + 60 * t.tm_hour + t.tm_min) % MINS_IN_WEEK
            return None

        events = []
        for day_of_week, biz_hours in enumerate(hours):
            day_open = get_weektime(day_of_week, biz_hours['Open'])
            day_close = get_weektime(day_of_week, biz_hours['Close'])

            if day_open is not None:
                events.append((day_open, True))

            if day_close is not None:
                if day_open is not None and day_close < day_open:
                    day_close += MINS_IN_DAY
                events.append((day_close, False))

        # sort by time, then open followed by close
        events = sorted(events, key=lambda x: x[0]+(not x[1]))

        # pad beginning as needed
        if len(events) and events[0][0]>0:
            events.insert(0, (0, events[-1][1]))

        self.events = events

    def find(self, **kwargs):
        gte = kwargs.get('gte')
        ge = kwargs.get('gt')
        open = kwargs.get('open')
        close = kwargs.get('close')

        for idx, ds in enumerate(bh.events):
            if ds[0]<=week_time:
                event_idx = idx
            else:
                break

        print(last_item)

        return -1

    # l = len(events)
    # if l:
    #     if events[0][0] != 0:
    #         events.insert(0, (0, events[]))
    # print(events)
    # exit()
    # l = len(open_times)
    #
    # for idx, item in enumerate(open_times):
    #     prev_item = open_times[(idx-1)%l]
    #     next_item = open_times[(idx+1)%l]
    #
    #     # there's an open event and no close event from yday
    #     if item[0] is not None and prev_item[1] is None:
    #         # there's a close time for today...
    #         if item[1] is not None:
    #             prev_item[1] = item[1]
    #             # print('closing 1', item[2])
    #             # item[2] = None
    #             item[3] = '🚫 closing time exists, prev %s' % prev_item
    #         else:
    #             # otherwise, today's open event is extraneous
    #             item[3] = '🚫 extraneous'
    #             # item[2] = None
    #
    #     # if item[1] is None:
    #     #     if next_item[1] is not None:
    #     #         item[1] = next_item[1]
    #     #         # next_item[2] = None
    #     #     else:
    #     #         item[1] = next_item[0] # better than nothing?
    #
    # # pprint(open_times)
    #
    # # open_times = [o for o in open_times if o[2] is not None]
    #     # if item[0] is None:
    #     #     item[0] = prev_item[0] # midnight prior?
    #     #     # find next closing time
    #     #
    #     # print('x', item, prev_item)
    #
    # # sun_ot, sat_ot = open_times[0], open_times[6]
    # # for day_of_week in range(6, -1, -1):
    # #
    # #     print(day_of_week)
    #
    # return open_times

def open_info_2(hours, austin_time):
    day_of_week_name = calendar.day_name[austin_time.weekday()]

    the_day = None
    for day_hour in hours:
        if day_of_week_name == day_hour['Day']:
            the_day = day_hour
            break

    bh = BusinessHours(hours)
    # Note: austin_time.weekday() means 0 = Monday
    # We need to convert to 0 = Sunday hence the (austin_time.weekday()+1) % 7
    week_time = (MINS_IN_DAY * ((austin_time.weekday()+1) % 7) + 60 * austin_time.hour + austin_time.minute) % MINS_IN_WEEK

    # find item in open_times where ts >= week_time and

    last_item = None
    event_idx = None





    for idx, ds in enumerate(bh.events):
        # print(ds, week_time)
        if ds[0]<=week_time:
            event_idx = idx
        else:
            break

    print(last_item)
    exit()
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

def open_info(hours, austin_time):

    def within(val, nmin, nmax):
        if nmax<nmin:
            return val >= nmin or val <= nmax
        return val >= nmin and val <= nmax


    day_of_week_name = calendar.day_name[austin_time.weekday()]

    the_day = None
    for day_hour in hours:
        if day_of_week_name == day_hour['Day']:
            the_day = day_hour
            break

    open_times = get_open_times(hours)
    # Note: austin_time.weekday() means 0 = Monday
    # We need to convert to 0 = Sunday hence the (austin_time.weekday()+1) % 7
    week_time = (MINS_IN_DAY * ((austin_time.weekday()+1) % 7) + 60 * austin_time.hour + austin_time.minute) % MINS_IN_WEEK

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
    hours = obj_data('north-austin-hours')
    austin_time = datetime.now(tz=pytz.timezone('America/Chicago'))
    is_open_now, next_open_time = open_info(hours, austin_time)
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

    is_open_now, next_open_time = open_info(hours, datetime.now(tz=pytz.timezone('America/Chicago')))
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

import unittest
class TestHours(unittest.TestCase):

    def get_test_hours(self):
        return json.loads("""
[
  {
    "Day": "Sunday",
    "Open": "",
    "Close": ""
  },
  {
    "Day": "Monday",
    "Open": "6:00 PM",
    "Close": "3:00 AM"
  },
  {
    "Day": "Tuesday",
    "Open": "6:00 PM",
    "Close": "3:00 AM"
  },
  {
    "Day": "Wednesday",
    "Open": "6:00 PM",
    "Close": "3:00 AM"
  },
  {
    "Day": "Thursday",
    "Open": "6:00 PM",
    "Close": ""
  },
  {
    "Day": "Friday",
    "Open": "4:00 PM",
    "Close": "4:00 AM"
  },
  {
    "Day": "Saturday",
    "Open": "4:00 PM",
    "Close": "4:00 PM"
  }
]
        """)

    def test_sort_of(self):

        DAYS_OF_WEEK_SURPRISE = """
Day | Planet  | Irregs            |
--- | ------- | ----------------- |
Sun | Sun     | Sōl, Helios       | ☉ |
Mon | Moon    | Luna, Selene      | ☾ |
Tue | Mars    | Mars, Ares        | ♂ | Ma  | Fe - Iron |
Wed | Mercury | Mercurius, Hermes | ☿ | Me  |
Thu | Jupiter | Iuppiter, Zeus    | ♃ |
Fri | Venus   | Venus, Aphrodite  | ♀ | V   |
Sat | Saturn  | Saturnus, Kronos  | ♄ |
        """
        # https://en.wikipedia.org/wiki/Planet_symbols

        hours = self.get_test_hours()

        bh = BusinessHours(hours)


        # self.assertEqual(4, len(open_times), 'open times - four days')

        print(json.dumps(bh.events, indent=2))
        exit()

        for dow_idx, dow_symbol in enumerate('☉☾♂☿♃♀♄'):
            day_hours = hours[dow_idx]
            print(f'{dow_symbol} {day_hours["Day"]}' )

            for hour_of_day in range(0, 23):
                for min in range(0, 60, 30):
                    austin_time = datetime(2019, 1, 6 + dow_idx, hour_of_day, min) #,tz=pytz.timezone('America/Chicago')
                    is_open_now, next_open_time = open_info_2(hours, austin_time)

                    print(austin_time.strftime('%H:%M '), end='')
                    if is_open_now:
                        print('Open.')
                    else:
                        print(f'Closed. Re-opens {next_open_time["Day"]} {next_open_time["Open"]} - {next_open_time["Close"]}')

        self.assertEqual('foo'.upper(), 'FOO')
