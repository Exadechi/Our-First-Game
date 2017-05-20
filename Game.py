import pygame
import Assets
import sys
import random
from Wizard import Wizard
from Enemy import Enemy
from pytmx import *


class Game():
    def __init__(self):
        # Initializing pygame
        pygame.init()

        # Create a clock to keep track of time / since when pygame was initialized
        self.clock = pygame.time.Clock()
        self.delta = self.clock.get_time()

        # Get display info and make a fullscreen window
        self.infoObject = pygame.display.Info()
        self.screen = pygame.display.set_mode((self.infoObject.current_w, self.infoObject.current_h), pygame.FULLSCREEN)

        # Create an instance of a wizard
        self.spawnPlayer()

        # Setting the name of the window
        pygame.display.set_caption("Dungeon Crawler")

        self.spawnEnemies(32)

        # A function to show the startup screen (currently empty)
    def startScreen(Rself):
        pass

    # The function used to run the game
    def run(self):

        self.checkIfQuit()
        self.updateTime()
        self.setScreenOffset()
        self.drawMap(32, Assets.tmx_ground, Assets.tmx_walls, self.wDrawOffset, self.hDrawOffset)
        self.enemiesShoot(self.wizard.rect.center)
        self.drawAllSprites()
        self.drawHealth()
        self.updateAll()

        # Update the screen display to the new changes made this frame
        pygame.display.flip()

    # Draw the tile images
    def drawMap(self, tmx_tilesize, tmx_ground_layer, tmx_wall_layer, wDrawOffset, hDrawOffset):

        self.screen.fill([0, 0, 0])
        self.screenArea = pygame.Rect(
            -wDrawOffset - tmx_tilesize,
            -hDrawOffset - tmx_tilesize,
            self.infoObject.current_w + tmx_tilesize,
            self.infoObject.current_h + tmx_tilesize)

        for x, y, image in tmx_ground_layer.tiles():

            # Checking if the tile is on screen for optimization
            if self.screenArea.collidepoint(x * tmx_tilesize, y * tmx_tilesize):
                self.screen.blit(image,
                             (x * tmx_tilesize + wDrawOffset,
                              y * tmx_tilesize + hDrawOffset))

        for x, y, image in tmx_wall_layer.tiles():

            # Checking if the tile is on screen for optimization
            if self.screenArea.collidepoint(x * tmx_tilesize, y * tmx_tilesize):
                self.screen.blit(image,
                             (x * tmx_tilesize + wDrawOffset,
                              y * tmx_tilesize + hDrawOffset))
        """
        Create a method that takes in the width and height of the screen,
        then checks which tiles are in range of the player and only blits
        those to reduce the currently high amount of lag
        """

    # Create all the rects for the map
    def createMapRects(self, tmx_map, tmx_wall_layer_name, tmx_wall_layer_tileset, tmx_wall_layer_gid):

        self.tmx_walls = util_pygame.build_rects(
            tmx_map,
            tmx_wall_layer_name,
            tileset=tmx_wall_layer_tileset,
            real_gid=tmx_wall_layer_gid)

    # Check if the user has given input to quit
    def checkIfQuit(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                sys.exit()

    # Draw all sprites according to the current offset (including player)
    def drawAllSprites(self):

        for sprite in Assets.allGroup:
            self.screen.blit(
                sprite.image,
                (sprite.rect.x + self.wDrawOffset,
                sprite.rect.y + self.hDrawOffset)
            )

        self.screen.blit(
            self.wizard.image,
            (self.wHalf - self.wizard.rect.width / 2,
            self.hHalf - self.wizard.rect.height / 2)
            )

    def drawHealth(self):
        for enemy in Assets.enemyGroup:
            enemy.drawHealth(self.screen, enemy.rect.centerx + self.wDrawOffset, enemy.rect.centery + self.hDrawOffset + 60)

        self.wizard.drawHealth(self.screen, self.wizard.rect.centerx + self.wDrawOffset, self.wizard.rect.centery + self.hDrawOffset + 60)

    # Update the game clock
    def updateTime(self):

        self.clock.tick(60)
        self.delta = self.clock.get_time()

    # Run the update function for all sprites
    def updateAll(self):

        Assets.allGroup.update(self.delta)

    # Get the new frame's screen offset according to the wizard position
    def setScreenOffset(self):

        self.wHalf = self.infoObject.current_w / 2
        self.hHalf = self.infoObject.current_h / 2

        self.wDrawOffset = -self.wizard.rect.centerx + self.wHalf
        self.hDrawOffset = -self.wizard.rect.centery + self.hHalf

    # Spawn an instance of an enemy
    def spawnEnemies(self, tile_size):

        for x, y, image in Assets.tmx_enemy_spawns.tiles():
            enemy = Enemy(x * tile_size, y * tile_size)
            enemy.add(Assets.enemyGroup, Assets.allGroup)

    def spawnPlayer(self):

        self.wizardXSpawnMin = 1000
        self.wizardXSpawnMax = 0
        self.wizardYSpawnMin = 1000
        self.wizardYSpawnMax = 0

        for x, y, image in Assets.tmx_player_spawn.tiles():
            if x > self.wizardXSpawnMax:
                self.wizardXSpawnMax = x
            if x < self.wizardXSpawnMin:
                self.wizardXSpawnMin = x
            if y > self.wizardYSpawnMax:
                self.wizardYSpawnMax = y
            if y < self.wizardYSpawnMin:
                self.wizardYSpawnMin = y

        self.wizardXSpawn = random.randrange(self.wizardXSpawnMin, self.wizardXSpawnMax)
        self.wizardYSpawn = random.randrange(self.wizardYSpawnMin, self.wizardYSpawnMax)

        self.wizard = Wizard(self.wizardXSpawn * 32, self.wizardYSpawn * 32)

        """
        get x min spawn
        get x max spawn
        get y min spawn
        get y max spawn

        randomize both

        use these coords to spawn wizard
        """

    def enemiesShoot(self, wizardPos):

        for enemy in Assets.enemyGroup:
            enemy.shootProjectiles(wizardPos)


# Create the game
game = Game()

# Show game startup
game.startScreen()

# Run the game
while True:
    game.run()
