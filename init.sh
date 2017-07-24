#!/bin/bash

curl \
    -H 'Api-Key: test123' \
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
]' http://localhost:5000/data/north-austin-hours


curl \
    -H 'Api-Key: test123' \
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
]' http://localhost:5000/data/north-austin-hours