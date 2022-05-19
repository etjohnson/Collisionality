import os
import ctypes


def is_user_admin(

):
    try:
        res = (os.getuid() == 0)
    except AttributeError:
        res = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return res


def list_users(

):

    return
