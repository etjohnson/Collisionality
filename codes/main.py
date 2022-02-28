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

	
#Import data
mm_data = df.encounter_import()
print('\n')
sc_data = df.sc_import()
print('Data import complete.')
print('\n')


#Data scrubbing
print('Scrubbing data...')

if enc == 0:
    dum_len = const.num_of_encs
else:
    dum_len = 1
    encount = const.encounter[0]

if const.scrub == True:
    for x in range(dum_len):
        l = -1
        k = -1
        encount = const.encounter[x]         
        for y in range(2):
            l = l + 1
            for z in mm_data[encount][const.encounter_names[y + 2*x]].keys():
                k = k + 1
                val = const.mm_units[l][k]
                mm_data[encount][const.encounter_names[y + 2*x]][z] = scrub(mm_data[encount][const.encounter_names[y + 2*x]][z], const.var_min[val], const.var_max[val])
            k = -1
            
        m = -1
        n = -1
        for y in range(const.num_of_sc):
            m = m + 1
            for z in sc_data[encount][const.sc_names[y]].keys():
                n = n + 1
                val = const.sc_units[l][k]
                sc_data[encount][const.sc_names[y]][z] = scrub(sc_data[encount][const.sc_names[y]][z], const.var_min[val], const.var_max[val])
            n = -1
            
        sc_data[encount][const.sc_names[0]] = lalo.latlong_psp(sc_data[encount][const.sc_names[0]])
        sc_data[encount][const.sc_names[1]] = lalo.latlong_psp(sc_data[encount][const.sc_names[1]])
        
    print('Data Scrub Complete')
else:
    print('Note: Data scrub suppressed.')
print('\n')


#Combine files if nessesory
print('Generating data file...')
tot_len_proton = 0
tot_len_alpha = 0
tot_len_spc = 0
for x in range(dum_len):
    encount = const.encounter[x]
    for y in range(1):
        tot_len_proton = tot_len_proton + len(mm_data[encount][const.encounter_names[2*x + y]]['time'])
    for y in range(1):
        tot_len_alpha = tot_len_alpha + len(mm_data[encount][const.encounter_names[2*x + 1]]['time'])
    for y in range(len(const.sc_names)):
        tot_len_spc = tot_len_spc + len(sc_data[encount][const.sc_names[y]]['time'])

p = 'proton'
a = 'alpha'
solar_data = {}
spc_data = {}
adjust = 0
for x in range(dum_len):
    encount = const.encounter[x]
    solar_data[p] = {}
    solar_data[a] = {}
    for y in range(1):
        for z in mm_data[encount][const.encounter_names[y + 2*x]].keys():
            solar_data[p][z] = []
            for w in range(len(mm_data[encount][const.encounter_names[y + 2*x]][z])):
                solar_data[p][z].append(mm_data[encount][const.encounter_names[2*x + y]][z][w])
        for z in mm_data[encount][const.encounter_names[1 + 2*x]].keys():
            solar_data[a][z] = []
            for w in range(len(mm_data[encount][const.encounter_names[1 + 2*x]][z])):
                solar_data[a][z].append(mm_data[encount][const.encounter_names[2*x + 1]][z][w])

    for y in range(len(const.sc_names)):
        spc_data[const.sc_names[y]] = {}
        for z in sc_data[encount][const.sc_names[y]].keys():
            spc_data[const.sc_names[y]][z] = []
            for w in range(len(sc_data[encount][const.sc_names[y]][z])):
                spc_data[const.sc_names[y]][z].append(sc_data[encount][const.sc_names[y]][z][w])
                                        

#Generate temperatures and velocity magnitudes
print('Generating velocity magnitudes...')
scalar_velocity = sc_gen.scalar_velocity(solar_data)
print('Generating temperature file...')
scalar_temps = sc_gen.scalar_temps(solar_data)
print('Note: Files have been generated and loaded in.')


#
time = solar_data[p]['time']
density_p = solar_data[p]['np1']
temp = scalar_temps['proton_1_k']
speed = solar_data[p]['v_mag']
density_a = np.interp(time,solar_data[a]['time'], solar_data[a]['na'])
theta = np.interp(time, solar_data[a]['time'], scalar_temps['theta_ap'])
wind_radius = np.full(shape=len(spc_data[const.sc_names[1]]['time']),fill_value=1,dtype=int)
psp_radius = np.interp(time, spc_data[const.sc_names[0]]['time'], spc_data[const.sc_names[0]]['RADIAL_DISTANCE_AU'])

final_theta = the_rad.tr(time, density_p, temp, speed, density_a, theta, wind_radius, psp_radius, True)


tt.toc()


