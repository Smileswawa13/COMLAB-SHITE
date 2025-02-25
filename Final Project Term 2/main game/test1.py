import pygame
import sys


def main():
    screen = pygame.display.set_mode((300, 100))
    FONT = pygame.font.SysFont(None, 64)
    text = FONT.render('Hello World', False, pygame.Color('darkorange'))
    text_rect = text.get_rect(center=(150, 50))

    box = pygame.Surface((text_rect.width + 20, text_rect.height + 20))
    box.fill((201, 60, 60))  # Fill the box with black color
    box_rect = box.get_rect(center=text_rect.center)

    clock = pygame.time.Clock()
    alpha = 0

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if alpha < 255:
            alpha += 5  # Adjust the increment value as needed

        box.set_alpha(alpha)
        text.set_alpha(alpha)

        screen.fill(pygame.Color('dodgerblue'))
        screen.blit(box, box_rect)
        screen.blit(text, text_rect)

        clock.tick(120)
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    main()