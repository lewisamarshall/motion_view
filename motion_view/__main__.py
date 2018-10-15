import skimage
from skimage import io
import pims
import click
import numpy as np


def background(images):
    images = np.stack(images)
    median = np.median(images, axis=0)
    median = median.astype(int)
    minima = np.min(images, axis=0)
    maxima = np.max(images, axis=0)
    io.imsave('minima.png', minima)
    io.imsave('maxima.png', maxima)
    io.imsave('median.png', median)

def motion_image(images):
    bg = io.imread('median.png')
    white = np.ones(bg.shape)*255
    new_frame = bg * .8
    for idx, frame in enumerate(images):
        if idx%10!=5: continue
        # new_frame = frame-bg

        new_frame = np.where((np.max(np.abs(frame-bg), axis=2)>20)[:, :, np.newaxis] , frame, new_frame )
    io.imsave(f'{idx}.png', new_frame.astype('uint8'))

if __name__ == '__main__':
    import sys
    import pathlib
    path = pathlib.Path(sys.argv[1])
    images = pims.Video(str(path))
    motion_image(images)
    # background(images)
