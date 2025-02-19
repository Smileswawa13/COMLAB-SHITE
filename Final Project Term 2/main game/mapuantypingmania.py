"""
Authors: Neil Justin Bermoy
         Tristan Angelo Buling
         Isiah Catan
         Lawrence Hao
Date Created: 02-16-2025
Game Program: Mapuan Typing Mania
Game Description: A typing game to see how good you are at typing
                    and how fast you can type. The game will generate
                    a random word and the player must type it as fast
                    as they can. The game will calculate the player's
                    typing speed and accuracy. Enter the championship and win
                    the title of the fastest typist in Mapua University.
"""
import pygame as pg
import numpy as np
import os
import sys
from buttons import Button
from intro import Intro
from stages import stages

pg.init()

width = 930
height = 650

def get_Font(size):
    return pg.font.Font(os.path.join(os.path.dirname(__file__), "resources/DejaVuSans.ttf"), size)

def apply_wave_effect(image, amplitude, frequency, phase, color_shift):
    arr = pg.surfarray.pixels3d(image)
    height, width, _ = arr.shape
    for x in range(width):
        offset = int(amplitude * np.sin(2 * np.pi * frequency * x + phase))
        arr[:, x] = np.roll(arr[:, x], offset, axis=0)
        arr[:, x] = np.clip(arr[:, x] + [color_shift, color_shift, color_shift], 0, 255)
    return pg.surfarray.make_surface(arr)

