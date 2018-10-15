import skimage
from skimage import io
import pims
import click
import numpy as np
import warnings

from . import background_methods
from . import object_detection
from . import comparison_methods

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
        except:
            raise RuntimeError(f'{m} is not a valid background method.')
        result = handle(images)
        io.imsave(f'{m}.png', result)

@cli.command()
@click.argument('path', click.Path(exists=True))
@click.option('--indices', '-i', type=int, multiple=True, default=(30, 40, 50))
@click.option('--background', '-b', type=click.Path(exists=True, file_okay=True, dir_okay=False), default='median.png')
@click.option('--method', '-m', type=str, multiple=False, default='threshold')
@click.option('--comparison', '-c', type=str, multiple=False, default='distance')
@click.option('--debug', '-d', is_flag=True, default=True)
def motion_image(path, indices, background, method, comparison, debug):
    images = pims.Video(path)
    composite = reference = io.imread(background)
    detector = getattr(object_detection, method)
    comparitor = getattr(comparison_methods, comparison)

    for idx in indices:
        frame = images[idx]
        if debug:
            io.imsave(f'comparison_{idx}.png', comparitor(frame, reference).astype('uint8'))
            io.imsave(f'detection_{idx}.png', detector(comparitor(frame, reference)).astype('bool')*255)
        composite = np.where(detector(comparitor(frame, reference))[:, :, np.newaxis] , frame, composite)
    io.imsave('composite.png', composite.astype('uint8'))

if __name__ == '__main__':
    cli()
