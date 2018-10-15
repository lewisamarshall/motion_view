import numpy as np
import numpy.linalg as linalg
from skimage import io, color

def max_difference(frame, reference):
    frame = color.rgb2hsv(frame)
    reference = color.rgb2hsv(reference)
    return np.max(np.abs(frame-reference), axis=-1)

def distance(frame, reference):
    frame = color.rgb2hsv(frame)
    reference = color.rgb2hsv(reference)
    return linalg.norm((frame-reference), axis=-1)

def normalized_distance(frame, reference):
    diff = frame-reference
    normalizer = io.imread('std_percent.png')
    ndiff = diff / normalizer
    return linalg.norm(ndiff, axis=-1)

def hue(frame, reference):
    pass
