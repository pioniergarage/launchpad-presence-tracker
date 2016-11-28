import datetime
from db.tables import *
from sqlobject import AND

delta = datetime.timedelta(hours=1)

def create():
    User.createTable(ifNotExists=True)
    Device.createTable(ifNotExists=True)
    Record.createTable(ifNotExists=True)
    UnknownUser()

def UnknownUser():
    users = User.select(User.q.name == "Unknown")
    user = None
    if users.count() == 0:
        user = User(name="Unknown")
    else:
        user = users[0]
    return user

def fakeData():
    insertDevice('3D:F2:C9:A6:B3:4F', name='John Doe')
    insertDevice('00:80:41:AE:FD:7E', name='John Doe')
    insertDevice('12:34:56:78:9A:BC', name='Tom Cook')

def insertDevice(address, name=None):
    devices = Device.select(Device.q.address == address)
    if devices.count() == 0:
        # No devices with the same address
        user = None
        if name != None:
            user = insertUser(name)
        else:
            user = UnknownUser()
        device = Device(address=address, user=user)
    else:
        device = devices[0]
    return device

def insertUser(name):
    users = User.select(User.q.name == name)
    user = None
    if users.count() == 0:
        # No users with the same name
        user = User(name=name)
    else:
        user = users[0]
    return user

def insertRecord(address):
    now = datetime.datetime.now()
    # The Device with the address. Created if needed.
    device = insertDevice(address)
    # All records from the device younger than the delta. Should be the latest record or none.
    records = Record.select(AND(Record.q.device == device,
        Record.q.date_to > now - delta))
    record = None
    if records.count() == 0:
        # There are no recent records.
        record = Record(device=device, date_from=now, date_to=now)
    else:
        # There are recent records. Update there time.
        for record in records:
            record.date_to = now
        record = records[0]
    return record
