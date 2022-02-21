import sys
import numpy as np

default_min = 0
default_max = 10**30

def scrub(
    array,
    min_val = default_min,
    max_val = default_max,
):
    r"""
    Input: Array to be scrubbed, minimum value, maximum value.

    Example:
    from features.scrub import scrub
    x = scrub([0,4],0,2)

    Return: Sorted array.
    """

    #---#

    if type(min_val) == int or type(min_val) == float:
        pass
    else:
        raise TypeError(
                f"Argument '{min_val}' and '{max_val}' must be numbers"
                f"instead get type '{min_val.shape}' and '{max_val.shape}'."
                )
    if type(max_val) == int or type(max_val) == float:
        pass
    else:
        raise TypeError(
                f"Argument '{min_val}' and '{max_val}' must be numbers"
                f"instead get type '{min_val.shape}' and '{max_val.shape}'."
                )
    
    for i in range(len(array)):
        array[i] = array[i]
        if abs(array[i]) > max_val:
            if i == 0:
                array[i] = 0
            else:
                array[i] = array[i-1]
        elif abs(array[i]) < min_val:
            if i == 0:
                array[i] = 0
            else:
                array[i] = array[i-1]
        else:
            array[i] = array[i]

        
    return array
    