class game_Menu(object):
    def __init__(self):
        self.SCREEN = pg.display.set_mode((width, height))
        pg.display.set_caption("Mapuan Typing Mania")
        self.BG = pg.image.load("resources/backgrounds/menu.jpg").convert()
        self.BG = pg.transform.scale(self.BG, (width, height))
        self.phase = 0

    def animate_background(self):
        amplitude = 5
        frequency = 0.01
        color_shift = 50
        self.phase += 0.05

        t = (np.sin(self.phase) + 1) / 2
        r = int(255 * (1 - t) + 128 * t)
        g = int(200 * (1 - t) + 128 * t)
        b = int(100 * (1 - t) + 128 * t)
        bg_color = (r, g, b)

        wavy_bg = apply_wave_effect(self.BG.copy(), amplitude, frequency, self.phase, color_shift)
        wavy_bg.fill(bg_color, special_flags=pg.BLEND_RGBA_MULT)
        return wavy_bg

    def play(self):
        while True:
            PLAY_MOUSE_POS = pg.mouse.get_pos()
            animated_bg = self.animate_background()
            self.SCREEN.blit(animated_bg, (0, 0))

            PLAY_TEXT = get_Font(30).render("Choose a stage:", True, "White")
            PLAY_RECT = PLAY_TEXT.get_rect(center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 4))
            self.SCREEN.blit(PLAY_TEXT, PLAY_RECT)

            INTRO_BUTTON = Button(image=None, pos=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2 - 50),
                                  text_input="INTRO", font=get_Font(50), base_color="White", hovering_color="Green")
            STAGE1_BUTTON = Button(image=None, pos=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2),
                                   text_input="STAGE 1", font=get_Font(50), base_color="White", hovering_color="Green")
            STAGE2_BUTTON = Button(image=None, pos=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2 + 70),
                                   text_input="STAGE 2", font=get_Font(50), base_color="White", hovering_color="Green")
            STAGE3_BUTTON = Button(image=None, pos=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2 + 150),
                                   text_input="STAGE 3", font=get_Font(50), base_color="White", hovering_color="Green")
            ENDING_BUTTON = Button(image=None, pos=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2 + 230),
                                   text_input="ENDING", font=get_Font(50), base_color="White", hovering_color="Green")

            INTRO_BUTTON.changeColor(PLAY_MOUSE_POS)
            STAGE1_BUTTON.changeColor(PLAY_MOUSE_POS)
            STAGE2_BUTTON.changeColor(PLAY_MOUSE_POS)
            STAGE3_BUTTON.changeColor(PLAY_MOUSE_POS)
            ENDING_BUTTON.changeColor(PLAY_MOUSE_POS)

            INTRO_BUTTON.update(self.SCREEN)
            STAGE1_BUTTON.update(self.SCREEN)
            STAGE2_BUTTON.update(self.SCREEN)
            STAGE3_BUTTON.update(self.SCREEN)
            ENDING_BUTTON.update(self.SCREEN)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if INTRO_BUTTON.checkForInput(PLAY_MOUSE_POS):
                        intro = Intro(self.SCREEN)
                        intro.run()
                    if STAGE1_BUTTON.checkForInput(PLAY_MOUSE_POS):
                        stage = stages(self.SCREEN, 1)
                        stage.run()
                    if STAGE2_BUTTON.checkForInput(PLAY_MOUSE_POS):
                        stage = stages(self.SCREEN, 2)
                        stage.run()
                    if STAGE3_BUTTON.checkForInput(PLAY_MOUSE_POS):
                        stage = stages(self.SCREEN, 3)
                        stage.run()
                    if ENDING_BUTTON.checkForInput(PLAY_MOUSE_POS):
                        stage = stages(self.SCREEN, 4)
                        stage.run()

            pg.display.update()

    def main_Menu(self):
        while True:
            MOUSE_POS = pg.mouse.get_pos()
            animated_bg = self.animate_background()
            self.SCREEN.blit(animated_bg, (0, 0))

            try:
                PLAY_BUTTON = Button(image=pg.image.load("resources/Play rect.png"),
                                     pos=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2 - 200),
                                     text_input="PLAY", font=get_Font(50), base_color="#e45c5c", hovering_color="Red")
                OPTIONS_BUTTON = Button(image=pg.image.load("resources/Options rect.png"),
                                        pos=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2 - 50),
                                        text_input="OPTIONS", font=get_Font(50), base_color="#e45c5c",
                                        hovering_color="Red")
                LEADERBOARD_BUTTON = Button(image=pg.image.load("resources/Leaderboard rect.png"),
                                            pos=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2 + 100),
                                            text_input="LEADERBOARD", font=get_Font(50), base_color="#e45c5c",
                                            hovering_color="Red")
                QUIT_BUTTON = Button(image=pg.image.load("resources/Quit rect.png"),
                                     pos=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2 + 250),
                                     text_input="QUIT", font=get_Font(50), base_color="#e45c5c", hovering_color="Red")
            except pg.error as e:
                print(f"Error loading images: {e}")
                sys.exit()

            PLAY_BUTTON.changeColor(MOUSE_POS)
            OPTIONS_BUTTON.changeColor(MOUSE_POS)
            LEADERBOARD_BUTTON.changeColor(MOUSE_POS)
            QUIT_BUTTON.changeColor(MOUSE_POS)

            PLAY_BUTTON.update(self.SCREEN)
            OPTIONS_BUTTON.update(self.SCREEN)
            LEADERBOARD_BUTTON.update(self.SCREEN)
            QUIT_BUTTON.update(self.SCREEN)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MOUSE_POS):
                        self.play()
                    if OPTIONS_BUTTON.checkForInput(MOUSE_POS):
                        self.options()
                    if LEADERBOARD_BUTTON.checkForInput(MOUSE_POS):
                        self.leaderboard()
                    if QUIT_BUTTON.checkForInput(MOUSE_POS):
                        pg.quit()
                        sys.exit()

            pg.display.update()

    def title_screen(self):
        while True:
            MOUSE_POS = pg.mouse.get_pos()
            animated_bg = self.animate_background()
            self.SCREEN.blit(animated_bg, (0, 0))

            title_image = pg.image.load("resources/backgrounds/title.gif").convert_alpha()
            title_image = pg.transform.scale(title_image,
                                             (int(title_image.get_width() * 1.2), title_image.get_height()))
            title_rect = title_image.get_rect(center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2.5))
            self.SCREEN.blit(title_image, title_rect)

            prompt_text = get_Font(30).render("Press any key or click to start", True, "White")
            prompt_rect = prompt_text.get_rect(center=(self.SCREEN.get_width() // 2, title_rect.bottom + 50))
            prompt_color = "Red" if prompt_rect.collidepoint(MOUSE_POS) else "White"
            prompt_text = get_Font(30).render("Press any key or click to start", True, prompt_color)
            self.SCREEN.blit(prompt_text, prompt_rect)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                    self.main_Menu()

            pg.display.update()

def main():
    game = game_Menu()
    game.title_screen()

if __name__ == "__main__":
    main()