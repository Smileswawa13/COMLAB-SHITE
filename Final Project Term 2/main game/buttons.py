# Module for the buttons of the game
import pygame

# Kato ni daan na button wala na gamit karun
class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        try:
            self.image = image
            self.x_pos = pos[0]
            self.y_pos = pos[1]
            self.font = font
            self.base_color, self.hovering_color = base_color, hovering_color
            self.text_input = text_input
            self.text = self.font.render(self.text_input, True, self.base_color)
            if self.image is None:
                self.image = self.text
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
            self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        except Exception as e:
            print(f"Error initializing Button: {e}")

    def update(self, screen):
        try:
            if self.image is not None:
                screen.blit(self.image, self.rect)
            screen.blit(self.text, self.text_rect)
        except Exception as e:
            print(f"Error updating Button: {e}")

    def checkForInput(self, position):
        try:
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                return True
            return False
        except Exception as e:
            print(f"Error checking for input: {e}")
            return False

    def changeColor(self, position):
        try:
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                self.text = self.font.render(self.text_input, True, self.hovering_color)
            else:
                self.text = self.font.render(self.text_input, True, self.base_color)
        except Exception as e:
            print(f"Error changing color: {e}")

# Kato ni na button gamit karun
class ImageButton:
    def __init__(self, image, pos):
        self.image = image
        self.original_image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        screen.blit(self.image, self.rect)

    def check_for_input(self, position):
        return self.rect.collidepoint(position)

    def change_size_on_hover(self, position):
        if self.rect.collidepoint(position):
            self.image = pygame.transform.scale(self.original_image,
                (int(self.original_image.get_width() * 0.95), int(self.original_image.get_height() * 0.95)))
        else:
            self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))