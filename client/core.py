from lib import IntervalTimer, HashSet, API, Activity, Airodump, get_interval_index
import parser
import datetime
import time
import config

"""
import logging

log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)

fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)
"""

def main():

    hashset = HashSet(config.salt)
    api = API(config.api_url)
    process = Airodump(config.interface, "temp")
    filter = lambda activities: [x for x in activities if config.bssid_filter(x.bssid) and config.mac_filter(x.mac)]

    interval = config.interval

    def start_func():
        process.start()

    def end_func():
        for activity in filter(parser.extract_activities(process.output())):
            hashset.add(activity, key=lambda x: x.mac)
        now = datetime.datetime.now().replace(microsecond=0)
        interval_info = {
            'from': (now - interval).isoformat(),
            'to': now.isoformat(),
            'length': str(interval),
            'index': get_interval_index(now-interval//2, interval)
        }
        api.post_activities(hashset.flush(), interval_info)
        process.stop()
        hashset.clear()

    timer = IntervalTimer(start_func, end_func, interval)
    start = timer.start()

    print("First interval starting {0}...".format(start.isoformat(" ")))

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("KeyboardInterrupt detected, stopping process...")
	process.stop()
	timer.stop()


if __name__ == '__main__':
    main()
