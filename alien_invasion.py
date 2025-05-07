import sys
import random
from time import sleep
import pygame
from settings_module import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship_module import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.bg_image = pygame.image.load(r"C:\Users\anike\OneDrive\Desktop\python\background12.jpg")
        self.bg_image = pygame.transform.scale(self.bg_image, (self.settings.screen_width, self.settings.screen_height))

        # for full screen the game display
        #caution: make sure to comment out the line just below these 3 codes to run it cleanly. 
        '''
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        '''
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("__<>__Alien Inv@sion__<>__")
        ## Create an instance to store game statistics.
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group() 
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        #Start Alien Invasion in an active state.
        self.game_active = False

        # Make the Play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
               self.ship.motion()
               self._update_bullets()
               self._update_aliens()
            self._update_screen()
            self.clock.tick(60)  # 60 fps 
            
    def _check_events(self):
        '''respond to keypresses and mouse events'''        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)               
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
        
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks paly."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True 
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.move_right = True
        if event.key == pygame.K_LEFT:
            self.ship.move_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.move_right = False
        if event.key == pygame.K_LEFT:
            self.ship.move_left = False

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        #self.screen.fill(self.settings.bg_color)  # Fill the screen with a color
        self.screen.blit(self.bg_image, (0, 0))


        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()
        
        self.ship.blitme()
        pygame.display.flip()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()
        
        ''' delete old bullets'''
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # uncomment to see how many bullets are on the screen
        # but remember to comment out the line below because it will slow down the game as it will print the number of bullets on the screen every frame.
        #print((len(self.bullets)))

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
            """Respond to bullet-alien collisions."""
            # Remove any bullets and aliens that have collided.
            # Check for any bulletsthat have hit aliens.
            #If so,get rid of the bullet and the alien.
            collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)

            if collisions:
                for aliens in collisions.values():
                    self.stats.score += self.settings.alien_points * len(aliens)
                    self.sb.prep_score()
                self.stats.score += self.settings.alien_points
                self.sb.prep_score()
                self.sb.check_high_score()

            if not self.aliens:
               # Destroy existing bullets and create a new fleet.
                self.bullets.empty()
                self._create_fleet()
                self.settings.increase_speed()

                # Increase level.
                self.stats.level += 1
                self.sb.prep_level()
    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullet_allowed_in_group:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Make an alien.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        max_aliens_x = available_space_x // (2 * alien_width)

        # random number of aliens in a row(at least 3)
        number_aliens_x = random.randint(3, max_aliens_x)

        #Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #random number of rows of aliens(at least 2)
        number_rows = random.randint(2, number_rows)
        
        #Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
    
    def _create_alien(self, alien_number,row_number):
        """Create an alien and place it in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break 

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
        then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()
        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()    

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Get rid of any remaining aliens and bullets.
            self.bullets.empty()
            self.aliens.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            # Pause.
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
                    
    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)  

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break
        
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()            
    #ai.screen.fill(ai.bg_color)
    #ai.screen.fill((230, 230, 230))