import matplotlib
import numpy as np
import pandas as pd
from iss4e.db import mysql
from iss4e.util.config import load_config
from scipy import stats

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
    trips = []
    for imei in l["IMEI"]:
        cursor.execute("SELECT start,end from trips where imei={imei}".format(imei=imei))
        result = cursor.fetchall()
        trips += [(start.replace(tzinfo=timezone('UTC')).astimezone(eastern),
                   end.replace(tzinfo=timezone('UTC')).astimezone(eastern)) for (start, end) in result]

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
    print("no. trips: {trips}".format(trips=str(len(ftrips + mtrips))))
    print("no. trips male: {trips}".format(trips=str(len(mtrips))))
    print("no. trips female: {trips}".format(trips=str(len(ftrips))))
    print("no. trips staff: {trips}".format(trips=str(len(staff))))
    print("no. trips students: {trips}".format(trips=str(len(students))))

    print("avg no. trips: {trips}".format(trips=str(
        len(ftrips + mtrips) / (len(male_staff) + len(male_students) + len(female_staff) + len(female_students)))))
    print("avg no. trips male: {trips}".format(trips=str(len(mtrips) / (len(male_staff) + len(male_students)))))
    print("avg no. trips female: {trips}".format(trips=str(len(ftrips) / (len(female_staff) + len(female_students)))))
    print("avg no. trips staff: {trips}".format(trips=str(len(staff) / (len(female_staff) + len(male_staff)))))
    print("avg no. trips students: {trips}".format(
        trips=str(len(students) / (len(male_students) + len(female_students)))))

    fig1 = plt.figure()
    data = [[start.hour for (start, end) in ftrips], [start.hour for (start, end) in mtrips]]
    print(stats.ranksums(data[0],data[1]))
    plt.hist(data, bins=range(25), normed=True,
             label=["female", "male"])
    plt.xticks(range(0, 24, 2))
    plt.xlabel("hour of day")
    plt.ylabel("probability density")
    plt.legend()
    plt.tight_layout()
    plt.savefig("trip_start_by_gender.png")

    fig2 = plt.figure()
    data = [[start.hour for (start, end) in staff], [start.hour for (start, end) in students]]
    print(stats.ranksums(data[0], data[1]))
    plt.hist(data, bins=range(25), normed=True,
             label=["staff/faculty", "students"])
    plt.xticks(range(0, 24, 2))
    plt.xlabel("hour of day")
    plt.ylabel("probability density")
    plt.legend()
    plt.tight_layout()
    plt.savefig("trip_start_by_occupation.png")

    fig3 = plt.figure()
    data = [start.hour for (start, end) in ftrips + mtrips]
    plt.hist(data,  bins=range(25), normed=True, rwidth=0.9, label="all participants")
    plt.xticks(range(0, 24,2 ))
    plt.xlabel("hour of day")
    plt.ylabel("probability density")
    plt.legend()
    plt.tight_layout()
    plt.savefig("trip_start_all.png")

    fig4 = plt.figure()
    data = [(end - start).total_seconds() / 60 for (start, end) in ftrips + mtrips]
    print("avg dur trips: {trips}".format(trips=np.mean(data)))
    bins = range(0, int(max(data)) + 5, 5)
    plt.hist(data, bins=bins, zorder=2, rwidth=0.9, label="all participants")
    plt.hist(data, bins=bins, cumulative=True, zorder=1, rwidth=0.9, label="all participants (cum.)")
    print("mean: {mean}".format(mean=np.mean(data)))
    print("std: {std}".format(std=np.std(data)))
    plt.xlabel("average trip duration (min)")
    plt.ylabel("frequency")
    plt.legend(loc=1)
    plt.tight_layout()
    plt.savefig("trip_duration_cum.png")

    fig5 = plt.figure()
    data = [[(end - start).total_seconds() / 60 for (start, end) in trips] for trips in [ftrips, mtrips]]
    print(stats.ranksums(data[0], data[1]))
    print("avg dur trips male: {trips}".format(trips=np.mean(data[0])))
    print("avg dur trips female: {trips}".format(trips=np.mean(data[1])))
    plt.hist(data, bins=bins, normed=True, label=["female", "male"])
    plt.xlabel("average trip duration (min)")
    plt.ylabel("probability")
    plt.legend()
    plt.tight_layout()
    plt.savefig("trip_duration_by_gender.png")

    fig6 = plt.figure()
    data = [[(end - start).total_seconds() / 60 for (start, end) in trips] for trips in [staff, students]]
    print(stats.ranksums(data[0], data[1]))
    print("avg dur trips staff: {trips}".format(trips=np.mean(data[0])))
    print("avg dur trips students: {trips}".format(trips=np.mean(data[1])))
    plt.hist(data, bins=bins, normed=True, label=["staff/faculty", "students"])
    plt.xlabel("average trip duration (min)")
    plt.ylabel("probability density")
    plt.legend()
    plt.tight_layout()
    plt.savefig("trip_duration_by_occupation.png")

    fig7 = plt.figure()
    data = [start.month for (start, end) in ftrips + mtrips]
    plt.hist(data, bins=range(1,14), normed=True, zorder=2, rwidth=0.9, label=["all participants"])
    plt.xticks(range(1,13),["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], rotation=30, ha="left")
    plt.ylabel("probability density")
    plt.legend()
    plt.tight_layout()
    plt.savefig("trip_by_month.png")
