import sys, pygame
pygame.init()

size = width, height = 320, 240
black = 0, 0, 0

screen = pygame.display.set_mode(size)

text = "Hello, World!"
font = pygame.font.Font(None, 36)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(black)  # Clear the screen with black color

    keys = pygame.key.get_pressed()
    if keys[pygame.K_l]:
        text1 = "Yup, the 'L' key is pressed"
        text_surface = font.render(text1, True, (123, 206, 34))
        screen.blit(text_surface, (50, 100))
    else:
        text_surface = font.render(text, True, (123, 206, 34))
        screen.blit(text_surface, (50, 100))

    pygame.display.flip()  # Update the display