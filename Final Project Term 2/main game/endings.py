import sys
import pygame as pg
from bgfix import stretch
from introduction import DynamicText
import introduction

"""ENDING START---------------------------------------------------------------------------------------------------"""

class Ending:
    def __init__(self, screen):
        self.SCREEN = screen
        width, height = self.SCREEN.get_size()
        self.background = stretch(pg.image.load("resources/backgrounds/bedrblur.jpg"), (width, height)).convert_alpha()
        self.background = pg.transform.smoothscale(self.background, self.SCREEN.get_size())
        self.font = pg.font.Font(None, 20)
        self.text = introduction.import_text("resources/ending.txt")
        self.message = DynamicText(self.font, self.text, (50, 50), speed=20, autoreset=False)
        self.skip_prompt = self.font.render("Press any key to skip", True, (255, 255, 255))
        self.skip_prompt_shadow = self.font.render("Press any key to skip", True, (0, 0, 0))
        self.skip_rect = self.skip_prompt.get_rect(center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - 50))
        self.text_fully_displayed = False
        self.fade_alpha = 0
        self.fading = False

    def run(self):
        pg.time.set_timer(pg.USEREVENT, self.message.speed)
        credits = CREDITS(self.SCREEN)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.USEREVENT:
                    self.message.update()
                if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                    if self.text_fully_displayed:
                        self.fading = True
                    else:
                        self.text_fully_displayed = True
                        self.message.done = True
                        self.message.rendered_sentences = [self.font.render(line, True, (255, 255, 255))
                                                           for line in self.text.split('\n')]
                        self.skip_prompt = self.font.render("Press any key to continue", True, (255, 255, 255))
                        self.skip_prompt_shadow = self.font.render("Press any key to continue", True, (0, 0, 0))
                        self.skip_rect = self.skip_prompt.get_rect(
                            center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - 50))

            if self.fading:
                self.fade_alpha = min(self.fade_alpha + 5, 255)
                fade_surface = pg.Surface(self.SCREEN.get_size())
                fade_surface.fill((0, 0, 0))
                fade_surface.set_alpha(self.fade_alpha)
                self.SCREEN.blit(fade_surface, (0, 0))
                if self.fade_alpha == 255:
                    credits.run()
            else:
                self.SCREEN.blit(self.background, (0, 0))
                self.message.draw(self.SCREEN)
                self.SCREEN.blit(self.skip_prompt_shadow, self.skip_rect.move(2, 2))
                self.SCREEN.blit(self.skip_prompt, self.skip_rect)

            pg.display.flip()
            pg.time.Clock().tick(60)

"""ENDINGS END ----------------------------------------------------------------------------------------------------

CREDITS START----------------------------------------------------------------------------------------------------"""

