import numpy as np
from skimage.filters import threshold_otsu, sobel
from skimage import io, morphology

def otsu(difference, closing=True):
    thresh = threshold_otsu(difference)
    print(f'Otsu threshold: {thresh}')
    result = difference > thresh
    if closing:
        result = morphology.binary_closing(result, np.ones((5, 5)))
    return result

def threshold(difference, thresh=.1, closing=True):
    result = difference > thresh
    if closing:
        pass
        result = morphology.binary_erosion(result)
        result = morphology.binary_dilation(result, np.ones((10, 10)))
    return result

def watershed(difference, debug=True):
    elevation_map = sobel(difference)
    markers = np.zeros_like(difference)
    markers[elevation_map<1]=1
    markers[elevation_map>10]=2
    segmentation = morphology.watershed(elevation_map, markers)
    if debug: io.imsave('elevation_map.png', elevation_map.astype('uint8'))
    if debug: io.imsave('segments.png', segmentation.astype('uint8')*10)
    return segmentation
