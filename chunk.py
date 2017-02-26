#!/usr/bin/env python3
import tkinter

class chunk:
    def __init__(self, divisions=(8, 6)):
        self.divisions = divisions
        self.set_screen_size()

    def set_screen_size(self, screen_size=None):
        if not screen_size:
            # initialize frame to get screeninfo
            root = tkinter.Tk()
            self.screen_size = (
                                int(root.winfo_screenwidth()) + 10,
                                int(root.winfo_screenheight())
                               )
            root.destroy()
        else:
            self.screen_size = screen_size

    @property
    def total_divisions(self):
        # total number of chunks
        return int(self.xdiv * self.ydiv)

    @property
    def dimensions(self):
        # single chunk size
        return (self.xpx, self.ypx)

    @property
    def xpx(self):
        return int(self.screen_size[0] / self.xdiv)

    @property
    def ypx(self):
        return int(self.screen_size[1] / self.ydiv)

    @property
    def xdiv(self):
        return int(self.divisions[0])

    @property
    def ydiv(self):
        return int(self.divisions[1])
