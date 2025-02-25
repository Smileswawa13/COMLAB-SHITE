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
"""TO DO:
    CLEAN UP CODE AND ADD PROPER COMMENTS
    POLISH
    CHECK FOR UNUSED FUNCTIONS
    HAVE SOME OF THE FUNCTIONS THAT ARE USED EVERYWHERE UNIVERSAL
    ADD SONGS
    PROPER GAME OVER
    STAGE 1 
    STAGE 2
    STAGE 3
    OPTIONS - SOUND, MUSIC, DIFFICULTY
    LEADERBOARD
    CHALLENGE MODE
    TIMED MODE
    MULTIPLAYER MODE
    DE
    LOCKED STAGES
    THREADS
    MAKE EVERYTHING RESIZABLE
    SAVE MODE
    SET UP HIGH SCORES
    ADD ABILITIES IN BETWEEN LEVELS"""

import os
import sys
import numpy as np
import pygame as pg
import introduction
from bgfix import stretch
from buttons import Button, ImageButton
from stages import Stage1, LoadingScreen, Tutorial
from PIL import Image, ImageFilter

pg.init()

width = 930
height = 650

"""UNIVERSAL FUNCTIONS------------------------------------------------------------------------------------------------"""
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

def process_images():
    # Load and blur the background image using Pillow
    pil_acadhall_image = Image.open('resources/backgrounds/acadhall.jpg')
    blurred_acadhall_image = pil_acadhall_image.filter(ImageFilter.BLUR)
    blurred_acadhall_image.save('resources/backgrounds/acadhall_blurred.jpg')

    pil_gym_image = Image.open('resources/backgrounds/gym.png')
    blurred_gym_image = pil_gym_image.filter(ImageFilter.BLUR)
    blurred_gym_image.save('resources/backgrounds/gym_blurred.png')

    pil_room_image = Image.open('resources/backgrounds/room.jpg')
    blurred_room_image = pil_room_image.filter(ImageFilter.BLUR)
    blurred_room_image.save('resources/backgrounds/room_blurred.jpg')

    pil_bedroom_image = Image.open('resources/backgrounds/bedroom.jpg')
    blurred_bedroom_image = pil_bedroom_image.filter(ImageFilter.BLUR)
    blurred_bedroom_image.save('resources/backgrounds/bedrblur.jpg')

"""UNIVERSAL FUNCTIONS------------------------------------------------------------------------------------------------"""

