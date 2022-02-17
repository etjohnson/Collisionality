import sys
import os.path
import numpy as np
import matplotlib.pyplot as plt

from core import constants as const
from core import tictoc 


tic()

valid_enc = [4,6,7]

print('Current loaded encounters:', valid_enc)

h = 1
while h > 0:
    val = input('Please enter which encounter to analysis:')
    if (int(val) in valid_enc):
        enc = val
        h = 0
    else:
        print('Error: Please enter a valid encounter.')







toc()


