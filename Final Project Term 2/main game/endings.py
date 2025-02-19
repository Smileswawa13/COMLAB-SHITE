import pygame as pg
import sys

class endings:
    def __init__(self, screen, stage_number):
        self.SCREEN = screen
        self.stage_number = stage_number
        self.BG = pg.image.load("resources/backgrounds/room.jpg").convert()
        self.BG = pg.transform.scale(self.BG, (screen.get_width(), screen.get_height()))
        self.phase = 0

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                    return

            self.SCREEN.blit(self.BG, (0, 0))
            pg.display.update()