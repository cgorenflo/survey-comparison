import pandas as pd
from pytz import timezone
from iss4e.util.config import load_config
from iss4e.db import mysql
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

eastern = timezone('Canada/Eastern')

config = load_config()


participants = pd.read_excel("participant map.xlsx", header=[1])
female_staff = participants.iloc[1:8][["Email", "IMEI"]]
male_staff = participants.iloc[10:16][["Email", "IMEI"]]
female_students = participants.iloc[18:23][["Email", "IMEI"]]
male_students = participants.iloc[25:32][["Email", "IMEI"]]
iss4e = participants.iloc[34:39][["Email", "IMEI"]]

parts = pd.concat([female_students, female_staff, male_students, male_staff, iss4e])

survey1 = pd.read_excel("survey 1.xlsx")
survey1.columns = map(str, range(182))
survey1.rename(columns={"172": "Email"}, inplace=True)

survey2 = pd.read_excel("survey 2 numerical.xls")
survey2.columns = map(str, range(167))
survey2.rename(columns={"5": "Email"}, inplace=True)

s1 = survey1[survey1["Email"].isin(parts["Email"])].sort_values("Email", ascending=True)
s2 = survey2[survey2["Email"].isin(parts["Email"])].sort_values("Email", ascending=True)

result1 = s1.merge(parts, how='left', on=["Email"])
result2 = s2.merge(parts, how='left', on=["Email"])

summer_trips = []
winter_trips = []
for slice in result1[["161","162","IMEI"]].iterrows():
    summer = [int(s) for s in str(slice[1]["161"]).split() if s.isdigit()]
    winter = [int(s) for s in str(slice[1]["162"]).split() if s.isdigit()]
    if summer and summer[0]<30:
        summer_trips.append((summer[0], int(slice[1]["IMEI"])))

    if winter and winter[0] < 30:
        winter_trips.append((winter[0], int(slice[1]["IMEI"])))



def get_trips(imei, start, end):
    if(int(start)<int(end)):
        cursor.execute("SELECT start,end from trips where imei={imei} and month(start)>{start} and MONTH (start)<{end}".format(imei=imei, start=start, end=end))
    else:
        cursor.execute(
            "SELECT start,end from trips where imei={imei} and (month(start)>{start} or MONTH (start)<{end})".format(
                imei=imei, start=start, end=end))
    result = cursor.fetchall()
    return [(start.replace(tzinfo=timezone('UTC')).astimezone(eastern),
               end.replace(tzinfo=timezone('UTC')).astimezone(eastern)) for (start, end) in result]


def plot(name, s ,e ):
    durations = []
    kms = []
    t = []
    for km, imei in summer_trips:
        trips = get_trips(imei, s, e)
        duration = 0
        for start, end in trips:
            duration += (end - start).total_seconds() / 60
        durations += [duration/(31+30+31+31+30+31)]
        kms += [km]
        t += [len(trips)/(31+30+31+31+30+31)]

    figsize = (5, 3.125)
    dpi = 720
    plt.figure(figsize=figsize, dpi=dpi)
    plt.xticks(range(0, 30, 5))
    plt.xlabel("estimated trip km range per day")
    plt.ylabel("average trip duration per day")
    plt.tight_layout()
    plt.scatter(kms, durations)
    plt.savefig(name)

    plt.figure(figsize=figsize, dpi=dpi)
    plt.xticks(range(0, 30, 5))
    plt.xlabel("estimated trip km range per day")
    plt.ylabel("average number of trips per day")
    plt.tight_layout()
    plt.scatter(kms, t)
    plt.savefig("number_of_"+ name)


with mysql.connect(**config["webike.mysql"]) as mysql_client:
    cursor = mysql_client.cursor()
    plot("summer_trips.png", "4", "11")
    plot("winter_trips.png", "10", "5")

