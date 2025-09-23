from sgp4.api import Satrec, jday
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os

def read_tle_file(filename):
    satellites = []
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
        for i in range(0, len(lines), 3):
            if i+2 < len(lines):
                name, line1, line2 = lines[i], lines[i+1], lines[i+2]
                satellites.append((name, line1, line2))
    return satellites

# Read TLEs from file in the same folder
tle_file = os.path.join(os.path.dirname(__file__), 'tle_list.txt')
satellites = read_tle_file(tle_file)

# Build time vector (e.g., 2 hours, 1-minute steps)
start = datetime.datetime.utcnow()
minutes = np.arange(0, 120, 1)

fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot(111, projection='3d')

# Earth sphere
u, v = np.mgrid[0:2*np.pi:40j, 0:np.pi:20j]
earth_x = 6371 * np.cos(u) * np.sin(v)
earth_y = 6371 * np.sin(u) * np.sin(v)
earth_z = 6371 * np.cos(v)
ax.plot_surface(earth_x, earth_y, earth_z, color='lightblue', alpha=0.5)

colors = ['r', 'g', 'b', 'm', 'c', 'y']
for idx, (name, line1, line2) in enumerate(satellites):
    sat = Satrec.twoline2rv(line1, line2)
    xs, ys, zs = [], [], []
    for m in minutes:
        dt = start + datetime.timedelta(minutes=int(m))
        jd, fr = jday(dt.year, dt.month, dt.day,
                      dt.hour, dt.minute, dt.second + dt.microsecond*1e-6)
        e, r, v = sat.sgp4(jd, fr)
        if e == 0:
            xs.append(r[0])
            ys.append(r[1])
            zs.append(r[2])
    color = colors[idx % len(colors)]
    ax.plot(xs, ys, zs, color, label=name)

ax.set_xlabel('X (km)')
ax.set_ylabel('Y (km)')
ax.set_zlabel('Z (km)')
ax.legend(loc='best')
plt.show()
