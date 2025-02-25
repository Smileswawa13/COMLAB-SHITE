import time as time
import pygame as pg
import sys
import math
import random
from PIL import Image, ImageFilter
from bgfix import stretch
from scores import load_score, write_score
import numpy as np
from genwords import generate_words_tutorial, generate_words_stage1, generate_words_stage2
import threading

"""UNIVERSAL FUNCTIONS---------------------------------------------------------------------------------------------------"""
def pause(screen, background):
    paused = True
    overlay = pg.Surface(screen.get_size(), pg.SRCALPHA)
    overlay.fill((50, 50, 50, 200))

    font = pg.font.Font("resources/DejaVuSans.ttf", 45)

    resume_text = "Press SpaceBar to continue playing"
    resume_text_surf = font.render(resume_text, True, pg.Color("white"))
    resume_text_shadow = font.render(resume_text, True, pg.Color("black"))
    resume_rect = resume_text_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    menu_text = "Press Esc to exit to menu"
    menu_text_surf = font.render(menu_text, True, pg.Color("white"))
    menu_text_shadow = font.render(menu_text, True, pg.Color("black"))
    menu_rect = menu_text_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))

    while paused:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    paused = False
                elif event.key == pg.K_ESCAPE:
                    from mapuantypingmania import game_Menu
                    game = game_Menu()
                    game.main_Menu()
                    return

        screen.blit(background, (0, 0))  # Draw the background
        screen.blit(overlay, (0, 0))  # Draw the overlay
        screen.blit(resume_text_shadow, resume_rect.move(2, 2))
        screen.blit(resume_text_surf, resume_rect)
        screen.blit(menu_text_shadow, menu_rect.move(2, 2))
        screen.blit(menu_text_surf, menu_rect)
        pg.display.flip()
        pg.time.Clock().tick(60)

def transform_color(color, changes, max_=255, min_=0, step=1):
    """ Return an RGB triplet which has changed slightly from the color taken as input """
    assert max_ < 256 and min_ >= 0 and max_ >= min_
    red, green, blue = color

    result = []
    for color in (red, green, blue):
        highest = min(color + changes, max_)
        lowest = max(color - changes, min_)

        if lowest >= highest:
            highest = lowest + 1

        result.append(random.randrange(lowest, highest))

    return tuple(result)


def apply_wave_effect(image, amplitude, frequency, phase, color_shift):
    arr = pg.surfarray.pixels3d(image)
    height, width, _ = arr.shape
    for x in range(width):
        offset = int(amplitude * np.sin(2 * np.pi * frequency * x + phase))
        arr[:, x] = np.roll(arr[:, x], offset, axis=0)
        arr[:, x] = np.clip(arr[:, x] + [color_shift, color_shift, color_shift], 0, 255)
    return pg.surfarray.make_surface(arr)

def handle_explosion_effect(screen, font, sprite_rect, completed_word, explosions):
    # Compute enemy text box dimensions similar to those in the draw method
    total_width = font.size(completed_word)[0]
    text_height = font.size(completed_word)[1]
    scaled_width = int(total_width * 1.5) + 20
    scaled_height = int(text_height * 1.5) + 10
    # Calculate the enemy text box rect at midright of the enemy sprite
    word_box_rect = pg.Rect(0, 0, scaled_width, scaled_height)
    word_box_rect.midright = (sprite_rect.left - 20, sprite_rect.centery)
    # Load and scale the explosion image
    explosion_image = pg.image.load(f'resources/transparent/boom-{random.randint(1, 3)}.gif').convert_alpha()
    scale_factor = 0.20  # Adjust explosion size as needed
    new_width = int(explosion_image.get_width() * scale_factor)
    new_height = int(explosion_image.get_height() * scale_factor)
    explosion_image = pg.transform.scale(explosion_image, (new_width, new_height))
    # Position explosion so its left edge touches the text box's right edge
    explosion_rect = explosion_image.get_rect(midleft=(word_box_rect.right, word_box_rect.centery))
    explosions.append((explosion_image, explosion_rect, pg.time.get_ticks()))

# for thread later
# def play_loading_music(music_file):
#     pg.mixer.music.load("resources/sounds/songs/)


"""UNIVERSAL FUNCTIONS---------------------------------------------------------------------------------------------------

LOADING SCREEN START -------------------------------------------------------------------------------------------------"""

