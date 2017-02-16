"""
The client core with the main function.
"""

import datetime
import time
import os

from lib import IntervalTimer, HashSet, API, Airodump, Dump
import parser
import config

# pylint: disable=no-member

def enable_scheduler_log():
    """
    Enables logging for apscheduler jobs.
    """
    import logging

    log = logging.getLogger('apscheduler.executors.default')
    log.setLevel(logging.INFO)

    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    log.addHandler(handler)

# enable_scheduler_log()

def save_dump_to_file(dump):
    """
    Saves dump information and activities in csv files.
    """
    assert isinstance(dump, Dump)

    with open("dumps.csv", "a") as dumps_file:
        dumps_file.write(dump.to_csv())
        dumps_file.write("\n")

    print("Saved {0} activities between {1} and {2}...".format(
        len(dump.activities),
        dump.from_datetime.isoformat(" "),
        dump.to_datetime.isoformat(" ")))



def main():
    """
    The main function of the client.
    """
    hashset = HashSet(config.salt)
    api = API(config.api_url)
    process = Airodump(config.interface, "temp")

    try:
        os.remove(process._temp_file_name)
    except OSError:
        pass

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
        hashset.clear()
        save_dump_to_file(dump)
        # api.post_activities(dump)
        process.stop()

    timer = IntervalTimer(start_func, end_func, interval)
    start = timer.start()

    print("First interval starting at {0}...".format(start.isoformat(" ")))

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("KeyboardInterrupt detected, stopping process...")
    process.stop()
    timer.stop()


if __name__ == '__main__':
    main()
