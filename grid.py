#!/usr/bin/env python3


import tkinter


class grid:
    def __init__(self, divisions=(8, 6)):
        self.divisions = divisions
        self.screen_size = self.current_screen_size
        self.size = self.current_screen_size

    @property
    def current_screen_size(self):
        root = tkinter.Tk()
        size = (
               int(root.winfo_screenwidth()) + 10,
               int(root.winfo_screenheight())
               )
        root.destroy()
        return size

    @property
    def total_divisions(self):
        """total number of divisions"""
        return int(self.xdiv * self.ydiv)

    @property
    def dimensions(self):
        """dimensions of a single division"""
        return (self.xpx, self.ypx)

    @property
    def xpx(self):
        """x size of a division in pixels"""
        return int(self.screen_size[0] / self.xdiv)

    @property
    def ypx(self):
        """y size of a division in pixels"""
        return int(self.screen_size[1] / self.ydiv)

    @property
    def xdiv(self):
        return int(self.divisions[0])

    @property
    def ydiv(self):
        return int(self.divisions[1])
