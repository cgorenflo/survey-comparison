from typing import List
from iss4e.db import influxdb, mysql

import pandas as pd
import matplotlib.pyplot as plt
from iss4e.util.config import load_config
from matplotlib.figure import Figure
from itertools import groupby

survey2 = pd.read_excel("survey2_participants.xlsx")
survey2 = survey2.drop([5, 9, 14, 18])
global_order_index = None


def plot_frequency(figure: Figure):
    ebikes_order = survey2["frequency_ebikes"].sort_values(ascending=True)
    ebikes_order = survey2.reindex(ebikes_order.index, copy=True)
    global global_order_index
    global_order_index = ebikes_order.index
    sub = figure.add_subplot(111, title="usage frequency (survey)", xticks=range(len(ebikes_order)),
                             xticklabels=ebikes_order.index,
                             xlim=[-1, len(ebikes_order)],
                             ylim=[0, 6], )

    p1 = sub.plot(6 - ebikes_order["frequency_ebikes"].values, c='red', marker='.', linestyle='--', label='ebike')
    p2 = sub.plot(6 - ebikes_order["frequency_bikes"].values, c='green', marker='+', linestyle='None', label='bike')
    p3 = sub.plot(6 - ebikes_order["frequency_cars"].values, c='black', marker='x', linestyle='None', label='car')
    p4 = sub.plot(6 - ebikes_order["frequency_transit"].values, c='blue', marker='1', linestyle='None',
                  label='pub. transit')
    p5 = sub.plot(6 - ebikes_order["frequency_walk"].values, c='orange', marker='2', linestyle='None', label='walking')

    yaxis = sub.yaxis
    yaxis.set_ticklabels(
        ["", "(almost) never", "less than once per month", "1-3 days per month", "1-3 days per week", "(almost) daily"])

    figure.tight_layout()


def plot_trip_length(figure: Figure):
    sub = figure.add_subplot(111, title="average trip length in km(survey)", xticks=range(len(survey2)),
                             xticklabels=survey2.index,
                             xlim=[-1, len(survey2)], )
    p1 = sub.plot(survey2["trip_length_work"].values, c='red', marker='.', linestyle='None', label='work')
    p2 = sub.plot(survey2["trip_length_school"].values, c='green', marker='+', linestyle='None', label='school')
    p3 = sub.plot(survey2["trip_length_shopping"].values, c='black', marker='x', linestyle='None',
                  label='shopping')
    p4 = sub.plot(survey2["trip_length_private"].values, c='blue', marker='1', linestyle='None',
                  label='private business')
    p5 = sub.plot(survey2["trip_length_shuttle"].values, c='orange', marker='2', linestyle='None',
                  label='"shuttle service"')
    p5 = sub.plot(survey2["trip_length_leisure"].values, c='gray', marker='3', linestyle='None', label='leisure')

    figure.tight_layout()


def plot_odometer(figure: Figure):
    ebikes_order = survey2["odometer"].sort_values(ascending=False)
    ebikes_order = survey2.reindex(global_order_index, copy=True)
    sub = figure.add_subplot(111, title="odometer reading (survey)", xticks=range(len(ebikes_order)),
                             xticklabels=ebikes_order.index,
                             xlim=[-1, len(ebikes_order)], )
    sub.plot(ebikes_order["odometer"].values, c='red', marker='o', linestyle='None', label='work')


fig1 = plt.figure(figsize=(10, 5))
plot_frequency(fig1)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout(rect=(0, 0, 0.8, 1))
plt.savefig("usage_frequency.png")

fig2 = plt.figure(figsize=(10, 5))
plot_trip_length(fig2)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout(rect=(0, 0, 0.8, 1))
plt.savefig("trip_distance.png")

fig3 = plt.figure(figsize=(10, 5))
plot_odometer(fig3)
plt.tight_layout(rect=(0, 0, 0.8, 1))
plt.savefig("odometer.png")

config = load_config()

with mysql.connect(**config["webike.mysql"]) as mysql_client, influxdb.connect(
        **config["webike.influx"]) as influx_client:
    cursor = mysql_client.cursor()
    cursor.execute("SELECT TIMEDIFF(trips.end, start) from trips")
    result = cursor.fetchall()

    plt.figure(figsize=(10, 5))
    plt.title("trip length in minutes")
    plt.tight_layout(rect=(0, 0, 0.8, 1))
    plt.hist(sorted([time[0].total_seconds() / 60.0 for time in result])[:-30], bins=30)
    plt.savefig("trip_length_hist.png")

    cursor.execute(
        "SELECT  users.name, AVG(TIMEDIFF(trips.end, trips.start))/60 as duration FROM trips join users on trips.imei LIKE concat('%', users.imei) GROUP BY trips.imei ")
    result = cursor.fetchall()
    plt.figure(figsize=(10, 5))
    plt.title("average trip length in minutes")
    plt.plot([value[1] for value in result])
    plt.xticks(range(len(result)), [value[0][0] for value in result])
    plt.tight_layout(rect=(0, 0, 0.8, 1))
    plt.savefig("avg_trip_length.png")
