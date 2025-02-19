import pygame as pg
from pygame import Surface
import os
import glob
import random
from collections import namedtuple

def stretch(surf, size, upscale_factor=2):
    width, height = size

    imgw, imgh = surf.get_rect().size

    # Upscale the image by the upscale_factor
    imgw, imgh = int(imgw * upscale_factor), int(imgh * upscale_factor)
    surf = pg.transform.smoothscale(surf, (imgw, imgh))

    xfactor = float(width) / imgw
    surf = pg.transform.smoothscale(surf, (int(imgw * xfactor), int(imgh * xfactor)))

    new_imgw, new_imgh = surf.get_rect().size

    if new_imgh < height:
        yfactor = float(height) / new_imgh
        surf = pg.transform.smoothscale(surf, (int(new_imgw * yfactor), int(new_imgh * yfactor)))

    return surf

def endswith_any(s, *suffixes):
    return any(s.endswith(suffix) for suffix in suffixes)


def is_image(fname):
    return endswith_any(fname, ".png", ".jpg", ".jpeg", ".bmp")

class Background(object):
    def __init__(self, size):
        self.size = size  # Ensure self.size is defined before it is used
        width, height = self.size

        self.surf = Surface(size)

        self.backgrounds = []

        files = glob.glob(os.path.join(os.path.dirname(__file__), "resources/backgrounds/*"))

        bg = namedtuple("background", "image")
        for fname in filter(is_image, files):
            self.backgrounds.append(
                bg(image=stretch(pg.image.load(fname).convert(), self.size))
            )

        random.shuffle(self.backgrounds)

        self.timer = 0
        self.frequency = 25  # new background every N seconds
        self.current_bg = 0  # index of the current bg in self.backgrounds

        self.fadetime = .7
        self.fading = 0
        self.donefading = True

        self.set_background()

    def update(self, timepassed):
        old_timer, self.timer = self.timer, (self.timer + timepassed) % self.frequency

        if self.fading < 0:
            self.donefading = True
            self.fading = 0
        elif self.fading:
            self.fading = self.fading - timepassed

        if old_timer > self.timer:
            old_bg, self.current_bg = self.current_bg, (self.current_bg + 1) % len(self.backgrounds)
            if self.current_bg != old_bg:
                self.fading = self.fadetime

        if self.fading:
            self.set_background()
        elif self.donefading:
            self.donefading = False
            self.set_background()

    def get_current_bg(self):
        return self.backgrounds[self.current_bg]

    def set_background(self):
        if self.fading:
            old_bg = (self.current_bg - 1) % len(self.backgrounds)
            new = self.get_current_bg().image
            old = self.backgrounds[old_bg].image.copy()
            old.set_alpha(self.fading * 255 / self.fadetime)

            self.blit(new)
            self.blit(old)
        else:
            self.blit(self.get_current_bg().image)

    def browse(self, direction):
        dirs = {'forward': 1, 'backward': -1}
        self.current_bg = (self.current_bg + dirs[direction]) % len(self.backgrounds)
        self.set_background()
        self.timer = 0

    def blit(self, surf):
        self.surf.blit(surf, surf.get_rect(centerx=self.surf.get_rect().centerx,
                                           centery=self.surf.get_rect().centery))