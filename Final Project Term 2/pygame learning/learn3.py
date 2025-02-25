import pygame as pg
import random
import sys

# Initialize Pygame
pg.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Simple Falling Typing Game")

# Set up fonts
font = pg.font.SysFont('Arial', 30)

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up game variables
words = ["hello", "world", "python", "pygame", "typing", "game"]
falling_words = []
word_speed = 2
score = 0
input_text = ""

# Function to add a new word
def add_word():
    word = random.choice(words)
    x = random.randint(0, WIDTH - font.size(word)[0])
    y = 0
    falling_words.append([word, x, y])

# Main game loop
clock = pg.time.Clock()
add_word()
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.key == pg.K_RETURN:
                for word in falling_words:
                    if word[0] == input_text:
                        falling_words.remove(word)
                        score += len(input_text)
                        input_text = ""
                        break
            else:
                input_text += event.unicode

    # Update word positions
    for word in falling_words:
        word[2] += word_speed
        if word[2] > HEIGHT:
            falling_words.remove(word)
            score -= 1

    # Add new word periodically
    if random.randint(1, 100) < 2:
        add_word()

    # Clear screen
    screen.fill(BLACK)

    # Draw tutorial_words
    for word in falling_words:
        word_surface = font.render(word[0], True, WHITE)
        screen.blit(word_surface, (word[1], word[2]))

    # Draw input text
    input_surface = font.render(input_text, True, WHITE)
    screen.blit(input_surface, (10, HEIGHT - 40))

    # Draw score
    score_surface = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surface, (WIDTH - 150, 10))

    # Update display
    pg.display.flip()

    # Cap the frame rate
    clock.tick(30)