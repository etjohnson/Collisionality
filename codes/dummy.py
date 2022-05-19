from core.rw import file_dir as fd
from core.security import users as usr

path = fd.dir_path()

x = usr.list_users()
print(x)
