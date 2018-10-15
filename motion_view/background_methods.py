import numpy as np
from skimage import io

def median(images):
    images = np.stack(images)
    median = np.median(images, axis=0)
    return median.astype(int)

def minimum(images):
    return np.min(images, axis=0)

def maximum(images):
    return np.max(images, axis=0)

def std(images):
    images = np.stack(images)
    result = np.std(images, axis=0)
    return result.astype(int)

def std_percent(images):
    median = io.imread('median.png')
    images = np.stack([np.abs(i.astype(float)-median.astype(float)) for i in images])
    result = np.percentile(images, 95, axis=0)
    return (result).astype('uint8')
