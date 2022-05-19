import os
import ctypes


class AdminStateUnknownError(Exception):
    print("Error: Cannot determine privilege level.")
    pass


def is_user_admin(

):
    try:
        return os.geteuid() == 0
    except AttributeError:
        pass
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except AttributeError:
        raise AdminStateUnknownError


