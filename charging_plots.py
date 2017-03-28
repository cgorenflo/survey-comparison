import ast
from scipy import stats
import matplotlib
import webike.data.SoC as soc
from iss4e.webike.trips.auxiliary import DateTime

import trip_plots

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pytz import timezone

eastern = timezone('Canada/Eastern')


def to_datetime(time):
    return DateTime(time)._datetime.replace(tzinfo=timezone('UTC')).astimezone(eastern)


with open("data/fstaff_charging", mode='r') as file:
    fstaff = [ast.literal_eval(line) for line in file.read().splitlines()]
    for line in fstaff:
        line["time"] = to_datetime(line["time"])
with open("data/mstaff_charging", mode='r') as file:
    mstaff = [ast.literal_eval(line) for line in file.read().splitlines()]
    for line in mstaff:
        line["time"] = to_datetime(line["time"])
with open("data/fstuds_charging", mode='r') as file:
    fstuds = [ast.literal_eval(line) for line in file.read().splitlines()]
    for line in fstuds:
        line["time"] = to_datetime(line["time"])
with open("data/mstuds_charging", mode='r') as file:
    mstuds = [ast.literal_eval(line) for line in file.read().splitlines()]
    for line in mstuds:
        line["time"] = to_datetime(line["time"])

fcharge = fstuds + fstaff
mcharge = mstuds + mstaff

staff = fstaff + mstaff
students = fstuds + mstuds

print("no. charges: {charge}".format(charge=str(len(staff + students))))
print("no. charges male: {charge}".format(charge=str(len(mcharge))))
print("no. charges female: {charge}".format(charge=str(len(fcharge))))
print("no. charges staff: {charge}".format(charge=str(len(staff))))
print("no. charges students: {charge}".format(charge=str(len(students))))

print("avg no. charges: {charge}".format(charge=str(
    len(staff + students) / (
        len(trip_plots.male_staff) + len(trip_plots.male_students) + len(trip_plots.female_staff) + len(
            trip_plots.female_students)))))
print("avg no. charges male: {charge}".format(
    charge=str(len(mcharge) / (len(trip_plots.male_staff) + len(trip_plots.male_students)))))
print("avg no. charges female: {charge}".format(
    charge=str(len(fcharge) / (len(trip_plots.female_staff) + len(trip_plots.female_students)))))
print("avg no. charges staff: {charge}".format(
    charge=str(len(staff) / (len(trip_plots.female_staff) + len(trip_plots.male_staff)))))
print("avg no. charges students: {charge}".format(
    charge=str(len(students) / (len(trip_plots.male_students) + len(trip_plots.female_students)))))

print("no. trips per charge: {charge}".format(
    charge=str(len(trip_plots.staff + trip_plots.students) / len(staff + students))))
print("no. trips per charge male: {charge}".format(charge=str(len(trip_plots.mtrips) / len(mcharge))))
print("no. trips per charge female: {charge}".format(charge=str(len(trip_plots.ftrips) / len(fcharge))))
print("no. trips per charge staff: {charge}".format(charge=str(len(trip_plots.staff) / len(staff))))
print("no. trips per charge students: {charge}".format(charge=str(len(trip_plots.students) / len(students))))

fig1 = plt.figure()
data = [[entry["time"].hour for entry in fcharge], [entry["time"].hour for entry in mcharge]]
print(stats.ranksums(data[0], data[1]))
plt.hist(data, bins=range(0, 25), normed=True, label=["female", "male"])
plt.xticks(range(0, 24, 2))
plt.xlabel("hour of day")
plt.ylabel("probability density")
plt.legend()
plt.tight_layout()
plt.savefig("charge_start_by_gender.png")

fig2 = plt.figure()
data = [[entry["time"].hour for entry in staff], [entry["time"].hour for entry in students]]
print(stats.ranksums(data[0], data[1]))
plt.hist(data, bins=range(0, 25), normed=True, label=["staff/faculty", "students"])
plt.xticks(range(0, 24, 2))
plt.xlabel("hour of day")
plt.ylabel("probability density")
plt.legend()
plt.tight_layout()
plt.savefig("charge_start_by_occupation.png")

fig3 = plt.figure()
plt.hist([entry["time"].hour for entry in fcharge + mcharge], bins=range(0,25), normed=True, rwidth=0.9, label=["all participants"])
plt.xticks(range(0, 24, 2))
plt.xlabel("hour of day")
plt.ylabel("probability density")
plt.legend()
plt.tight_layout()
plt.savefig("charge_start_all.png")


def calc_soc_data(l):
    return [soc.calc_soc(soc.choose_temp(entry["temp"]), entry["voltage"]) for entry in l if
            entry["voltage"] is not None and entry["temp"] is not None]


bins = 20
fig4 = plt.figure()
plt.hist(calc_soc_data(fcharge + mcharge), bins, rwidth=0.9, zorder=2, label = "all aprticipants")
plt.hist(calc_soc_data(fcharge + mcharge), bins, rwidth=0.9, cumulative=True,label = "all participants (cum.)",
         zorder=1)
plt.xlabel("state of charge (percentage)")
plt.ylabel("frequency")
plt.legend()
plt.tight_layout()
plt.savefig("charge_start_by_soc.png")


fig5 = plt.figure()
plt.hist([calc_soc_data(fcharge), calc_soc_data(mcharge)], bins, normed=True, label=["female", "male"])
plt.xlabel("state of charge (percentage)")
plt.ylabel("probability density")
plt.legend()
plt.tight_layout()
plt.savefig("charge_start_by_soc_by_gender.png")

fig6 = plt.figure()
plt.hist([calc_soc_data(staff), calc_soc_data(students)], bins, normed=True,label=["staff/faculty", "students"])
plt.xlabel("state of charge (percentage)")
plt.ylabel("probability density")
plt.legend()
plt.tight_layout()
plt.savefig("charge_start_by_soc_by_occupation.png")
