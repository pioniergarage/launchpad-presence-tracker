import sys
import hashlib
import re
from apscheduler.schedulers.background import BackgroundScheduler

from config import interval_time
import api

# MAC addresses with activities in the last monotoring interval
hash_dict = {}

# regular expression for extracting the MAC address from the commandline input
line_regex = re.compile('^(MAC-ADDRESS: )(([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})).*$')
line_regex_mac_group = 2

def listen():
    k = 0
    # background scheduler for the monotoring interval
    scheduler = BackgroundScheduler()
    scheduler.start()
    try:
        scheduler.add_job(print_hash_dict, 'interval', seconds = interval_time)
        buff = ''
        while True:
            buff += sys.stdin.read(1)
            if buff.endswith('\n'):
                consume_line(buff[:-1])
                buff = ''
                k = k + 1
    except KeyboardInterrupt:
        sys.stdout.flush()
        scheduler.shutdown()
        pass
    print('{0} lines processed'.format(k))

def consume_line(line):
    mac = line_regex.search(line).group(line_regex_mac_group)
    #print('MAC: {0}'.format(mac))
    mac_hash = hashlib.sha256(mac.encode('UTF-8')).hexdigest()
    hash_dict[mac] = {
        'hash': mac_hash
    }

def print_hash_dict():
    api.post_activities(hash_dict)
    hash_dict.clear()
