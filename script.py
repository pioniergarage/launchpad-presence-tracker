import datetime
from db.tables import *
import output
from db import database
from sqlobject import AND

def main():
    output.print_all_users()
    output.print_all_devices()
    output.print_all_records()
    #database.insertRecord('3D:F2:C9:A6:B3:4F')
    #database.insertRecord('23:D3:F4:87:34:A3')
    #database.insertRecord('00:80:41:AE:FD:7E')
    #database.insertRecord('12:34:56:78:9A:BC')
    #output.print_last_records(delta = datetime.timedelta(minutes=2))

if __name__ == "__main__":
    database.create()
    #database.fakeData()
    main()
