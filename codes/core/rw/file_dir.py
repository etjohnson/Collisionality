import os
import pathlib


def dir_path(

):
    directory = os.getcwd()
    path = str(pathlib.Path(directory).parent)

    return path


parent_path = dir_path(


def dir_make(
        name,
        loc=parent_path,
):
    if not isinstance(name, str):
        raise TypeError(
            f"Directory name passed is not a string, "
            f"instead got {type(name)}"
        )

    path = slash_check(loc) + name  # jws

    os.mkdir(path)

    return


def file_list(
        loc=parent_path,
):
    path = slash_check(loc)
    res = next(os.walk(path))[2]

    return res


def file_num(
        loc=parent_path,
):
    L = file_list(loc)
    res = len(L)

    return res


def folder_list(
        loc=parent_path,
):
    path = slash_check(loc)
    res = next(os.walk(path))[1]

    return res


def folder_num(
        loc=parent_path,
):
    L = folder_list(loc)
    res = len(L)

    return res


def dir_list(
        loc=parent_path,
):
    path = slash_check(loc)
    res = os.listdir(path)

    return res


def dir_num(
        loc=parent_path,
):
    L = dir_list(loc)
    res = len(L)

    return res


