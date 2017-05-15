import pygame, Assets, sys, random, os, math

#Initializing pygame
pygame.init()

class Game():

    #Gets the total width and height of the display in pixels and creates a fullscreen display
    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)

    #Create a clock to keep track of time / since when pygame was initialized
    clock = pygame.time.Clock()

