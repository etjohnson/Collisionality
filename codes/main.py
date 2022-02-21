import sys
import os.path
import numpy as np
import matplotlib.pyplot as plt

from core.constants import const
from core.scrub import scrub
from core import data_import as df
from core import tictoc as tt

from features import latlong as lalo

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

if const.scrub == True:
    for x in range(dum_len):
        l = -1
        k = -1
        
        if enc == 0:
            encount = const.encounter[x]
        else:
            encount = const.encounter[0]
            
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


#    
    




tt.toc()


