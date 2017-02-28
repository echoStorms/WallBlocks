#!/usr/bin/env python3
import math
from random import randint
from chunk import chunk
from image_thread import mosaic_thread

class layout:
    layouts = {
            # 4 quadrants
            '0':
            [
                [ 4, 0, 1, 1, 1, 1, 4, 0],
                [ 0, 0, 1, 1, 1, 1, 0, 0],
                [ 1, 1, 1, 1, 1, 1, 1, 1],
                [ 1, 1, 1, 1, 1, 1, 1, 1],
                [ 4, 0, 1, 1, 1, 1, 4, 0],
                [ 0, 0, 1, 1, 1, 1, 0, 0]
            ],
            # medium blocks
            '1':
            [
                [ 4, 0, 4, 0, 4, 0, 4, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [ 4, 0, 4, 0, 4, 0, 4, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [ 4, 0, 4, 0, 4, 0, 4, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            # 6 blocks v1
            '2':
            [
                [ 4, 0, 1, 1, 1, 1, 4, 0],
                [ 0, 0, 1, 1, 1, 1, 0, 0],
                [ 1, 1, 4, 0, 4, 0, 1, 1],
                [ 1, 1, 0, 0, 0, 0, 1, 1],
                [ 4, 0, 1, 1, 1, 1, 4, 0],
                [ 0, 0, 1, 1, 1, 1, 0, 0]
            ],
            # 6 blocks v2
            '3':
            [
                [ 4, 0, 1, 1, 1, 1, 4, 0],
                [ 0, 0, 1, 1, 1, 1, 0, 0],
                [ 2, 0, 4, 0, 4, 0,-2,-2],
                [ 2, 0, 0, 0, 0, 0, 0, 0],
                [ 4, 0, 3, 0, 0, 1, 4, 0],
                [ 0, 0, 1, 3, 0, 0, 0, 0]
            ],
            # singles
            '4':
            [
                [ 1, 1, 1, 1, 1, 1, 1, 1],
                [ 1, 1, 1, 1, 1, 1, 1, 1],
                [ 1, 1, 1, 1, 1, 1, 1, 1],
                [ 1, 1, 1, 1, 1, 1, 1, 1],
                [ 1, 1, 1, 1, 1, 1, 1, 1],
                [ 1, 1, 1, 1, 1, 1, 1, 1]
            ],
            # huge center
            '5':
            [
                [ 4, 0, 1, 1, 1, 1, 4, 0],
                [ 0, 0,16, 0, 0, 0, 0, 0],
                [ 2, 0, 0, 0, 0, 0,-2,-2],
                [ 2, 0, 0, 0, 0, 0, 0, 0],
                [ 4, 0, 0, 0, 0, 0, 4, 0],
                [ 0, 0, 1, 3, 0, 0, 0, 0]
            ],
            # horizontal
            '6':
            [
                [ 2, 0, 2, 0, 2, 0, 2, 0],
                [ 1, 2, 0, 2, 0, 2, 0, 1],
                [ 2, 0, 2, 0, 2, 0, 2, 0],
                [ 1, 2, 0, 2, 0, 2, 0, 1],
                [ 2, 0, 2, 0, 2, 0, 2, 0],
                [ 1, 2, 0, 2, 0, 2, 0, 1]
            ],
            # large blocks
            '7':
            [
                [-2, 1,-2, 1,-2, 1,-2, 1],
                [ 0,-2, 0,-2, 0,-2, 0,-2],
                [-2, 0,-2, 0,-2, 0,-2, 0],
                [ 0,-2, 0,-2, 0,-2, 0,-2],
                [-2, 0,-2, 0,-2, 0,-2, 0],
                [ 0, 1, 0, 1, 0, 1, 0, 1]
            ],
            # large blocks
            '8':
            [
                [-2, 1,-2, 1,-2, 1,-2, 1],
                [ 0, 1, 0,-2, 0, 1, 0,-2],
                [-2, 4, 0, 0,-2, 4, 0, 0],
                [ 0, 0, 0,-2, 0, 0, 0,-2],
                [-2, 1,-2, 0,-2, 1,-2, 0],
                [ 0, 1, 0, 1, 0, 1, 0, 1]
            ],
            # 2 large random fill
            '9':
            [
                [ 2, 0, 1,-2, 1,-2, 1,-2],
                [ 9, 0, 0, 0,-2, 0,-2, 0],
                [ 0, 0, 0,-2, 0, 1, 0,-2],
                [ 0, 0, 0, 0, 9, 0, 0, 0],
                [ 2, 0, 1,-2, 0, 0, 0,-2],
                [ 1, 2, 0, 0, 0, 0, 0, 0]
            ],
            # 2 large random fill
            '10':
            [
                [-3, 9, 0, 0, 9, 0, 0,-3],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [-3, 3, 0, 0, 2, 0, 2, 0],
                [ 0, 9, 0, 0, 4, 0, 4, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            # 2 huge v1
            '11':
            [
                [16, 0, 0, 0, 4, 0, 4, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0,16, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [ 4, 0, 4, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            # 2 huge v2
            '12':
            [
                [ 4, 0, 4, 0,16, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [16, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 4, 0, 4, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            # 2 huge v3
            '13':
            [
                [-2, 3, 0, 0,16, 0, 0, 0],
                [ 0, 3, 0, 0, 0, 0, 0, 0],
                [16, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 3, 0, 0,-2],
                [ 0, 0, 0, 0, 3, 0, 0, 0]
            ],
            # 2 huge v4
            '14':
            [
                [ 3, 0, 0,-2,16, 0, 0, 0],
                [ 3, 0, 0, 0, 0, 0, 0, 0],
                [16, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0,-2, 3, 0, 0],
                [ 0, 0, 0, 0, 0, 3, 0, 0]
            ],
            # medium offsets
            '15':
            [
                [ 2, 0, 4, 0, 2, 0, 4, 0],
                [ 4, 0, 0, 0, 4, 0, 0, 0],
                [ 0, 0, 4, 0, 0, 0, 4, 0],
                [ 4, 0, 0, 0, 4, 0, 0, 0],
                [ 0, 0, 4, 0, 0, 0, 4, 0],
                [ 2, 0, 0, 0, 2, 0, 0, 0]
            ],
        }

    def __init__(self):
        self.chunk = chunk()
        self.pick()
        self.create_size_matrix()

    def pick(self, index=None):
        if index:
            name = str(index)
        else:
            name = str(randint(0, len(self.layouts)))

        self.layout = self.layouts[name]
        self.length = len(self.layouts[name])

    # translate the human readable layout matrix into a pixel size matrix
    def create_size_matrix(self):
        # prep iterating values
        size_matrix = []
        pic_count = 0

        # TODO: more pythonic loop
        rows = len(self.layout)
        cols = len(self.layout[0])
        for x in range(0, rows):
            for y in range(0, cols):
                size = self.determine_size(self.layout[x][y], self.chunk)
                size_matrix.append(size)
                if size != (0, 0):
                    pic_count += 1

        self.pic_count = pic_count
        self.size_matrix = size_matrix

    def determine_size(self, code, pic_chunk):
        size = (0, 0)

        xpx, ypx = pic_chunk.dimensions

        xmod, ymod = (1, 1)

        if is_square(code):
            xmod = math.sqrt(math.fabs(code))
            ymod = math.sqrt(math.fabs(code))
        else:
            if code > 0:
                # horizontal image
                xmod = math.fabs(code)
            else:
                # vertical image
                ymod = math.fabs(code)

        size = (int(xpx*xmod), int(ypx*ymod))

        return size

    def split(self, images, thread_count=3):
        # TODO: could be done more efficiently also by integrating generate_wallpapers

        # find how many sizes each thread will take care of
        s = int( len(self.size_matrix)/thread_count )

        # split the matrix into equal sizes
        sm1 = self.size_matrix[   :s  ]
        sm2 = self.size_matrix[  s:s*2]
        sm3 = self.size_matrix[s*2:   ]
        del self.size_matrix

        # find the non-zero size images for each section
        nz1 = sum(1 for size in sm1 if size != (0, 0))
        nz2 = sum(1 for size in sm2 if size != (0, 0))
        nz3 = sum(1 for size in sm3 if size != (0, 0))

        im1 = images[       :nz1    ]
        im2 = images[nz1    :nz1+nz2]
        im3 = images[nz1+nz2:       ]
        del images

        # Prepare threads
        thread1 = mosaic_thread(threadID=1, name='Thread-1', counter=1, images=im1, size_matrix=sm1, ratio=3)
        thread2 = mosaic_thread(threadID=2, name='Thread-2', counter=2, images=im2, size_matrix=sm2, ratio=3)
        thread3 = mosaic_thread(threadID=3, name='Thread-3', counter=3, images=im3, size_matrix=sm3, ratio=3)



        # Start threads
        try:
            thread1.start()
            thread2.start()
            thread3.start()
        except:
            print("Error: Threads won't start.")

        t3 = thread3.join()
        t2 = thread2.join()
        t1 = thread1.join()

        return (t1, t2, t3)

def is_square(integer):
    pos_integer = math.fabs(integer)
    root = math.sqrt(pos_integer)
    if int(root + 0.5) ** 2 == pos_integer: 
        return True
    else:
        return False
