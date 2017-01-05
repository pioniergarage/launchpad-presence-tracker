import datetime

"""
The api endpoint to post the hash values to.
"""
api_url = "https://api.example.com/v1"


"""
The secret for the api access.
"""
api_secret = ""


"""
Filter for bssids.
"""
bssid_filter = lambda bssid: True

"""
Filter for mac addresses.
"""
mac_filter = lambda mac: True


"""
The interval between posts to the server. The interval must divide a day cleanly.

All possible values are:

less than 2 minute:
    1s, 2s, 3s, 4s, 5s, 6s, 8s, 9s, 10s, 12s, 15s, 16s, 18s, 20s, 24s, 25s,
    27s, 30s, 32s, 36s, 40s, 45s, 48s, 50s, 54s, 1m, 1m 4s, 1m 12s, 1m 15s,
    1m 20s, 1m 30s, 1m 36s, 1m 40s, 1m 48s

less than 10 minutes:
    2m, 2m 8s, 2m 15s, 2m 24s, 2m 30s, 2m 40s, 3m, 3m 12s, 3m 20s, 3m 36s,
    3m 45s, 4m, 4m 30s, 4m 48s, 5m, 5m 20s, 6m, 6m 24s, 6m 40s, 7m 12s, 7m 30s,
    8m, 9m, 9m 36s

less than 30 minutes:
    10m, 10m 40s, 11m 15s, 12m, 13m 20s, 14m 24s, 15m, 16m, 18m, 19m 12s, 20m,
    22m 30s, 24m, 26m 40s, 28m 48s

30 minutes or more:
    30m, 32m, 36m, 40m, 45m, 48m, 53m 20s, 57m 36s, 1h, 1h 12m, 1h 20m, 1h 30m,
    1h 36m, 2h, 2h 24m, 2h 40m, 3h, 4h, 4h 48m, 6h, 8h, 12h, 1day
"""
interval = datetime.timedelta(minutes=30)


"""
The salt for hashing the mac addresses.
"""
salt = ""


"""
WLan interface to use.
"""
interface = "wlan0"