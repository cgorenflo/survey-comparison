import ast
from iss4e.webike.trips.auxiliary import DateTime
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

fig1 = plt.figure()
plt.hist([[entry["time"].hour for entry in fcharge], [entry["time"].hour for entry in mcharge]], 24, normed=True)
plt.savefig("charge_start_by_gender.png")

fig2 = plt.figure()
plt.hist([[entry["time"].hour for entry in staff], [entry["time"].hour for entry in students]], 24, normed=True)
plt.savefig("charge_start_by_occupation.png")

fig3 = plt.figure()
plt.hist([entry["time"].hour for entry in fcharge + mcharge], 24, normed=True, rwidth=0.9)
plt.savefig("charge_start_all.png")
