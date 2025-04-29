
import pygame

class Ship:
    """A class to manage the ship."""

    def __init__(self, a_game):
        """Initialize the ship and set its starting position."""
        self.screen = a_game.screen
        self.settings = a_game.settings
        self.screen_rect = a_game.screen.get_rect()
        
        # Load the ship image and get its rect.
        self.image = pygame.image.load(r"C:\Users\aryan\OneDrive\Desktop\python game\alien_invasion\spaceship (2).png")
        self.rect = self.image.get_rect()  

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom 
        
        # store a float value for for ships position.
        self.x = float(self.rect.x)

        # Set the ship's initial position.
        self.move_right = False
        self.move_left = False    

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
    
    def motion(self):
        '''moves the ship in x direction.'''
        # update ship's x value and not rect.
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.move_left and self.rect.left > 0 :
            self.x -= self.settings.ship_speed
        # update rect object from self.x
        self.rect.x = self.x
