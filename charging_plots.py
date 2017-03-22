import matplotlib
import pandas as pd
from iss4e.db import influxdb, mysql
from iss4e.util.config import load_config
from iss4e.webike.trips.auxiliary import DateTime

matplotlib.use('Agg')
from pytz import timezone

config = load_config()

participants = pd.read_excel("participant map.xlsx", header=[1])
female_staff = participants.iloc[1:8][["Email", "IMEI"]]
male_staff = participants.iloc[10:16][["Email", "IMEI"]]
female_students = participants.iloc[18:23][["Email", "IMEI"]]
male_students = participants.iloc[25:32][["Email", "IMEI"]]

eastern = timezone('Canada/Eastern')

def analyze_charge(list):
    last_entry = None
    for entry in list:
        if last_entry is None or (DateTime(entry["time"]) - DateTime(last_entry["time"])).total_seconds() > 3600:
            last_entry = entry
            yield entry
        else:
            last_entry = entry


def get_charging(l):
    charges = []
    for imei in l["IMEI"]:
        query = "select charging_current, discharge_current from sensor_data where imei='{imei}' and \
            (charging_current>30 or (discharge_current < 490 and discharge_current >0)) limit 3".format(imei=int(imei))
        print(query)
        result = influx_client.query(query)
        print(result)
        charges += list(analyze_charge(result))
        global last_entry
        last_entry = None
    return charges


with mysql.connect(**config["webike.mysql"]) as mysql_client, influxdb.connect(
        **config["webike.influx"]) as influx_client:
    fstaff = get_charging(female_staff)
    print(fstaff)
