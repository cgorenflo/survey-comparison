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
    start = None
    for entry in list[config["webike.measurement"]]:
        time = DateTime(entry["time"])
        if start is None:
            start = time
            start_entry = entry
        elif last_time is not None and (time - last_time).total_seconds() > 3600*8 and (last_time - start).total_seconds() > 600:
            yield {"time": str(start), "voltage":start_entry["voltage"], "temp":start_entry["battery_temperature"]}
            start = time
            start_entry = entry

        last_time = time


def get_charging(l):
    charges = []
    for imei in l["IMEI"]:
        query = "select charging_current, discharge_current,voltage, battery_temperature from {measurement} where imei='{imei}' and \
            (charging_current>30 or (discharge_current < 470 and discharge_current >0))".format(measurement=config["webike.measurement"], imei=int(imei))
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


