import sys
import pygame as pg
from PIL import Image, ImageFilter
from bgfix import stretch
from stages import LoadingScreen, Stage1

"""UNIVERSAL FUNCTIONS------------------------------------------------------------------------------------------------"""
# Import text
def import_text_intro(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def text_generator(text):
    tmp = ''
    for letter in text:
        tmp += letter
        yield tmp

class DynamicText:
    def __init__(self, font, text, pos, speed=20, autoreset=False, line_spacing=0.5):
        self.done = False
        self.font = font
        self.text = text.split('\n')
        self.pos = pos
        self.speed = speed
        self.autoreset = autoreset
        self.line_spacing = line_spacing
        self.current_sentence = 0
        self._gen = text_generator(self.text[self.current_sentence])
        self.rendered_sentences = []
        self.current_text = ''
        self.update()

    def reset(self):
        self._gen = text_generator(self.text[self.current_sentence])
        self.done = False
        self.rendered_sentences = []
        self.current_text = ''
        self.update()

    def update(self):
        if not self.done:
            try:
                self.current_text = next(self._gen)
            except StopIteration:
                self.rendered_sentences.append(self.font.render(self.current_text, True, (255, 255, 255)))
                self.current_sentence += 1
                if self.current_sentence < len(self.text):
                    self._gen = text_generator(self.text[self.current_sentence])
                    self.current_text = ''
                else:
                    self.done = True
                    if self.autoreset:
                        self.current_sentence = 0
                        self.reset()

    def draw(self, screen):
        y_offset = 0
        line_height = self.font.get_height()
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        shadow_offset = (1, 1)  # Offset for the text shadow

        # Calculate the maximum number of lines that can fit on the screen
        max_lines = screen_height // (line_height + int(line_height * self.line_spacing))

        previous_rect = None

        for sentence in self.rendered_sentences[:max_lines]:
            text_rect = sentence.get_rect(center=(screen_width // 2, self.pos[1] + y_offset))
            shadow_rect = text_rect.move(*shadow_offset)
            shadow_surface = self.font.render(self.text[self.rendered_sentences.index(sentence)], True, (0, 0, 0))

            # Draw gradient background with corner cuts
            self.draw_gradient_rect(screen, text_rect.inflate(10, 10), (212, 57, 57, 150), (57, 57, 212, 150))

            screen.blit(shadow_surface, shadow_rect)
            screen.blit(sentence, text_rect)

            if previous_rect and text_rect.colliderect(previous_rect):
                y_offset += 2  # Add a 2-pixel gap if overlap is detected

            y_offset += line_height + int(line_height * self.line_spacing)
            previous_rect = text_rect

        if not self.done and self.current_sentence < max_lines:
            current_render = self.font.render(self.current_text, True, (255, 255, 255))
            text_rect = current_render.get_rect(center=(screen_width // 2, self.pos[1] + y_offset))
            shadow_rect = text_rect.move(*shadow_offset)
            shadow_surface = self.font.render(self.current_text, True, (0, 0, 0))

            # Draw gradient background with corner cuts
            self.draw_gradient_rect(screen, text_rect.inflate(10, 10), (212, 57, 57, 150), (57, 57, 212, 150))

            screen.blit(shadow_surface, shadow_rect)
            screen.blit(current_render, text_rect)

    def draw_gradient_rect(self, screen, rect, color1, color2, overlap_rect=None):
        """Draw a vertical gradient rectangle with corner cuts."""
        color1 = pg.Color(*color1)
        color2 = pg.Color(*color2)
        height = rect.height
        width = rect.width
        cut_size = 10  # Size of the corner cuts

        # Create a surface with per-pixel alpha
        gradient_surface = pg.Surface((width, height), pg.SRCALPHA)

        for y in range(height):
            ratio = y / height
            r = int(color1.r * (1 - ratio) + color2.r * ratio)
            g = int(color1.g * (1 - ratio) + color2.g * ratio)
            b = int(color1.b * (1 - ratio) + color2.b * ratio)
            a = int(color1.a * (1 - ratio) + color2.a * ratio)
            color = (r, g, b, a)

            if y < cut_size:
                pg.draw.line(gradient_surface, color, (cut_size - y, y), (width - cut_size + y, y))
            elif y > height - cut_size:
                pg.draw.line(gradient_surface, color, (y - (height - cut_size), y),
                             (width - y + (height - cut_size), y))
            else:
                pg.draw.line(gradient_surface, color, (0, y), (width, y))

        if overlap_rect:
            gradient_surface.set_clip(overlap_rect)

        # Blit the gradient surface onto the screen
        screen.blit(gradient_surface, rect.topleft)

"""UNIVERSAL FUNCTIONS END ----------------------------------------------------------------------------------------------------

INTRODUCTION START----------------------------------------------------------------------------------------------------"""
class Intro:
    def __init__(self, screen):
        self.SCREEN = screen
        width, height = self.SCREEN.get_size()
        self.background = stretch(pg.image.load("resources/backgrounds/acadhall_blurred.jpg"), (width, height)).convert_alpha()
        self.background = pg.transform.smoothscale(self.background, self.SCREEN.get_size())
        self.font = pg.font.Font(None, 22)
        self.text = import_text_intro("resources/introtext.txt")
        self.message = DynamicText(self.font, self.text, (50, 50), speed=20, autoreset=False)
        self.skip_prompt = self.font.render("Press any key to skip", True, (255, 255, 255))
        self.skip_prompt_shadow = self.font.render("Press any key to skip", True, (0, 0, 0))
        self.skip_rect = self.skip_prompt.get_rect(center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - 50))
        self.text_fully_displayed = False

    def run(self):
        pg.time.set_timer(pg.USEREVENT, self.message.speed)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.USEREVENT:
                    self.message.update()
                if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                    if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        from mapuantypingmania import game_Menu
                        game = game_Menu()
                        game.play()
                    if self.text_fully_displayed:
                        try:
                            if event.type == pg.KEYDOWN:
                                LoadingScreen(self.SCREEN).run()
                                Stage1Intro(self.SCREEN).run()
                        except Exception as e:
                            print(e)
                    else:
                        self.text_fully_displayed = True
                        self.message.done = True
                        self.message.rendered_sentences = [self.font.render(line, True, (255, 255, 255))
                                                           for line in self.text.split('\n')]
                        self.skip_prompt = self.font.render("Press any key to continue or press esc to go back",
                                                            True,
                                                            (255, 255, 255))
                        self.skip_prompt_shadow = self.font.render("Press any key to continue or press esc to go back",
                                                                  True,
                                                                  (0, 0, 0))
                        self.skip_rect = self.skip_prompt.get_rect(
                            center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - 50))


            self.SCREEN.blit(self.background, (0, 0))
            self.message.draw(self.SCREEN)
            self.SCREEN.blit(self.skip_prompt_shadow, self.skip_rect.move(2, 2))
            self.SCREEN.blit(self.skip_prompt, self.skip_rect)
            pg.display.flip()
            pg.time.Clock().tick(60)
"""INTRODUCTION END --------------------------------------------------------------------------------------------------------

STAGE 1 INTRO-OUTRO START----------------------------------------------------------------------------------------------------"""
class Stage1Intro:
    def __init__(self, screen):
        self.SCREEN = screen
        width, height = self.SCREEN.get_size()
        self.background = stretch(pg.image.load("resources/backgrounds/room_blurred.jpg"), (width, height)).convert_alpha()
        self.background = pg.transform.smoothscale(self.background, self.SCREEN.get_size())
        self.font = pg.font.Font(None, 22)
        self.text = import_text_intro("resources/stage1intro.txt")
        self.message = DynamicText(self.font, self.text, (50, 50), speed=20, autoreset=False)
        self.skip_prompt = self.font.render("Press any key to skip", True, (255, 255, 255))
        self.skip_prompt_shadow = self.font.render("Press any key to skip", True, (0, 0, 0))
        self.skip_rect = self.skip_prompt.get_rect(center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - 50))
        self.text_fully_displayed = False

    def run(self):
        pg.time.set_timer(pg.USEREVENT, self.message.speed)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.USEREVENT:
                    self.message.update()
                if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                    if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        from mapuantypingmania import game_Menu
                        game = game_Menu()
                        game.play()
                    if self.text_fully_displayed:
                        try:
                            if event.type == pg.KEYDOWN:
                                LoadingScreen(self.SCREEN).run()
                                Stage1(self.SCREEN, 1).run()
                                return
                        except Exception as e:
                            print(e)
                    else:
                        self.text_fully_displayed = True
                        self.message.done = True
                        self.message.rendered_sentences = [self.font.render(line, True, (255, 255, 255))
                                                           for line in self.text.split('\n')]
                        self.skip_prompt = self.font.render("Press any key to continue or press esc to go back",
                                                            True,
                                                            (255, 255, 255))
                        self.skip_prompt_shadow = self.font.render("Press any key to continue or press esc to go back",
                                                                   True,
                                                                   (0, 0, 0))
                        self.skip_rect = self.skip_prompt.get_rect(
                            center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - 50))

            self.SCREEN.blit(self.background, (0, 0))
            self.message.draw(self.SCREEN)
            self.SCREEN.blit(self.skip_prompt_shadow, self.skip_rect.move(2, 2))
            self.SCREEN.blit(self.skip_prompt, self.skip_rect)
            pg.display.flip()
            pg.time.Clock().tick(60)

class Stage1Outro:
    def __init__(self, screen):
        self.SCREEN = screen
        width, height = self.SCREEN.get_size()

        self.background = stretch(pg.image.load("resources/backgrounds/room_blurred.jpg"), (width, height)).convert_alpha()
        self.background = pg.transform.smoothscale(self.background, self.SCREEN.get_size())
        self.font = pg.font.Font(None, 22)
        self.text = import_text_intro("resources/stage1outro.txt")
        self.message = DynamicText(self.font, self.text, (50, 50), speed=20, autoreset=False)
        self.skip_prompt = self.font.render("Press any key to skip", True, (255, 255, 255))
        self.skip_prompt_shadow = self.font.render("Press any key to skip", True, (0, 0, 0))
        self.skip_rect = self.skip_prompt.get_rect(center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - 50))
        self.text_fully_displayed = False

    def run(self):
        pg.time.set_timer(pg.USEREVENT, self.message.speed)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.USEREVENT:
                    self.message.update()
                if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                    if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        from mapuantypingmania import game_Menu
                        game = game_Menu()
                        game.play()
                    if self.text_fully_displayed:
                        try:
                            if event.type == pg.KEYDOWN:
                                LoadingScreen(self.SCREEN).run()
                                from stages import Stage2
                                Stage2(self.SCREEN, 2).run()
                                return
                        except Exception as e:
                            print(e)
                    else:
                        self.text_fully_displayed = True
                        self.message.done = True
                        self.message.rendered_sentences = [self.font.render(line, True, (255, 255, 255))
                                                           for line in self.text.split('\n')]
                        self.skip_prompt = self.font.render("Press any key to continue or press esc to go back",
                                                            True,
                                                            (255, 255, 255))
                        self.skip_prompt_shadow = self.font.render("Press any key to continue or press esc to go back",
                                                                   True,
                                                                   (0, 0, 0))
                        self.skip_rect = self.skip_prompt.get_rect(
                            center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - 50))

            self.SCREEN.blit(self.background, (0, 0))
            self.message.draw(self.SCREEN)
            self.SCREEN.blit(self.skip_prompt_shadow, self.skip_rect.move(2, 2))
            self.SCREEN.blit(self.skip_prompt, self.skip_rect)
            pg.display.flip()
            pg.time.Clock().tick(60)

