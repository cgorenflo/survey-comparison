import ast
from iss4e.webike.trips.auxiliary import DateTime
import webike.data.SoC as soc
import matplotlib
import trip_plots

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pytz import timezone


eastern = timezone('Canada/Eastern')

def to_datetime(time):
    return DateTime(time)._datetime.replace(tzinfo=timezone('UTC')).astimezone(eastern)


with open("fstaff", mode='r') as file:
    fstaff = [ast.literal_eval(line) for line in file.read().splitlines()]
    for line in fstaff:
        line["time"] = to_datetime(line["time"])
with open("mstaff", mode='r') as file:
    mstaff = [ast.literal_eval(line) for line in file.read().splitlines()]
    for line in mstaff:
        line["time"] = to_datetime(line["time"])
with open("fstuds", mode='r') as file:
    fstuds = [ast.literal_eval(line) for line in file.read().splitlines()]
    for line in fstuds:
        line["time"] = to_datetime(line["time"])
with open("mstuds", mode='r') as file:
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
    len(staff + students) / (len(trip_plots.male_staff) + len(trip_plots.male_students) + len(trip_plots.female_staff) + len(trip_plots.female_students)))))
print("avg no. charges male: {charge}".format(charge=str(len(mcharge) / (len(trip_plots.male_staff) + len(trip_plots.male_students)))))
print("avg no. charges female: {charge}".format(charge=str(len(fcharge) / (len(trip_plots.female_staff) + len(trip_plots.female_students)))))
print("avg no. charges staff: {charge}".format(charge=str(len(staff) / (len(trip_plots.female_staff) + len(trip_plots.male_staff)))))
print("avg no. charges students: {charge}".format(
    charge=str(len(students) / (len(trip_plots.male_students) + len(trip_plots.female_students)))))

print("no. trips per charge: {charge}".format(charge=str(len(trip_plots.staff + trip_plots.students)/ len(staff + students))))
print("no. trips per charge male: {charge}".format(charge=str(len(trip_plots.mtrips)/ len(mcharge))))
print("no. trips per charge female: {charge}".format(charge=str(len(trip_plots.ftrips)/len(fcharge))))
print("no. trips per charge staff: {charge}".format(charge=str(len(trip_plots.staff )/len(staff))))
print("no. trips per charge students: {charge}".format(charge=str(len(trip_plots.students)/len(students))))

fig1 = plt.figure()
plt.hist([[entry["time"].hour for entry in fcharge], [entry["time"].hour for entry in mcharge]], 24, normed=True)
plt.savefig("charge_start_by_gender.png")

fig2 = plt.figure()
plt.hist([[entry["time"].hour for entry in staff], [entry["time"].hour for entry in students]], 24, normed=True)
plt.savefig("charge_start_by_occupation.png")

fig3 = plt.figure()
plt.hist([entry["time"].hour for entry in fcharge + mcharge], 24, normed=True, rwidth=0.9)
plt.savefig("charge_start_all.png")

fig4 = plt.figure()
plt.hist([soc.calc_soc(soc.choose_temp(entry["temp"]),entry["voltage"]) for entry in fcharge + mcharge if entry["voltage"] is not None and entry["temp"] is not None], normed = True, rwidth=0.9)
plt.savefig("charge_start_by_soc.png")