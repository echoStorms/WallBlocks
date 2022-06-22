#!/usr/bin/env python3

import argparse
import sys
import os
import datetime
import glob
import shutil
import subprocess
from configparser import ConfigParser

from mosaic import generate_mosaic


# TODO: debug only
#from profilehooks import profile


def remove_thing(path):
    """deletes a file or directory"""
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


def empty_directory(path):
    """deletes all files and directories inside a directory"""
    for i in glob.glob(os.path.join(path, '*')):
        remove_thing(i)


def link_image(source, dest, i, name):
    """Create sym link from image to mosaic gallery path"""
    #TODO: remove i from the requirements
    os.symlink(
               os.path.join(source, name),
               os.path.join(dest, "{:>02}".format(str(i) + '_' + name))
               )


def link_blocks(source, dest, image_names):
    """Add symlinks for each block to another destination"""
    for i in range(0, len(image_names)):
        link_image(source, dest, i, image_names[i])

#@profile
def main(input_dir, output_dir, batch_size=1, style=False):

    print('Working...')
    print('Please wait...')

    if batch_size > 1:
        # TODO: Implement batch
        print('Sorry batch mode not implemented yet...')
        # print('Generating ' + str(batch_size) + ' wallpapers.')
        # batch(directory, batch_size)
        # print(f'Done! Your files are here {output_dir}')
    else:
        print('Generating wallpaper.')
        masterpiece, image_names = generate_mosaic(input_dir)
        output_file = os.path.join(output_dir, f'wallblock-{datetime.datetime.now()}.png')
        masterpiece.convert('RGB').save(output_file, 'PNG')
        print(f'Done! Your file is here: {output_file}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    def check_positive(value):
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError('{} is an invalid positive int value'.format(value))
        return ivalue

    parser.add_argument('-i', '--input', type=str,
            help='directory to read images from')
    parser.add_argument('-o', '--output', type=str,
            help='directory to write images to')
    parser.add_argument('-s', '--style', type=int, default=0,
            help='style of image')
    parser.add_argument('-b', '--batch', type=check_positive, default=1,
            help='number of images to create. default is 1')
    parser.add_argument('-x', '--immediate', action='store_true', default=False,
            help='set wallpaper immediately, instead of waiting for new generation')

    args = parser.parse_args()

    # TODO: Use a configuration file that overrides defaults, but keeps explicit commands
    # parser = ConfigParser()
    # parser.read('/home/user/.config/wallblocks/config')

    # style = style if style else parser.get('config','style')
    # save = output if output else parser.get('config','save')
    # mosaic = mosaic if mosaic else parser.get('config','mosaic')
    # wallpaper = wallpaper if wallpaper else parser.get('config','wallpaper')

    main(input_dir=args.input, output_dir=args.output, style=args.style, batch_size=args.batch)