"""STAGE 1 INTRO-OUTRO END ----------------------------------------------------------------------------------------------------

STAGE 2 INTRO-OUTRO START----------------------------------------------------------------------------------------------------"""

class Stage2Intro:
    def __init__(self, screen):
        self.SCREEN = screen
        width, height = self.SCREEN.get_size()
        self.background = stretch(pg.image.load("resources/backgrounds/gym_blurred.png"), (width, height)).convert_alpha()
        self.background = pg.transform.smoothscale(self.background, self.SCREEN.get_size())
        self.font = pg.font.Font(None, 20)
        self.text = import_text_intro("resources/stage2intro.txt")
        self.message = DynamicText(self.font, self.text, (50, 50), speed=20, autoreset=False)
        self.skip_prompt = self.font.render("Press any key to skip", True, (255, 255, 255))
        self.skip_prompt_shadow = self.font.render("Press any key to skip", True, (0, 0, 0))
        self.skip_rect = self.skip_prompt.get_rect(center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - 50))
        self.text_fully_displayed = False

    def run(self):
        pg.time.set_timer(pg.USEREVENT, self.message.speed)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.USEREVENT:
                    self.message.update()
                if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                    if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        from mapuantypingmania import game_Menu
                        game = game_Menu()
                        game.play()
                    if self.text_fully_displayed:
                        try:
                            if event.type == pg.KEYDOWN:
                                LoadingScreen(self.SCREEN).run()
                                from stages import Stage2
                                Stage2(self.SCREEN, 2).run()
                                return
                        except Exception as e:
                            print(e)
                    else:
                        self.text_fully_displayed = True
                        self.message.done = True
                        self.message.rendered_sentences = [self.font.render(line, True, (255, 255, 255))
                                                           for line in self.text.split('\n')]
                        self.skip_prompt = self.font.render("Press any key to continue or press esc to go back",
                                                            True,
                                                            (255, 255, 255))
                        self.skip_prompt_shadow = self.font.render("Press any key to continue or press esc to go back",
                                                                   True,
                                                                   (0, 0, 0))
                        self.skip_rect = self.skip_prompt.get_rect(
                            center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - 50))

            self.SCREEN.blit(self.background, (0, 0))
            self.message.draw(self.SCREEN)
            self.SCREEN.blit(self.skip_prompt_shadow, self.skip_rect.move(2, 2))
            self.SCREEN.blit(self.skip_prompt, self.skip_rect)
            pg.display.flip()
            pg.time.Clock().tick(60)

