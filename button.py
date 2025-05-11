import pygame
import pygame.font 

class Button:
    """A class to create a button."""

    def __init__(self, ai_game, msg = None):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #Loadd and scale the button image
        self.image = pygame.image.load(r"C:\Users\ayush\OneDrive\Desktop\game project\alien_invasion\images\Screenshot 2025-05-11 154852.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center

    def draw_button(self):
        """Draw blank button and then draw the message."""
        self.screen.blit(self.image, self.rect)