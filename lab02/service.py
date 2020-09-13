import numpy as np

def rgb_to_string(r,g,b):
    return '#%02x%02x%02x' % (r, g, b)

def permutate_array(y_x):
    intensities = y_x[0]
    counts = y_x[1]
    max = np.amax(counts)
    counts = counts/max
    counts *= 100
    return dict(zip(intensities,counts))