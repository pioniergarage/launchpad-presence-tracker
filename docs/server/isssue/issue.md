# Presence Tracker System

## Requirements

+ Users should be able to
  + register their devices with their MAC addresses and
  + delete registered devices.
+ The presence of a user is concluded by the activity of its devices.
+ The analyses of the aggregated presence by time and weekday should be possible.

## Objects

![diagram](https://cloud.githubusercontent.com/assets/13613870/20796296/e269a156-b7d5-11e6-8c57-58a61895438c.png)

+ **User**: a person using the system. Connected to a slack account.
+ **Team**: several users are in a team.
+ **Presence**: a period a user is present at the launchpad.
+ **Device**: a device owned by a user.
+ **Activity**: an activity of a device within a monotoring interval.
+ **Dump**: all activities within the same monotoring interval.

## Data discretion

The data is blurred by the size of the monotoring intervals and grouping of active intervals to a presence period. Also presence is only correlated to the user and not a single device.

+ **interval-time**: Size of monotoring intervals. _Example: 5 minutes._
+ **union-time**: Maximum gap between activities to be considered part of the same presence. _Example: 30 minutes._

## Algorithm

The algorithm used to conclude from device activity to user presence.

```
for all hashes:
  device := {device with the hash}
  if device exists:
    user := {owner of the device}
    last_presence := {last presence from the user}
    if last_present exists && last_presence is younger than union_time:
      update last_presence
    else:
      add new presence from the user
```

## Presence Tracker Client

The client gathers the information, transforms it and sends it to the server. The github project for the client can be found [here](https://github.com/pioniergarage/launchpad-presence-tracker).

## API Endpoint

Every monotoring interval the active devices in the vicinity of a client are recorded and encoded as a SHA256 hash value of the MAC Address. The hash values are sent to the API Endpoint via a HTTP POST request.

### Example

```
POST /activities HTTP/1.1
{
  "activities": [
    {
      "hash": "5fbf2c53d0ab6895cf8a5133d7b2a0bd5bba954f033bffaba87b40892fe71b03"
    },
    ...
    {
      "hash": "84f6408053b4d7998140d01a4c620ccc273557b2d1d366b3239c199ca91abd3b"
    }
  ],
  "date": "2016-12-01T18:38:48.447607"
}

HTTP/1.1 201 Created
{
  "success": true
}
```
