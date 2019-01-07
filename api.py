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

class BusinessHours:
    def __init__(self, hours):
        events = []
        for day_of_week, biz_hours in enumerate(hours):
            day_open = BusinessHours.get_weektime(day_of_week, biz_hours['Open'])
            day_close = BusinessHours.get_weektime(day_of_week, biz_hours['Close'])

            if day_close is not None:
                if day_open is not None and day_close < day_open:
                    day_close += MINS_IN_DAY

            if day_open != day_close: # open and closing at the same time makes no sense
                if day_open is not None:
                    events.append([day_open, True])

                if day_close is not None:
                    events.append([day_close, False])

        # sort by time, then open followed by close
        events = sorted(events, key=lambda x: x[0])

        l = len(events)
        if l:
            # pad beginning as needed
            if events[0][0]>0:
                # for idx in range(l-1, -1, -1):
                #     if
                # exit()
                # # TODO: events[-1][1] isn't right...
                events.insert(0, [0, events[-1][1]])

            l = len(events)
            # link them
            events = [
                [idx] + parts + [(idx + 1) % l]
                for idx, parts in enumerate(events)
            ]

        self.events = events

    @classmethod
    def get_weektime(cls, day_of_week, time_str):
        time_str = time_str.strip().upper().replace(' ', '')
        if time_str:
            t = time.strptime(time_str, "%I:%M%p")
            return (MINS_IN_DAY * day_of_week + 60 * t.tm_hour + t.tm_min) % MINS_IN_WEEK
        return None

    @classmethod
    def friendly_weektime(cls, weektime):
        days=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        day_idx = weektime // MINS_IN_DAY
        time_of_day = weektime % MINS_IN_DAY
        hh = time_of_day // 60
        mm = time_of_day % 60
        ampm = 'PM' if hh > 12 else 'AM'
        if hh > 12: hh -= 12
        return day_idx, days[day_idx], simplify_time('%0.2d:%0.2d %s' % (hh, mm, ampm))


    def get_open_info(self, austin_time):
        def last(iter):
            return list(iter)[-1]

        def offset_events(offset):
            l = len(self.events)
            return [self.events[(idx+offset)%l] for idx, e in enumerate(self.events)]

        l = len(self.events)

        austin_dow = austin_time.weekday()
        week_time = (MINS_IN_DAY * ((austin_time.weekday()+1) % 7) + 60 * austin_time.hour + austin_time.minute) % MINS_IN_WEEK


        curr = last(e for e in self.events if e[1] <= week_time)
        is_open_now = curr[2]

        next_open_text_parts = []
        if is_open_now:
            pass
        else:
            # TS Open/Close next_idx
            up_next = offset_events(curr[0]+1)
            next_open = next(e for e in offset_events(curr[0]+1) if e[2])
            next_close = next(e for e in offset_events(next_open[0]+1) if not e[2])

            open_dow, open_day, open_time = BusinessHours.friendly_weektime(next_open[1])

            if open_dow == austin_dow:
                open_day = 'Today'

            next_open_text_parts += [open_day, open_time]

            close_dow, close_day, close_time = BusinessHours.friendly_weektime(next_close[1])

            next_open_text_parts += ['-']

            if (close_dow - open_dow) % 7 != 1:
                next_open_text_parts += [close_day]
            next_open_text_parts += [close_time]

        return is_open_now, ' '.join(next_open_text_parts)

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

@app.route("/dump-week")
def dump_week():
    location = request.args.get('location', 'north-austin')
    hours = obj_data('%s-hours' % location)

    austin_time = datetime.now(tz=pytz.timezone('America/Chicago'))

    bh = BusinessHours(hours)
    is_open_now, next_open_time = bh.get_open_info(austin_time)

    return Response(dump_info(hours, bh), mimetype='text/plain')

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

    bh = BusinessHours(hours)
    is_open_now, next_open_time = bh.get_open_info(austin_time)

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

def dump_info(hours, bh):
    lines = []

    for dow_idx, dow_symbol in enumerate('☉☾♂☿♃♀♄'):
        day_hours = hours[dow_idx]
        lines += ['%s %s' % (dow_symbol, day_hours["Day"])]

        for hour_of_day in range(0, 23):
            for min in range(0, 60, 30):
                austin_time = datetime(2019, 1, 6 + dow_idx, hour_of_day, min)
                is_open_now, next_open_time = bh.get_open_info(austin_time)

                lines += [ austin_time.strftime('%a %H:%M ') +
                    ('Open.' if is_open_now else 'Closed. Re-opens ' + next_open_time) ]
    return '\n'.join(lines)

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
    "Open": "4:15 PM",
    "Close": "4:30 AM"
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

        print(json.dumps(bh.events, indent=2))

        for dow_idx, dow_symbol in enumerate('☉☾♂☿♃♀♄'):
            day_hours = hours[dow_idx]
            print('%s %s' % (dow_symbol, day_hours["Day"]) )

            for hour_of_day in range(0, 23):
                for min in range(0, 60, 30):
                    austin_time = datetime(2019, 1, 6 + dow_idx, hour_of_day, min)
                    is_open_now, next_open_time = bh.get_open_info(austin_time)

                    print(austin_time.strftime('%a %H:%M '), end='')
                    if is_open_now:
                        print('Open.')
                    else:
                        print('Closed. Re-opens ' + next_open_time)

        self.assertEqual('foo'.upper(), 'FOO')
