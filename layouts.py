#!/usr/bin/env python3
import math
from random import randint
from grid import grid

styles = {
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
        # large offsets
        '16':
        [
            [ 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0,16, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0]
        ],
    }


def is_square(integer):
    """Returns if integer is a perfect square"""
    pos_integer = math.fabs(integer)
    root = math.sqrt(pos_integer)
    if int(root + 0.5) ** 2 == pos_integer: 
        return True
    else:
        return False


class layout:
    def __init__(self):
        #TODO: Make all elements available in init, not hidden in the functions
        self.grid = grid()
        self.pick()
        self.size_matrix = self.create_size_matrix()

    def pick(self, index=None):
        """Selects a random style and updates length"""
        if index:
            name = str(index)
        else:
            name = str(randint(0, len(styles)-1))

        self.style = styles[name]
        self.length = len(styles[name])

    def create_size_matrix(self):
        """Translate the human readable layout matrix into a pixel size matrix"""
        # prep iterating values
        size_matrix = []
        pic_count = 0

        # TODO: more pythonic loop must be achievable
        rows = len(self.style)
        cols = len(self.style[0])
        for x in range(0, rows):
            for y in range(0, cols):
                size = self.determine_size(self.style[x][y], self.grid)
                size_matrix.append(size)
                if size != (0, 0):
                    pic_count += 1

        #TODO: I think pic_count was already replaced by block_count
        self.pic_count = pic_count
        return size_matrix

    def determine_size(self, code, grid):
        """Translates the integer code to a pixel size"""
        size = (0, 0)

        xpx, ypx = grid.dimensions

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

    @property
    def block_count(self):
        """Find the non-zero size images for each section"""
        count = sum(1 for size in self.size_matrix if size != (0, 0))
        return count

    def cut_matrix(self, _slice):
        """Select a region of the matrix"""
        self.size_matrix = self.size_matrix[_slice]

    def copy(self):
        new = type(self)()
        new.style = self.style
        new.length = self.length
        new.size_matrix = self.size_matrix.copy()

        return new



