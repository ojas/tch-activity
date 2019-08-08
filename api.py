import os
from flask import Flask, request, Response, jsonify, send_from_directory, render_template, abort
import pytz
import json
from datetime import datetime
import calendar
import time
from collections import namedtuple

API_KEYS = os.environ.get('API_KEYS', '').split(',')
MINS_IN_DAY = 24 * 60;
MINS_IN_WEEK = MINS_IN_DAY * 7

Event = namedtuple('Event', ['wt', 'open'])
EventWithIndex = namedtuple('EventWithIndex', ['idx', 'wt', 'open'])

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
    """Takes an hours object (from JSON) in, gives you an object that helps you determine if we're open at a given time"""
     
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
                    events.append(Event(day_open % MINS_IN_WEEK, True))

                if day_close is not None:
                    events.append(Event(day_close % MINS_IN_WEEK, False))

        # sort by time
        events = sorted(events, key=lambda x: x.wt)
        collapsed_events = []

        l = len(events)

        for idx, item in enumerate(events):
            prev_idx = (idx - 1) % l
            if idx == prev_idx:
                continue
            prev_item = events[prev_idx]
            if item.open == prev_item.open:
                continue
            collapsed_events.append(item)
                # collapsed_events

        self.events = collapsed_events

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

        # Get day [0,6], minutes into the day [0, 60*24)
        day_idx = weektime // MINS_IN_DAY
        time_of_day = weektime % MINS_IN_DAY

        # Get hours [0,23) and minutes [0,59)
        hh = time_of_day // 60
        mm = time_of_day % 60

        # PM is if hours >= noon (">" is incorrect)
        ampm = 'PM' if hh >= 12 else 'AM'

        # if hours > 12 (">=" is incorrect)
        if hh > 12: hh -= 12
    
        return day_idx, days[day_idx], simplify_time('%s:%0.2d %s' % (hh, mm, ampm))


    def get_open_info(self, austin_time):
        # build padded_events
        padded_events = [e for e in self.events]
        if len(padded_events) and padded_events[0].wt>0:
            padded_events.insert(0, Event(0, padded_events[-1][1]))

        padded_events_with_idx = [EventWithIndex(idx, e[0], e[1]) for idx, e in enumerate(padded_events)]

        l = len(padded_events_with_idx)

        def last(iter):
            return list(iter)[-1]

        def offset_events(offset):
            return [padded_events_with_idx[(idx+offset)%l] for idx, e in enumerate(padded_events_with_idx)]

        austin_dow = austin_time.weekday()
        week_time = (MINS_IN_DAY * ((austin_time.weekday()+1) % 7) + 60 * austin_time.hour + austin_time.minute) % MINS_IN_WEEK
        austin_day_of_week_name = calendar.day_name[austin_time.weekday()]

        curr = last(e for e in padded_events_with_idx if e.wt <= week_time)
        is_open_now = curr.open

        next_open_text_parts = []
        if is_open_now:
            pass
        else:
            # TS Open/Close next_idx
            up_next = offset_events(curr.idx+1)
            next_open_event = next(e for e in offset_events(curr.idx+1) if e.open)
            next_close_event = next(e for e in offset_events(next_open_event.idx+1) if not e.open)
            next_open_dow_idx, next_open_dow_name, next_open_time_friendly = BusinessHours.friendly_weektime(next_open_event.wt)

            if next_open_dow_name == austin_day_of_week_name:
                next_open_dow_name = 'Today'

            next_open_text_parts += [next_open_dow_name, next_open_time_friendly]

            next_close_dow_idx, next_close_dow_name, next_close_time_friendly = BusinessHours.friendly_weektime(next_close_event.wt)

            next_open_text_parts += ['-']

            if (next_close_dow_idx - next_open_dow_idx) % 7 != 1:
                next_open_text_parts += [next_close_dow_name]
            next_open_text_parts += [next_close_time_friendly]

        return is_open_now, ' '.join(next_open_text_parts)
        
def simplify_time(s):
    s = s.replace(' PM', 'p')
    s = s.replace(' AM', 'a')
    s = s.replace(':00', '')
    s = s.replace('0a', 'midnight')
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

    lines += ['Transitions']
    for idx, event in enumerate(bh.events):
        tt = BusinessHours.friendly_weektime(event.wt)
        lines += ['%2s %s at (%5s) %s %s' % (idx, 'Open ' if event.open else 'Close', event.wt, tt[1], tt[2])]

    lines += ['']

    for dow_idx, dow_symbol in enumerate('☉☾♂☿♃♀♄'):
        day_hours = hours[dow_idx]
        if len(lines):
            lines += ['']
        lines += ['%s %s' % (dow_symbol, day_hours["Day"])]

        for hour_of_day in range(0, 23):
            for min in range(0, 60, 30):
                austin_time = datetime(2019, 1, 6 + dow_idx, hour_of_day, min)
                is_open_now, next_open_time = bh.get_open_info(austin_time)

                lines += [ austin_time.strftime('%a %H:%M ') +
                    ('Open NOW' if is_open_now else 'Open ' + next_open_time.upper()) ]
    return '\n'.join(lines)

import unittest
class TestHours(unittest.TestCase):
    """Test open/closed hours

    We should show the number of check-ins when open, and diplay when we'll reopen if closed.
    get_open_info contains the interesting bits.

    Run tests via `python -m unittest api.TestHours`
    """

    def get_test_hours(self):
        # You can test your own JSON file via something like this:
        return json.load(open('data/my-site-hours.json'))

        # Or just test an inline JSON
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
    "Close": "4:00 AM"
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

        lf = '%-10s|%8s|%8s'
        print('## Hours')
        print()
        print(lf % ('Day', 'Open', 'Close'))
        print(lf % ('-'*10, '-'*8, '-'*8))
        for h in hours:
            print(lf % (h['Day'], h['Open'], h['Close']))

        bh = BusinessHours(hours)

        lf = '%-10s|%8s|%8s'
        print()
        print('## Events')
        print()
        print(lf % ('Day', 'Time', 'Open'))
        print(lf % ('-'*10, '-'*8, '-'*8))
        for ev in bh.events:
            idx, wn, t = bh.friendly_weektime(ev.wt)
            print(lf % (wn, t, ev.open))
        print()

        lf = '%-10s|%-45s'
        print()
        print('## Test Result')
        print()
        print(lf % ('Daytime', 'Status'))
        print(lf % ('-'*10, '-'*45))

        for dow_idx, dow_symbol in enumerate('☉☾♂☿♃♀♄'):
            day_hours = hours[dow_idx]
            for hour_of_day in range(0, 23):
                for minutes in range(0, 60, 30):
                    austin_time = datetime(2019, 1, 6 + dow_idx, hour_of_day, minutes)
                    is_open_now, next_open_time = bh.get_open_info(austin_time)

                    status = 'Open' if is_open_now else 'Closed. Re-opens ' + next_open_time

                    # print(austin_time.strftime('%a %H:%M '), end='')
                    print(lf % (austin_time.strftime('%a %H:%M '), status))

        self.assertEqual('foo'.upper(), 'FOO')
