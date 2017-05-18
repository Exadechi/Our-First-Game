import pygame
from pytmx import *

pygame.init()

# Gets the total width and height of the display in pixels and creates a fullscreen display
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
wHalf = infoObject.current_w / 2
hHalf = infoObject.current_h / 2

# Loading a fart sound effect
fart = pygame.mixer.Sound('fart.wav')

wizardHorizontal = pygame.image.load('NewWizard.png')
wizardUpward = pygame.image.load('NewWizard3.png')
wizardDownward = pygame.image.load('NewWizard2.png')
fireballImage = pygame.image.load('Fireball.png')

# Loading the tmxmap containing all of the tiles
tmx_map = util_pygame.load_pygame("WizardTileEnlarged.tmx")


# The names of the ground and wall layers
tmx_ground_name = 'Ground'
tmx_wall_name = 'Walls'
tmx_tileset = 'WizardTilesEnlarged'
tmx_wall_gid = 4

# Getting both the layer containing the ground tiles you can walk on, and the wall tiles you cannot, respectively
tmx_ground = tmx_map.get_layer_by_name(tmx_ground_name)
tmx_wall = tmx_map.get_layer_by_name(tmx_wall_name)


# Creating the rectangles for collision with the walls
tmx_rects = util_pygame.build_rects(tmx_map, tmx_wall_name, tileset=tmx_tileset, real_gid=tmx_wall_gid)


# These are the various sprite groups;
"""
charGroup contains the players (wizard)
allyProjectileGroup contains friendly projectiles
ProjectileGroup contains the enemy projectiles
allGroup contains all sprites, for smooth rendering
"""
charGroup = pygame.sprite.LayeredUpdates()
allyProjectileGroup = pygame.sprite.Group()
enemyProjectileGroup = pygame.sprite.Group()
ProjectileGroup = pygame.sprite.Group()
allGroup = pygame.sprite.LayeredUpdates()

#class Assets():
#    def images(self):


