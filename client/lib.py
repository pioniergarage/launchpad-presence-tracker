import hashlib
import datetime
import time
import json
import subprocess
import os
from apscheduler.schedulers.background import BackgroundScheduler

def round_down(number, multiple):
    assert type(number) is int
    assert type(multiple) is int
    return number - (number % multiple)

def get_seconds_from_day(datetime_value):
    return datetime_value.hour * 60 * 60 + datetime_value.minute * 60 + datetime_value.second

def get_interval_index(datetime_value, interval):
    assert type(interval) is datetime.timedelta
    seconds = get_seconds_from_day(datetime_value)
    return seconds // interval.seconds

def get_next_start(interval):
    assert type(interval) is datetime.timedelta
    now = datetime.datetime.now()
    now_seconds = get_seconds_from_day(now)
    last_start_seconds = round_down(now_seconds, interval.seconds)
    hour = last_start_seconds // (60*60)
    minute = (last_start_seconds // 60) % 60
    second = last_start_seconds % (60)
    last_start = now.replace(hour=hour,minute=minute,second=second,microsecond=0)
    return last_start + interval


class IntervalTimer:
    def __init__(self, start_func, end_func, interval):
        assert type(interval) is datetime.timedelta
        # assert 24 * 60 * 60 % interval.seconds == 0
        self.start_func = start_func
        self.end_func = end_func
        self.interval = interval
        self.scheduler = BackgroundScheduler()

    def start(self):
        next_start = get_next_start(self.interval)
        next_restart = next_start + self.interval

        self.scheduler.add_job(self.start_func, 'date', run_date=next_start)

        def restart_func():
            self.end_func()
            self.start_func()

        self.scheduler.add_job(restart_func, 'interval', next_run_time=next_restart, seconds=self.interval.seconds)

        self.scheduler.start()

	return next_start

    def stop(self):
	for job in self.scheduler.get_jobs():
		job.remove()
	self.scheduler.shutdown()


class Airodump:
    def __init__(self, interface, file_name):
        self._cmd = [
            'airodump-ng',
            '--write', file_name,
            '--output-format', 'csv',
            interface
        ]
        self._temp_file = file_name + '-01.csv'
        self._process = None
        self._devnull = open(os.devnull, 'wb')

    def __del__(self):
        self.stop()
        self._devnull.close()

    def start(self):
        self._process = subprocess.Popen(self._cmd,
            stdout=subprocess.PIPE,
            stderr=self._devnull)

    def running(self):
        return self._process != None and self._process.poll() == None

    def stop(self):
        try:
            # Throws error when terminate is called more than once
            self._process.terminate()
        except (OSError, AttributeError):
            pass
        # Make sure process is terminated
        while self.running():
            time.sleep(0.1)
        try:
            os.remove(self._temp_file)
        except OSError:
            return

    def restart(self):
        self.stop()
        self.start()

    def output(self):
        lines = []
        with open(self._temp_file) as file:
            line = file.readline()
            while line:
                lines.append(line)
                line = file.readline()
        return lines


class Activity:
    def __init__(self, mac, first, last, bssid):
        self.mac = mac
        self.first = first
        self.last = last
        self.bssid = bssid

    def __str__(self):
        return self.to_csv()

    def to_csv(self):
        return ", ".join([self.mac, self.bssid, self.first.isoformat(" "), self.last.isoformat(" ")])


class HashSet:
    """
    An Object which keeps the set of hash values from added items.
    """

    def __init__(self, salt=""):
        self.table = {}
        self.set = set()
        self.salt = salt

    def add(self, item, key=lambda x: x):
        assert isinstance(key(item), str)
        table_item = self.table.get(key(item))
        if table_item == None:
            item_hash = hashlib.sha256(key(item).encode('utf-8') + self.salt).hexdigest()
            table_item = (item_hash, item)
            self.table[key(item)] = table_item
        self.set.add(table_item)

    def clear(self):
        self.set.clear()

    def flush(self):
        return list(self.set)


class API:
    """
    A wrapper for API calls.
    """

    def __init__(self, base_url):
        self.base_url = base_url

    def post_activities(self, hashset_list, interval_info):
        url = "{0}/activities".format(self.base_url)
        now = datetime.datetime.now()
        body_dict = {
            'activities': [{
                # 'mac': item.mac,
                # 'bssid': item.bssid,
                # 'first': item.first.isoformat(),
                # 'last': item.last.isoformat(),
                'hash': hash_value
            } for (hash_value, item) in hashset_list],
            'interval': interval_info,
            'count': len(hashset_list),
            'datetime': now.replace(microsecond=0).isoformat()
        }
        json_str = json.dumps(body_dict, indent=2)

        print("POST HTTP 1.1 {0}".format(url))
        print(json_str)
