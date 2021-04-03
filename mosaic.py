#!/usr/bin/env python3

import os
import argparse
from os import system, path, listdir, symlink

from PIL import Image, ImageChops


from layouts import layout
from random import randint
from shutil import copyfile
from grid import grid
from image_thread import mosaic_thread


def set_wallpaper(file_path):
    """Set mosaic on linux, depends on feh"""
    os.system('feh --bg-fill ' + path.expanduser(file_path))


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
         raise argparse.ArgumentTypeError('{} is an invalid positive int value'.format(value))
    return ivalue


def make_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def settings():
    home_path = '/home/user/'
    base_path = home_path + 'pictures/wallblocks/'
    paths = {
           'save':     base_path + 'save/',
           'mosaic':   base_path + 'mosaic/',
           'general':  home_path + 'pictures/favorite/',
           }

    make_directory(paths['save'])
    make_directory(paths['mosaic'])

    files = {
           'last_images':  open(paths['mosaic'] + 'last_images.txt', 'w'),
           'feh_images':   open(paths['mosaic'] + 'feh_images.txt', 'w'),
           'mosaic':paths['mosaic'] + 'mosaic.png',
           }
    return (paths, files)

#TODO: remove dependency on this global variable
paths, files = settings()

def select_images(directory, num):
    """Select image files to be used"""
    file_names = get_files(directory)

    if len(file_names) < num :
        print('Warning: Not enough images in directory. Expect duplicates.')
        # copy list in case we run out of images
        fn_copy = file_names[:]

    selected = []

    for i in range(0, num):
        r = randint(0, len(file_names)-1)
        selected.append(file_names[r])

    return selected


def write_image():
    #TODO: remove gloval variable settings
    files['feh_images'].write(image, dest)


def load_images(image_names, directory, num):
    """Loads images into memory"""
    images = []

    for i in range(0, num):
        images.append(Image.open(os.path.join(directory, image_names[i])))

        # drop the a file name that is already used
        if len(image_names) > 1:
            continue
        else:
            # if we run out of files, then repeat the last file
            image_names.extend(fn_copy)

    return images


def get_files(directory, inc_ext=['jpg', 'bmp', 'png', 'gif']):
    """Gets file names of file types from a directory"""
    file_names = [
            filename \
            for filename in os.listdir(os.path.realpath(directory)) \
            if any(filename.endswith(ext) for ext in inc_ext)
            ]
    return file_names


def merge_layers(layers):
    """Pastes canvas layers one on top of another"""
    #TODO: generalize to n-layers
    temp = ImageChops.multiply(layers[2], layers[1])
    final = ImageChops.multiply(layers[0], temp)
    return final


class mosaic():
    def __init__(self, directory, threads=3):
        self.layout = layout()
        self.directory = directory
        self.image_names = select_images(directory, self.layout.block_count)
        self.thread_count = threads

    def populate(self):
        """Load images into memory"""
        return load_images(self.image_names, self.directory, self.layout.block_count)

    @property
    def image_paths(self):
        """Construct list of full image paths"""
        return [os.path.join(self.directory, name) for name in self.image_names]

    def prepare_threads(self):
        """Split resource intensive task of modifying images into different threads"""
        #TODO: generalize the fuction to it can split into more than just 3 theads

        # find how many grid blocks each thread will take care of
        grid_slice = int( len(self.layout.size_matrix)/self.thread_count )

        sl0, sl1, sl2 = (self.layout.copy() for i in range(0,3))

        # split the matrix into equal sizes
        sl0.cut_matrix(slice(None, grid_slice))
        sl1.cut_matrix(slice(grid_slice, grid_slice*2))
        sl2.cut_matrix(slice(grid_slice*2, None))

        images = self.populate()

        im0 = images[                               :sl0.block_count]
        im1 = images[sl0.block_count                :sl0.block_count+sl1.block_count]
        im2 = images[sl0.block_count+sl1.block_count:       ]
        del images

        thread0 = mosaic_thread(threadID=1, name='Thread-0', counter=1, ratio =3,
                images=im0,
                size_matrix=sl0.size_matrix,
                )

        thread1 = mosaic_thread(threadID=2, name='Thread-1', counter=2, ratio =3,
                images=im1,
                size_matrix=sl1.size_matrix,
                )

        thread2 = mosaic_thread(threadID=3, name='Thread-2', counter=3, ratio =3,
                images=im2,
                size_matrix=sl2.size_matrix,
                )

        return (thread0, thread1, thread2)

    def thread_layers(self):
        """Starts and joins the threads"""
        #TODO: currently hardcoded to 3 threads, it should be generalized

        thread0, thread1, thread2 = self.prepare_threads()

        try:
            thread0.start()
            thread1.start()
            thread2.start()
        except:
            print("Error: Threads won't start.")

        # wait for the last thread started and join
        t2 = thread2.join()
        t1 = thread1.join()
        t0 = thread0.join()

        return (t0, t1, t2)


def generate_mosaic(directory):
    """Stitches canvases, files, images and threads"""

    m = mosaic(directory)


    #TODO: link images to the storage directory
    #link_image(image_paths)

    #NOTE: thread_layers() is what takes the longest to process in this program
    paints = m.thread_layers()

    indexes = range(0, m.thread_count)

    screen_size = m.layout.grid.size
    yscreen = screen_size[1]

    canvas = [
        Image.new(
            'RGBA',
            screen_size,
            color=(255, 255, 255, 0)
            )
        for i in indexes
        ]


    def offset_layers(paints, yoffset):
        """Apply each paint on separate canvas, but offset vertically"""
        yoffset = int(yscreen / m.thread_count)
        for index, block, paint in zip(indexes, canvas, paints):
            box = (0, yoffset*index)
            block.paste(paint, box=box)

            # TODO: move to debug mode
            block.convert('RGB').save('/home/user/pictures/wallblocks/mosaic/layer' + str(index), 'PNG')
        return canvas

    canvas = offset_layers(paints, yoffset=int(yscreen / m.thread_count))
    masterpiece = merge_layers(canvas)
    #TODO: remove gloval variable settings
    masterpiece.convert('RGB').save(files['mosaic'], 'PNG')

    return (masterpiece, m.image_names)