class Stage2Outro:
    def __init__(self, screen):
        self.SCREEN = screen
        width, height = self.SCREEN.get_size()
        self.background = stretch(pg.image.load("resources/backgrounds/gym_blurred.png"), (width, height)).convert_alpha()
        self.background = pg.transform.smoothscale(self.background, self.SCREEN.get_size())
        self.font = pg.font.Font(None, 22)
        self.text = import_text_intro("resources/stage2outro.txt")
        self.message = DynamicText(self.font, self.text, (50, 50), speed=20, autoreset=False)
        self.skip_prompt = self.font.render("Press any key to skip", True, (255, 255, 255))
        self.skip_prompt_shadow = self.font.render("Press any key to skip", True, (0, 0, 0))
        self.skip_rect = self.skip_prompt.get_rect(center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - 50))
        self.text_fully_displayed = False

    def run(self):
        pg.time.set_timer(pg.USEREVENT, self.message.speed)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.USEREVENT:
                    self.message.update()
                if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                    if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        from mapuantypingmania import game_Menu
                        game = game_Menu()
                        game.play()
                    if self.text_fully_displayed:
                        try:
                            if event.type == pg.KEYDOWN:
                                LoadingScreen(self.SCREEN).run()
                                # from stages import Stage3
                                # Stage3(self.SCREEN, 3).run()
                                return
                        except Exception as e:
                            print(e)
                    else:
                        self.text_fully_displayed = True
                        self.message.done = True
                        self.message.rendered_sentences = [self.font.render(line, True, (255, 255, 255))
                                                           for line in self.text.split('\n')]
                        self.skip_prompt = self.font.render("Press any key to continue or press esc to go back",
                                                            True,
                                                            (255, 255, 255))
                        self.skip_prompt_shadow = self.font.render("Press any key to continue or press esc to go back",
                                                                   True,
                                                                   (0, 0, 0))
                        self.skip_rect = self.skip_prompt.get_rect(
                            center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - 50))

            self.SCREEN.blit(self.background, (0, 0))
            self.message.draw(self.SCREEN)
            self.SCREEN.blit(self.skip_prompt_shadow, self.skip_rect.move(2, 2))
            self.SCREEN.blit(self.skip_prompt, self.skip_rect)
            pg.display.flip()
            pg.time.Clock().tick(60)

"""STAGE 2 INTRO-OUTRO END ---------------------------------------------------------------------------------------------

STAGE 3 INTRO-OUTRO START----------------------------------------------------------------------------------------------------"""