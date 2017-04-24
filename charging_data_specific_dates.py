import matplotlib
import pandas as pd
from iss4e.db import influxdb, mysql
from iss4e.util.config import load_config
from iss4e.webike.trips.auxiliary import DateTime

from pytz import timezone

config = load_config()

def analyze_charge(list):
    last_time = None
    start = None
    entires_count = 0
    for entry in list[config["webike.measurement"]]:
        time = DateTime(entry["time"])
        if start is None:
            start = time
            start_entry = entry
            entries_count = 1
        elif (time - last_time).total_seconds() > 60*5:
            if entries_count >= 5 and (last_time - start).total_seconds() >= 5 * 60:
                if(start._datetime.hour > 8 and start._datetime.hour < 10):
                    print(start_entry)
                yield {"time": str(start), "voltage":start_entry["voltage"], "temp":start_entry["battery_temperature"]}

            start = time
            start_entry = entry
            entries_count = 1
        else:
            entries_count += 1

        last_time = time


def get_charging(date1, date2):
    query = "select charging_current, discharge_current,voltage, battery_temperature from {measurement} where time>'{start}'and time < '{end}'\
            (charging_current>70 or (discharge_current < 450 and discharge_current >50))".format(measurement=config["webike.measurement"], start=date1, end=date2)
    result = influx_client.query(query)
    return analyze_charge(result)


with mysql.connect(**config["webike.mysql"]) as mysql_client, influxdb.connect(
        **config["webike.influx"]) as influx_client:
    print(len(get_charging("2015-10-23","2015-10-25")))
    print(len(get_charging("2015-06-15", "2015-06-17")))
    print(len(get_charging("2016-04-19", "2016-04-21")))