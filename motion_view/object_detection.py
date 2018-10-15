import numpy as np
from skimage.filters import threshold_otsu

def otsu(difference):
    thresh = threshold_otsu(difference)
    return (difference>thresh)

def threshold(difference, thresh=8):
    return (difference>thresh)

def waterfall_single_object(frame, reference):
    pass