class LoadingScreen:
    def __init__(self, screen):
        self.SCREEN = screen
        width, height = self.SCREEN.get_size()
        self.BG = stretch(pg.image.load("resources/backgrounds/menu.jpg"), (width, height)).convert_alpha()
        self.BG = pg.transform.scale(self.BG, (width, height))
        self.font = pg.font.Font(None, 22)
        self.text_prompt = self.font.render("LOADING NEXT...", True, (255, 255, 255))
        self.text_prompt_rect = self.text_prompt.get_rect(center=(width // 2, height // 2 + 150))
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

    def run(self):
        title_image = pg.image.load("resources/backgrounds/title.gif").convert_alpha()
        title_image = pg.transform.scale(title_image,
                                         (int(title_image.get_width() * 1.2), title_image.get_height()))
        title_rect = title_image.get_rect(center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2.5))
        clock = pg.time.Clock()
        start_time = pg.time.get_ticks()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            current_time = pg.time.get_ticks()
            if current_time - start_time > 1500:  # 1000 milliseconds = 1 seconds
                return

            animated_bg = self.animate_background()
            self.SCREEN.blit(animated_bg, (0, 0))
            self.SCREEN.blit(title_image, title_rect)
            self.SCREEN.blit(self.text_prompt, self.text_prompt_rect)
            pg.display.update()
            clock.tick(60)

"""LOADING SCREEN END ---------------------------------------------------------------------------------------------------

TUTORIAL START -------------------------------------------------------------------------------------------------------"""
class Tutorial:
    def __init__(self, screen):
        self.SCREEN = screen
        width, height = self.SCREEN.get_size()
        self.font = pg.font.Font("resources/DejaVuSans.ttf", 22)
        self.BG = stretch(pg.image.load("resources/backgrounds/bedrblur.jpg").convert_alpha(), (width, height))
        self.phase = 0

        pg.key.set_repeat(250, 30)

        self.clock = pg.time.Clock()
        self.words = generate_words_tutorial()
        self.current_words = {}
        self.word_timer = 0
        self.word_frequency = 2.5
        self.level = 1
        self.score = 0
        self.health = 10
        self.prompt_content = ''
        self.word_speed = 50
        self.word_widths = {}
        self.highscore = load_score()
        self.enemy = TutorialEnemy(screen, self.level)
        self.enemy.talking = True
        self.fade_alpha = 0
        self.fade_direction = 1
        self.damage_flash_alpha = 0

        # Load background music
        pg.mixer.init()
        self.prebattle_music = "resources/sounds/songs/prebattle.mp3"
        self.inbattle_music = "resources/sounds/songs/inbattle.mp3"

        # Load sound effects
        self.enemyhit_sfx = pg.mixer.Sound("resources/sounds/sfx/enemyhit.mp3")
        self.win_sfx = pg.mixer.Sound("resources/sounds/sfx/win.mp3")
        self.wordcomplete_sfx = pg.mixer.Sound("resources/sounds/sfx/wordcomplete.mp3")

        self.explosions = []

    def run(self):
        width, height = self.SCREEN.get_size()
        battle_started = False

        self.help_display()
        self.before_battle_display()
        battle_started = True

        pg.mixer.music.load(self.inbattle_music)
        pg.mixer.music.play(-1)

        while True:
            timepassed = self.clock.tick(60) / 1000.0

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        if battle_started:
                            pause(self.SCREEN, self.BG)
                        else:
                            return
                    if battle_started:
                        if event.unicode.isalpha():
                            self.prompt_content += event.unicode
                        elif event.key == pg.K_BACKSPACE:
                            self.prompt_content = self.prompt_content[:-1]
                        elif event.key == pg.K_RETURN:
                            self.prompt_content = ''

            self.SCREEN.blit(self.BG, (0, 0))

            if self.health <= 0:
                self.display_game_over()
                return

            if not battle_started:
                prompt_text = "Press Enter to start the battle"
                prompt_surf = self.font.render(prompt_text, True, pg.Color("white"))
                prompt_rect = prompt_surf.get_rect(center=(width // 2, height // 2))
                self.SCREEN.blit(prompt_surf, prompt_rect)
            else:
                if self.fade_alpha < 255:
                    self.apply_fade_effect()
                else:
                    self.word_timer += timepassed
                    if self.word_timer > self.word_frequency and len(self.current_words) < len(self.words):
                        self.add_word(width)
                        self.word_timer = 0

                    while len(self.current_words) < 3:
                        self.add_word(width)

                    for word, meta in list(self.current_words.items()):
                        meta[1] += timepassed
                        y = (meta[1] * self.word_speed) + abs(math.cos(meta[1] * 3) * 10)
                        word_rect = pg.Rect(meta[0], y, self.font.size(word)[0], self.font.size(word)[1])
                        if y > height:
                            del self.current_words[word]
                            self.health -= 1
                            self.damage_flash_alpha = 150
                        elif word == self.prompt_content:
                            del self.current_words[word]
                            self.score += len(word) * 2
                            self.prompt_content = ""
                            self.wordcomplete_sfx.play()
                            self.handle_explosion_effect(word_rect)
                            if word == self.enemy.current_word:
                                damage = len(word) * 0.2
                                self.enemy.hitpoints = max(0, self.enemy.hitpoints - damage)
                                self.enemy.is_hit = True
                                self.enemy.reset_word(self.current_words)
                                self.enemyhit_sfx.play()
                            else:
                                self.enemy.is_hit = False
                        else:
                            word_surf = self.create_word_surf(word, meta[2])
                            word_rect = word_surf.get_rect(center=(meta[0], y))
                            enemy_rect = self.enemy.sprite_rect
                            if word_rect.colliderect(enemy_rect):
                                if enemy_rect.left - word_rect.width - 10 >= 0:
                                    word_rect.right = enemy_rect.left - 10
                                else:
                                    word_rect.left = enemy_rect.right + 10
                            self.SCREEN.blit(word_surf, word_rect)

                    if self.current_words:
                        if self.enemy.update(timepassed, self.prompt_content, self.current_words):
                            self.health -= 1
                            self.damage_flash_alpha = 150

                    if self.enemy.hitpoints <= 0:
                        self.win_sfx.play()
                        pg.mixer.music.stop()
                        self.display_defeat()
                        return

                self.enemy.draw()
                self.SCREEN.blit(self.generate_prompt_surf(), (0, height - 50))
                self.draw_ui()
                self.draw_enemy_hitpoints()

                if self.damage_flash_alpha > 0:
                    flash_surf = pg.Surface(self.SCREEN.get_size(), pg.SRCALPHA)
                    flash_surf.fill((255, 0, 0, self.damage_flash_alpha))
                    self.SCREEN.blit(flash_surf, (0, 0))
                    self.damage_flash_alpha = max(0, self.damage_flash_alpha - 8)

                # Draw and manage explosions
                current_time = pg.time.get_ticks()
                self.explosions = [(img, rect, start_time) for img, rect, start_time in self.explosions if
                                   current_time - start_time < 500 ]
                for img, rect, start_time in self.explosions:
                    self.SCREEN.blit(img, rect)

                pg.display.flip()

    def handle_explosion_effect(self, word_rect):
        explosion_image = pg.image.load(f'resources/transparent/boom-{random.randint(1, 3)}.gif').convert_alpha()
        scale_factor = 0.20  # Adjust this factor to make the explosion image larger
        new_width = int(explosion_image.get_width() * scale_factor)
        new_height = int(explosion_image.get_height() * scale_factor)
        explosion_image = pg.transform.scale(explosion_image, (new_width, new_height))
        explosion_rect = explosion_image.get_rect(center=word_rect.center)
        self.explosions.append((explosion_image, explosion_rect, pg.time.get_ticks()))

    def help_display(self):
        # Play pre-battle music
        pg.mixer.music.load(self.prebattle_music)
        pg.mixer.music.play(-1)

        help_images = [stretch(pg.image.load(f"resources/help/help-{i}.png").convert_alpha(), self.SCREEN.get_size())
                       for i in range(1, 7)]
        current_image_index = 0

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return
                    elif event.key == pg.K_LEFT and current_image_index > 0:
                        current_image_index -= 1
                    elif event.key == pg.K_RIGHT and current_image_index < len(help_images) - 1:
                        current_image_index += 1
                    elif event.key == pg.K_RETURN and current_image_index == len(help_images) - 1:
                        self.before_battle_display()
                        return

            self.SCREEN.blit(self.BG, (0, 0))

            # Display the current help image
            help_image = help_images[current_image_index]
            self.SCREEN.blit(help_image, (0, 0))

            # Create a smaller font
            small_font = pg.font.Font("resources/DejaVuSans.ttf", 18)

            # Draw the left arrow prompt if not on the first image
            if current_image_index > 0:
                left_prompt_text = "Press Left Arrow to go back"
                left_prompt_surf = small_font.render(left_prompt_text, True, pg.Color("white"))
                left_prompt_shadow = small_font.render(left_prompt_text, True, pg.Color("black"))
                left_prompt_rect = left_prompt_surf.get_rect(
                    bottomright=(self.SCREEN.get_width() - 10, self.SCREEN.get_height() - 60))
                self.SCREEN.blit(left_prompt_shadow, left_prompt_rect.move(2, 2))
                self.SCREEN.blit(left_prompt_surf, left_prompt_rect)

            # Draw the right arrow prompt if not on the last image
            if current_image_index < len(help_images) - 1:
                right_prompt_text = "Press Right Arrow to continue"
                right_prompt_surf = small_font.render(right_prompt_text, True, pg.Color("white"))
                right_prompt_shadow = small_font.render(right_prompt_text, True, pg.Color("black"))
                right_prompt_rect = right_prompt_surf.get_rect(
                    bottomright=(self.SCREEN.get_width() - 10, self.SCREEN.get_height() - 40))
                self.SCREEN.blit(right_prompt_shadow, right_prompt_rect.move(2, 2))
                self.SCREEN.blit(right_prompt_surf, right_prompt_rect)

            # Draw the prompt to continue at the last image
            if current_image_index == len(help_images) - 1:
                continue_prompt_text = "Press Enter to go to the battle"
                continue_prompt_surf = small_font.render(continue_prompt_text, True, pg.Color("white"))
                continue_prompt_shadow = small_font.render(continue_prompt_text, True, pg.Color("black"))
                continue_prompt_rect = continue_prompt_surf.get_rect(
                    bottomright=(self.SCREEN.get_width() - 10, self.SCREEN.get_height() - 40))
                self.SCREEN.blit(continue_prompt_shadow, continue_prompt_rect.move(2, 2))
                self.SCREEN.blit(continue_prompt_surf, continue_prompt_rect)

            pg.display.flip()
            self.clock.tick(60)

    def before_battle_display(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        from mapuantypingmania import game_Menu
                        game = game_Menu()
                        game.main_Menu()
                        return
                    elif event.key == pg.K_RETURN:
                        return  # Exit the display and start the battle

            self.SCREEN.blit(self.BG, (0, 0))

            # Draw the enemy sprite talking
            talk_sprite = self.enemy.talk_sprite
            talk_sprite_rect = talk_sprite.get_rect(
                center=(self.SCREEN.get_width() - 250, self.SCREEN.get_height() // 2))
            self.SCREEN.blit(talk_sprite, talk_sprite_rect)

            # Draw the dialogue box using tutorial.gif
            dialogue_text = "\"Take it easy champ!\""
            small_font = pg.font.Font("resources/DejaVuSans.ttf", 25)
            dlg_surf = small_font.render(dialogue_text, True, pg.Color("black"))

            # Load and scale the tutorial.gif image for the dialogue box
            word_bg_image = pg.image.load("resources/transparent/tutorial.gif").convert_alpha()
            box_width = int(dlg_surf.get_width() * 1.5) + 20
            box_height = int(dlg_surf.get_height() * 1.5) + 20
            word_bg_image_scaled = pg.transform.scale(word_bg_image, (box_width, box_height))

            # Position the dialogue box with a negative x-coordinate to overlay over the sprite
            dlg_box_rect = word_bg_image_scaled.get_rect(
                midright=(talk_sprite_rect.left - 20, talk_sprite_rect.centery))
            dlg_box_rect.x += 140  # Adjust this value as needed to overlay the dialogue box

            # Blit the dialogue box and then the text centered in it
            self.SCREEN.blit(word_bg_image_scaled, dlg_box_rect)
            self.SCREEN.blit(dlg_surf, dlg_surf.get_rect(center=dlg_box_rect.center))

            # Draw the prompt to continue
            prompt_text = "Press Enter to go to the battle"
            prompt_surf = self.font.render(prompt_text, True, pg.Color("white"))
            prompt_surf_shadow = self.font.render(prompt_text, True, pg.Color("black"))
            prompt_rect = prompt_surf.get_rect(
                center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2 + 300))
            self.SCREEN.blit(prompt_surf_shadow, prompt_rect.move(2, 2))
            self.SCREEN.blit(prompt_surf, prompt_rect)

            pg.display.flip()
            self.clock.tick(60)

    def display_defeat(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    self.display_victory()
            # Redraw the background and enemy defeat screen
            self.SCREEN.blit(self.BG, (0, 0))
            self.enemy.draw()
            # Draw the defeat text box at the left side of the enemy
            text = "\"Nice one man!...press any key to go victory screen\""
            small_font = pg.font.Font("resources/DejaVuSans.ttf", 15)
            dlg_surf = small_font.render(text, True, pg.Color("black"))
            # Reduce extra padding from 20 to 10 pixels total (5 on each side)
            dlg_box = pg.Surface((dlg_surf.get_width() + 10, dlg_surf.get_height() + 10), pg.SRCALPHA)
            dlg_box.fill((49, 143, 47, 230))
            # Set the box to start at enemy's left side with a 5-pixel gap and vertically centered
            dlg_box_rect = dlg_box.get_rect(midright=(self.enemy.sprite_rect.left - 5, self.enemy.sprite_rect.centery))
            self.SCREEN.blit(dlg_box, dlg_box_rect)
            # Center the text within the dialog box
            self.SCREEN.blit(dlg_surf, dlg_surf.get_rect(center=dlg_box_rect.center))
            pg.display.flip()
            self.clock.tick(60)

    def display_victory(self):
        if self.score > self.highscore:
            self.highscore = self.score
            write_score(self.highscore)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        from mapuantypingmania import game_Menu
                        game = game_Menu()
                        game.play()
                    else:
                        from introduction import Intro
                        LoadingScreen(self.SCREEN).run()
                        Intro(self.SCREEN).run()

            # Prepare text surfaces and their positions
            center = (self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2)
            victory_surf = self.font.render("VICTORY!", True, pg.Color("white"))
            highscore_text = f"Highscore: {self.highscore}"
            highscore_surf = self.font.render(highscore_text, True, pg.Color("white"))
            prompt_text = "Press any key for next stage, or Esc for main menu"
            prompt_surf = self.font.render(prompt_text, True, pg.Color("white"))

            victory_rect = victory_surf.get_rect(center=(center[0], center[1] - 40))
            hs_rect = highscore_surf.get_rect(center=center)
            prompt_rect = prompt_surf.get_rect(center=(center[0], center[1] + 40))

            # Calculate the bounding rectangle of all text surfaces and add padding
            union_rect = victory_rect.union(hs_rect).union(prompt_rect)
            padding = 10
            dlg_rect = pg.Rect(
                union_rect.left - padding,
                union_rect.top - padding,
                union_rect.width + 2 * padding,
                union_rect.height + 2 * padding
            )

            # Create the dialog box surface with an opaque yellow red color
            dlg_box = pg.Surface((dlg_rect.width, dlg_rect.height))
            dlg_box.fill((255, 193, 33))

            # Draw background and dialog box
            self.SCREEN.blit(self.BG, (0, 0))
            self.SCREEN.blit(dlg_box, dlg_rect.topleft)
            # Draw border if desired (optional)
            pg.draw.rect(self.SCREEN, (255, 0, 0), dlg_rect, 3)

            # Blit each text surface centered at their respective positions
            self.SCREEN.blit(victory_surf, victory_rect)
            self.SCREEN.blit(highscore_surf, hs_rect)
            self.SCREEN.blit(prompt_surf, prompt_rect)

            pg.display.flip()
            self.clock.tick(60)

    def draw_enemy_hitpoints(self):
        hp_text = f"Enemy HP: {self.enemy.hitpoints:.1f}"
        hp_surf = self.font.render(hp_text, True, (255, 255, 255))
        hp_box = pg.Surface((hp_surf.get_width() + 10, hp_surf.get_height() + 10), pg.SRCALPHA)
        hp_box.fill((27, 219, 24, 190))

        # Initialize and update fade alpha for enemy hitpoints
        if not hasattr(self, 'hp_alpha'):
            self.hp_alpha = 0
        if self.hp_alpha < 255:
            self.hp_alpha += 5  # Adjust increment as needed for smoother or faster fade
        hp_box.set_alpha(self.hp_alpha)

        hp_box_rect = hp_box.get_rect(midtop=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - 100))

        self.SCREEN.blit(hp_box, hp_box_rect)
        self.SCREEN.blit(hp_surf, hp_surf.get_rect(center=hp_box_rect.center))

        # Draw a bar line to separate the hitpoints and prompt surface
        pg.draw.line(self.SCREEN, (255, 255, 255),
                     (0, self.SCREEN.get_height() - 50),
                     (self.SCREEN.get_width(), self.SCREEN.get_height() - 50), 2)

    def apply_fade_effect(self):
        if self.fade_direction != 0:
            self.fade_alpha += self.fade_direction * 10
            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.fade_direction = 0
            elif self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.fade_direction = 0
        fade_surf = pg.Surface(self.SCREEN.get_size(), pg.SRCALPHA)
        fade_surf.fill((255, 0, 0, self.fade_alpha))
        self.SCREEN.blit(fade_surf, (0, 0))

    def add_word(self, width):
        found_word = False
        while not found_word and len(self.current_words) < len(self.words):
            selected = random.choice(self.words)
            if all(not w.startswith(selected[0]) for w in self.current_words):
                if selected not in self.word_widths:
                    self.word_widths[selected] = self.font.size(selected)[0]
                w_width = self.word_widths[selected]
                x = random.randrange(45, width - w_width - 10)  # Ensure the word does not overlap the screen edges
                # Ensure the word does not overlap with the enemy sprite and other tutorial_words
                if not (self.enemy.sprite_rect.left < x < self.enemy.sprite_rect.right) and \
                        all(abs(x - meta[0]) > w_width + 15 for meta in self.current_words.values()):
                    self.current_words[selected] = [x, 0, (150, 150, 150)]
                    found_word = True

    def create_word_surf(self, word, color):
        w, h = self.font.size(word)
        w += 12  # Increase width for padding
        h += 12  # Increase height for padding
        Surf = pg.Surface((w, h), pg.SRCALPHA, 32)

        # Create a rounded rectangle background with a constant color
        bg_color = (77, 120, 77, 200)  # Constant background color with some opacity
        pg.draw.rect(Surf, bg_color, Surf.get_rect(), border_radius=10)

        being_written = self.prompt_content and word.startswith(self.prompt_content)
        start_text = self.prompt_content if being_written else ''
        end_text = word[len(self.prompt_content):] if being_written else word
        start_surf = self.font.render(start_text, True, pg.Color("black"))

        # Apply transform_color to the end_text color for more vibrancy
        transformed_color = transform_color(color, 100)
        end_surf = self.font.render(end_text, True, transformed_color)

        Surf.blit(start_surf, (8, 8))
        Surf.blit(end_surf, end_surf.get_rect(right=w - 8, centery=h // 2))
        return Surf

    def generate_prompt_surf(self):
        width = self.SCREEN.get_width()
        surf = pg.Surface((width, 50), pg.SRCALPHA)
        surf.fill((25, 24, 77))

        if not hasattr(self, 'prompt_alpha'):
            self.prompt_alpha = 0
        if self.prompt_alpha < 255:
            self.prompt_alpha += 1
        surf.set_alpha(self.prompt_alpha)

        color = pg.Color(255, 253, 11) if any(w.startswith(self.prompt_content) for w in self.current_words) \
            else pg.Color(214, 24, 24)
        rendered = self.font.render(self.prompt_content, True, color)

        # Create shadow text
        shadow_color = pg.Color(180, 200, 255)
        shadow_rendered = self.font.render(self.prompt_content, True, shadow_color)

        # Center the prompt text horizontally on the surface
        rect = rendered.get_rect(centerx=width // 2, centery=25)
        shadow_rect = shadow_rendered.get_rect(centerx=width // 2 + 2, centery=26)  # Slightly offset for shadow effect

        # Blit shadow first, then main text
        surf.blit(shadow_rendered, shadow_rect)
        surf.blit(rendered, rect)

        return surf

    def draw_ui(self):
        top_box = pg.Surface((self.SCREEN.get_width(), 40), pg.SRCALPHA)
        top_box.fill((194, 31, 31))
        top_box_rect = top_box.get_rect()
        if not hasattr(self, 'ui_alpha'):
            self.ui_alpha = 0

        if self.ui_alpha < 255:
            self.ui_alpha += 1  # Adjust the increment value as needed

        top_box.set_alpha(self.ui_alpha)
        self.SCREEN.blit(top_box, top_box_rect)

        score_surf = self.font.render(f"Score: {self.score}",
                                      True, (255, 255, 255))
        health_surf = self.font.render(f"Health: {self.health}",
                                       True, (255, 255, 255))
        enemy_name = self.font.render(f"Enemy: Tutorial Guy",
                                      True, (255, 255, 255))

        # Calculate positions for the text
        screen_width = self.SCREEN.get_width()
        score_pos = (10, 10)
        health_pos = (screen_width // 3, 10)
        enemy_pos = (2 * screen_width // 3, 10)

        self.SCREEN.blit(score_surf, score_pos)
        self.SCREEN.blit(health_surf, health_pos)
        self.SCREEN.blit(enemy_name, enemy_pos)

        pg.draw.line(self.SCREEN, (255, 255, 255),
                     (screen_width // 3 - 5, 0),
                     (screen_width // 3 - 5, 40), 2)
        pg.draw.line(self.SCREEN, (255, 255, 255),
                     (2 * screen_width // 3 - 5, 0),
                     (2 * screen_width // 3 - 5, 40), 2)

    def display_game_over(self):
        write_score(self.score)
        game_over = self.font.render("GAME OVER", True, (255, 0, 0))
        center = (self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2)
        self.SCREEN.blit(game_over, game_over.get_rect(center=center))
        pg.display.flip()
        pg.time.wait(2000)

class TutorialEnemy:
    def __init__(self, screen, level):
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        self.font = pg.font.Font("resources/DejaVuSans.ttf", 36)
        self.hitpoints = 10 + level * 5
        self.word_speed = 2
        self.current_word = ""
        self.word_progress = 0
        self.start_timer = 2.5
        self.is_hit = False
        self.sprite_alpha = 0

        self.normal_sprite = pg.image.load("resources/sprites/neil-fight.png").convert_alpha()
        self.hit_sprite = pg.image.load("resources/sprites/neil-hit-color.gif").convert_alpha()
        self.talk_sprite = pg.image.load("resources/sprites/neil-talk.png").convert_alpha()
        self.defeat_sprite = pg.image.load("resources/sprites/neil-defeat.png").convert_alpha()
        self.normal_sprite = pg.transform.scale(self.normal_sprite, (450, 650))
        self.hit_sprite = pg.transform.scale(self.hit_sprite, (450, 650))
        self.talk_sprite = pg.transform.scale(self.talk_sprite, (450, 650))
        self.defeat_sprite = pg.transform.scale(self.defeat_sprite, (450, 650))
        self.sprite_rect = self.normal_sprite.get_rect()
        self.sprite_rect.centerx = self.width - 250
        self.sprite_rect.centery = self.height // 2
        self.word_bg_image = pg.image.load("resources/transparent/tutorial.gif").convert_alpha()
        self.explosions = []

    def reset_word(self, current_words):
        if self.current_word in current_words:
            del current_words[self.current_word]
        self.current_word = ""
        self.word_progress = 0
        self.start_timer = 2.5

    def update(self, timepassed, player_input, current_words):
        if self.sprite_alpha < 255:
            self.sprite_alpha += 5

        if self.hitpoints <= 0:
            return False

        if not self.current_word and current_words:
            self.current_word = random.choice(list(current_words.keys()))
            self.word_progress = 0

        if self.current_word and (self.current_word not in current_words):
            self.current_word = ""
            self.word_progress = 0
            self.start_timer = 2.5

        if self.start_timer > 0:
            self.start_timer -= timepassed
            return False

        if self.current_word:
            self.word_progress += timepassed * self.word_speed
            meta = current_words[self.current_word]
            # Use the updated meta data for y-position
            word_x = meta[0]
            meta_y = meta[1]
            y = (meta_y * self.word_speed) + abs(math.cos(meta_y * 3) * 10)
            word_rect = pg.Rect(word_x, y, self.font.size(self.current_word)[0],
                                self.font.size(self.current_word)[1])
            if self.word_progress >= len(self.current_word):
                # Store the completed word before resetting
                completed_word = self.current_word
                handle_explosion_effect(self.screen, self.font, self.sprite_rect, completed_word, self.explosions)
                if self.current_word in current_words:
                    current_words.pop(self.current_word)
                self.current_word = ""
                self.word_progress = 0
                self.start_timer = 2.0
                return True

        return False

    def draw(self):
        if self.hitpoints <= 0:
            current_sprite = self.defeat_sprite
        else:
            current_sprite = self.hit_sprite if self.is_hit else self.normal_sprite

        sprite_with_alpha = current_sprite.copy()
        sprite_with_alpha.set_alpha(self.sprite_alpha)
        self.screen.blit(sprite_with_alpha, self.sprite_rect)

        if self.hitpoints > 0 and self.current_word:
            # Render the typed and remaining portions of the word
            typed = self.current_word[:int(self.word_progress)]
            remaining = self.current_word[int(self.word_progress):]
            typed_surf = self.font.render(typed, True, (255, 0, 0))
            remaining_surf = self.font.render(remaining, True, (100, 100, 100))

            total_width = typed_surf.get_width() + remaining_surf.get_width()
            text_height = typed_surf.get_height()

            # Define the text box size based on the text dimensions with extra margin
            box_width = int(total_width * 1.5) + 20
            box_height = int(text_height * 1.5) + 10

            # Scale the background image for the word box
            word_bg_image_scaled = pg.transform.scale(self.word_bg_image, (box_width, box_height))

            # Position the text box with a negative x-coordinate to overlay over the sprite
            word_box_rect = word_bg_image_scaled.get_rect(
                midright=(self.sprite_rect.left - 20, self.sprite_rect.centery))
            word_box_rect.x += 100  # Adjust this value as needed to overlay the text box

            # Calculate centered text position within the text box
            text_x = word_box_rect.left + (box_width - total_width) // 2
            text_y = word_box_rect.top + (box_height - text_height) // 2

            # Blit the text box and then the text centered in it
            self.screen.blit(word_bg_image_scaled, word_box_rect)
            self.screen.blit(typed_surf, (text_x, text_y))
            self.screen.blit(remaining_surf, (text_x + typed_surf.get_width(), text_y))

        # Draw any active explosions
        current_time = pg.time.get_ticks()
        self.explosions = [(img, rect, start_time) for img, rect, start_time in self.explosions
                           if current_time - start_time < 500]
        for img, rect, _ in self.explosions:
            self.screen.blit(img, rect)
"""TUTORIAL END ---------------------------------------------------------------------------------------------------------

STAGE 1 START --------------------------------------------------------------------------------------------------------"""
class Stage1:
    def __init__(self, screen, level):
        self.SCREEN = screen
        width, height = self.SCREEN.get_size()
        self.font = pg.font.Font("resources/DejaVuSans.ttf", 22)
        self.BG = stretch(pg.image.load("resources/backgrounds/roomblur.jpg").convert_alpha(), (width, height))
        self.phase = 0

        pg.key.set_repeat(250, 30)

        self.clock = pg.time.Clock()
        self.stage1_words, self.bonus_words, self.bossfight_words = generate_words_stage1()
        self.current_words = {}
        self.word_timer = 0
        self.word_frequency = 2.5
        self.level = level
        self.score = 0
        self.health = 20
        self.prompt_content = ''
        self.word_speed = 50
        self.word_widths = {}
        self.highscore = load_score()
        self.enemies = [Minion1(screen, self.level), Minion2(screen, self.level), Minion3(screen, self.level),
                        Boss(screen, self.level)]
        self.current_enemy_index = 0
        self.enemy = self.enemies[self.current_enemy_index]
        self.enemy.talking = True
        self.fade_alpha = 0
        self.fade_direction = 1
        self.damage_flash_alpha = 0
        self.bonus_word_counter = 0

        # Load background music
        pg.mixer.init()
        self.prebattle_music = "resources/sounds/songs/prebattle.mp3"
        self.inbattle_music = "resources/sounds/songs/inbattle.mp3"

        # Load sound effects
        self.enemyhit_sfx = pg.mixer.Sound("resources/sounds/sfx/enemyhit.mp3")
        self.win_sfx = pg.mixer.Sound("resources/sounds/sfx/win.mp3")
        self.wordcomplete_sfx = pg.mixer.Sound("resources/sounds/sfx/wordcomplete.mp3")

        self.explosions = []
        self.bossfight_pause_timer = 0
        self.falling_words_pause_timer = 0
        self.last_bonus_action = 'damage'

    def run(self):
        width, height = self.SCREEN.get_size()
        battle_started = False
        hue = 0

        while self.current_enemy_index < len(self.enemies):
            self.enemy = self.enemies[self.current_enemy_index]
            self.before_battle_display(self.enemy)
            battle_started = True

            pg.mixer.music.load(self.inbattle_music)
            pg.mixer.music.play(-1)

            while True:
                timepassed = self.clock.tick(60) / 1000.0

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            if battle_started:
                                pause(self.SCREEN, self.BG)
                            else:
                                return
                        if battle_started:
                            if event.unicode.isprintable():
                                self.prompt_content += event.unicode
                            elif event.key == pg.K_BACKSPACE:
                                self.prompt_content = self.prompt_content[:-1]
                            elif event.key == pg.K_RETURN:
                                self.prompt_content = ''

                self.SCREEN.blit(self.BG, (0, 0))

                if self.health <= 0:
                    self.display_game_over()
                    return

                if not battle_started:
                    prompt_text = "Press Enter to start the battle"
                    prompt_surf = self.font.render(prompt_text, True, pg.Color("white"))
                    prompt_rect = prompt_surf.get_rect(center=(width // 2, height // 2))
                    self.SCREEN.blit(prompt_surf, prompt_rect)
                else:
                    if self.fade_alpha < 255:
                        self.apply_fade_effect()
                    else:
                        # if self.words_started_falling:
                        self.word_timer += timepassed
                        if self.word_timer > self.word_frequency and len(self.current_words) < len(
                                self.stage1_words):
                            self.add_word(width, self.stage1_words, 'stage1', self.enemy)
                            self.word_timer = 0

                        while len(self.current_words) < 3:
                            self.add_word(width, self.stage1_words, 'stage1', self.enemy)

                        for word, meta in list(self.current_words.items()):
                            meta[1] += timepassed
                            y = (meta[1] * self.word_speed) + abs(math.cos(meta[1] * 3) * 10)
                            word_rect = pg.Rect(meta[0], y, self.font.size(word)[0], self.font.size(word)[1])
                            if y > height:
                                del self.current_words[word]
                                self.health -= 1
                                self.damage_flash_alpha = 150
                            elif word == self.prompt_content:
                                del self.current_words[word]
                                self.score += len(word) * 2
                                self.prompt_content = ""
                                self.wordcomplete_sfx.play()
                                self.handle_explosion_effect(word_rect)
                                if word == self.enemy.current_word:
                                    self.apply_damage(1, word)
                                    self.handle_explosion_effect(word_rect)
                                elif word in self.bonus_words:
                                    if self.last_bonus_action == 'damage':
                                        self.apply_damage(3, word)
                                        self.last_bonus_action = 'health'
                                        self.handle_explosion_effect(word_rect)
                                    else:
                                        self.health = min(self.health + 1.5, 50)
                                        self.last_bonus_action = 'damage'
                                        self.enemy.reset_word(self.current_words)
                                        self.enemy.is_hit = True
                                        self.enemyhit_sfx.play()
                                        self.handle_explosion_effect(word_rect)
                                elif word in self.bossfight_words:
                                    self.apply_damage(5, word)
                                    self.handle_explosion_effect(word_rect)
                                    self.bossfight_pause_timer = 3.0
                                    self.falling_words_pause_timer = 1.0
                                    self.handle_explosion_effect(word_rect)
                                else:
                                    self.enemy.is_hit = False

                            else:
                                word_surf = self.create_word_surf(word, meta[2], hue, meta[3])
                                word_rect = word_surf.get_rect(center=(meta[0], y))
                                enemy_rect = self.enemy.sprite_rect
                                if word_rect.colliderect(enemy_rect):
                                    if enemy_rect.left - word_rect.width - 10 >= 0:
                                        word_rect.right = enemy_rect.left - 10
                                    else:
                                        word_rect.left = enemy_rect.right + 10
                                self.SCREEN.blit(word_surf, word_rect)

                        if self.current_words:
                            if self.enemy.update(timepassed, self.prompt_content, self.current_words):
                                if isinstance(self.enemy, Boss):
                                    self.health -= 2 * self.level  # Boss deals twice the damage
                                else:
                                    self.health -= self.level  # Minions deal damage based on the level
                                self.damage_flash_alpha = 150

                        if self.enemy.hitpoints <= 0:
                            self.win_sfx.play()
                            pg.mixer.music.stop()
                            self.defeat_display(self.enemy)
                            self.current_enemy_index += 1
                            break

                    self.enemy.draw()
                    self.SCREEN.blit(self.generate_prompt_surf(), (0, height - 50))
                    self.draw_ui()
                    self.draw_enemy_hitpoints()

                    if self.damage_flash_alpha > 0:
                        flash_surf = pg.Surface(self.SCREEN.get_size(), pg.SRCALPHA)
                        flash_surf.fill((255, 0, 0, self.damage_flash_alpha))
                        self.SCREEN.blit(flash_surf, (0, 0))
                        self.damage_flash_alpha = max(0, self.damage_flash_alpha - 8)

                    # Draw and manage explosions
                    current_time = pg.time.get_ticks()
                    self.explosions = [(img, rect, start_time) for img, rect, start_time in self.explosions if
                                       current_time - start_time < 500]
                    for img, rect, _ in self.explosions:
                        self.SCREEN.blit(img, rect)

                    pg.display.flip()
                    hue = (hue + 1) % 360  # Update hue for the next frame

        self.display_victory()
        from introduction import Stage1Outro
        outro = Stage1Outro(self.SCREEN)
        outro.run()

    def apply_damage(self, damage, word, reset_word=True, play_sound=True):
        self.enemy.hitpoints = max(0, self.enemy.hitpoints - ((damage * len(word)) * 0.25))
        self.enemy.is_hit = True
        if reset_word:
            self.enemy.reset_word(self.current_words)
        if play_sound:
            self.enemyhit_sfx.play()

    def handle_explosion_effect(self, word_rect):
        explosion_image = pg.image.load(f'resources/transparent/boom-{random.randint(1, 3)}.gif').convert_alpha()
        scale_factor = 0.20  # Adjust this factor to make the explosion image larger
        new_width = int(explosion_image.get_width() * scale_factor)
        new_height = int(explosion_image.get_height() * scale_factor)
        explosion_image = pg.transform.scale(explosion_image, (new_width, new_height))
        explosion_rect = explosion_image.get_rect(center=word_rect.center)
        self.explosions.append((explosion_image, explosion_rect, pg.time.get_ticks()))

    def before_battle_display(self, minion):
        fade_duration = 1.0  # Duration of the fade-in effect in seconds
        fade_alpha = 0  # Initial alpha value for fade-in effect
        fade_increment = 255 / (fade_duration * 60)  # Increment per frame (assuming 60 FPS)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        from mapuantypingmania import game_Menu
                        game = game_Menu()
                        game.main_Menu()
                        return
                    elif event.key == pg.K_RETURN:
                        return  # Exit the display and start the battle

            self.SCREEN.blit(self.BG, (0, 0))

            # Draw the minion sprite talking with fade-in effect
            talk_sprite = minion.talk_sprite.copy()
            talk_sprite.set_alpha(fade_alpha)
            talk_sprite_rect = talk_sprite.get_rect(
                center=(self.SCREEN.get_width() - 250, self.SCREEN.get_height() // 2))
            self.SCREEN.blit(talk_sprite, talk_sprite_rect)

            # Draw the dialogue box using tutorial.gif with fade-in effect
            small_font = pg.font.Font("resources/DejaVuSans.ttf", 20)
            dlg_surf = small_font.render(minion.dialogue_text, True, pg.Color(251, 255, 52))
            dlg_surf.set_alpha(fade_alpha)

            # Load and scale the tutorial.gif image for the dialogue box
            word_bg_image = pg.image.load("resources/transparent/tristan.gif").convert_alpha()
            box_width = int(dlg_surf.get_width() * 1.5) + 5
            box_height = int(dlg_surf.get_height() * 1.5) + 30
            word_bg_image_scaled = pg.transform.scale(word_bg_image, (box_width, box_height))
            word_bg_image_scaled.set_alpha(fade_alpha)

            # Position the dialogue box with a negative x-coordinate to overlay over the sprite
            dlg_box_rect = word_bg_image_scaled.get_rect(
                midright=(talk_sprite_rect.left - 20, talk_sprite_rect.centery))
            dlg_box_rect.x += 140  # Adjust this value as needed to overlay the dialogue box

            # Blit the dialogue box and then the text centered in it
            self.SCREEN.blit(word_bg_image_scaled, dlg_box_rect)
            self.SCREEN.blit(dlg_surf, dlg_surf.get_rect(center=dlg_box_rect.center))

            # Draw the bottom bar with fade-in effect
            bottom_bar_height = 100
            bottom_bar = pg.Surface((self.SCREEN.get_width(), bottom_bar_height), pg.SRCALPHA)
            bottom_bar.fill((25, 24, 77, fade_alpha))
            self.SCREEN.blit(bottom_bar, (0, self.SCREEN.get_height() - bottom_bar_height))

            # Draw the prompt to continue with fade-in effect
            prompt_text = "Press Enter to start the battle"
            prompt_surf = self.font.render(prompt_text, True, pg.Color("white"))
            prompt_surf_shadow = self.font.render(prompt_text, True, pg.Color("black"))
            prompt_surf.set_alpha(fade_alpha)
            prompt_surf_shadow.set_alpha(fade_alpha)
            prompt_rect = prompt_surf.get_rect(
                center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - bottom_bar_height // 2))
            self.SCREEN.blit(prompt_surf_shadow, prompt_rect.move(2, 2))
            self.SCREEN.blit(prompt_surf, prompt_rect)

            # Apply fade-in effect
            if fade_alpha < 255:
                fade_alpha = min(255, fade_alpha + fade_increment)

            pg.display.flip()
            self.clock.tick(60)

    def display_victory(self):
        if self.score > self.highscore:
            self.highscore = self.score
            write_score(self.highscore)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        from mapuantypingmania import game_Menu
                        game = game_Menu()
                        game.play()
                    else:
                        from introduction import Intro
                        LoadingScreen(self.SCREEN).run()
                        Intro(self.SCREEN).run()

            # Prepare text surfaces and their positions
            center = (self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2)
            victory_surf = self.font.render("VICTORY!", True, pg.Color("white"))
            highscore_text = f"Highscore: {self.highscore}"
            highscore_surf = self.font.render(highscore_text, True, pg.Color("white"))
            prompt_text = "Press any key for next stage, or Esc for main menu"
            prompt_surf = self.font.render(prompt_text, True, pg.Color("white"))

            victory_rect = victory_surf.get_rect(center=(center[0], center[1] - 40))
            hs_rect = highscore_surf.get_rect(center=center)
            prompt_rect = prompt_surf.get_rect(center=(center[0], center[1] + 40))

            # Calculate the bounding rectangle of all text surfaces and add padding
            union_rect = victory_rect.union(hs_rect).union(prompt_rect)
            padding = 10
            dlg_rect = pg.Rect(
                union_rect.left - padding,
                union_rect.top - padding,
                union_rect.width + 2 * padding,
                union_rect.height + 2 * padding
            )

            # Create the dialog box surface with an opaque yellow red color
            dlg_box = pg.Surface((dlg_rect.width, dlg_rect.height))
            dlg_box.fill((255, 193, 33))

            # Draw background and dialog box
            self.SCREEN.blit(self.BG, (0, 0))
            self.SCREEN.blit(dlg_box, dlg_rect.topleft)
            # Draw border if desired (optional)
            pg.draw.rect(self.SCREEN, (255, 0, 0), dlg_rect, 3)

            # Blit each text surface centered at their respective positions
            self.SCREEN.blit(victory_surf, victory_rect)
            self.SCREEN.blit(highscore_surf, hs_rect)
            self.SCREEN.blit(prompt_surf, prompt_rect)

            pg.display.flip()
            self.clock.tick(60)

    def draw_enemy_hitpoints(self):
        hp_text = f"Enemy HP: {self.enemy.hitpoints:.1f}"
        hp_surf = self.font.render(hp_text, True, (255, 255, 255))
        hp_box = pg.Surface((hp_surf.get_width() + 10, hp_surf.get_height() + 10), pg.SRCALPHA)
        hp_box.fill((27, 219, 24, 190))

        # Initialize and update fade alpha for enemy hitpoints
        if not hasattr(self, 'hp_alpha'):
            self.hp_alpha = 0
        if self.hp_alpha < 255:
            self.hp_alpha += 5  # Adjust increment as needed for smoother or faster fade
        hp_box.set_alpha(self.hp_alpha)

        hp_box_rect = hp_box.get_rect(midtop=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - 100))

        self.SCREEN.blit(hp_box, hp_box_rect)
        self.SCREEN.blit(hp_surf, hp_surf.get_rect(center=hp_box_rect.center))

        # Draw a bar line to separate the hitpoints and prompt surface
        pg.draw.line(self.SCREEN, (255, 255, 255),
                     (0, self.SCREEN.get_height() - 50),
                     (self.SCREEN.get_width(), self.SCREEN.get_height() - 50), 2)

    def defeat_display(self, minion):
        fade_duration = 1.0
        fade_alpha = 0
        fade_increment = 255 / (fade_duration * 60)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        from mapuantypingmania import game_Menu
                        game = game_Menu()
                        game.main_Menu()
                        return
                    elif event.key == pg.K_RETURN:
                        return

            self.SCREEN.blit(self.BG, (0, 0))

            defeat_sprite = minion.defeat_sprite.copy()
            defeat_sprite.set_alpha(fade_alpha)
            defeat_sprite_rect = defeat_sprite.get_rect(
                center=(self.SCREEN.get_width() - 250, self.SCREEN.get_height() // 2))
            self.SCREEN.blit(defeat_sprite, defeat_sprite_rect)

            small_font = pg.font.Font("resources/DejaVuSans.ttf", 20)
            dlg_surf = small_font.render(minion.defeat_text, True, pg.Color(251, 255, 52))
            dlg_surf.set_alpha(fade_alpha)

            word_bg_image = pg.image.load("resources/transparent/tristan.gif").convert_alpha()
            box_width = int(dlg_surf.get_width() * 1.5) + 5
            box_height = int(dlg_surf.get_height() * 1.5) + 30
            word_bg_image_scaled = pg.transform.scale(word_bg_image, (box_width, box_height))
            word_bg_image_scaled.set_alpha(fade_alpha)

            dlg_box_rect = word_bg_image_scaled.get_rect(
                midright=(defeat_sprite_rect.left - 20, defeat_sprite_rect.centery))
            dlg_box_rect.x += 140

            self.SCREEN.blit(word_bg_image_scaled, dlg_box_rect)
            self.SCREEN.blit(dlg_surf, dlg_surf.get_rect(center=dlg_box_rect.center))

            bottom_bar_height = 100
            bottom_bar = pg.Surface((self.SCREEN.get_width(), bottom_bar_height), pg.SRCALPHA)
            bottom_bar.fill((25, 24, 77, fade_alpha))
            self.SCREEN.blit(bottom_bar, (0, self.SCREEN.get_height() - bottom_bar_height))

            prompt_text = "Press Enter to continue"
            prompt_surf = self.font.render(prompt_text, True, pg.Color("white"))
            prompt_surf_shadow = self.font.render(prompt_text, True, pg.Color("black"))
            prompt_surf.set_alpha(fade_alpha)
            prompt_surf_shadow.set_alpha(fade_alpha)
            prompt_rect = prompt_surf.get_rect(
                center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - bottom_bar_height // 2))
            self.SCREEN.blit(prompt_surf_shadow, prompt_rect.move(2, 2))
            self.SCREEN.blit(prompt_surf, prompt_rect)

            if fade_alpha < 255:
                fade_alpha = min(255, fade_alpha + fade_increment)

            pg.display.flip()
            self.clock.tick(60)

    def rainbow(self, hue):
        color = pg.Color("white")
        hue = (hue + 1) % 360
        color.hsva = (hue, 100, 100, 100)
        return color

    def add_word(self, width, words, word_type, enemy):
        found_word = False
        while not found_word and len(self.current_words) < len(words):
            if self.bonus_word_counter >= 4 and word_type != 'bossfight':
                selected = random.choice(self.bossfight_words)
                self.bonus_word_counter = 0 # Reset the counter after adding a bossfight word
            elif word_type == 'bonus' or (self.bonus_word_counter >= 6 and word_type != 'bossfight'):
                selected = random.choice(self.bonus_words)
                self.bonus_word_counter = 0  # Reset the counter after adding a bonus word
            elif word_type == 'bossfight' and isinstance(enemy,
                                                         Boss):  # Ensure bossfight words only appear during boss fights
                selected = random.choice(self.bossfight_words)
            else:
                # Adjust the selection logic to balance word lengths on screen
                word_lengths = [len(word) for word in words]
                current_lengths = [len(word) for word in self.current_words.keys()]

                # Count the occurrences of each word length currently on screen
                length_counts = {length: current_lengths.count(length) for length in set(word_lengths)}

                # Calculate weights to balance the word lengths
                weights = []
                for length in word_lengths:
                    if length_counts.get(length, 0) < 2:  # Adjust this threshold as needed
                        weights.append(1)
                    else:
                        weights.append(0.1)

                selected = random.choices(words, weights=weights, k=1)[0]
                self.bonus_word_counter += 1  # Increment the counter for normal words

            if all(not w.startswith(selected[0]) for w in self.current_words):
                if selected not in self.word_widths:
                    self.word_widths[selected] = self.font.size(selected)[0]
                w_width = self.word_widths[selected]
                x = random.randrange(45, width - w_width - 10)  # Ensure the word does not overlap the screen edges
                # Ensure the word does not overlap with the enemy sprite and other words
                if not (enemy.sprite_rect.left < x < enemy.sprite_rect.right) and \
                        all(abs(x - meta[0]) > w_width + 15 for meta in self.current_words.values()):
                    self.current_words[selected] = [x, 0, (150, 150, 150), word_type]
                    found_word = True

                    # Adjust word frequency based on word type
                    if word_type == 'bonus':
                        self.word_frequency = max(1.0, self.word_frequency - 0.1)
                    elif word_type == 'bossfight':
                        self.word_frequency = max(0.5, self.word_frequency - 0.2)
                    else:
                        self.word_frequency = min(3.0, self.word_frequency + 0.1)

    def create_word_surf(self, word, color, hue, word_type):
        w, h = self.font.size(word)
        w += 12  # Increase width for padding
        h += 12  # Increase height for padding
        Surf = pg.Surface((w, h), pg.SRCALPHA, 32)

        pg.draw.rect(Surf, (222, 153, 0, 200), Surf.get_rect(), border_radius=10)

        being_written = self.prompt_content and word.startswith(self.prompt_content)
        start_text = self.prompt_content if being_written else ''
        end_text = word[len(self.prompt_content):] if being_written else word
        start_surf = self.font.render(start_text, True, pg.Color("black"))

        # Set constant colors for bonus and bossfight word types
        if word in self.bonus_words:
            transformed_color = pg.Color("gold")
            # print("bonus")
        elif word in self.bossfight_words:
            transformed_color = pg.Color("red")
            # print("bossfight")
        else:
            transformed_color = self.rainbow(hue)
            # print("normal")

        end_surf = self.font.render(end_text, True, transformed_color)
        Surf.blit(start_surf, (8, 8))
        Surf.blit(end_surf, end_surf.get_rect(right=w - 8, centery=h // 2))
        return Surf

    def generate_prompt_surf(self):
        width = self.SCREEN.get_width()
        surf = pg.Surface((width, 50), pg.SRCALPHA)
        surf.fill((25, 24, 77))

        if not hasattr(self, 'prompt_alpha'):
            self.prompt_alpha = 0
        if self.prompt_alpha < 255:
            self.prompt_alpha += 1
        surf.set_alpha(self.prompt_alpha)

        color = pg.Color(255, 253, 11) if any(w.startswith(self.prompt_content) for w in self.current_words) \
            else pg.Color(214, 24, 24)
        rendered = self.font.render(self.prompt_content, True, color)

        # Create shadow text
        shadow_color = pg.Color(180, 200, 255)
        shadow_rendered = self.font.render(self.prompt_content, True, shadow_color)

        # Center the prompt text horizontally on the surface
        rect = rendered.get_rect(centerx=width // 2, centery=25)
        shadow_rect = shadow_rendered.get_rect(centerx=width // 2 + 2, centery=26)  # Slightly offset for shadow effect

        # Blit shadow first, then main text
        surf.blit(shadow_rendered, shadow_rect)
        surf.blit(rendered, rect)

        return surf

    def draw_ui(self):
        top_box = pg.Surface((self.SCREEN.get_width(), 40), pg.SRCALPHA)
        top_box.fill((194, 31, 31))
        top_box_rect = top_box.get_rect()
        if not hasattr(self, 'ui_alpha'):
            self.ui_alpha = 0

        if self.ui_alpha < 255:
            self.ui_alpha += 1  # Adjust the increment value as needed

        top_box.set_alpha(self.ui_alpha)
        self.SCREEN.blit(top_box, top_box_rect)

        score_surf = self.font.render(f"Score: {self.score}",
                                      True, (255, 255, 255))
        health_surf = self.font.render(f"Health: {self.health}",
                                       True, (255, 255, 255))
        enemy_name = self.font.render(f"Enemy: Tutorial Guy",
                                      True, (255, 255, 255))

        # Calculate positions for the text
        screen_width = self.SCREEN.get_width()
        score_pos = (10, 10)
        health_pos = (screen_width // 3, 10)
        enemy_pos = (2 * screen_width // 3, 10)

        self.SCREEN.blit(score_surf, score_pos)
        self.SCREEN.blit(health_surf, health_pos)
        self.SCREEN.blit(enemy_name, enemy_pos)

        pg.draw.line(self.SCREEN, (255, 255, 255),
                     (screen_width // 3 - 5, 0),
                     (screen_width // 3 - 5, 40), 2)
        pg.draw.line(self.SCREEN, (255, 255, 255),
                     (2 * screen_width // 3 - 5, 0),
                     (2 * screen_width // 3 - 5, 40), 2)

    def display_game_over(self):
        write_score(self.score)
        game_over = self.font.render("GAME OVER", True, (255, 0, 0))
        center = (self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2)
        self.SCREEN.blit(game_over, game_over.get_rect(center=center))
        pg.display.flip()
        pg.time.wait(2000)

    def apply_fade_effect(self):
        if self.fade_direction != 0:
            self.fade_alpha += self.fade_direction * 10
            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.fade_direction = 0
            elif self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.fade_direction = 0
        fade_surf = pg.Surface(self.SCREEN.get_size(), pg.SRCALPHA)
        fade_surf.fill((255, 0, 0, self.fade_alpha))
        self.SCREEN.blit(fade_surf, (0, 0))

class Stage1Enemies:
    def __init__(self, screen, level, normal_sprite_path, hit_sprite_path):
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        self.font = pg.font.Font("resources/DejaVuSans.ttf", 36)
        self.hitpoints = 25 + level * 5
        self.word_speed = 1
        self.current_word = ""
        self.word_progress = 0
        self.start_timer = 2.5
        self.is_hit = False
        self.sprite_alpha = 0

        self.normal_sprite = pg.image.load(normal_sprite_path).convert_alpha()
        self.hit_sprite = pg.image.load(hit_sprite_path).convert_alpha()
        self.talk_sprite = pg.image.load(normal_sprite_path).convert_alpha()
        self.defeat_sprite = pg.image.load(normal_sprite_path).convert_alpha()
        self.normal_sprite = pg.transform.scale(self.normal_sprite, (300, 500))
        self.hit_sprite = pg.transform.scale(self.hit_sprite, (300, 500))
        self.talk_sprite = pg.transform.scale(self.talk_sprite, (300, 500))
        self.defeat_sprite = pg.transform.scale(self.defeat_sprite, (300, 500))
        self.sprite_rect = self.normal_sprite.get_rect()
        self.sprite_rect.centerx = self.width - 250
        self.sprite_rect.centery = self.height - 300  # Adjusted to align with the prompt surf
        self.word_bg_image = pg.image.load("resources/transparent/tristan.gif").convert_alpha()
        self.explosions = []

    def reset_word(self, current_words):
        if self.current_word in current_words:
            del current_words[self.current_word]
        self.current_word = ""
        self.word_progress = 0
        self.start_timer = 2.5

    def update(self, timepassed, player_input, current_words):
        if self.sprite_alpha < 255:
            self.sprite_alpha += 5

        if self.hitpoints <= 0:
            return False

        if not self.current_word and current_words:
            self.current_word = random.choice(list(current_words.keys()))
            self.word_progress = 0

        if self.current_word and (self.current_word not in current_words):
            self.current_word = ""
            self.word_progress = 0
            self.start_timer = 2.5

        if self.start_timer > 0:
            self.start_timer -= timepassed
            return False

        if self.current_word:
            self.word_progress += timepassed * self.word_speed
            meta = current_words[self.current_word]
            # Use the updated meta data for y-position
            word_x = meta[0]
            meta_y = meta[1]
            y = (meta_y * self.word_speed) + abs(math.cos(meta_y * 3) * 10)
            word_rect = pg.Rect(word_x, y, self.font.size(self.current_word)[0],
                                self.font.size(self.current_word)[1])
            if self.word_progress >= len(self.current_word):
                # Store the completed word before resetting
                completed_word = self.current_word
                handle_explosion_effect(self.screen, self.font, self.sprite_rect, completed_word, self.explosions)
                if self.current_word in current_words:
                    current_words.pop(self.current_word)
                self.current_word = ""
                self.word_progress = 0
                self.start_timer = 2.0
                return True

        return False

    def get_font_size(self, word_length):
        if word_length > 5:
            return 24  # Smaller font size for words longer than 5 letters
        else:
            return 28  # Default font size

    def draw(self):
        if self.hitpoints <= 0:
            current_sprite = self.defeat_sprite
        else:
            current_sprite = self.hit_sprite if self.is_hit else self.normal_sprite

        sprite_with_alpha = current_sprite.copy()
        sprite_with_alpha.set_alpha(self.sprite_alpha)
        self.screen.blit(sprite_with_alpha, self.sprite_rect)

        if self.hitpoints > 0 and self.current_word:
            # Render the typed and remaining portions of the word
            typed = self.current_word[:int(self.word_progress)]
            remaining = self.current_word[int(self.word_progress):]

            # Get appropriate font size based on word length
            font_size = self.get_font_size(len(self.current_word))
            font = pg.font.Font("resources/DejaVuSans.ttf", font_size)

            typed_surf = font.render(typed, True, (255, 0, 0))
            remaining_surf = font.render(remaining, True, (100, 100, 100))

            total_width = typed_surf.get_width() + remaining_surf.get_width()
            text_height = typed_surf.get_height()

            # Define the text box size based on the text dimensions with extra margin
            box_width = int(total_width * 1.5) + 20
            box_height = int(text_height * 1.5) + 10

            # Scale the background image for the word box
            word_bg_image_scaled = pg.transform.scale(self.word_bg_image, (box_width, box_height))

            # Position the text box with a negative x-coordinate to overlay over the sprite
            word_box_rect = word_bg_image_scaled.get_rect(
                midright=(self.sprite_rect.left - 20, self.sprite_rect.centery))
            word_box_rect.x += 100  # Adjust this value as needed to overlay the text box

            # Calculate centered text position within the text box
            text_x = word_box_rect.left + (box_width - total_width) // 2
            text_y = word_box_rect.top + (box_height - text_height) // 2

            # Blit the text box and then the text centered in it
            self.screen.blit(word_bg_image_scaled, word_box_rect)
            self.screen.blit(typed_surf, (text_x, text_y))
            self.screen.blit(remaining_surf, (text_x + typed_surf.get_width(), text_y))

        # Draw any active explosions
        current_time = pg.time.get_ticks()
        self.explosions = [(img, rect, start_time) for img, rect, start_time in self.explosions
                           if current_time - start_time < 500]
        for img, rect, _ in self.explosions:
            self.screen.blit(img, rect)

    def draw_before_battle(self):
        self.screen.blit(self.normal_sprite, self.sprite_rect)

class Minion1(Stage1Enemies):
    def __init__(self, screen, level):
        super().__init__(screen, level, "resources/sprites/White-1.png", "resources/sprites/White-1-hit.gif")
        self.dialogue_text = "\"Prepare yourself for the battle!\""
        self.defeat_text = "\"Congrats!\""
        self.word_speed = 1

class Minion2(Stage1Enemies):
    def __init__(self, screen, level):
        super().__init__(screen, level, "resources/sprites/White-2.png",
                         "resources/sprites/White-2-hit.gif")
        self.dialogue_text = "\"Prepare yourself for the battle!\""
        self.defeat_text = "\"Congrats!\""
        self.word_speed = 1.2

class Minion3(Stage1Enemies):
    def __init__(self, screen, level):
        super().__init__(screen, level, "resources/sprites/White-3.png",
                         "resources/sprites/White-3-hit.gif")
        self.dialogue_text = "\"Prepare yourself for the battle!\""
        self.defeat_text = "\"Congrats!\""
        self.word_speed = 1.3

class Boss(Stage1Enemies):
    def __init__(self, screen, level):
        super().__init__(screen, level, "resources/sprites/White-1.png", "resources/sprites/White-1-hit.gif")
        self.dialogue_text = "\"I am the final challenge! Prepare yourself!\""
        self.defeat_text = "\"Congrats!\""
        self.hitpoints = 50 + level * 10  # Boss has more hitpoints
        self.word_speed = 2.5 # Boss has a faster word speed


"""STAGE 1 END----------------------------------------------------------------------------------------------------------

STAGE 2 START--------------------------------------------------------------------------------------------------------"""
class Stage2:
    def __init__(self, screen, level):
        self.SCREEN = screen
        width, height = self.SCREEN.get_size()
        self.font = pg.font.Font("resources/DejaVuSans.ttf", 22)
        self.BG = stretch(pg.image.load("resources/backgrounds/gym_blurred.png").convert_alpha(), (width, height))
        self.phase = 0

        pg.key.set_repeat(250, 30)

        self.clock = pg.time.Clock()
        self.stage2_words, self.bonus_words, self.bossfight_words = generate_words_stage2()
        self.current_words = {}
        self.word_timer = 0
        self.word_frequency = 2.5
        self.level = level
        self.score = 0
        self.health = 20
        self.prompt_content = ''
        self.word_speed = 50
        self.word_widths = {}
        self.highscore = load_score()
        self.enemies = [Minion1STwo(screen, self.level), Minion2STwo(screen, self.level), Minion3STwo(screen, self.level),
                        BossSTwo(screen, self.level)]
        self.current_enemy_index = 0
        self.enemy = self.enemies[self.current_enemy_index]
        self.enemy.talking = True
        self.fade_alpha = 0
        self.fade_direction = 1
        self.damage_flash_alpha = 0
        self.bonus_word_counter = 0

        # Load background music
        pg.mixer.init()
        self.prebattle_music = "resources/sounds/songs/prebattle.mp3"
        self.inbattle_music = "resources/sounds/songs/inbattle.mp3"

        # Load sound effects
        self.enemyhit_sfx = pg.mixer.Sound("resources/sounds/sfx/enemyhit.mp3")
        self.win_sfx = pg.mixer.Sound("resources/sounds/sfx/win.mp3")
        self.wordcomplete_sfx = pg.mixer.Sound("resources/sounds/sfx/wordcomplete.mp3")

        self.explosions = []
        self.bossfight_pause_timer = 0
        self.falling_words_pause_timer = 0
        self.last_bonus_action = 'damage'

    def run(self):
        width, height = self.SCREEN.get_size()
        battle_started = False
        hue = 0

        # while self.current_enemy_index < len(self.enemies):
        #     self.enemy = self.enemies[self.current_enemy_index]
        #     self.before_battle_display(self.enemy)
        #     battle_started = True
        #
        #     if isinstance(self.enemy, BossSTwo):
        #         max_health = self.enemy.get_max_health()
        #         self.enemy.hitpoints = min(self.enemy.hitpoints + 0.2 * timepassed, max_health)

        self.current_enemy_index = 3

        while self.current_enemy_index == 3 :
            self.enemy = self.enemies[self.current_enemy_index]
            self.before_battle_display(self.enemy)
            battle_started = True

            pg.mixer.music.load(self.inbattle_music)
            pg.mixer.music.play(-1)

            while True:
                timepassed = self.clock.tick(60) / 1000.0

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            if battle_started:
                                pause(self.SCREEN, self.BG)
                            else:
                                return
                        if battle_started:
                            if event.unicode.isprintable():
                                self.prompt_content += event.unicode
                            elif event.key == pg.K_BACKSPACE:
                                self.prompt_content = self.prompt_content[:-1]
                            elif event.key == pg.K_RETURN:
                                self.prompt_content = ''

                self.SCREEN.blit(self.BG, (0, 0))

                if isinstance(self.enemy, BossSTwo):
                    max_health = self.enemy.get_max_health()
                    self.enemy.hitpoints = min(self.enemy.hitpoints + 0.02 * timepassed, max_health)

                if self.health <= 0:
                    self.display_game_over()
                    return

                if not battle_started:
                    prompt_text = "Press Enter to start the battle"
                    prompt_surf = self.font.render(prompt_text, True, pg.Color("white"))
                    prompt_rect = prompt_surf.get_rect(center=(width // 2, height // 2))
                    self.SCREEN.blit(prompt_surf, prompt_rect)
                else:
                    if self.fade_alpha < 255:
                        self.apply_fade_effect()
                    else:
                        # if self.words_started_falling:
                        self.word_timer += timepassed
                        if self.word_timer > self.word_frequency and len(self.current_words) < len(
                                self.stage2_words):
                            self.add_word(width, self.stage2_words, 'stage2', self.enemy)
                            self.word_timer = 0

                        while len(self.current_words) < 3:
                            self.add_word(width, self.stage2_words, 'stage2', self.enemy)

                        for word, meta in list(self.current_words.items()):
                            meta[1] += timepassed
                            y = (meta[1] * self.word_speed) + abs(math.cos(meta[1] * 3) * 10)
                            word_rect = pg.Rect(meta[0], y, self.font.size(word)[0], self.font.size(word)[1])
                            if y > height:
                                del self.current_words[word]
                                self.health -= 1
                                self.damage_flash_alpha = 150
                            elif word == self.prompt_content:
                                del self.current_words[word]
                                self.score += len(word) * 2
                                self.prompt_content = ""
                                self.wordcomplete_sfx.play()
                                self.handle_explosion_effect(word_rect)
                                if word == self.enemy.current_word:
                                    self.apply_damage(1, word)
                                    self.handle_explosion_effect(word_rect)
                                elif word in self.bonus_words:
                                    if self.last_bonus_action == 'damage':
                                        self.apply_damage(3, word)
                                        self.last_bonus_action = 'health'
                                        self.handle_explosion_effect(word_rect)
                                    else:
                                        self.health = min(self.health + 1.5, 50)
                                        self.last_bonus_action = 'damage'
                                        self.enemy.reset_word(self.current_words)
                                        self.enemy.is_hit = True
                                        self.enemyhit_sfx.play()
                                        self.handle_explosion_effect(word_rect)
                                elif word in self.bossfight_words:
                                    self.apply_damage(5, word)
                                    self.handle_explosion_effect(word_rect)
                                    self.bossfight_pause_timer = 3.0
                                    self.falling_words_pause_timer = 1.0
                                    self.handle_explosion_effect(word_rect)
                                else:
                                    self.enemy.is_hit = False

                            else:
                                word_surf = self.create_word_surf(word, meta[2], hue, meta[3])
                                word_rect = word_surf.get_rect(center=(meta[0], y))
                                enemy_rect = self.enemy.sprite_rect
                                if word_rect.colliderect(enemy_rect):
                                    if enemy_rect.left - word_rect.width - 10 >= 0:
                                        word_rect.right = enemy_rect.left - 10
                                    else:
                                        word_rect.left = enemy_rect.right + 10
                                self.SCREEN.blit(word_surf, word_rect)

                        if self.current_words:
                            if self.enemy.update(timepassed, self.prompt_content, self.current_words):
                                if isinstance(self.enemy, Boss):
                                    self.health -= 1.25 * self.level  # Boss deals near twice the damage
                                else:
                                    self.health -= self.level  # Minions deal damage based on the level
                                self.damage_flash_alpha = 150

                        if self.enemy.hitpoints <= 0:
                            self.win_sfx.play()
                            pg.mixer.music.stop()
                            self.defeat_display(self.enemy)
                            self.current_enemy_index += 1
                            break

                    self.enemy.draw()
                    self.SCREEN.blit(self.generate_prompt_surf(), (0, height - 50))
                    self.draw_ui()
                    self.draw_enemy_hitpoints()

                    if self.damage_flash_alpha > 0:
                        flash_surf = pg.Surface(self.SCREEN.get_size(), pg.SRCALPHA)
                        flash_surf.fill((255, 0, 0, self.damage_flash_alpha))
                        self.SCREEN.blit(flash_surf, (0, 0))
                        self.damage_flash_alpha = max(0, self.damage_flash_alpha - 8)

                    # Draw and manage explosions
                    current_time = pg.time.get_ticks()
                    self.explosions = [(img, rect, start_time) for img, rect, start_time in self.explosions if
                                       current_time - start_time < 500]
                    for img, rect, _ in self.explosions:
                        self.SCREEN.blit(img, rect)

                    pg.display.flip()
                    hue = (hue + 1) % 360  # Update hue for the next frame

        self.display_victory()
        from introduction import Stage2Outro
        outro = Stage2Outro(self.SCREEN)
        outro.run()

    def apply_damage(self, damage, word, reset_word=True, play_sound=True):
        self.enemy.hitpoints = max(0, self.enemy.hitpoints - ((damage * len(word)) * 0.25))
        self.enemy.is_hit = True
        if reset_word:
            self.enemy.reset_word(self.current_words)
        if play_sound:
            self.enemyhit_sfx.play()

    def handle_explosion_effect(self, word_rect):
        explosion_image = pg.image.load(f'resources/transparent/boom-{random.randint(1, 3)}.gif').convert_alpha()
        scale_factor = 0.20  # Adjust this factor to make the explosion image larger
        new_width = int(explosion_image.get_width() * scale_factor)
        new_height = int(explosion_image.get_height() * scale_factor)
        explosion_image = pg.transform.scale(explosion_image, (new_width, new_height))
        explosion_rect = explosion_image.get_rect(center=word_rect.center)
        self.explosions.append((explosion_image, explosion_rect, pg.time.get_ticks()))

    def before_battle_display(self, minion):
        fade_duration = 1.0  # Duration of the fade-in effect in seconds
        fade_alpha = 0  # Initial alpha value for fade-in effect
        fade_increment = 255 / (fade_duration * 60)  # Increment per frame (assuming 60 FPS)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        from mapuantypingmania import game_Menu
                        game = game_Menu()
                        game.main_Menu()
                        return
                    elif event.key == pg.K_RETURN:
                        return  # Exit the display and start the battle

            self.SCREEN.blit(self.BG, (0, 0))

            # Draw the minion sprite talking with fade-in effect
            talk_sprite = minion.talk_sprite.copy()
            talk_sprite.set_alpha(fade_alpha)
            talk_sprite_rect = talk_sprite.get_rect(
                center=(self.SCREEN.get_width() - 250, self.SCREEN.get_height() // 2))
            self.SCREEN.blit(talk_sprite, talk_sprite_rect)

            # Draw the dialogue box using tutorial.gif with fade-in effect
            small_font = pg.font.Font("resources/DejaVuSans.ttf", 20)
            dlg_surf = small_font.render(minion.dialogue_text, True, pg.Color(251, 255, 52))
            dlg_surf.set_alpha(fade_alpha)

            # Load and scale the tutorial.gif image for the dialogue box
            word_bg_image = pg.image.load("resources/transparent/tristan.gif").convert_alpha()
            box_width = int(dlg_surf.get_width() * 1.5) + 5
            box_height = int(dlg_surf.get_height() * 1.5) + 30
            word_bg_image_scaled = pg.transform.scale(word_bg_image, (box_width, box_height))
            word_bg_image_scaled.set_alpha(fade_alpha)

            # Position the dialogue box with a negative x-coordinate to overlay over the sprite
            dlg_box_rect = word_bg_image_scaled.get_rect(
                midright=(talk_sprite_rect.left - 20, talk_sprite_rect.centery))
            dlg_box_rect.x += 140  # Adjust this value as needed to overlay the dialogue box

            # Blit the dialogue box and then the text centered in it
            self.SCREEN.blit(word_bg_image_scaled, dlg_box_rect)
            self.SCREEN.blit(dlg_surf, dlg_surf.get_rect(center=dlg_box_rect.center))

            # Draw the bottom bar with fade-in effect
            bottom_bar_height = 100
            bottom_bar = pg.Surface((self.SCREEN.get_width(), bottom_bar_height), pg.SRCALPHA)
            bottom_bar.fill((25, 24, 77, fade_alpha))
            self.SCREEN.blit(bottom_bar, (0, self.SCREEN.get_height() - bottom_bar_height))

            # Draw the prompt to continue with fade-in effect
            prompt_text = "Press Enter to start the battle"
            prompt_surf = self.font.render(prompt_text, True, pg.Color("white"))
            prompt_surf_shadow = self.font.render(prompt_text, True, pg.Color("black"))
            prompt_surf.set_alpha(fade_alpha)
            prompt_surf_shadow.set_alpha(fade_alpha)
            prompt_rect = prompt_surf.get_rect(
                center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - bottom_bar_height // 2))
            self.SCREEN.blit(prompt_surf_shadow, prompt_rect.move(2, 2))
            self.SCREEN.blit(prompt_surf, prompt_rect)

            # Apply fade-in effect
            if fade_alpha < 255:
                fade_alpha = min(255, fade_alpha + fade_increment)

            pg.display.flip()
            self.clock.tick(60)

    def display_victory(self):
        if self.score > self.highscore:
            self.highscore = self.score
            write_score(self.highscore)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        from mapuantypingmania import game_Menu
                        game = game_Menu()
                        game.play()
                    else:
                        from introduction import Intro
                        LoadingScreen(self.SCREEN).run()
                        Intro(self.SCREEN).run()

            # Prepare text surfaces and their positions
            center = (self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2)
            victory_surf = self.font.render("VICTORY!", True, pg.Color("white"))
            highscore_text = f"Highscore: {self.highscore}"
            highscore_surf = self.font.render(highscore_text, True, pg.Color("white"))
            prompt_text = "Press any key for next stage, or Esc for main menu"
            prompt_surf = self.font.render(prompt_text, True, pg.Color("white"))

            victory_rect = victory_surf.get_rect(center=(center[0], center[1] - 40))
            hs_rect = highscore_surf.get_rect(center=center)
            prompt_rect = prompt_surf.get_rect(center=(center[0], center[1] + 40))

            # Calculate the bounding rectangle of all text surfaces and add padding
            union_rect = victory_rect.union(hs_rect).union(prompt_rect)
            padding = 10
            dlg_rect = pg.Rect(
                union_rect.left - padding,
                union_rect.top - padding,
                union_rect.width + 2 * padding,
                union_rect.height + 2 * padding
            )

            # Create the dialog box surface with an opaque yellow red color
            dlg_box = pg.Surface((dlg_rect.width, dlg_rect.height))
            dlg_box.fill((255, 193, 33))

            # Draw background and dialog box
            self.SCREEN.blit(self.BG, (0, 0))
            self.SCREEN.blit(dlg_box, dlg_rect.topleft)
            # Draw border if desired (optional)
            pg.draw.rect(self.SCREEN, (255, 0, 0), dlg_rect, 3)

            # Blit each text surface centered at their respective positions
            self.SCREEN.blit(victory_surf, victory_rect)
            self.SCREEN.blit(highscore_surf, hs_rect)
            self.SCREEN.blit(prompt_surf, prompt_rect)

            pg.display.flip()
            self.clock.tick(60)

    def draw_enemy_hitpoints(self):
        hp_text = f"Enemy HP: {self.enemy.hitpoints:.1f}"
        hp_surf = self.font.render(hp_text, True, (255, 255, 255))
        hp_box = pg.Surface((hp_surf.get_width() + 10, hp_surf.get_height() + 10), pg.SRCALPHA)
        hp_box.fill((27, 219, 24, 190))

        # Initialize and update fade alpha for enemy hitpoints
        if not hasattr(self, 'hp_alpha'):
            self.hp_alpha = 0
        if self.hp_alpha < 255:
            self.hp_alpha += 5  # Adjust increment as needed for smoother or faster fade
        hp_box.set_alpha(self.hp_alpha)

        hp_box_rect = hp_box.get_rect(midtop=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - 100))

        self.SCREEN.blit(hp_box, hp_box_rect)
        self.SCREEN.blit(hp_surf, hp_surf.get_rect(center=hp_box_rect.center))

        # Draw a bar line to separate the hitpoints and prompt surface
        pg.draw.line(self.SCREEN, (255, 255, 255),
                     (0, self.SCREEN.get_height() - 50),
                     (self.SCREEN.get_width(), self.SCREEN.get_height() - 50), 2)

    def defeat_display(self, minion):
        fade_duration = 1.0
        fade_alpha = 0
        fade_increment = 255 / (fade_duration * 60)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        from mapuantypingmania import game_Menu
                        game = game_Menu()
                        game.main_Menu()
                        return
                    elif event.key == pg.K_RETURN:
                        return

            self.SCREEN.blit(self.BG, (0, 0))

            defeat_sprite = minion.defeat_sprite.copy()
            defeat_sprite.set_alpha(fade_alpha)
            defeat_sprite_rect = defeat_sprite.get_rect(
                center=(self.SCREEN.get_width() - 250, self.SCREEN.get_height() // 2))
            self.SCREEN.blit(defeat_sprite, defeat_sprite_rect)

            small_font = pg.font.Font("resources/DejaVuSans.ttf", 20)
            dlg_surf = small_font.render(minion.defeat_text, True, pg.Color(251, 255, 52))
            dlg_surf.set_alpha(fade_alpha)

            word_bg_image = pg.image.load("resources/transparent/tristan.gif").convert_alpha()
            box_width = int(dlg_surf.get_width() * 1.5) + 5
            box_height = int(dlg_surf.get_height() * 1.5) + 30
            word_bg_image_scaled = pg.transform.scale(word_bg_image, (box_width, box_height))
            word_bg_image_scaled.set_alpha(fade_alpha)

            dlg_box_rect = word_bg_image_scaled.get_rect(
                midright=(defeat_sprite_rect.left - 20, defeat_sprite_rect.centery))
            dlg_box_rect.x += 140

            self.SCREEN.blit(word_bg_image_scaled, dlg_box_rect)
            self.SCREEN.blit(dlg_surf, dlg_surf.get_rect(center=dlg_box_rect.center))

            bottom_bar_height = 100
            bottom_bar = pg.Surface((self.SCREEN.get_width(), bottom_bar_height), pg.SRCALPHA)
            bottom_bar.fill((25, 24, 77, fade_alpha))
            self.SCREEN.blit(bottom_bar, (0, self.SCREEN.get_height() - bottom_bar_height))

            prompt_text = "Press Enter to continue"
            prompt_surf = self.font.render(prompt_text, True, pg.Color("white"))
            prompt_surf_shadow = self.font.render(prompt_text, True, pg.Color("black"))
            prompt_surf.set_alpha(fade_alpha)
            prompt_surf_shadow.set_alpha(fade_alpha)
            prompt_rect = prompt_surf.get_rect(
                center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() - bottom_bar_height // 2))
            self.SCREEN.blit(prompt_surf_shadow, prompt_rect.move(2, 2))
            self.SCREEN.blit(prompt_surf, prompt_rect)

            if fade_alpha < 255:
                fade_alpha = min(255, fade_alpha + fade_increment)

            pg.display.flip()
            self.clock.tick(60)

    def rainbow(self, hue):
        color = pg.Color("white")
        hue = (hue + 1) % 360
        color.hsva = (hue, 100, 100, 100)
        return color

    def add_word(self, width, words, word_type, enemy):
        found_word = False
        while not found_word and len(self.current_words) < len(words):
            if self.bonus_word_counter >= 4 and word_type != 'bossfight':
                selected = random.choice(self.bossfight_words)
                self.bonus_word_counter = 0 # Reset the counter after adding a bossfight word
            elif word_type == 'bonus' or (self.bonus_word_counter >= 6 and word_type != 'bossfight'):
                selected = random.choice(self.bonus_words)
                self.bonus_word_counter = 0  # Reset the counter after adding a bonus word
            elif word_type == 'bossfight' and isinstance(enemy,
                                                         Boss):  # Ensure bossfight words only appear during boss fights
                selected = random.choice(self.bossfight_words)
            else:
                # Adjust the selection logic to balance word lengths on screen
                word_lengths = [len(word) for word in words]
                current_lengths = [len(word) for word in self.current_words.keys()]

                # Count the occurrences of each word length currently on screen
                length_counts = {length: current_lengths.count(length) for length in set(word_lengths)}

                # Calculate weights to balance the word lengths
                weights = []
                for length in word_lengths:
                    if length_counts.get(length, 0) < 2:  # Adjust this threshold as needed
                        weights.append(1)
                    else:
                        weights.append(0.1)

                selected = random.choices(words, weights=weights, k=1)[0]
                self.bonus_word_counter += 1  # Increment the counter for normal words

            if all(not w.startswith(selected[0]) for w in self.current_words):
                if selected not in self.word_widths:
                    self.word_widths[selected] = self.font.size(selected)[0]
                w_width = self.word_widths[selected]
                x = random.randrange(45, width - w_width - 10)  # Ensure the word does not overlap the screen edges
                # Ensure the word does not overlap with the enemy sprite and other words
                if not (enemy.sprite_rect.left < x < enemy.sprite_rect.right) and \
                        all(abs(x - meta[0]) > w_width + 15 for meta in self.current_words.values()):
                    self.current_words[selected] = [x, 0, (150, 150, 150), word_type]
                    found_word = True

                    # Adjust word frequency based on word type
                    if word_type == 'bonus':
                        self.word_frequency = max(1.0, self.word_frequency - 0.1)
                    elif word_type == 'bossfight':
                        self.word_frequency = max(0.5, self.word_frequency - 0.2)
                    else:
                        self.word_frequency = min(3.0, self.word_frequency + 0.1)

    def create_word_surf(self, word, color, hue, word_type):
        w, h = self.font.size(word)
        w += 12  # Increase width for padding
        h += 12  # Increase height for padding
        Surf = pg.Surface((w, h), pg.SRCALPHA, 32)

        pg.draw.rect(Surf, (222, 153, 0, 200), Surf.get_rect(), border_radius=10)

        being_written = self.prompt_content and word.startswith(self.prompt_content)
        start_text = self.prompt_content if being_written else ''
        end_text = word[len(self.prompt_content):] if being_written else word
        start_surf = self.font.render(start_text, True, pg.Color("black"))

        # Set constant colors for bonus and bossfight word types
        if word in self.bonus_words:
            transformed_color = pg.Color("gold")
            # print("bonus")
        elif word in self.bossfight_words:
            transformed_color = pg.Color("red")
            # print("bossfight")
        else:
            transformed_color = self.rainbow(hue)
            # print("normal")

        end_surf = self.font.render(end_text, True, transformed_color)
        Surf.blit(start_surf, (8, 8))
        Surf.blit(end_surf, end_surf.get_rect(right=w - 8, centery=h // 2))
        return Surf

    def generate_prompt_surf(self):
        width = self.SCREEN.get_width()
        surf = pg.Surface((width, 50), pg.SRCALPHA)
        surf.fill((25, 24, 77))

        if not hasattr(self, 'prompt_alpha'):
            self.prompt_alpha = 0
        if self.prompt_alpha < 255:
            self.prompt_alpha += 1
        surf.set_alpha(self.prompt_alpha)

        color = pg.Color(255, 253, 11) if any(w.startswith(self.prompt_content) for w in self.current_words) \
            else pg.Color(214, 24, 24)
        rendered = self.font.render(self.prompt_content, True, color)

        # Create shadow text
        shadow_color = pg.Color(180, 200, 255)
        shadow_rendered = self.font.render(self.prompt_content, True, shadow_color)

        # Center the prompt text horizontally on the surface
        rect = rendered.get_rect(centerx=width // 2, centery=25)
        shadow_rect = shadow_rendered.get_rect(centerx=width // 2 + 2, centery=26)  # Slightly offset for shadow effect

        # Blit shadow first, then main text
        surf.blit(shadow_rendered, shadow_rect)
        surf.blit(rendered, rect)

        return surf

    def draw_ui(self):
        top_box = pg.Surface((self.SCREEN.get_width(), 40), pg.SRCALPHA)
        top_box.fill((194, 31, 31))
        top_box_rect = top_box.get_rect()
        if not hasattr(self, 'ui_alpha'):
            self.ui_alpha = 0

        if self.ui_alpha < 255:
            self.ui_alpha += 1  # Adjust the increment value as needed

        top_box.set_alpha(self.ui_alpha)
        self.SCREEN.blit(top_box, top_box_rect)

        score_surf = self.font.render(f"Score: {self.score}",
                                      True, (255, 255, 255))
        health_surf = self.font.render(f"Health: {self.health}",
                                       True, (255, 255, 255))
        enemy_name = self.font.render(f"Enemy: Tutorial Guy",
                                      True, (255, 255, 255))

        # Calculate positions for the text
        screen_width = self.SCREEN.get_width()
        score_pos = (10, 10)
        health_pos = (screen_width // 3, 10)
        enemy_pos = (2 * screen_width // 3, 10)

        self.SCREEN.blit(score_surf, score_pos)
        self.SCREEN.blit(health_surf, health_pos)
        self.SCREEN.blit(enemy_name, enemy_pos)

        pg.draw.line(self.SCREEN, (255, 255, 255),
                     (screen_width // 3 - 5, 0),
                     (screen_width // 3 - 5, 40), 2)
        pg.draw.line(self.SCREEN, (255, 255, 255),
                     (2 * screen_width // 3 - 5, 0),
                     (2 * screen_width // 3 - 5, 40), 2)

    def display_game_over(self):
        write_score(self.score)
        game_over = self.font.render("GAME OVER", True, (255, 0, 0))
        center = (self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2)
        self.SCREEN.blit(game_over, game_over.get_rect(center=center))
        pg.display.flip()
        pg.time.wait(2000)

    def apply_fade_effect(self):
        if self.fade_direction != 0:
            self.fade_alpha += self.fade_direction * 10
            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.fade_direction = 0
            elif self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.fade_direction = 0
        fade_surf = pg.Surface(self.SCREEN.get_size(), pg.SRCALPHA)
        fade_surf.fill((255, 0, 0, self.fade_alpha))
        self.SCREEN.blit(fade_surf, (0, 0))

class Stage2Enemies:
    def __init__(self, screen, level, normal_sprite_path, hit_sprite_path):
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        self.font = pg.font.Font("resources/DejaVuSans.ttf", 36)
        self.hitpoints = 25 + level * 5
        self.word_speed = 1
        self.current_word = ""
        self.word_progress = 0
        self.start_timer = 2.5
        self.is_hit = False
        self.sprite_alpha = 0

        self.normal_sprite = pg.image.load(normal_sprite_path).convert_alpha()
        self.hit_sprite = pg.image.load(hit_sprite_path).convert_alpha()
        self.talk_sprite = pg.image.load(normal_sprite_path).convert_alpha()
        self.defeat_sprite = pg.image.load(normal_sprite_path).convert_alpha()
        self.normal_sprite = pg.transform.scale(self.normal_sprite, (300, 500))
        self.hit_sprite = pg.transform.scale(self.hit_sprite, (300, 500))
        self.talk_sprite = pg.transform.scale(self.talk_sprite, (300, 500))
        self.defeat_sprite = pg.transform.scale(self.defeat_sprite, (300, 500))
        self.sprite_rect = self.normal_sprite.get_rect()
        self.sprite_rect.centerx = self.width - 250
        self.sprite_rect.centery = self.height - 300  # Adjusted to align with the prompt surf
        self.word_bg_image = pg.image.load("resources/transparent/hao.gif").convert_alpha()
        self.explosions = []

    def reset_word(self, current_words):
        if self.current_word in current_words:
            del current_words[self.current_word]
        self.current_word = ""
        self.word_progress = 0
        self.start_timer = 2.5

    def update(self, timepassed, player_input, current_words):
        if self.sprite_alpha < 255:
            self.sprite_alpha += 5

        if self.hitpoints <= 0:
            return False

        if not self.current_word and current_words:
            self.current_word = random.choice(list(current_words.keys()))
            self.word_progress = 0

        if self.current_word and (self.current_word not in current_words):
            self.current_word = ""
            self.word_progress = 0
            self.start_timer = 2.5

        if self.start_timer > 0:
            self.start_timer -= timepassed
            return False

        if self.current_word:
            self.word_progress += timepassed * self.word_speed
            meta = current_words[self.current_word]
            # Use the updated meta data for y-position
            word_x = meta[0]
            meta_y = meta[1]
            y = (meta_y * self.word_speed) + abs(math.cos(meta_y * 3) * 10)
            word_rect = pg.Rect(word_x, y, self.font.size(self.current_word)[0],
                                self.font.size(self.current_word)[1])
            if self.word_progress >= len(self.current_word):
                # Store the completed word before resetting
                completed_word = self.current_word
                handle_explosion_effect(self.screen, self.font, self.sprite_rect, completed_word, self.explosions)
                if self.current_word in current_words:
                    current_words.pop(self.current_word)
                self.current_word = ""
                self.word_progress = 0
                self.start_timer = 2.0
                return True

        return False

    def get_font_size(self, word_length):
        if word_length > 5:
            return 24  # Smaller font size for words longer than 5 letters
        else:
            return 28  # Default font size

    def draw(self):
        if self.hitpoints <= 0:
            current_sprite = self.defeat_sprite
        else:
            current_sprite = self.hit_sprite if self.is_hit else self.normal_sprite

        sprite_with_alpha = current_sprite.copy()
        sprite_with_alpha.set_alpha(self.sprite_alpha)
        self.screen.blit(sprite_with_alpha, self.sprite_rect)

        if self.hitpoints > 0 and self.current_word:
            # Render the typed and remaining portions of the word
            typed = self.current_word[:int(self.word_progress)]
            remaining = self.current_word[int(self.word_progress):]

            # Get appropriate font size based on word length
            font_size = self.get_font_size(len(self.current_word))
            font = pg.font.Font("resources/DejaVuSans.ttf", font_size)

            typed_surf = font.render(typed, True, (255, 0, 0))
            remaining_surf = font.render(remaining, True, (100, 100, 100))

            total_width = typed_surf.get_width() + remaining_surf.get_width()
            text_height = typed_surf.get_height()

            # Define the text box size based on the text dimensions with extra margin
            box_width = int(total_width * 1.5) + 20
            box_height = int(text_height * 1.5) + 10

            # Scale the background image for the word box
            word_bg_image_scaled = pg.transform.scale(self.word_bg_image, (box_width, box_height))

            # Position the text box with a negative x-coordinate to overlay over the sprite
            word_box_rect = word_bg_image_scaled.get_rect(
                midright=(self.sprite_rect.left - 20, self.sprite_rect.centery))
            word_box_rect.x += 100  # Adjust this value as needed to overlay the text box

            # Calculate centered text position within the text box
            text_x = word_box_rect.left + (box_width - total_width) // 2
            text_y = word_box_rect.top + (box_height - text_height) // 2

            # Blit the text box and then the text centered in it
            self.screen.blit(word_bg_image_scaled, word_box_rect)
            self.screen.blit(typed_surf, (text_x, text_y))
            self.screen.blit(remaining_surf, (text_x + typed_surf.get_width(), text_y))

        # Draw any active explosions
        current_time = pg.time.get_ticks()
        self.explosions = [(img, rect, start_time) for img, rect, start_time in self.explosions
                           if current_time - start_time < 500]
        for img, rect, _ in self.explosions:
            self.screen.blit(img, rect)

    def draw_before_battle(self):
        self.screen.blit(self.normal_sprite, self.sprite_rect)

class Minion1STwo(Stage2Enemies):
    def __init__(self, screen, level):
        super().__init__(screen, level, "resources/sprites/Yellow-1.png", "resources/sprites/Yellow-1-hit.gif")
        self.dialogue_text = "\"Prepare yourself for the battle!\""
        self.defeat_text = "\"Congrats!\""
        self.word_speed = 1

class Minion2STwo(Stage2Enemies):
    def __init__(self, screen, level):
        super().__init__(screen, level, "resources/sprites/Yellow-2.png",
                         "resources/sprites/Yellow-2-hit.gif")
        self.dialogue_text = "\"Prepare yourself for the battle!\""
        self.defeat_text = "\"Congrats!\""
        self.word_speed = 1.3

class Minion3STwo(Stage2Enemies):
    def __init__(self, screen, level):
        super().__init__(screen, level, "resources/sprites/Yellow-3.png",
                         "resources/sprites/Yellow-3-hit.gif")
        self.dialogue_text = "\"Prepare yourself for the battle!\""
        self.defeat_text = "\"Congrats!\""
        self.word_speed = 1.5

class BossSTwo(Stage2Enemies):
    def __init__(self, screen, level):
        super().__init__(screen, level, "resources/sprites/Yellow-1.png", "resources/sprites/Yellow-1-hit.gif")
        self.dialogue_text = "\"I am the final challenge! Prepare yourself!\""
        self.defeat_text = "\"Congrats!\""
        self.hitpoints = 50 + level * 10  # Boss has more hitpoints
        self.max_health = self.hitpoints  # Store the initial maximum health
        self.word_speed = 2.8 # Boss has a faster word speed

    def get_max_health(self):
        return self.max_health


