import pygame as pg
import random
from mapuantypingmania import apply_wave_effect
import numpy as np

class Leaderboard:
    def __init__(self, screen):
        self.SCREEN = screen
        width, height = self.SCREEN.get_size()
        self.font = pg.font.Font(None, 30)
        self.title_font = pg.font.Font(None, 40)
        self.prompt_font = pg.font.Font(None, 25)
        self.background_path = "resources/backgrounds/menu.jpg"
        self.scorefile_path = "resources/highscore.txt"
        self.max_leaders = 6
        try:
            self.background = pg.image.load(self.background_path)
            self.background = pg.transform.scale(self.background, (width, height))
        except Exception as e:
            print(f"Error loading background: {e}")
            self.background = pg.Surface((width, height))
        self.phase = 0

    def quick_sort(self, arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[0]
        left = [item for item in arr[1:] if item[1] > pivot[1]]
        right = [item for item in arr[1:] if item[1] <= pivot[1]]
        return self.quick_sort(left) + [pivot] + self.quick_sort(right)

    def load_scores(self):
        try:
            with open(self.scorefile_path, "r") as file:
                scores = {}
                for line in file.readlines():
                    if ':' in line:
                        name, score_str = line.strip().split(":", 1)
                        try:
                            score = int(score_str.strip())
                        except ValueError:
                            score = 0
                        scores[name.strip()] = score
            items = list(scores.items())
            sorted_scores = self.quick_sort(items)
            return sorted_scores[:self.max_leaders]
        except IOError:
            return []

    def animate_background(self):
        amplitude = 5
        frequency = 0.01
        color_shift = 50
        self.phase += 0.05

        # Calculate color transition based on phase
        t = (np.sin(self.phase) + 1) / 2
        r = int(255 * (1 - t) + 128 * t)
        g = int(200 * (1 - t) + 128 * t)
        b = int(100 * (1 - t) + 128 * t)
        bg_color = (r, g, b)

        try:
            # Apply wave effect to the background image
            wavy_bg = apply_wave_effect(self.background.copy(), amplitude, frequency, self.phase, color_shift)
            wavy_bg.fill(bg_color, special_flags=pg.BLEND_RGBA_MULT)
        except Exception as e:
            print(f"Error animating background: {e}")
            return self.background  # Return the original background in case of error

        return wavy_bg

    def run(self):
        clock = pg.time.Clock()
        while True:
            animated_bg = self.animate_background()
            try:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        return
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            return

                self.SCREEN.blit(animated_bg, (0, 0))

                # Calculate the vertical starting position as 1/4 of the screen's height
                quarter_height = self.SCREEN.get_height() // 4

                # Draw centered title at 1/4 down the screen
                title_text = self.title_font.render("HIGHSCORES:", True, (255, 215, 0))
                title_shadow = self.title_font.render("HIGHSCORES:", True, (0, 0, 0))
                title_rect = title_text.get_rect(center=(self.SCREEN.get_width() // 2, quarter_height))
                self.SCREEN.blit(title_shadow, title_rect.move(2, 2))
                self.SCREEN.blit(title_text, title_rect)

                # Define an offset so that the scores start a few pixels below the title
                score_start_y = quarter_height + 50

                # Draw centered scores starting below the title
                scores = self.load_scores()
                for i, (name, score) in enumerate(scores):
                    line = f"{name}  {score}"
                    text = self.font.render(line, True, (255, 255, 255))
                    text_shadow = self.font.render(line, True, (0, 0, 0))
                    text_rect = text.get_rect(center=(self.SCREEN.get_width() // 2, score_start_y + i * 35))
                    self.SCREEN.blit(text_shadow, text_rect.move(2, 2))
                    self.SCREEN.blit(text, text_rect)

                # Draw shadowed prompt centered at bottom
                prompt = "Press ESC to go back to main menu"
                prompt_shadow = self.prompt_font.render(prompt, True, (0, 0, 0))
                prompt_text = self.prompt_font.render(prompt, True, (255, 255, 255))
                prompt_rect = prompt_text.get_rect(center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - 30))
                self.SCREEN.blit(prompt_shadow, prompt_rect.move(2, 2))
                self.SCREEN.blit(prompt_text, prompt_rect)

                pg.display.flip()
                clock.tick(30)
            except Exception as e:
                print(f"Error running Leaderboard: {e}")