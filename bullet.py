
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''to manage the bullet fired by the ship'''

    def __init__(self, ai_game):
        '''create a bullet object at the ship's current position'''

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # create a bullet rect at (0, 0) and set the correct position
        self.image = pygame.image.load(r"C:\Users\anike\OneDrive\Desktop\bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.ship.rect.midtop

        # store the bullet's position as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        '''move the bullet up the screen'''

        # update the decimal position of the bullet
        self.y -= self.settings.bullet_speed
        # update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        '''draw the bullet on the screen'''
        self.screen.blit(self.image, self.rect)  