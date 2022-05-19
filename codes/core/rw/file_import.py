import pandas as pd
import numpy as np
from core.rw.file_types import types

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
            data = csv_load(location)
        elif file_ext == valid_file_types[1]:
            data = excel_load(location)
        elif file_ext == valid_file_types[2]:
            data = pickle_load(location)
        else:
            raise ValueError(
                "File type is missing."
            )
    else:
        raise TypeError(
            "The file type is unsupported, please try a different file type."
        )

    result = {}
    for key in data.keys():
        new_key = key.replace('+AF8-', '_')
        result[new_key] = np.array(data[key])

    return result


def csv_load(
        location,
):
    if not isinstance(location, str):
        raise ValueError(
            f"Argument '{location}' should be a string,"
            f"instead got '{location.type}'."
        )

    res = pd.read_csv(location)

    return res


def excel_load(
        location,
):
    if not isinstance(location, str):
        raise ValueError(
            f"Argument '{location}' should be a string,"
            f"instead got '{location.type}'."
        )

    res = pd.read_excel(location)

    return res


def pickle_load(
        location,
):
    if not isinstance(location, str):
        raise ValueError(
            f"Argument '{location}' should be a string,"
            f"instead got '{location.type}'."
        )

    res = pd.to_pickle(location)

    return res
