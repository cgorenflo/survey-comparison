from geopy.distance import vincenty
import ast
from iss4e.webike.trips.auxiliary import DateTime
from scipy import stats
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def read (file_name):
    with open(file_name, mode='r') as file:
        return ast.literal_eval(file.read())

fgps = read("data/fgps")
mgps = read("data/mgps")
staffgps = read("data/staffgps")
studentsgps = read("data/studentsgps")


def get_average_speed(gps_by_trips):
    speeds = []
    for trip in gps_by_trips:
        t_tot = 0
        d_tot = 0
        if(len(trip) <5):
            continue
        for i in range(len(trip) - 1):
            t = (DateTime(trip[i + 1]["time"]) - DateTime(trip[i]["time"])).total_seconds()	    
            if(t !=0):                
                d = vincenty((trip[i]["latitude"], trip[i]["longitude"]),
                         (trip[i + 1]["latitude"], trip[i + 1]["longitude"])).m
                if(d/t*3.6 > 3 and d/t*3.6 < 60):
                    t_tot +=t
                    d_tot += d
        if(trip and t_tot > 0): 
            speeds.append(d_tot/t_tot*3.6)
    return speeds


fspeed = get_average_speed(fgps)
mspeed = get_average_speed(mgps)
staffspeed = get_average_speed(staffgps)
studentsspeed = get_average_speed(studentsgps)

bins = np.arange(0,61,2.5)

fig1 = plt.figure()
print(stats.ranksums(fspeed, mspeed))
plt.hist([fspeed,mspeed], bins=bins,normed=True, label=["female", "male"])
plt.xlabel("speed (kph)")
plt.ylabel("probability")
plt.legend()
plt.tight_layout()
plt.savefig("speed_by_gender.png")

fig2 = plt.figure()
print(stats.ranksums(staffspeed, studentsspeed))
plt.hist([staffspeed, studentsspeed],bins=bins, normed=True, label=["staff/faculty","students"])
plt.xlabel("speed (kph)")
plt.ylabel("probability")
plt.legend()
plt.tight_layout()
plt.savefig("speed_by_occupation.png")

fig3 = plt.figure()
plt.hist(fspeed+mspeed, bins=bins, normed=True, rwidth=0.9, label="all participants")
plt.xlabel("speed (kph)")
plt.ylabel("probability")
plt.legend()
plt.tight_layout()
plt.savefig("speed_all.png")
