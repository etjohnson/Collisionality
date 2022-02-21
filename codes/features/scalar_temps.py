import sys
import numpy as np
from core.constants import *

def generate_scalar_temps(
    data,
):
    
    key_names = {}
    file_names = []
    for file in data:
        file_names.append(file)
        key_names[file] = []
        for key in file:
            key_names[file] = data[file].keys()

    proton = const.encounter_names[0]
    alpha = const.encounter_names[1]
    
    factor = 11604
    
    length = []
    for file in data:
        val = str(list(data[file].keys())[0])
        length.append(len(data[file][val]))
        
    result = {}
    result_keys = ['proton_scalar_temp_1','proton_scalar_temp_2','alpha_scalar_temp','theta_ap','dens_ap','proton_perpar','alpha_perpar','proton_1_k','alpha_k']
    
    result[result_keys[0]] = np.zeros(length[0])
    result[result_keys[1]] = np.zeros(length[0])
    result[result_keys[2]] = np.zeros(length[1])
    result[result_keys[3]] = np.zeros(length[1])
    result[result_keys[4]] = np.zeros(length[1])
    result[result_keys[5]] = np.zeros(length[0])
    result[result_keys[6]] = np.zeros(length[1])
    
    result['proton_1_k'] = np.zeros(length[0])
    result['alpha_k'] = np.zeros(length[1])
    
    for i in range(length[0]):
        val = 'Tperp1'
        result[result_keys[0]][i] = ((2*data[proton][val][i] + data[proton]['Trat1'][i])/3) 
        result[result_keys[1]][i] = ((2*data[proton]['Tperp2'][i] + data[proton]['Trat2'][i])/3)
        result[result_keys[5]][i] = data[proton][val][i]/data[proton]['Trat1'][i]
        result['proton_1_k'][i] = result[result_keys[0]][i]*factor
        
    for i in range(length[1]):
        result[result_keys[2]][i] = (2*data[alpha]['Ta_perp'][i] + data[alpha]['Trat'][i])/3
        result[result_keys[3]][i] = result[result_keys[2]][i]/result[result_keys[0]][i]
        result[result_keys[6]][i] = data[alpha]['Ta_perp'][i]/data[alpha]['Trat'][i]      
        result['alpha_k'][i] = result[result_keys[2]][i]*factor
         

        if data[proton]['np1'][i] == 0:
            result[result_keys[4]][i] = 0
        else:    
            result[result_keys[4]][i] = data[alpha]['na'][i]/data[proton]['np1'][i]
          
    return result
    