class CREDITS:
    def __init__(self, screen):
        self.SCREEN = screen
        width, height = self.SCREEN.get_size()
        self.backgrounds = [
            stretch(pg.image.load(f"resources/backgrounds/{img}"), (width, height)).convert_alpha()
            for img in ["gym_blurred.png", "acadhall_blurred.jpg", "bedrblur.jpg", "plaza_blurred.jpg", "room_blurred.jpg"]
        ]
        self.current_bg_index = 0
        self.fade_alpha = 0
        self.fade_in = True
        self.font = pg.font.Font(None, 24)
        self.text = self.import_text("resources/credits.txt").split('\n')
        self.skip_prompt = self.font.render("Press ESC to exit", True, (255, 255, 255))
        self.skip_prompt_shadow = self.font.render("Press ESC to exit", True, (0, 0, 0))
        self.skip_rect = self.skip_prompt.get_rect(
            center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - 50))
        self.last_switch_time = pg.time.get_ticks()

    def run(self):
        pg.time.set_timer(pg.USEREVENT, 100)
        from mapuantypingmania import game_Menu
        game = game_Menu()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.USEREVENT:
                    pass
                if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                    if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        game.play()
                        return  # Exit the credits loop and return to the main menu

            self.update_background()
            self.SCREEN.blit(self.backgrounds[self.current_bg_index], (0, 0))
            self.draw_text()
            self.SCREEN.blit(self.skip_prompt_shadow, self.skip_rect.move(2, 2))
            self.SCREEN.blit(self.skip_prompt, self.skip_rect)
            pg.display.flip()
            pg.time.Clock().tick(60)

    def update_background(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_switch_time > 5000:  # Switch every 5 seconds
            self.last_switch_time = current_time
            self.fade_in = not self.fade_in
            if not self.fade_in:
                self.current_bg_index = (self.current_bg_index + 1) % len(self.backgrounds)

        if self.fade_in:
            self.fade_alpha = min(self.fade_alpha + 5, 255)
        else:
            self.fade_alpha = max(self.fade_alpha - 5, 0)

        self.backgrounds[self.current_bg_index].set_alpha(self.fade_alpha)

    def draw_text(self):
        screen_width = self.SCREEN.get_width()
        screen_height = self.SCREEN.get_height()
        line_height = self.font.get_height()
        y_offset = 50
        shadow_offset = (2, 2)

        # Draw gradient background
        text_block_rect = pg.Rect(15, y_offset - 8, screen_width - 30, screen_height - y_offset)
        self.draw_gradient_rect(self.SCREEN, text_block_rect, (168, 0, 0, 150), (38, 19, 94, 150))

        # Draw the first four sentences in the center
        for i in range(4):
            sentence = self.text[i]
            text_surface = self.font.render(sentence, True, (255, 255, 255))
            shadow_surface = self.font.render(sentence, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(screen_width // 2, y_offset))
            shadow_rect = text_rect.move(*shadow_offset)
            self.SCREEN.blit(shadow_surface, shadow_rect)
            self.SCREEN.blit(text_surface, text_rect)
            y_offset += line_height + 10

        # Draw the remaining sentences in three columns
        col1_x = screen_width // 6
        col2_x = screen_width // 2
        col3_x = 5 * screen_width // 6
        col1_y_offset = y_offset
        col2_y_offset = y_offset
        col3_y_offset = y_offset

        # Donut man and Cold in the first column
        for i in range(4, 17):
            sentence = self.text[i]
            text_surface = self.font.render(sentence, True, (255, 255, 255))
            shadow_surface = self.font.render(sentence, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(col1_x, col1_y_offset))
            shadow_rect = text_rect.move(*shadow_offset)
            self.SCREEN.blit(shadow_surface, shadow_rect)
            self.SCREEN.blit(text_surface, text_rect)
            col1_y_offset += line_height + 10

        # Ma'am mmy in the middle column
        for i in range(17, 21):
            sentence = self.text[i]
            text_surface = self.font.render(sentence, True, (255, 255, 255))
            shadow_surface = self.font.render(sentence, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(col2_x, col2_y_offset))
            shadow_rect = text_rect.move(*shadow_offset)
            self.SCREEN.blit(shadow_surface, shadow_rect)
            self.SCREEN.blit(text_surface, text_rect)
            col2_y_offset += line_height + 10

        # Tan and Hao in the third column
        for i in range(22, len(self.text)):
            sentence = self.text[i]
            text_surface = self.font.render(sentence, True, (255, 255, 255))
            shadow_surface = self.font.render(sentence, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(col3_x, col3_y_offset))
            shadow_rect = text_rect.move(*shadow_offset)
            self.SCREEN.blit(shadow_surface, shadow_rect)
            self.SCREEN.blit(text_surface, text_rect)
            col3_y_offset += line_height + 10

    def draw_gradient_rect(self, surface, rect, color1, color2):
        """Draw a vertical gradient rectangle with rounded corners."""
        color1 = pg.Color(*color1)
        color2 = pg.Color(*color2)
        height = rect.height
        width = rect.width
        radius = 20  # Radius for rounded corners

        # Create a surface with per-pixel alpha
        gradient_surface = pg.Surface((width, height), pg.SRCALPHA)

        # Draw the gradient
        for y in range(height):
            color = color1.lerp(color2, y / height)
            pg.draw.line(gradient_surface, color, (0, y), (width, y))

        # Create a mask for rounded corners
        mask = pg.Surface((width, height), pg.SRCALPHA)
        pg.draw.rect(mask, (255, 255, 255, 255), (0, 0, width, height), border_radius=radius)

        # Apply the mask to the gradient surface
        gradient_surface.blit(mask, (0, 0), special_flags=pg.BLEND_RGBA_MIN)

        # Blit the gradient surface onto the target surface
        surface.blit(gradient_surface, rect.topleft)

    def import_text(self, filename):
        with open(filename, 'r') as file:
            return file.read()

"""CREDITS END----------------------------------------------------------------------------------------------------"""