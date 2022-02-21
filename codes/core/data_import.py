import os
import numpy as np
import pandas as pd
from core.constants import const

def encounter_import(

):
    files = {}

    for i in range(const.num_of_encs):
        print('Data File: ' + const.encounter[i])
        files[const.encounter[i]] = {}
        for j in range(2):
            val = str(const.encounter[i] + '/' + const.encounter_names[j +2*i])
            files[const.encounter[i]][const.encounter_names[j + 2*i]] = file_import(val, const.str_dir)
    return files

def sc_import(

):

    files = {}    

    for i in range(const.num_of_encs):
        print('Spacecraft for ' + const.encounter[i])
        files[const.encounter[i]] = {}
        for key in const.sc_names:
            val = str(const.encounter[i] + '/Position/' + key)
            files[const.encounter[i]][key] = file_import(val,const.str_dir)
    print('\n')
    print('Warning: Please ensure all data is in the correct time range for the encounter.')
    print('\n')
    return files



def file_import(
    load_location,
    str_dir = '',
):

    r"""
    Input: Load location, string directory.

    Return: Data from file loaded into an array.
    """

    #---#

    #---#


    for arg_name in ("load_location","str_dir"):
        val = locals()[arg_name]
        if not isinstance(arg_name, str):
            raise ValueError(
                f"Argument '{val}' should be a string,"
                f"instead got '{val.type}'."
            )

    print(str_dir+load_location)

    data = pd.read_csv(str_dir+load_location)
    result = {}
    for key in data.keys():
        result[key] = np.array(data[key])

    return result
