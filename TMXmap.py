import Assets
import pygame
import random
from Wizard import Wizard
from pytmx import *

class TMXmap():

    def __init__(self):
        self.tmxMapSpawn = util_pygame.load_pygame('SpawnRoom.tmx')
        self.tmxMapEnd = util_pygame.load_pygame('ExitRoom.tmx')
        self.tmxCompleteMap = []
        self.tmxCompleteMap.append(self.tmxMapSpawn)
        self.tmxCompleteMap.append(self.tmxMapEnd)
        self.tmxRoomCount = 5
        self.tmxMapRooms = []
        self.tmxCurrentRoomExit = None
        currentRoomCounter = 0
        
        for i in range(self.tmxRoomCount):
            currentRoom = util_pygame.load_pygame('Room' + str(i + 1) + '.tmx')
            self.tmxMapRooms.append(currentRoom)
            self.tmxCompleteMap.append(currentRoom)
        for x, y, image in self.tmxMapSpawn.get_layer_by_name('Room Exit').tiles():
            self.tmxCurrentRoomExit = (x, y)

    def spawnPlayer(self, tmx_tilesize):

        self.wizardXSpawnMin = 1000
        self.wizardXSpawnMax = 0
        self.wizardYSpawnMin = 1000
        self.wizardYSpawnMax = 0

        for x, y, image in Assets.tmx_player_spawn.tiles():
            if x > self.wizardXSpawnMax:
                self.wizardXSpawnMax = x
            if x < self.wizardXSpawnMin:
                self.wizardXSpawnMin = x
            if y < self.wizardYSpawnMin:
                self.wizardYSpawnMin = y
            if y > self.wizardYSpawnMax:
                self.wizardYSpawnMax = y

        self.wizardXSpawn = random.randrange(self.wizardXSpawnMin, self.wizardXSpawnMax) * tmx_tilesize
        self.wizardYSpawn = random.randrange(self.wizardYSpawnMin, self.wizardYSpawnMax) * tmx_tilesize

        return (self.wizardXSpawn, self.wizardYSpawn)

    def spawnEnemies(self, tmx_enemy_layer):

        pass

    def drawMap(self, screen, tmx_tilesize, tmx_ground_layer, tmx_wall_layer, screenW, screenH, wDrawOffset, hDrawOffset):
        """
        Have to find a way to make it draw the ground layer of each tmx map first
        then draw the wall tiles of every tile map
        then spawn enemies
        to constantly generate rooms

        :param screen:
        :param tmx_tilesize:
        :param tmx_ground_layer:
        :param tmx_wall_layer:
        :param screenW:
        :param screenH:
        :param wDrawOffset:
        :param hDrawOffset:
        :return:
        """
        screen.fill([0, 0, 0])
        self.screenArea = pygame.Rect(
            -wDrawOffset - tmx_tilesize,
            -hDrawOffset - tmx_tilesize,
            screenW + tmx_tilesize,
            screenH + tmx_tilesize)

        self.tmxCurrentRoomExit = (self.tmxCurrentRoomExit[0] + tmx_tilesize, self.tmxCurrentRoomExit[1])

        for x, y, image in tmx_ground_layer.tiles():

            # Checking if the tile is on screen for optimization
            if self.screenArea.collidepoint(x * tmx_tilesize, y * tmx_tilesize):
                screen.blit(
                    image,
                    (x * tmx_tilesize + wDrawOffset,
                     y * tmx_tilesize + hDrawOffset)
                )

        for x, y, image in tmx_wall_layer.tiles():

            # Checking if the tile is on screen for optimization
            if self.screenArea.collidepoint(x * tmx_tilesize, y * tmx_tilesize):
                screen.blit(
                    image,
                    (x * tmx_tilesize + wDrawOffset,
                     y * tmx_tilesize + hDrawOffset)
                )


    def createMapRects(self, tmx_map, tmx_wall_layer_name, tmx_wall_layer_tileset, tmx_wall_layer_gid):
        """
        Create all the rects for the map
        """
        self.tmx_walls = util_pygame.build_rects(
            tmx_map,
            tmx_wall_layer_name,
            tileset=tmx_wall_layer_tileset,
            real_gid=tmx_wall_layer_gid
            )