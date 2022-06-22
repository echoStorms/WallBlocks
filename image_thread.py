#!/usr/bin/env python3

import threading as thread


from PIL import Image, ImageOps, ImageFilter


from grid import grid


class mosaic_thread (thread.Thread):
    def __init__(self, threadID, name, counter, images, size_matrix, ratio):
        thread.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.images = images
        self.ratio = ratio
        self.size_matrix = size_matrix
        self.grid = grid()
        self.image_size = self.grid.size

    def join(self):
        thread.Thread.join(self)
        return self.out

    def run(self):
        self.out = self.thread_image_mod()

    def thread_image_mod(self):
        #TODO: Add to debug
        #print('Thread name:', thread.current_thread().name)

        # TODO: integrate variable names
        images = self.images
        size_matrix = self.size_matrix
        ratio = self.ratio

        # aqua = (10, 40, 50)
        aqua = (0, 150, 136)
        darkaqua = (7, 54, 66)
        orange = (181, 137, 0)
        lime = (102, 128, 16)
        black = (0, 10, 16)
        color_fill = darkaqua
        blur = 0

        cnt = 0
        error_cnt = 0
        img_cnt = 0

        canvas = Image.new('RGBA', self.image_size, (255, 255, 255, 0))
        xpx, ypx = self.grid.dimensions
        xdiv, ydiv = self.grid.divisions
        xstop, ystop = (int(xpx*xdiv), int(ypx*ydiv/ratio))

        for y in range(0, ystop, ypx):
            for x in range(0, xstop, xpx):
                if size_matrix[0] != (0, 0):
                    img = mod_image(images[0],
                          size_matrix[0],
                          blur=blur,
                          color_fill=color_fill
                          )
                    images.pop(0) # dequeue
                    canvas.paste(img, (x, y))
                # finally
                size_matrix.pop(0) # dequeue

        return canvas


def mod_image(image, size, border=5, blur=0, color_fill=(0, 0, 0), centering=(0.5, 0.5), method=Image.ANTIALIAS):
    image = ImageOps.fit(image, size, method=method, bleed=border, centering=centering)

    # create border
    image = ImageOps.crop(image, border=border)
    image = ImageOps.expand(image, border=border, fill=color_fill)

    # img = ImageOps.grayscale(img)
    #               .flip(img)
    #               .mirror(img)
    #               .solarize(img, threshold = 128)
    #               .invert(img)
    # there is a problem with invert and solarize and png images :()
    image = image.filter(ImageFilter.GaussianBlur(radius=blur))
    #                 (ImageFilter.DETAIL)
    # BLUR / CONTOUR / DETAIL/ EDGE_ENHANCE / EDGE_ENHANCE_MORE
    # EMBOSS/ FIND_EDGES / SMOOTH / SMOOTH_MORE / SHARPEN
    return image



# def threaded_animation(images, ratio):
#     screen_size = (2560, int(1080/ratio))
#     bg = Image.new('RGBA', screen_size)

#     cnt = 0
#     border = 0.00

#     for y in range(0, int(180*6/ratio), 180):
#         for x in range(0, 320*8, 320):
#             img = ImageOps.fit(images[cnt], (320, 180), Image.BICUBIC, bleed = border, centering = (0.5, 0.5))
#             bg.paste(img, (x, y))
#             cnt += 1
#     return bg;
