import json
import datetime
from db.tables import *

def print_all_users():
    all_users = User.select().orderBy(User.q.id)
    print(users_to_json(all_users))

def print_all_devices():
    all_devices = Device.select().orderBy(Device.q.address)
    print(devices_to_json(all_devices))

def print_all_records():
    all_records = Record.select().orderBy(Record.q.date_from)
    print(records_to_json(all_records))

def print_last_records(delta = datetime.timedelta(minutes=10)):
    now = datetime.datetime.now()
    # All records younger than the delta.
    records = Record.select(Record.q.date_to > now - delta).orderBy(Record.q.date_to)
    print(records_to_json(records))

### Parsing
def user_to_dict(user):
    return {
        'id' : user.id,
        'name': user.name,
        'devices': [ device.address for device in user.devices]
    }
def users_to_json(users):
    return dict_to_json([user_to_dict(user) for user in users])

def device_to_dict(device):
    user = None
    if device.user != None:
        user = {
            'id' : device.user.id,
            'name': device.user.name
        }
    return {
        'id' : device.id,
        'address' : device.address,
        'user' : user
    }
def devices_to_json(devices):
    return dict_to_json([device_to_dict(device) for device in devices])

def record_to_dict(record):
    return {
        'id' : record.id,
        'address' : record.device.address,
        'from' : record.date_from.isoformat(),
        'to' : record.date_to.isoformat()
    }
def records_to_json(records):
    return dict_to_json([record_to_dict(record) for record in records])

def dict_to_json(dict):
    return json.dumps(dict, indent=2)
