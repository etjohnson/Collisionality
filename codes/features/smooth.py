import sys
import numpy as np

def smooth(
    y,
    box_pts = 1,
):

    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    
    return y_smooth
