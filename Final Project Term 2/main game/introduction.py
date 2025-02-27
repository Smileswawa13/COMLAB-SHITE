import sys
import threading
import pygame as pg
from bgfix import stretch
from stages import LoadingScreen, Stage1

"""UNIVERSAL FUNCTIONS------------------------------------------------------------------------------------------------"""
# load mixer
pg.mixer.init()

# Import text
def import_text(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
        return ""  # Return an empty string in case of error

# Text generator
def text_generator(text):
    tmp = ''
    for letter in text:
        tmp += letter
        yield tmp  # Yield the current state of the text

# Mao ni nagahimo atung mga linya sa mga intro ug outro
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
        try:
            self._gen = text_generator(self.text[self.current_sentence])
            self.done = False
            self.rendered_sentences = []
            self.current_text = ''
            self.update()
        except Exception as e:
            print(f"Error resetting text: {e}")

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
            except Exception as e:
                print(f"Error updating text: {e}")

    def draw_gradient_rect(self, screen, rect, color1, color2, color3):
        """Draw a vertical gradient rectangle with corner cuts."""
        try:
            color1 = pg.Color(*color1)
            color2 = pg.Color(*color2)
            color3 = pg.Color(*color3)
            height = rect.height
            width = rect.width
            cut_size = 10  # Size of the corner cuts

            # Create a surface with per-pixel alpha
            gradient_surface = pg.Surface((width, height), pg.SRCALPHA)

            half_height = height // 2

            for y in range(height):
                if y < half_height:
                    ratio = y / half_height
                    r = int(color1.r * (1 - ratio) + color2.r * ratio)
                    g = int(color1.g * (1 - ratio) + color2.g * ratio)
                    b = int(color1.b * (1 - ratio) + color2.b * ratio)
                    a = int(color1.a * (1 - ratio) + color2.a * ratio)
                else:
                    ratio = (y - half_height) / half_height
                    r = int(color2.r * (1 - ratio) + color3.r * ratio)
                    g = int(color2.g * (1 - ratio) + color3.g * ratio)
                    b = int(color2.b * (1 - ratio) + color3.b * ratio)
                    a = int(color2.a * (1 - ratio) + color3.a * ratio)

                color = (r, g, b, a)

                if y < cut_size:
                    pg.draw.line(gradient_surface, color, (cut_size - y, y), (width - cut_size + y, y))
                elif y > height - cut_size:
                    pg.draw.line(gradient_surface, color, (y - (height - cut_size), y),
                                 (width - y + (height - cut_size), y))
                else:
                    pg.draw.line(gradient_surface, color, (0, y), (width, y))

            # Blit the gradient surface onto the screen
            screen.blit(gradient_surface, rect.topleft)
        except Exception as e:
            print(f"Error drawing gradient rectangle: {e}")

    def draw(self, screen):
        y_offset = 0
        line_height = self.font.get_height()
        screen_width = screen.get_width()
        shadow_offset = (1.8, 1.8)  # Offset for the text shadow

        try:
            # Calculate the total height of the text block
            total_height = len(self.rendered_sentences) * (line_height + int(line_height * self.line_spacing))
            if not self.done:
                total_height += line_height + int(line_height * self.line_spacing)

            # Draw the gradient background for the entire text block
            text_block_rect = pg.Rect(15, self.pos[1] - 8, screen_width - 60, total_height + 10)
            self.draw_gradient_rect(screen, text_block_rect, (190, 32, 17, 210), (25, 38, 50, 175),
                                    (225, 187, 182, 150))

            for sentence in self.rendered_sentences:
                # Render each sentence with a shadow
                text_rect = sentence.get_rect(center=(screen_width // 2, self.pos[1] + y_offset))
                shadow_rect = text_rect.move(*shadow_offset)
                shadow_surface = self.font.render(self.text[self.rendered_sentences.index(sentence)], True, (0, 0, 0))

                screen.blit(shadow_surface, shadow_rect)
                screen.blit(sentence, text_rect)

                y_offset += line_height + int(line_height * self.line_spacing)

            if not self.done:
                # Render the current text with a shadow
                current_render = self.font.render(self.current_text, True, (255, 255, 255))
                text_rect = current_render.get_rect(center=(screen_width // 2, self.pos[1] + y_offset))
                shadow_rect = text_rect.move(*shadow_offset)
                shadow_surface = self.font.render(self.current_text, True, (0, 0, 0))

                screen.blit(shadow_surface, shadow_rect)
                screen.blit(current_render, text_rect)
        except Exception as e:
            print(f"Error drawing text: {e}")

"""UNIVERSAL FUNCTIONS END ----------------------------------------------------------------------------------------------------

INTRODUCTION START----------------------------------------------------------------------------------------------------"""
class Intro:
    def __init__(self, screen):
        self.SCREEN = screen
        width, height = self.SCREEN.get_size()
        try:
            self.background = stretch(pg.image.load("resources/backgrounds/acadhall_blurred.jpg"),
                                      (width, height)).convert_alpha()
            self.background = pg.transform.smoothscale(self.background, self.SCREEN.get_size())
            self.font = pg.font.Font(None, 22)
            self.text = import_text("resources/introtext.txt")
            self.message = DynamicText(self.font, self.text, (50, 50), speed=20, autoreset=False)
            self.skip_prompt = self.font.render("Press any key to skip", True, (255, 255, 255))
            self.skip_prompt_shadow = self.font.render("Press any key to skip", True, (0, 0, 0))
            self.skip_rect = self.skip_prompt.get_rect(center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - 50))
            self.text_fully_displayed = False

            # Start a new thread to load and play intro music
            self.music_thread = threading.Thread(target=self.load_and_play_music)
            self.music_thread.start()
        except Exception as e:
            print(f"Error initializing Intro: {e}")
            sys.exit()

    def load_and_play_music(self):
        try:
            # Load and play intro song
            self.intro_music = "resources/sounds/songs/intro.mp3"
            pg.mixer.music.load(self.intro_music)
            pg.mixer.music.play(-1)
        except Exception as e:
            print(f"Error loading and playing music: {e}")

    def run(self):
        pg.time.set_timer(pg.USEREVENT, self.message.speed)
        while True:
            try:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type == pg.USEREVENT:
                        self.message.update()
                    if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                            pg.mixer.music.stop()
                            from mapuantypingmania import game_Menu
                            game = game_Menu()
                            game.play()

                        if self.text_fully_displayed:
                            try:
                                if event.type == pg.KEYDOWN:
                                    LoadingScreen(self.SCREEN).run()
                                    pg.mixer.music.stop()
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
            except Exception as e:
                print(f"Error running intro: {e}")
"""INTRODUCTION END --------------------------------------------------------------------------------------------------------

STAGE 1 INTRO-OUTRO START----------------------------------------------------------------------------------------------------"""
class Stage1Intro:
    def __init__(self, screen):
        self.SCREEN = screen
        width, height = self.SCREEN.get_size()
        try:
            self.background = stretch(pg.image.load("resources/backgrounds/room_blurred.jpg"),
                                      (width, height)).convert_alpha()
            self.background = pg.transform.smoothscale(self.background, self.SCREEN.get_size())
            self.font = pg.font.Font(None, 22)
            self.text = import_text("resources/stage1intro.txt")
            self.message = DynamicText(self.font, self.text, (50, 50), speed=20, autoreset=False)
            self.skip_prompt = self.font.render("Press any key to skip", True, (255, 255, 255))
            self.skip_prompt_shadow = self.font.render("Press any key to skip", True, (0, 0, 0))
            self.skip_rect = self.skip_prompt.get_rect(center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - 50))
            self.text_fully_displayed = False

            # Start a new thread to load and play intro music
            self.music_thread = threading.Thread(target=self.load_and_play_music)
            self.music_thread.start()
        except Exception as e:
            print(f"Error initializing Stage1Intro: {e}")
            sys.exit()

    def load_and_play_music(self):
        try:
            # Load and play intro song
            self.music = "resources/sounds/songs/s1_inout.mp3"
            pg.mixer.music.load(self.music)
            pg.mixer.music.play(-1)
        except Exception as e:
            print(f"Error loading and playing music: {e}")

    def run(self):
        pg.time.set_timer(pg.USEREVENT, self.message.speed)
        while True:
            try:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type == pg.USEREVENT:
                        self.message.update()
                    if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                            pg.mixer.music.stop()
                            from mapuantypingmania import game_Menu
                            game = game_Menu()
                            game.play()
                        if self.text_fully_displayed:
                            try:
                                if event.type == pg.KEYDOWN:
                                    pg.mixer.music.stop()
                                    LoadingScreen(self.SCREEN).run()
                                    Stage1(self.SCREEN, 1).run()
                                    return
                            except Exception as e:
                                print(f"Error loading next stage {e}")
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
            except Exception as e:
                print(f"Error running Stage1Intro: {e}")

class Stage1Outro:
    def __init__(self, screen):
        self.SCREEN = screen
        width, height = self.SCREEN.get_size()
        try:
            self.background = stretch(pg.image.load("resources/backgrounds/room_blurred.jpg"),
                                      (width, height)).convert_alpha()
            self.background = pg.transform.smoothscale(self.background, self.SCREEN.get_size())
            self.font = pg.font.Font(None, 22)
            self.text = import_text("resources/stage1outro.txt")
            self.message = DynamicText(self.font, self.text, (50, 50), speed=20, autoreset=False)
            self.skip_prompt = self.font.render("Press any key to skip", True, (255, 255, 255))
            self.skip_prompt_shadow = self.font.render("Press any key to skip", True, (0, 0, 0))
            self.skip_rect = self.skip_prompt.get_rect(center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - 50))
            self.text_fully_displayed = False
        except Exception as e:
            print(f"Error initializing Stage1Outro: {e}")
            sys.exit()

    def load_and_play_music(self):
        try:
            # Load and play outro song
            self.music = "resources/sounds/songs/s1_inout.mp3"
            pg.mixer.music.load(self.music)
            pg.mixer.music.play(-1)
        except Exception as e:
            print(f"Error loading and playing music: {e}")

    def run(self):
        pg.time.set_timer(pg.USEREVENT, self.message.speed)
        while True:
            try:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type == pg.USEREVENT:
                        self.message.update()
                    if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                            pg.mixer.music.stop()
                            from mapuantypingmania import game_Menu
                            game = game_Menu()
                            game.play()
                        if self.text_fully_displayed:
                            try:
                                if event.type == pg.KEYDOWN:
                                    LoadingScreen(self.SCREEN).run()
                                    pg.mixer.music.stop()
                                    Stage2Intro(self.SCREEN).run()
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
            except Exception as e:
                print(f"Error running Stage1Outro: {e}")
"""STAGE 1 INTRO-OUTRO END ----------------------------------------------------------------------------------------------------

STAGE 2 INTRO-OUTRO START----------------------------------------------------------------------------------------------------"""


class Stage2Intro:
    def __init__(self, screen):
        self.SCREEN = screen
        width, height = self.SCREEN.get_size()
        self.background = stretch(pg.image.load("resources/backgrounds/gym_blurred.png"),
                                  (width, height)).convert_alpha()
        self.background = pg.transform.smoothscale(self.background, self.SCREEN.get_size())
        self.font = pg.font.Font(None, 20)
        self.text = import_text("resources/stage2intro.txt")
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
        self.background = stretch(pg.image.load("resources/backgrounds/gym_blurred.png"),
                                  (width, height)).convert_alpha()
        self.background = pg.transform.smoothscale(self.background, self.SCREEN.get_size())
        self.font = pg.font.Font(None, 22)
        self.text = import_text("resources/stage2outro.txt")
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
                                Stage3Intro(self.SCREEN).run()
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

STAGE 3 INTRO-OUTRO START--------------------------------------------------------------------------------------------"""
class Stage3Intro:
    def __init__(self, screen):
        self.SCREEN = screen
        width, height = self.SCREEN.get_size()
        self.background = stretch(pg.image.load("resources/backgrounds/plaza_blurred.jpg"),
                                  (width, height)).convert_alpha()
        self.background = pg.transform.smoothscale(self.background, self.SCREEN.get_size())
        self.font = pg.font.Font(None, 24)
        self.text = import_text("resources/stage3intro.txt")
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
                                from stages import Stage3
                                Stage3(self.SCREEN, 3).run()
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


class Stage3Outro:
    def __init__(self, screen):
        self.SCREEN = screen
        width, height = self.SCREEN.get_size()
        self.background = stretch(pg.image.load("resources/backgrounds/plaza_blurred.jpg"),
                                  (width, height)).convert_alpha()
        self.background = pg.transform.smoothscale(self.background, self.SCREEN.get_size())
        self.font = pg.font.Font(None, 24)
        self.text = import_text("resources/stage3outro.txt")
        self.message = DynamicText(self.font, self.text, (50, 50), speed=20, autoreset=False)
        self.skip_prompt = self.font.render("Press any key to skip", True, (255, 255, 255))
        self.skip_prompt_shadow = self.font.render("Press any key to skip", True, (0, 0, 0))
        self.skip_rect = self.skip_prompt.get_rect(
            center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - 50))
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
                                from endings import Ending
                                Ending(self.SCREEN).run()
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
                        self.skip_prompt_shadow = self.font.render(
                            "Press any key to continue or press esc to go back",
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


"""STAGE 3 INTRO-OUTRO END ---------------------------------------------------------------------------------------------"""
