# TCH Live Activity

## Dev

```
env FLASK_APP=api.py env FLASK_DEBUG=1 env API_KEYS=test flask run
```


## Usage

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

##### Bad Beat

Here is the URL you can use to display bad beat…

```
https://tch-activity.apps.sage-iq.com/hero-text?id=bad-beat
```

You can add the same way as the checkins URL and can also add an option font-size parameter, as well.

### Data API

`API_KEYS` environment varible is a comma-seperated list of API keys

#### Activity API

##### Endpoints

```
POST https://tch-activity.apps.sage-iq.com/data/north-austin
POST https://tch-activity.apps.sage-iq.com/data/south-austin
POST https://tch-activity.apps.sage-iq.com/data/houston
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
POST https://tch-activity.apps.sage-iq.com/data/houston-hours
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