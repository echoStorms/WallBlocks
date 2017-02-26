#!/usr/bin/env python3

import argparse
from PIL import Image, ImageChops
from os import listdir, path, system
from random import randint
from shutil import copyfile

from layouts import layout
from chunk import chunk

def setWallpaper(file_path):
    # set wallpaper on linux, depends on feh
    system('feh --bg-fill ' + path.expanduser(file_path))

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
         raise argparse.ArgumentTypeError('{} is an invalid positive int value'.format(value))
    return ivalue

# GLOBALS
home_path = '/home/meiji/'
base_path = home_path + '.wallpaper/'
paths = {
        'save':     base_path,
        'mosaic':   base_path + 'mosaic/',
        'general':  home_path + 'pictures/wally/general/',
        }

files = {
        'last_images':  open(paths['mosaic'] + 'last_images.txt', 'w'),
        'feh_images':   open(paths['mosaic'] + 'feh_images.txt', 'w'),
        'mosaic':paths['mosaic'] + 'mosaic.png',
        }

# TODO: move this somewhere else
from profilehooks import profile

@profile
def main(directory, num_wallpapers=1, immediate=False):
    global files

    #TODO: Check if dictionares can use keys defined in the same dic

    print('Working...')

    if num_wallpapers > 1:
        batch(directory, num_wallpapers)
    else:
        if immediate:
            setWallpaper(files['mosaic'])
            generate_wallpaper(directory)
        else:
            generate_wallpaper(directory)
            setWallpaper(files['mosaic'])

    print('Done!')

def get_images(images_folder_path, num):
    #TODO: add permanent solution
    global files

    file_names = get_files(images_folder_path)

    if len(file_names) < num :
            print('Error: Not enough images in directory. Expect duplicates.')
            # copy list in case we run out of images
            fn_copy = file_names[:]

    images = []
    for i in range(0, num):
        r = randint(0, len(file_names))
        picture_name = file_names[r]

        images.append( Image.open(path.join(images_folder_path, picture_name)) )
        # write feh file
        files['feh_images'].write(path.join(images_folder_path, picture_name+'\n'))

        #copy image to mosaic path
        copyfile(
                path.join(images_folder_path, picture_name),
                path.join(paths['mosaic'], "{:>02}_".format(str(i+1)) 
                    + picture_name))

        # drop the a file name that is already used
        if len(file_names) > 1:
            file_names.pop(r)
        else:
            # if we run out of files, then repeat
            file_names.extend(fn_copy)

    return images

def get_files(directory):
	inc_ext = ['jpg', 'bmp', 'png', 'gif']
	file_names = [fn for fn in listdir(directory) if any(fn.endswith(ext) for ext in inc_ext)]
	return file_names

def generate_wallpaper(directory):
    lay = layout()
    screen_size = lay.chunk.screen_size

    images = get_images(directory, lay.pic_count);
    painted_canvas = lay.split(images) # t1, t2, t3

    # Image1 = (0, 0)        (2560, 1080*1/3)
    # Image2 = (0, 1080*1/3) (2560, 1080*2/3)
    # Image3 = (0, 1080*2/3) (2560, 1080*3/3)
    xpx, ypx = lay.chunk.dimensions
    xscreen, yscreen = screen_size
    yspace = int(yscreen / 3)

    frames = (
            Image.new('RGBA', screen_size, (255,255,255,0)),
            Image.new('RGBA', screen_size, (255,255,255,0)),
            Image.new('RGBA', screen_size, (255,255,255,0)),
            )

    for index, canvas, paint in zip((0, 1, 2), frames, painted_canvas):
        box = (index, yspace*index)
        canvas.paste(paint, box=box)

    # Paste the image contributions from each thread
    # left upper right lower

    # TODO: Simba, remember who you are
    # Dont remember... X_x
    temp1 = ImageChops.multiply(frames[2], frames[1])
    final = ImageChops.multiply(frames[0], temp1)

    # bg.show()
    # bg1.save(path, 'JPEG', quality=100)
    # bg1.convert('RGB').save(path, 'PNG')
    final.convert('RGB').save(files['mosaic'], 'PNG')




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