"""#Sorta the whole game ============================================================================================="""
class game_Menu(object):
    def __init__(self):
        # self.SCREEN = pg.display.set_mode((width, height), pg.RESIZABLE)
        self.SCREEN = pg.display.set_mode((width, height))
        pg.display.set_caption("Mapuan Typing Mania")
        self.BG = stretch(pg.image.load("resources/backgrounds/menu.jpg"), (width, height)).convert_alpha()
        self.BG = pg.transform.scale(self.BG, (width, height))
        self.phase = 0

        # Load and play menu song
        pg.mixer.init()
        self.menu_music = "resources/sounds/songs/menu.mp3"
        pg.mixer.music.load(self.menu_music)
        pg.mixer.music.play(-1)

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

    # def handle_resize_event(self, event):
    #     self.SCREEN = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
    #     self.BG = stretch(pg.image.load("resources/backgrounds/menu.jpg"), (event.w, event.h)).convert_alpha()
    #     self.BG = pg.transform.scale(self.BG, (event.w, event.h))

    def play(self):
        while True:
            PLAY_MOUSE_POS = pg.mouse.get_pos()
            animated_bg = self.animate_background()
            self.SCREEN.blit(animated_bg, (0, 0))

            gap = 85  # Define the gap between buttons

            PLAY_TEXT = get_Font(30).render("Choose a stage:", True, "White")
            PLAY_RECT = PLAY_TEXT.get_rect(center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2 - 220))
            self.SCREEN.blit(PLAY_TEXT, PLAY_RECT)

            button_y_start = self.SCREEN.get_height() // 2 - 140

            TUTORIAL_BUTTON = ImageButton(pg.image.load("resources/buttons/tutorial.gif"),
                                          pos=(self.SCREEN.get_width() // 2, button_y_start))
            INTRO_BUTTON = ImageButton(pg.image.load("resources/buttons/intro.gif"),
                                       pos=(self.SCREEN.get_width() // 2, button_y_start + gap))
            STAGE1_BUTTON = ImageButton(pg.image.load("resources/buttons/stage1.gif"),
                                        pos=(self.SCREEN.get_width() // 2, button_y_start + 2 * gap))
            STAGE2_BUTTON = ImageButton(pg.image.load("resources/buttons/stage2.gif"),
                                        pos=(self.SCREEN.get_width() // 2, button_y_start + 3 * gap))
            STAGE3_BUTTON = ImageButton(pg.image.load("resources/buttons/stage3.gif"),
                                        pos=(self.SCREEN.get_width() // 2, button_y_start + 4 * gap))
            ENDING_BUTTON = ImageButton(pg.image.load("resources/buttons/ending.gif"),
                                        pos=(self.SCREEN.get_width() // 2, button_y_start + 5 * gap))

            TUTORIAL_BUTTON.change_size_on_hover(PLAY_MOUSE_POS)
            INTRO_BUTTON.change_size_on_hover(PLAY_MOUSE_POS)
            STAGE1_BUTTON.change_size_on_hover(PLAY_MOUSE_POS)
            STAGE2_BUTTON.change_size_on_hover(PLAY_MOUSE_POS)
            STAGE3_BUTTON.change_size_on_hover(PLAY_MOUSE_POS)
            ENDING_BUTTON.change_size_on_hover(PLAY_MOUSE_POS)

            TUTORIAL_BUTTON.update(self.SCREEN)
            INTRO_BUTTON.update(self.SCREEN)
            STAGE1_BUTTON.update(self.SCREEN)
            STAGE2_BUTTON.update(self.SCREEN)
            STAGE3_BUTTON.update(self.SCREEN)
            ENDING_BUTTON.update(self.SCREEN)

            # Main game loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if TUTORIAL_BUTTON.check_for_input(PLAY_MOUSE_POS):
                        pg.mixer.music.stop()
                        LoadingScreen(self.SCREEN).run()
                        Tutorial(self.SCREEN).run()
                    elif INTRO_BUTTON.check_for_input(PLAY_MOUSE_POS):
                        LoadingScreen(self.SCREEN).run()
                        game_intro = introduction.Intro(self.SCREEN)
                        game_intro.run()
                    elif STAGE1_BUTTON.check_for_input(PLAY_MOUSE_POS):
                        stage_intro = introduction.Stage1Intro(self.SCREEN)
                        stage_intro.run()
                    elif STAGE2_BUTTON.check_for_input(PLAY_MOUSE_POS):
                        LoadingScreen(self.SCREEN).run()
                        game_intro2 = introduction.Stage2Intro(self.SCREEN)
                        game_intro2.run()
                    elif STAGE3_BUTTON.check_for_input(PLAY_MOUSE_POS):
                        LoadingScreen(self.SCREEN).run()
                        Stage1(self.SCREEN, 3).run()
                        Stage1(self.SCREEN, 3).run()
                    elif ENDING_BUTTON.check_for_input(PLAY_MOUSE_POS):
                        LoadingScreen(self.SCREEN).run()
                        Stage1(self.SCREEN, 4).run()
                        break
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    return

            pg.display.update()

    def main_Menu(self):
        while True:
            MOUSE_POS = pg.mouse.get_pos()
            animated_bg = self.animate_background()
            self.SCREEN.blit(animated_bg, (0, 0))

            try:
                PLAY_BUTTON = ImageButton(pg.image.load("resources/buttons/play.gif"),
                                          pos=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2 - 200))
                OPTIONS_BUTTON = ImageButton(pg.image.load("resources/buttons/options.gif"),
                                          pos=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2 - 50))
                LEADERBOARD_BUTTON = ImageButton(pg.image.load("resources/buttons/leaderboard.gif"),
                                            pos=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2 + 100))
                QUIT_BUTTON = ImageButton(pg.image.load("resources/buttons/quit.gif"),
                                         pos=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2 + 250))
            except pg.error as e:
                print(f"Error loading images: {e}")
                sys.exit()

            PLAY_BUTTON.change_size_on_hover(MOUSE_POS)
            OPTIONS_BUTTON.change_size_on_hover(MOUSE_POS)
            LEADERBOARD_BUTTON.change_size_on_hover(MOUSE_POS)
            QUIT_BUTTON.change_size_on_hover(MOUSE_POS)

            PLAY_BUTTON.update(self.SCREEN)
            OPTIONS_BUTTON.update(self.SCREEN)
            LEADERBOARD_BUTTON.update(self.SCREEN)
            QUIT_BUTTON.update(self.SCREEN)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                # elif event.type == pg.VIDEORESIZE:
                #     self.handle_resize_event(event)
                if event.type == pg.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.check_for_input(MOUSE_POS):
                        self.play()
                    elif OPTIONS_BUTTON.check_for_input(MOUSE_POS):
                        self.options()
                    elif LEADERBOARD_BUTTON.check_for_input(MOUSE_POS):
                        self.leaderboard()
                    else:
                        if QUIT_BUTTON.check_for_input(MOUSE_POS):
                            pg.quit()
                            sys.exit()

            pg.display.update()

    def title_screen(self):
        username = ""
        input_active = True
        font = get_Font(30)
        title_image = pg.image.load("resources/backgrounds/title.gif").convert_alpha()
        title_image = pg.transform.scale(title_image,
                                         (int(title_image.get_width() * 1.2), title_image.get_height()))
        title_rect = title_image.get_rect(center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2.5))
        input_box = pg.Rect(self.SCREEN.get_width() // 2 - 100, title_rect.bottom + 70, 200, 50)
        color_inactive = pg.Color(255, 255, 255)
        color_active = pg.Color('red')
        color = color_inactive

        while True:
            MOUSE_POS = pg.mouse.get_pos()
            animated_bg = self.animate_background()
            self.SCREEN.blit(animated_bg, (0, 0))

            self.SCREEN.blit(title_image, title_rect)

            # if input_active:
            #     prompt_text = font.render("Enter your name:", True, "White")
            #     prompt_rect = prompt_text.get_rect(center=(self.SCREEN.get_width() // 2, title_rect.bottom + 50))
            #     self.SCREEN.blit(prompt_text, prompt_rect)
            #
            #     txt_surface = font.render(username, True, color)
            #     width = max(200, txt_surface.get_width() + 10)
            #     input_box.w = width
            #     self.SCREEN.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            #     pg.draw.rect(self.SCREEN, color, input_box, 2)
            # else:
            #     prompt_text = font.render("Press any key to continue", True, "White")
            #     prompt_rect = prompt_text.get_rect(center=(self.SCREEN.get_width() // 2, title_rect.bottom + 50))
            #     prompt_color = "Red" if prompt_rect.collidepoint(MOUSE_POS) else "White"
            #     prompt_text = font.render("Press any key to continue", True, prompt_color)
            #     self.SCREEN.blit(prompt_text, prompt_rect)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                # if input_active:
                #     if event.type == pg.MOUSEBUTTONDOWN:
                #         if input_box.collidepoint(event.pos):
                #             color = color_active
                #         else:
                #             color = color_inactive
                #     if event.type == pg.KEYDOWN:
                #         if event.key == pg.K_RETURN:
                #             input_active = False
                #             with open("resources/players.txt", "a") as file:
                #                 file.write(username + "\n")
                #         elif event.key == pg.K_BACKSPACE:
                #             username = username[:-1]
                #         else:
                #             username += event.unicode
                # else:
                # remember to remove else down here
                else:
                    if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                        self.main_Menu()

            pg.display.update()

"""#Sorta the whole game *class ============================================================================================="""

"""ENGINE SOUNDS VROOM VROOM ============================================================================================="""
def main():
    process_images()  # Run the image processing code before starting the game
    game = game_Menu()
    game.title_screen()

#HOLDER OF REALITY
if __name__ == "__main__":
    main()
"""ENGINE SOUNDS VROOM VROOM ============================================================================================="""