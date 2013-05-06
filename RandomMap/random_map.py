#===============================================================================
# Create a random map
#===============================================================================

import sys
import pygame
from pygame.locals import *
import time

#Map generation techniques
from _map_generating_methods.hill_algorithm import * #@UnusedWildImport
from _map_generating_methods.particle_deposition import * #@UnusedWildImport
from _map_generating_methods.sparks import * #@UnusedWildImport
from _map_generating_methods.value_noise import * #@UnusedWildImport
from _map_generating_methods.diamond_square import * #@UnusedWildImport


#Init
WHITE = (255,255,255)
BLACK = (0,0,0)
WATER = (0,148,255)
DEEPWATER = (0,0,255)
SAND = (255,178,127)
GRASS = (0,255,0)
FORREST = (0,127,14)
STONE = (64,64,64)

GAME_WIDTH = 512
GAME_HEIGHT = 512

SCALING = 1 #The size of the generated map


#------------------------------------------------------------------------------ 
# Classes
class Tiles(pygame.sprite.Sprite):
    
    def __init__(self, start_x, start_y, color):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface([SCALING, SCALING])
        self.image.fill(color)
 
        self.rect = pygame.rect.Rect([start_x*SCALING,start_y*SCALING],self.image.get_size())



pygame.init()

#Screen
screen = pygame.display.set_mode([GAME_WIDTH,GAME_HEIGHT],0,32) #Size,full_screen,colors #pygame.FULLSCREEN,32 needed?
pygame.display.set_caption('Best Map-generator Ever!')

#No cursor
pygame.mouse.set_visible(0)

#Sprites
background = pygame.sprite.Group()


#coordinates = Sparks(GAME_WIDTH/SCALING,GAME_HEIGHT/SCALING)
#coordinates = ParticleDeposition(GAME_WIDTH/SCALING,GAME_HEIGHT/SCALING)
#coordinates = HillAlgorithm(GAME_WIDTH/SCALING,GAME_HEIGHT/SCALING)
#coordinates = HillAlgorithm_mod(GAME_WIDTH/SCALING,GAME_HEIGHT/SCALING)
#coordinates = ValueNoise2(GAME_WIDTH/SCALING,GAME_HEIGHT/SCALING)
coordinates = DiamondSquare(513) #The size has to be 2^n+1


#print coordinates

for item in coordinates:
    
    #Begin with the highest to simplify the >= x <=
    if item[2] > 160:
        color = STONE
    elif item[2] > 120:
        color = FORREST
    elif item[2] > 100:
        color = GRASS
    elif item[2] > 90:
        color = SAND
    elif item[2] > 80:
        color = WATER
    else:
        color = DEEPWATER
    
    #tile = Tiles(item[0],item[1],(item[2],item[2],item[2]))
    tile = Tiles(item[0],item[1],color)
    background.add(tile)


#------------------------------------------------------------------------------ 
# Game loop
clock = pygame.time.Clock()

done = False
while done == False:
    #------------------------------------------------------------------------------ 
    # Handle events
    for event in pygame.event.get():
        #Stop the program when the user closes the window or hits escape
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): 
            done = True
            pygame.quit()
            sys.exit()
    
    #Movements
    #foreground.update()
    
    #------------------------------------------------------------------------------ 
    # Draw the game state to the screen
    
    #Clear the screen
    screen.fill(WHITE)
    
    #Draw sprites
    background.draw(screen)
    
    pygame.display.update()
    
    clock.tick(60)