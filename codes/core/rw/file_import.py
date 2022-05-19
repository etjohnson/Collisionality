import os
import pathlib
import pandas as pd
import numpy as np
from core.rw.file_types import types

import csv

res = types()
valid_file_types = types.valid_file_types


def file_import(
        location,
):
    if not isinstance(location, str):
        raise ValueError(
            f"Argument '{location}' should be a string,"
            f"instead got '{location.type}'."
        )

    arg_ = location.partition(".")
    file_ext = arg_[-1]

    if file_ext in valid_file_types:
        if file_ext == valid_file_types[0]:
            data = pd.read_csv(location)
        elif file_ext == valid_file_types[1]:
            print('sdfdsf')
    else:
        raise TypeError(
            "The file type is unsupported, please try a different file type."
        )

    result = {}
    for key in data.keys():
        new_key = key.replace('+AF8-', '_')
        result[new_key] = np.array(data[key])

    return result
