import skimage
from skimage import io
import pims
import click
import numpy as np

@click.group()
def cli():
    pass


@cli.command()
@click.argument('path', click.Path(exists=True))
def background(path):
    images = pims.Video(str(path))
    images = np.stack(images)
    median = np.median(images, axis=0)
    median = median.astype(int)
    minima = np.min(images, axis=0)
    maxima = np.max(images, axis=0)
    io.imsave('minima.png', minima)
    io.imsave('maxima.png', maxima)
    io.imsave('median.png', median)

@cli.command()
@click.argument('path', click.Path(exists=True))
@click.option('--indices', '-i', type=int, multiple=True, default=(30, 40, 50))
def motion_image(path, indices):
    images = pims.Video(str(path))
    bg = io.imread('median.png')
    white = np.ones(bg.shape)*255
    new_frame = bg * .8
    for idx in indices:
        frame = images[idx]
        new_frame = np.where((np.max(np.abs(frame-bg), axis=2)>20)[:, :, np.newaxis] , frame, new_frame )
    io.imsave('composite.png', new_frame.astype('uint8'))

if __name__ == '__main__':
    cli()
