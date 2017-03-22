import matplotlib
import pandas as pd
from iss4e.db import influxdb, mysql
from iss4e.util.config import load_config

matplotlib.use('Agg')
from pytz import timezone

config = load_config()

participants = pd.read_excel("participant map.xlsx", header=[1])
female_staff = participants.iloc[1:8][["Email", "IMEI"]]
male_staff = participants.iloc[10:16][["Email", "IMEI"]]
female_students = participants.iloc[18:23][["Email", "IMEI"]]
male_students = participants.iloc[25:32][["Email", "IMEI"]]

eastern = timezone('Canada/Eastern')

last_entry = None

def analyze_charge(entry):
    print(entry)
    global last_entry
    if last_entry is None or last_entry["time"] + 60* 1000< entry["time"]:
        last_entry = entry
        return entry
    else:
        last_entry = entry


def get_charging(l):
    charges = []
    for imei in l["IMEI"]:
        result = influx_client.stream_query(
            "select count(charging_current), count(discharge_current) from sensor_data where imei='353323057856089' and "
            "(charging_current>30 or (discharge_current < 490 and discharge_current >0) ) limit 10")
        charges += [analyze_charge(entry) for entry in result]
    return charges


with mysql.connect(**config["webike.mysql"]) as mysql_client, influxdb.connect(
        **config["webike.influx"]) as influx_client:
    fstaff = get_charging(female_staff)
