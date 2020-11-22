import logging
import sys
import dockermirror
import time
import schedule
import configparser
import re

# Log information to stdout. Change log level from "root.setLevel"
root = logging.getLogger()
root.setLevel(logging.INFO)  # Here you can change the log level

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

# Collect interval and time period from config.ini schedule section
config = configparser.ConfigParser()
config.read('config.ini')
refresh = config['DEFAULT']['refresh']  # Read refresh value
interval = int(re.sub('[^0-9]', '', refresh))  # Construct refresh interval
time_period = (re.sub('[^A-Z-a-z]', '', refresh))  # Construct refresh period


# Define timer for scheduler
def timer(value):
    when = value
    return when


if time_period == 'm':
    schedule.every(timer(interval)).minutes.do(dockermirror.run)  # Run every n minutes
elif time_period == "d":
    schedule.every(timer(interval)).days.do(dockermirror.run)  # Run every n days
elif time_period == "w":
    schedule.every(timer(interval)).weeks.do(dockermirror.run)  # Run every n weeks
elif interval == 0:
    dockermirror.run()
else:
    print("Incorrect refresh value. Accepted values are: 0, <n>m, <n>d, <n>w, where n is a positive integer")
    exit(128)
schedule.run_all()  # Running initial mirroring

if not interval == 0:
    while True:
        schedule.run_pending()
        time.sleep(1)
