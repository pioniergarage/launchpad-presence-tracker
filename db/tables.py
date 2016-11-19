import re
from sqlobject import *
from db.connection import conn

class User(SQLObject):
    _connection = conn
    name = StringCol(unique=True)
    devices = MultipleJoin('Device', joinColumn='user_id')

class Device(SQLObject):
    _connection = conn
    user = ForeignKey('User')
    address = StringCol(length=17, unique=True)

    def _set_address(self, value):
        if re.match('^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$', value):
            self._SO_set_address(value)
        else:
            raise ValueError('Not a MAC address: %s' % value)

class Record(SQLObject):
    _connection = conn
    device = ForeignKey('Device')
    date_from = DateTimeCol()
    date_to = DateTimeCol()
