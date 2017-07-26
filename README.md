# TCH Live Activity


Just here are the URLs you can use to display current activity…

```
https://tch-activity.apps.sage-iq.com/activity-text?location=north-austin
https://tch-activity.apps.sage-iq.com/activity-text?location=south-austin
```

In the Wix editor:

1. Add an "Embed a Site" element to the page (Add > More > HTML & Flash)
2. Press the Gear icon
3. Enter one of the addresses above


You can change font-size like this:

```
https://tch-activity.apps.sage-iq.com/activity-text?location=north-austin&font-size=24
https://tch-activity.apps.sage-iq.com/activity-text?location=north-austin&font-size=12
```

Note: You can open the URLs in your browser - it's just a normal HTML page. However, because the background is transparent and the font is white, the text probably won't be visible. You can do a select all (Ctrl+A or Command+A) to see it.

The text is displayed formats like this…

- 42 Players Checked-In Right Now
- Open Right Now *(if checkins for the given location is null)*
- Open Friday 6:00 PM - 3:00 AM





###

```
set -x API_KEYS test123


flask run

set -x API_KEYS test123



export API_KEYS=test123
export FLASK_DEBUG=1
export FLASK_APP=api.py
flask run
```

- Go to <https://docs.google.com/spreadsheets/> and create a google sheet with two sheets.
- First one named "Activity" and two columns "Players" and "Games"
- Second one named "Hours" and three columns "Day", "Open", and "Close" and seven rows under Days (Sunday ~ Saturday)
- Do File > Publish to Web (Entire Document, As Web Page), copy the URL (eg https://docs.google.com/spreadsheets/d/1oXieCimzK5EL__6G-BgODD9QsDHuCPbMdafSA_Gl67c/pubhtml)
- Notice URL. The part after `spreadsheets/d/` and before `/pubhtml` is the SPREADSHEET_ID which you'll use in the embed code… 
- Embed in your web page by adding this code…

```
<div id="activityContainer">
</div>
<script src="https://rawcdn.githack.com/ojas/tch-activity/master/tch.js"></script>
<script type='text/javascript'>
	TCH.renderActivity('SPREADSHEET_ID', 'activityContainer')
</script>
```

Example for TCH - North Austin

```
<div id="activityContainerNorth">
</div>
<script src="https://rawcdn.githack.com/ojas/tch-activity/master/tch.js"></script>
<script type='text/javascript'>
	TCH.renderActivity('1oXieCimzK5EL__6G-BgODD9QsDHuCPbMdafSA_Gl67c', 'activityContainerNorth')
</script>
```

Example for TCH - South Austin

```
<div id="activityContainerSouth">
</div>
<script src="https://rawcdn.githack.com/ojas/tch-activity/master/tch.js"></script>
<script type='text/javascript'>
	TCH.renderActivity('1Whjm-QWr3s2xpgoPHJtIVkEUDxyKVNTHtjt66scnhTs', 'activityContainerSouth')
</script>
```

### Data API

`API_KEYS` environment varible is a comma-seperated list of API keys

#### Activity API

##### Endpoints

```
POST https://tch-activity.apps.sage-iq.com/data/north-austin
POST https://tch-activity.apps.sage-iq.com/data/south-austin
```

##### Headers:

```
Api-Key: <YOUR API KEY>
Content-Type: application/json
```

##### Body (JSON):

```
{
  "checkins" : 123
}
```

##### Examples

Set north location to 42 checkins…

```
curl \
    -H 'Api-Key: <YOUR API KEY>' \
    -H 'Content-Type: application/json' \
    --data '{"checkins": 42}' \
    https://tch-activity.apps.sage-iq.com/data/north-austin
```

Set south location to unknown/null checkins…

```
curl \
    -H 'Api-Key: <YOUR API KEY>' \
    -H 'Content-Type: application/json' \
    --data '{"checkins": null}' \
    https://tch-activity.apps.sage-iq.com/data/south-austin
```



#### Location Hours API

##### Endpoints

```
POST https://tch-activity.apps.sage-iq.com/data/north-austin-hours
POST https://tch-activity.apps.sage-iq.com/data/south-austin-hours
```

##### Headers:

```
Api-Key: <YOUR API KEY>
Content-Type: application/json
```

##### Body (JSON):

See examples below.

##### Examples

Set north location to hours…

```
curl \
    -H 'Api-Key: <YOUR API KEY>' \
    -H 'Content-Type: application/json' \
    --data '
[
  {
    "Day": "Sunday",
    "Open": "2:30 PM",
    "Close": "11:59 PM"
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
    "Close": "4:00 AM"
  },
  {
    "Day": "Friday",
    "Open": "4:00 PM",
    "Close": "4:00 AM"
  },
  {
    "Day": "Saturday",
    "Open": "4:00 PM",
    "Close": "4:00 AM"
  }
]' https://tch-activity.apps.sage-iq.com/data/north-austin-hours
```

Set south location to hours…

```
curl \
    -H 'Api-Key: <YOUR API KEY>' \
    -H 'Content-Type: application/json' \
    --data '
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
    "Close": "3:00 AM"
  },
  {
    "Day": "Friday",
    "Open": "4:00 PM",
    "Close": "4:00 AM"
  },
  {
    "Day": "Saturday",
    "Open": "4:00 PM",
    "Close": "4:00 AM"
  }
]' https://tch-activity.apps.sage-iq.com/data/south-austin-hours
```


#### Bad Beat API

##### Endpoints

```
POST https://tch-activity.apps.sage-iq.com/data/bad-beat
```

##### Headers:

```
Api-Key: <YOUR API KEY>
Content-Type: application/json
```

##### Body (JSON):

```
"$1,000,000 dollars"
```

##### Examples

Set bad beat text to 1 million dollars…

```
curl \
    -H 'Api-Key: <YOUR API KEY>' \
    -H 'Content-Type: application/json' \
    --data '"$1,000,000 dollars"' \
    https://tch-activity.apps.sage-iq.com/data/bad-beat
```