import skimage
from skimage import io
import pims
import click
import numpy as np
import warnings

from . import background_methods

@click.group()
@click.option('--warn', '-w', is_flag=True)
def cli(warn):
    if not warn:
        warnings.simplefilter('ignore', Warning)


@cli.command()
@click.argument('path', click.Path(exists=True))
@click.option('--method', '-m', type=str, multiple=True, default=('median',))
def background(path, method):
    images = pims.Video(str(path))
    for m in method:
        try:
            handle = getattr(background_methods, m)
            result = handle(images)
            io.imsave(f'{m}.png', result)
        except:
            raise RuntimeError(f'{m} is not a valid background method.')

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
