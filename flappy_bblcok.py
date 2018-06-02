import math
import pygame
import random
 
# Global constants
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

 
 
class Player(pygame.sprite.Sprite):
    """
    This class represents the bar at the bottom that the player controls.
    """
 
    # -- Methods
    def __init__(self):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        
        width = 30
        height = 30
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
        
        # score
        self.distTraveled = 25
        self.score = 0
         
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
        
        
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None
 
    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x
        self.distTraveled += self.change_x
        self.score = math.floor(self.distTraveled / 300)
        colorID = random.randrange(0, 3, 1)
        if colorID == 0:
            color = RED
        elif colorID == 1:
            color = WHITE
        else:
            color = GREEN
        self.image.fill(color)
        
        # See if we hit anything
        

        
        
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
       
        # if len(block_hit_list) > 0:
        #    font = pygame.font.SysFont('Calibri', 25, True, False)
        #    text = font.render("BETTER LUCK NEXT TIME",True,RED)
        #    screen.blit(text, [250, 250])
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.65
 
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working w
 
        # If it is ok to jump, set our speed upwards
    
        self.change_y = -7
 
    # Player-controlled movement:
    
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 3
 
    
 
 
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
 
        self.rect = self.image.get_rect()
    
 
class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
 
        # How far this world has been scrolled left/right
        self.world_shift = 0
 
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        screen.fill(BLUE)
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
 
    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """
 
        # Keep track of the shift amount
        self.world_shift += shift_x
 
        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
 
        
 
 
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        self.level_limit = -1000
 

        # Array with width, height, x, and y of platform

        first_x = 400
        height_wall = 0
        x_wall=700
        level=[]
        first_tube1 = [50, 250, first_x, 0]
        first_tube2 = [50, 500-250, first_x, 100+250]
        level.append(first_tube1)
        level.append(first_tube2)
        for i in range(50):
            height_wall = random.randrange(75, 425, 1)
            green_tube1 = [50, height_wall, x_wall, 0]
            green_tube2 = [50, 500-height_wall, x_wall, 100+height_wall]
            level.append(green_tube1)
            level.append(green_tube2)
            x_wall += 300
     
        
                 
                 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
 
 

 
 
def main():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    
    pygame.display.set_caption("Flappy Block")
 
    # Create the player
    player = Player()
 
    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))
    
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    player.rect.x = 100
    player.rect.y = 400
    active_sprite_list.add(player)
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
            player.go_right()
            if event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_LEFT:
                    # player.go_left()
                
                if event.key == pygame.K_UP:
                    player.jump()
 
         
            
        # Update the player.
        active_sprite_list.update()
 
        # Update items in the level
        current_level.update()

        block_hit_list = pygame.sprite.spritecollide(player, player.level.platform_list, False)
        if len(block_hit_list) > 0:
            break
         
 
        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)  
 
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        
        colorID = random.randrange(0, 3, 1)
        if colorID == 0:
            color = RED
        elif colorID == 1:
            color = WHITE
        else:
            color = GREEN
            
        font = pygame.font.SysFont('Arial', 40, True, False)
        text = font.render(str(player.score),True,color)
        screen.blit(text, [20, 20])

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    # Select the font to use, size, bold, italics
    font = pygame.font.SysFont('Arial', 25, True, False)
     
    # Render the text. "True" means anti-aliased text.
    # Black is the color. The variable BLACK was defined
    # above as a list of [0, 0, 0]
    # Note: This line creates an image of the letters,
    # but does not put it on the screen yet.
    text = font.render("CLICK SPACE TO RESTART, YOUR SCORE IS:" + str(player.score),True,color)
    
    
 
# Put the image of the text on the screen at 250x250
    screen.blit(text, [70, 300])
    
    pygame.display.flip()
    
if __name__ == "__main__":
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                main()
            elif event.type == pygame.QUIT:
                pygame.quit()
            
        
