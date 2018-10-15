import numpy as np

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
