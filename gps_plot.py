from geopy.distance import vincenty
import ast
from iss4e.webike.trips.auxiliary import DateTime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def read (file_name):
    with open(file_name, mode='r') as file:
        return ast.literal_eval(file.read())

fgps = read("fgps")
mgps = read("mgps")
staffgps = read("staffgps")
studentsgps = read("studentsgps")


def get_average_speed(gps_by_trips):
    speeds = []
    for trip in gps_by_trips:
        v = 0
        for i in range(len(trip) - 1):
            t = DateTime(trip[i + 1]["time"]) - DateTime(trip[i]["time"]).totalseconds() / 3600
            d = vincenty((trip[i]["latitude"], trip[i]["longitude"]),
                         (trip[i + 1]["latitude"], trip[i + 1]["longitude"])).km
            v += 1 / i(d / t - v)
        speeds.append(v)
    return speeds


fspeed = get_average_speed(fgps)
mspeed = get_average_speed(mgps)
staffspeed = get_average_speed(staffgps)
studentsspeed = get_average_speed(studentsgps)

fig1 = plt.figure()
plt.hist([fspeed,mspeed], normed=True)
plt.savefig("speed_by_gender.png")

fig2 = plt.figure()
plt.hist([staffspeed, studentsspeed], normed=True)
plt.savefig("speed_by_occupation.png")

fig3 = plt.figure()
plt.hist(fspeed+mspeed, normed=True, rwidth=0.9)
plt.savefig("speed_all.png")