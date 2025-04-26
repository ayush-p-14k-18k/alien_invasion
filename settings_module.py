
class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = ((0,0,0))  # White background
        self.ship_speed = 1.5

        # bullet settings
        self.bullet_speed = 2.0
        self.bullet_height = 15
        self.bullet_width = 3
        self.bullet_color = (255,0,0)
        self.bullet_allowed_in_group = 5

        #Alien settings 
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        #fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1



        