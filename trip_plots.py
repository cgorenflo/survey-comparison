from iss4e.db import mysql
from iss4e.util.config import load_config
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


config = load_config()

participants = pd.read_excel("participant map.xlsx", header=[1])
female_staff = participants.iloc[1:8][["Email","IMEI"]]
male_staff = participants.iloc[10:16][["Email","IMEI"]]
female_students = participants.iloc[18:23][["Email","IMEI"]]
male_students = participants.iloc[25:32][["Email","IMEI"]]


def get_trips(l):
    trips = []
    for imei in l["IMEI"]:
        cursor.execute("SELECT start,end from trips where imei={imei}".format(imei=imei))
        result = cursor.fetchall()
        trips += result

    return trips


with mysql.connect(**config["webike.mysql"]) as mysql_client:
    cursor = mysql_client.cursor()
    fstu_trips = get_trips(female_students)
    fsta_trips = get_trips(female_staff)
    mstu_trips = get_trips(male_students)
    msta_trips = get_trips(male_staff)

    ftrips = fstu_trips + fsta_trips
    mtrips = mstu_trips + msta_trips

    staff = fsta_trips + msta_trips
    students = fstu_trips + mstu_trips

    fig1 = plt.figure()
    plt.hist([[start.hour for (start,end) in ftrips],[start.hour for (start, end) in mtrips]],24, normed=True)
    plt.savefig("trip_start_by_gender.png")

    fig2 = plt.figure()
    plt.hist([[start.hour for (start,end) in staff],[start.hour for (start, end) in students]],24, normed=True)
    plt.savefig("trip_start_by_occupation.png")

    fig3 = plt.figure()
    plt.hist([(end - start).total_seconds()//60 for (start,end) in ftrips+mtrips], normed=True, zorder=2)
    plt.hist([(end - start).total_seconds() // 60 for (start, end) in ftrips + mtrips], cumulative=True, normed=True, zorder=1)
    plt.savefig("trip_duration_cum.png")