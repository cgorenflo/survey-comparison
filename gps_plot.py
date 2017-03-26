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
        n=1
        t_tot = 0
        d_tot = 0
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

bins = 20

fig1 = plt.figure()
plt.hist([fspeed,mspeed], bins,normed=True)
plt.savefig("speed_by_gender.png")

fig2 = plt.figure()
plt.hist([staffspeed, studentsspeed],bins, normed=True)
plt.savefig("speed_by_occupation.png")

fig3 = plt.figure()
plt.hist(fspeed+mspeed, bins, normed=True, rwidth=0.9)
plt.savefig("speed_all.png")