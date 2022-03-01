import sys
import os.path
import numpy as np
import matplotlib.pyplot as plt

from core.constants import const
from core.scrub import scrub
from core import data_import as df
from core import tictoc as tt

from features import latlong as lalo
from features import gen_scalars as sc_gen
from features import theta_radial as the_rad

tt.tic()
p = 'proton'
a = 'alpha'
valid_enc = [4,6,7]
print('Current loaded encounters:', valid_enc, '\n')


#Choose which data set(s) to work with
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

	
#Import data
mm_data = df.encounter_import()
print('\n')
sc_data = df.sc_import()
print('Data import complete.')


#Combine files if nessesory
print('Generating data file...','\n')
solar_data = {}
spc_data = {}
solar_data[p] = {}
solar_data[a] = {}
for x in range(1):
    encount = const.encounter[x]
    for y in range(1):
        for z in mm_data[encount][const.encounter_names[y + 2*x]].keys():
            solar_data[p][z] = []
        for z in mm_data[encount][const.encounter_names[1 + 2*x]].keys():
            solar_data[a][z] = []
    for y in range(len(const.sc_names)):
        spc_data[const.sc_names[y]] = {}
        for z in sc_data[encount][const.sc_names[y]].keys():
            spc_data[const.sc_names[y]][z] = []

for x in range(dum_len):
	encount = const.encounter[x]
	for y in range(1):
		for z in solar_data[p].keys():
			for w in range(len(mm_data[encount][const.encounter_names[y + 2*x]][z])):
				solar_data[p][z].append(mm_data[encount][const.encounter_names[y + 2*x]][z][w])
		for z in solar_data[a].keys():
			for w in range(len(mm_data[encount][const.encounter_names[2*x + 1]][z])):
				solar_data[a][z].append(mm_data[encount][const.encounter_names[2*x + 1]][z][w])
	for y in const.sc_names:
		for z in spc_data[y].keys():
			for w in range(len(sc_data[encount][y][z])):
				spc_data[y][z].append(sc_data[encount][y][z][w])

                                      
#Generate fill values
solar_lens = []
spc_lens = []
for x in solar_data.keys():
	solar_lens.append(len(solar_data[x]['time']))
for x in spc_data.keys():
	spc_lens.append(len(spc_data[x]['time']))

solar_len_max = max(solar_lens)
spc_len_max = max(spc_lens)

if solar_len_max > spc_len_max or solar_len_max == spc_len_max:
	index_loc = solar_lens.index(solar_len_max)
	if isinstance(index_loc, int):
		t_ = solar_data[p]['time']
	else:
		t_ = solar_data[a]['time']
elif spc_len_max > solar_len_max:
	index_loc = spc_lens.index(spc_len_max)
	t_ = spc_data[const.sc_names[index_loc]]['time']
else:
	raise Exception('Fatal Error: Length of arrays could not be determined.')

for x in solar_data.keys():
	xp = solar_data[x]['time']
	for y in solar_data[x].keys():
		fp = solar_data[x][y]
		solar_data[x][y] = np.interp(t_,xp,fp)
for x in spc_data.keys():
	xp = spc_data[x]['time']
	for y in spc_data[x].keys():
		fp = spc_data[x][y]
		spc_data[x][y] = np.interp(t_,xp,fp)
	

#Data scrubbing
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
		k = -1
	m = -1
	n = -1
	for x in spc_data.keys():            
		m = m + 1
		for y in spc_data[x].keys():
			n = n + 1
			val = const.sc_units[l][k]
			spc_data[x][y] = scrub(spc_data[x][y], const.var_min[val], const.var_max[val])
		n = -1        
	sc_data[encount][const.sc_names[0]] = lalo.latlong_psp(sc_data[encount][const.sc_names[0]])
	sc_data[encount][const.sc_names[1]] = lalo.latlong_psp(sc_data[encount][const.sc_names[1]]) 
	print('Data Scrub Complete', '\n')
else:
    print('Note: Data scrub suppressed.','\n')
	
		
#Generate temperatures and velocity magnitudes
print('Generating velocity magnitudes...')
scalar_velocity = sc_gen.scalar_velocity(solar_data)
print('Generating temperature file...','\n')
scalar_temps = sc_gen.scalar_temps(solar_data)
#Generate single time set for the whole data set in approiate unit
solar_data['time'] = []
for i in range(len(solar_data[p]['time'])):
	solar_data['time'].append(df.epoch_time(solar_data[p]['time'][i]))
print('Note: Files have been generated and loaded in.','\n')


plt.plot(solar_data['time'], solar_data[p]['np1'])
plt.plot(solar_data['time'], solar_data[p]['np2'])
plt.yscale('log')
plt.show()

#
time = solar_data[p]['time']
density_p = solar_data[p]['np1']
temp = scalar_temps['proton_1_k']
speed = solar_data[p]['v_mag']
density_a = np.interp(time,solar_data[a]['time'], solar_data[a]['na'])
theta = np.interp(time, solar_data[a]['time'], scalar_temps['theta_ap'])
wind_radius = np.full(shape=len(spc_data[const.sc_names[1]]['time']),fill_value=1,dtype=int)
psp_radius = np.interp(time, spc_data[const.sc_names[0]]['time'], spc_data[const.sc_names[0]]['RADIAL_DISTANCE_AU'])

#final_theta = the_rad.tr(time, density_p, temp, speed, density_a, theta, wind_radius, psp_radius, True)


tt.toc()


