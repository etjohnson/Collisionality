import sys
import os.path
import numpy as np
import matplotlib.pyplot as plt

from core.constants import const
from core import data_import as df
from core import tictoc as tt

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
spdf_data = 0

print(mm_data)

#Data scrubbing
print('\n')
print('Scrubbing data...')


if const.scrub == True:
    for x in range(const.num_of_encs):
        l = -1
        k = -1
        for i in const.encounter_names[x]:
            l = l + 1
            for j in mm_data[const.encounter[x]][i].keys():
               k = k + 1
               val = const.mm_units[l][k]
               mm_data[const.encounter[x]][i][j] = scrub(mm_data[const.encounter[x]][i][j],const.var_min[val],const.var_max[val])
            k = - 1

        l = -1
        k = -1
        for i in const.spacecraft_names:
            l = l + 1
            for j in spdf_data[i].keys():
                k = k + 1
                val = const.spdf_units[l][k]
                spdf_data[i][j] = scrub(spdf_data[i][j],const.var_min[val],const.var_max[val])
            k = - 1

    print('Data Scrub Complete')
else:
    print('Note: Data scrub suppressed.')
print('\n')








print('Data import complete. \n')





tt.toc()


