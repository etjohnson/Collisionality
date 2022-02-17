import sys
import os.path
import numpy as np
import matplotlib.pyplot as plt

from core.constants import const
from core import tictoc as tt

tt.tic()

valid_enc = [4,6,7]
print('Current loaded encounters:', valid_enc)


#Choose which data set(s) to work with
h = 1 
while h > 0:
	val = input('Full data set or single data set? (F/S)')
	if (val == 'F' or val == 'f'):
		enc = 0
		h = 0
	elif (val == 'S' or val == 's'):
		value = input('Please enter an encounter:')
		try: 
			int(value)
			value_int = True
		except ValueError:
			value_int = False
		if value_int == True:
			if (int(value) in valid_enc):
				enc = value
				h = 0
			else: 
				print('Error: Please enter a valid encounter.')
		elif value_int == False:
			print('Error: Please enter a valid integer.')
	elif (val == ''):
		print('Error: No input recieved.')
	else:
		print('Error: Please make a valid selection.')
		
x = const(enc, valid_enc)
print(x, '\n')

	
#Import data





print('Data import complete. \n')





tt.toc()


