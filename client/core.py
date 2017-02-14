import datetime
import time

from lib import IntervalTimer, HashSet, API, Airodump, Dump
import parser
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
    """
    The main function of the client.
    """
    hashset = HashSet(config.salt)
    api = API(config.api_url)
    process = Airodump(config.interface, "temp")

    activity_filter = lambda activities: (
        [x for x in activities
         if config.bssid_filter(x.bssid) and config.mac_filter(x.mac)])

    interval = config.interval

    def start_func():
        """Function that is executed at the start of an interval."""
        process.start()

    def end_func():
        """Function that is executed at the end of an interval."""
        for activity in activity_filter(parser.extract_activities(process.output())):
            hashset.add(activity, key=lambda x: x.mac)
        now = datetime.datetime.now().replace(microsecond=0)

        dump = Dump(hashset.flush(), (now - interval), now)
        api.post_activities(dump)
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
