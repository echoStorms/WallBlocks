#!/usr/bin/env python3

import argparse
import sys
import os
import glob
import shutil
import subprocess
from configparser import ConfigParser


sys.path.insert(0, '/usr/local/lib')
sys.path.insert(0, os.path.expanduser('~/lib'))


from mosaic import setWallpaper
from mosaic import check_positive
from mosaic import settings
from mosaic import generate_mosaic


# TODO: debug only
#from profilehooks import profile


def remove_thing(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


def empty_directory(path):
    for i in glob.glob(os.path.join(path, '*')):
        remove_thing(i)


#@profile
def main(directory, batch_size=1, immediate=False):
    parser = ConfigParser()
    parser.read('/home/user/.config/wallblocks/config')

    style = parser.get('config','style')
    save = parser.get('config','save')
    mosaic = parser.get('config','mosaic')
    wallpaper = parser.get('config','wallpaper')

    if style != 'random':
        print('WARNING', 'The style selection has not been implemented yet.')

    print('Working...')
    print('Please wait...')

    empty_directory(save)

    if batch_size > 1:
        print('Generating ' + str(batch_size) + ' wallpapers.')
        batch(directory, batch_size)
    else:
        print('Generating wallpaper.')
        if immediate:
            print('Displaying old image first.')
            setWallpaper(files['mosaic'])
            # TODO: pass settings instead of directory
            generate_mosaic(directory)
        else:
            generate_mosaic(directory)
            setWallpaper(wallpaper)

    print('Done!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=str,
            help='directory to read images from')
    parser.add_argument('-b', '--batch', type=check_positive, default=1,
            help='number of images to create. default is 1')
    parser.add_argument('-i', '--immediate', action='store_true', default=False,
            help='set wallpaper immediately, instead of waiting for new generation')

    args = parser.parse_args()

    main(directory=args.directory, batch_size=args.batch, immediate=args.immediate)
