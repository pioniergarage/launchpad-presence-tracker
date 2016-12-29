from lib import IntervalTimer, HashSet, API, Activity, Airodump
import parser
import datetime
import time

def main():

    hashset = HashSet()
    api = API("https://api.com/v1/")
    process = Airodump("wlan1", "temp")

    interval = datetime.timedelta(seconds=5)

    def start_func():
        process.start()

    def end_func():
        for activity in parser.extract_activities(process.output()):
            hashset.add(activity, key=lambda x: x.mac)
        process.stop()
        API.post_activities(hashset.flush())
        hashset.clear()

    timer = IntervalTimer(start_func, end_func, interval)
    timer.start()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("KeyboardInterrupt detected, stopping process...")


if __name__ == '__main__':
    main()
