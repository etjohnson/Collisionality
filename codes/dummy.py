from core.rw import file_dir as fd
from core.security import users as usr
from core.variables import bool_man as bm

path = fd.dir_path()

print('dfs')
x = True
y = False

z = bm._and(x, y)
print(z)

