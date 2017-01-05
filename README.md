# launchpad-presence-tracker
A tool for tracking and analyzing the presence of devices in the launchpad.

## Running the script

```
sudo python client
```

## How does it work?

1. Start detecting Wi-Fi traffic of nearby devices and networks.
1. Devices are filtered by the network they are active in and their mac addresses.
1. After a specified interval:
    + The `sha-256` hashes of the filtered active device mac addresses are send to the server.
    + All information is wiped.
1. The next interval starts.

## Requirements

Make sure to install the [Aircrack-ng](http://www.aircrack-ng.org/) suite and have a compatible WLan Adapter. For help to determine if your adapter is compatible click [here](http://www.aircrack-ng.org/doku.php?id=compatibility_drivers).

We are using [TP-Link TL-WN722N](http://www.tp-link.de/products/details/cat-11_TL-WN722N.html).

### To install python modules:

```
pip install -r requirements.txt
```

### To configure your version:

Edit the `config.default.py` script. Configureable values are:

````
api_url = "https://api.example.com/v1"
api_secret = ""
bssid_filter = lambda bssid: True
mac_filter = lambda mac: True
interval = datetime.timedelta(minutes=30)
salt = ""
interface = "wlan0"
```