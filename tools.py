#!/usr/bin/env python3

from os import system, path, listdir
from layouts import layout
from random import randint
from shutil import copyfile
from chunk import chunk
from PIL import Image, ImageChops
import argparse

def setWallpaper(file_path):
    # set wallpaper on linux, depends on feh
    system('feh --bg-fill ' + path.expanduser(file_path))

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
         raise argparse.ArgumentTypeError('{} is an invalid positive int value'.format(value))
    return ivalue

def settings():
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
    return (paths, files)


def get_images(images_folder_path, num):
    #TODO: add permanent solution
    paths, files = settings()

    file_names = get_files(images_folder_path)

    if len(file_names) < num :
        print('Error: Not enough images in directory. Expect duplicates.')
        # copy list in case we run out of images
        fn_copy = file_names[:]

    images = []
    for i in range(0, num):
        r = randint(0, len(file_names))
        picture_name = file_names[r]

        images.append(Image.open(path.join(images_folder_path, picture_name)))
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
    paths, files = settings()
    lay = layout()
    screen_size = lay.chunk.screen_size
    thread_count = 3

    images = get_images(directory, lay.pic_count);
    painted_canvas = lay.split(images, thread_count=thread_count) # t1, t2, t3

    # TODO: merge lay.split and the stuff below

    indexes = range(0, thread_count)

    frames = []
    for i in indexes:
        frames.append(Image.new('RGBA', screen_size, color=(255, 255, 255, 0)))

    # Image1 = (0, 0)        (2560, 1080*1/3)
    # Image2 = (0, 1080*1/3) (2560, 1080*2/3)
    # Image3 = (0, 1080*2/3) (2560, 1080*3/3)
    xpx, ypx = lay.chunk.dimensions
    xscreen, yscreen = screen_size
    ydelta = int(yscreen / thread_count)
    for index, canvas, paint in zip(indexes, frames, painted_canvas):
        box = (0, ydelta*index)
        canvas.paste(paint, box=box)
        del paint

    # TODO: Simba, remember who you are
    # Dont remember... X_x
    temp = ImageChops.multiply(frames[2], frames[1])
    final = ImageChops.multiply(frames[0], temp)

    final.convert('RGB').save(files['mosaic'], 'PNG')



