import sys
import os.path
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

from core.constants import const
from core.scrub import scrub
from core import data_import as df
from core import tictoc as tt

from features import latlong as lalo
from features import gen_scalars as sc_gen
from features import theta_radial as the_rad
from features.smooth import smooth

tt.tic()
p = 'proton'
a = 'alpha'
valid_enc = [4, 6, 7]
print('Current loaded encounters:', valid_enc, '\n')

# Choose which data set(s) to work with
h = 1
while h > 0:
    val = input('Full data set or single data set? (F/S)')
    if (val == 'F' or val == 'f'):
        enc = 0
        h = 0
    elif (val == 'S' or val == 's'):
        h = 0
        g = 1
        while g > 0:
            value = input('Please enter an encounter:')
            try:
                int(value)
                value_int = True
            except ValueError:
                value_int = False

            if value_int == True:
                if (int(value) in valid_enc):
                    enc = value
                    g = 0
                else:
                    print('Error: Please enter a valid encounter. \n')
            elif value_int == False:
                print('Error: Please enter a valid integer. \n')
            else:
                print('Error: Could not determine if the input was an integer.')
    elif (val == ''):
        print('Error: No input recieved. \n')
    else:
        print('Error: Please make a valid selection.')
x = const(enc, valid_enc)
print(x, '\n')
if enc == 0:
    dum_len = const.num_of_encs
else:
    dum_len = 1
    encount = const.encounter[0]

# Import data
mm_data = df.encounter_import()
print('\n')
sc_data = df.sc_import()
print('Data import complete.')

# Generate fill values

mm_len_max = 0
sc_len_max = 0

for x in const.encounter:
    print(x)
    for y in mm_data[x].keys():
        if len(mm_data[x][y]['time']) > mm_len_max:
            mm_len_max = len(mm_data[x][y]['time'])
            dum_encount = x
            dum_mm_file = y
        else:
            pass

    for y in sc_data[x].keys():
        if len(sc_data[x][y]) > sc_len_max:
            sc_len_max = len(sc_data[x][y])
            dum_encount = x
            dum_sc_craft = y
        else:
            pass

for x in const.encounter:
    if mm_len_max > sc_len_max or mm_len_max == sc_len_max:
        t_ = mm_data[dum_encount][dum_mm_file]['time']
    elif mm_len_max < sc_len_max:
        t_ = sc_data[dum_encount][dum_sc_craft]['time']

    for y in mm_data[x].keys():
        xp = mm_data[x][y]['time']
        for z in mm_data[x][y].keys():
            fp = mm_data[x][y][z]
            mm_data[x][y][z] = np.interp(t_, xp, fp)

    for y in sc_data[x].keys():
        xp = sc_data[x][y]['time']
        for z in sc_data[x][y].keys():
            fp = sc_data[x][y][z]
            sc_data[x][y][z] = np.interp(t_, xp, fp)

# Combine files if nessesory
print('Generating data file...', '\n')
solar_data = {}
spc_data = {}
solar_data[p] = {}
solar_data[a] = {}

for x in range(1):
    encount = const.encounter[x]
    for y in range(1):
        for z in mm_data[encount][const.encounter_names[y + 2 * x]].keys():
            solar_data[p][z] = []
        for z in mm_data[encount][const.encounter_names[1 + 2 * x]].keys():
            solar_data[a][z] = []
    for y in range(len(const.sc_names)):
        spc_data[const.sc_names[y]] = {}
        for z in sc_data[encount][const.sc_names[y]].keys():
            spc_data[const.sc_names[y]][z] = []

for x in const.encounter:
    for y in mm_data[x].keys():
        for z in mm_data[x][y]:
            solar_data[p][y].append(mm_data[x][y][z])
            solar_data[a][y].append(mm_data[x][y][z])

    for y in sc_data[x].keys():
        for z in sc_data[x][y]:
            spc_data[y].append(sc_data[x][y][z])

# Data scrubbing
print('Scrubbing data...')
if const.scrub == True:
    l = -1
    k = -1
    for x in solar_data.keys():
        l = l + 1
        for y in solar_data[x].keys():
            k = k + 1
            val = const.data_units[l][k]
            solar_data[x][y] = scrub(solar_data[x][y], const.var_min[val], const.var_max[val])
        print(f"{(l / len(solar_data)) * 100:.2f} %", end="\r")
        k = -1
    m = -1
    n = -1
    for x in spc_data.keys():
        m = m + 1
        for y in spc_data[x].keys():
            n = n + 1
            val = const.sc_units[l][k]
            spc_data[x][y] = scrub(spc_data[x][y], const.var_min[val], const.var_max[val])
        print(f"{(m / len(spc_data)) * 100:.2f} %", end="\r")
        n = -1
    sc_data[encount][const.sc_names[0]] = lalo.latlong_psp(sc_data[encount][const.sc_names[0]])
    sc_data[encount][const.sc_names[1]] = lalo.latlong_psp(sc_data[encount][const.sc_names[1]])
    print('Data Scrub Complete', '\n')
else:
    print('Note: Data scrub suppressed.', '\n')

# Generate temperatures and velocity magnitudes
print('Generating velocity magnitudes...')
scalar_velocity = sc_gen.scalar_velocity(solar_data)
print('Generating temperature file...', '\n')
scalar_temps = sc_gen.scalar_temps(solar_data)
# Generate single time set for the whole data set in approiate unit
solar_data['time'] = []
for i in range(len(solar_data[p]['time'])):
    solar_data['time'].append(df.epoch_time(solar_data[p]['time'][i]))
print('Note: Files have been generated and loaded in.', '\n')

plt.figure(figsize=(const.x_dim, const.y_dim))
plt.plot(solar_data['time'], solar_data[p]['np1'])
plt.show()

plt.figure(figsize=(const.x_dim, const.y_dim))
plt.plot(solar_data['time'], scalar_temps['theta_ap'])
plt.show()

plt.figure(figsize=(const.x_dim, const.y_dim))
plt.title('Histogram of α-proton relative temperatures', fontsize=22)
plt.ylabel('Probability density', fontsize=16)
plt.xlabel('α-proton relative temperature', fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.hist(smooth(scalar_temps['theta_ap'], 10), 500, density=True, alpha=0.75, histtype='step', linewidth=3, fill=False)
plt.xlim([0, 15])
plt.grid()
plt.show()

#
time = solar_data[p]['time']
density_p = solar_data[p]['np1']
temp = scalar_temps['proton_1_k']
speed = solar_data[p]['v_mag']
density_a = np.interp(time, solar_data[a]['time'], solar_data[a]['na'])
theta = np.interp(time, solar_data[a]['time'], scalar_temps['theta_ap'])
wind_radius = np.full(shape=len(spc_data[const.sc_names[1]]['time']), fill_value=1, dtype=int)
psp_radius = np.interp(time, spc_data[const.sc_names[0]]['time'], spc_data[const.sc_names[0]]['RADIAL_DISTANCE_AU'])

#final_theta = the_rad.tr(time, density_p, temp, speed, density_a, theta, wind_radius, psp_radius, False)

tt.toc()
