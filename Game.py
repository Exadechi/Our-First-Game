import pygame
import Assets
import sys
import random
from Wizard import Wizard
from Enemy import Enemy
from pytmx import *
from TMXmap import TMXmap


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
        pygame.display.set_icon(Assets.fireballImage)

        #Cre
        self.tmxMap = TMXmap()

        # Create an instance of a wizard
        self.spawnPlayer(32)

        # Spawn all the enemies
        self.spawnEnemies(32)

        # Setting the name of the window
        pygame.display.set_caption("Dungeon Crawler")

    def startScreen(self):
        """
        A function to show the startup screen (currently empty)
        """

        pass

    def run(self):
        """
        The function used to run the game
        """

        self.checkIfQuit()

        self.updateTime(self.clock)

        self.setScreenOffset(self.infoObject.current_w,
                             self.infoObject.current_h,
                             self.wizard.rect.centerx,
                             self.wizard.rect.centery)

        self.drawMap(self.screen,
                     32,
                     Assets.tmx_ground,
                     Assets.tmx_walls,
                     self.infoObject.current_w,
                     self.infoObject.current_h,
                     self.wDrawOffset,
                     self.hDrawOffset)

        self.enemiesShoot((self.wizard.rect.centerx,
                           self.wizard.rect.centery))

        self.drawAllSprites(self.screen,
                            Assets.allGroup)

        self.drawHealth(self.screen, Assets.enemyGroup, self.wizard)

        self.updateAll(Assets.allGroup, self.delta)

        # Update the screen display to the new changes made this frame
        pygame.display.flip()

    def checkIfQuit(self):
        """
        Check if the user has given input to quit
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                sys.exit()

    def updateTime(self, clock):
        """
        Update the game clock
        :param clock:
        :return:
        """

        clock.tick(60)
        self.delta = self.clock.get_time()

    def setScreenOffset(self, screenW, screenH, wizardX, wizardY):
        """
        Get the new frame's screen offset according to the wizard position
        :param screenW:
        :param screenH:
        :param wizardX:
        :param wizardY:
        :return:
        """

        self.wHalf = screenW / 2
        self.hHalf = screenH / 2

        self.wDrawOffset = -wizardX + self.wHalf
        self.hDrawOffset = -wizardY + self.hHalf

    def drawMap(self, screen, tmx_tilesize, tmx_ground_layer, tmx_wall_layer, screenW, screenH, wDrawOffset, hDrawOffset):
        """
        Draw the tile images
        """

        self.tmxMap.drawMap(screen, tmx_tilesize, tmx_ground_layer, tmx_wall_layer, screenW, screenH, wDrawOffset, hDrawOffset)
        # screen.fill([0, 0, 0])
        # self.screenArea = pygame.Rect(
        #     -wDrawOffset - tmx_tilesize,1
        #     -hDrawOffset - tmx_tilesize,
        #     screenW + tmx_tilesize,
        #     screenH + tmx_tilesize)
        #
        # for x, y, image in tmx_ground_layer.tiles():
        #
        #     # Checking if the tile is on screen for optimization
        #     if self.screenArea.collidepoint(x * tmx_tilesize, y * tmx_tilesize):
        #         screen.blit(
        #             image,
        #             (x * tmx_tilesize + wDrawOffset,
        #              y * tmx_tilesize + hDrawOffset)
        #             )
        #
        # for x, y, image in tmx_wall_layer.tiles():
        #
        #     # Checking if the tile is on screen for optimization
        #     if self.screenArea.collidepoint(x * tmx_tilesize, y * tmx_tilesize):
        #         screen.blit(
        #             image,
        #             (x * tmx_tilesize + wDrawOffset,
        #              y * tmx_tilesize + hDrawOffset)
        #         )
        """
        Create a method that takes in the width and height of the screen,
        then checks which tiles are in range of the player and only blits
        those to reduce the currently high amount of lag
        """

    def enemiesShoot(self, wizardPos):
        """
        Make all enemies shoot
        :param wizardPos:
        :return:
        """

        for enemy in Assets.enemyGroup:
            enemy.shootProjectiles(wizardPos)

    def drawAllSprites(self, screen, allGroup):
        """
        Draw all sprites according to the current offset (including player)
        :param screen:
        :param allGroup:
        :return:
        """

        for sprite in allGroup:
            screen.blit(
                sprite.image,
               (sprite.rect.x + self.wDrawOffset,
                sprite.rect.y + self.hDrawOffset)
            )

        screen.blit(
            self.wizard.image,
           (self.wHalf - self.wizard.rect.width / 2,
            self.hHalf - self.wizard.rect.height / 2)
            )

    def drawHealth(self, screen, enemyGroup, wizard):
        """
        A function to draw all healthbars
        :param screen:
        :param enemyGroup:
        :param wizard:
        :return:
        """

        for enemy in enemyGroup:
            enemy.drawHealth(
                screen,
                enemy.rect.centerx + self.wDrawOffset,
                enemy.rect.centery + self.hDrawOffset + 60)

        wizard.drawHealth(
            self.screen,
            10,
            10)

    def updateAll(self, allGroup, delta):
        """
        Run the update function for all sprites
        :param allGroup:
        :param delta:
        :return:
        """

        allGroup.update(delta)

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

    def spawnEnemies(self, tile_size):
        """
        Spawn all enemies at the tmx_enemy_spawn tiles
        :param tile_size:
        :return:
        """

        for x, y, image in Assets.tmx_enemy_spawns.tiles():
            enemy = Enemy(x * tile_size, y * tile_size)
            enemy.add(Assets.enemyGroup, Assets.allGroup)

    def spawnPlayer(self, tmx_tilesize):
        """
        Spawn a instance of the wizard
        :param tmx_tilesize:
        :return:
        """

        self.tmxMap.spawnPlayer(tmx_tilesize)

        self.wizard = Wizard(self.tmxMap.spawnPlayer(tmx_tilesize))

        """
        get x min spawn
        get x max spawn
        get y min spawn
        get y max spawn

        randomize both

        use these coords to spawn wizard
        SOLVED
        """

    # A function to make all enemies shoot

# Create the game
game = Game()

# Show game startup
game.startScreen()

# Run the game
while True:
    game.run()
