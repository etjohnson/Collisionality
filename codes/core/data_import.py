import os
import numpy as np
import pandas as pd
from core.constants import const
from core.load import file_import as fimp


def encounter_import(

):
    files = {}

    for i in range(const.num_of_encs):
        print('Data File: ' + const.encounter[i])
        files[const.encounter[i]] = {}
        for j in range(2):
            val = str(const.encounter[i] + '/' + const.encounter_names[j + 2 * i])
            files[const.encounter[i]][const.encounter_names[j + 2 * i]] = fimp.file_import(const.str_dir + val)
    return files


def sc_import(

):
    files = {}

    for i in range(const.num_of_encs):
        print('Spacecraft for ' + const.encounter[i])
        files[const.encounter[i]] = {}
        for key in const.sc_names:
            val = str(const.encounter[i] + '/Position/' + key)
            files[const.encounter[i]][key] = fimp.file_import(const.str_dir + val)
    print('\n',
          'Warning: Please ensure all data is in the correct time range for the encounter.',
          '\n')
    return files



def epoch_time(
        epoch_time,
):
    import datetime
    res = datetime.datetime.fromtimestamp(epoch_time)

    return res


def error_import(

):
    files = {}

    for i in range(const.num_of_encs):
        print('Error File: ' + const.encounter[i])
        files[const.encounter[i]] = {}
        for j in range(2):
            val = str(const.encounter[i] + '/' + const.encounter_errors[j + 2 * i])
            files[const.encounter[i]][const.encounter_errors[j + 2 * i]] = fimp.file_import(const.str_dir + val)
    return files
