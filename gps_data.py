import matplotlib
import numpy as np
import pandas as pd
from iss4e.db import influxdb, mysql
from iss4e.util.config import load_config

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pytz import timezone

config = load_config()

participants = pd.read_excel("participant map.xlsx", header=[1])
female_staff = participants.iloc[1:8][["Email", "IMEI"]]
male_staff = participants.iloc[10:16][["Email", "IMEI"]]
female_students = participants.iloc[18:23][["Email", "IMEI"]]
male_students = participants.iloc[25:32][["Email", "IMEI"]]

eastern = timezone('Canada/Eastern')


def get_trips(l):
    trips_by_imei = {}
    for imei in l["IMEI"]:
        cursor.execute("SELECT start,end from trips where imei={imei}".format(imei=imei))
        result = cursor.fetchall()
        trips_by_imei[str(int(imei))] = [(start, end) for (start, end) in
                                         result]

    return trips_by_imei


def write_gps_data(trips_collection, file_name):
    gps = []
    for imei, trips in trips_collection.items():
        for start, end in trips:
            query = "select latitude, longitude from {measurement} where imei='{imei}' and time >= '{start}' and time <= '{end}' and longitude != 0 and latitude != 0".format(
                imei=imei, measurement=config["webike.measurement"], start=start, end=end)

            result = influx_client.query(query)
            gps.append(list(result[config["webike.measurement"]]))
    with open(file_name, mode='w') as file:
        file.write(str(gps))


with mysql.connect(**config["webike.mysql"]) as mysql_client, influxdb.connect(
        **config["webike.influx"]) as influx_client:
    cursor = mysql_client.cursor()
    fstu_trips = get_trips(female_students)
    fsta_trips = get_trips(female_staff)
    mstu_trips = get_trips(male_students)
    msta_trips = get_trips(male_staff)

    ftrips = dict(fstu_trips, **fsta_trips)
    mtrips = dict(mstu_trips, **msta_trips)
    staff = dict(fsta_trips, **msta_trips)
    students = dict(fstu_trips, **mstu_trips)

    write_gps_data(ftrips, "fgps")
    write_gps_data(mtrips, "mgps")
    write_gps_data(staff, "staffgps")
    write_gps_data(students, "studentsgps")
