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
    last_time = None
    print(list)
    for entry in list['sensor_data']:
        print(entry)
        time = DateTime(entry["time"])
        if last_time is None or (time - last_time).total_seconds() > 3600:
            yield {"time": str(time), "voltage":entry["voltage"], "temp":entry["battery_temperature"]}

        last_time = time


def get_charging(l):
    charges = []
    for imei in l["IMEI"]:
        query = "select charging_current, discharge_current,voltage, battery_temperature from sensor_data where imei='{imei}' and \
            (charging_current>30 or (discharge_current < 490 and discharge_current >0)) limit 1".format(imei=int(imei))
        result = influx_client.query(query)
        charges += list(analyze_charge(result))
    return charges


with mysql.connect(**config["webike.mysql"]) as mysql_client, influxdb.connect(
        **config["webike.influx"]) as influx_client:
    fstaff = get_charging(female_staff)
    with open("fstaff",mode='w') as file:
        file.writelines("{line}\n".format(line= line) for line in fstaff)
    mstaff = get_charging(male_staff)
    with open("mstaff",mode='w') as file:
        file.writelines("{line}\n".format(line=line) for line in mstaff)
    fstuds = get_charging(female_students)
    with open("fstuds",mode='w') as file:
        file.writelines("{line}\n".format(line=line) for line in fstuds)
    mstuds = get_charging(male_students)
    with open("mstuds",mode='w') as file:
        file.writelines("{line}\n".format(line=line) for line in mstuds)
