# TCH Live Activity

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


Endpoints

```
POST https://tch-activity.apps.sage-iq.com/data/north-austin
POST https://tch-activity.apps.sage-iq.com/data/south-austin
```

Headers:

```
Api-Key: test123
Content-Type: application/json
```

Body (JSON):

```
{
  "checkins" : 123
}
```

Examples

Set north location to 42 checkins…

```
curl \
    -H 'Api-Key: test123' \
    -H 'Content-Type: application/json' \
    --data '{"checkins": 42}' \
    http://localhost:5000/data/north-austin
```

Set south location to 56 checkins…

```
curl \
    -H 'Api-Key: test123' \
    -H 'Content-Type: application/json' \
    --data '{"checkins": 56}' \
    http://localhost:5000/data/south-austin
```