#!/usr/bin/env python3

import argparse
import sys
import os
import glob
import shutil
import subprocess


sys.path.insert(0, '/usr/local/lib')
sys.path.insert(0, os.path.expanduser('~/lib'))


from tools import setWallpaper
from tools import check_positive
from tools import settings
from tools import generate_wallpaper

# TODO: debug only
from profilehooks import profile

def remove_thing(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)

def empty_directory(path):
    for i in glob.glob(os.path.join(path, '*')):
        remove_thing(i)


@profile
def main(directory, num_wallpapers=1, immediate=False):
    paths, files = settings()

    print('Working...')

    empty_directory('/home/meiji/.wallpaper/mosaic/')

    if num_wallpapers > 1:
        batch(directory, num_wallpapers)
    else:
        if immediate:
            # setWallpaper(files['mosaic'])
            # TODO: pass settings instead of directory
            generate_wallpaper(directory)
        else:
            generate_wallpaper(directory)
            # setWallpaper(files['mosaic'])

    print('Done!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=str,
            help='directory to use images from')
    parser.add_argument('-n', '--number', type=check_positive, default=1,
            help='number of images to create. default is 1')
    parser.add_argument('-i', '--immediate', action='store_true', default=False,
            help='set wallpaper immediately, instead of waiting for new generation')

    args = parser.parse_args()

    # handle immediate argument
    if args.immediate:
        print('Displaying old image first.')

    # handle number argument
    if args.number >= 2:
        print('Generating ' + str(args.number) + ' wallpapers.')
    else:
        print('Generating wallpaper.')
    # finally
    print('Please wait...')

    main(directory=args.directory, num_wallpapers=args.number, immediate=args.immediate)
