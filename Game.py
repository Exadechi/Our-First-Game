import pygame
import Assets
import sys
from Wizard import Wizard
from pytmx import *


class Game():
    def __init__(self):
        # Initializing pygame
        pygame.init()

        # Create a clock to keep track of time / since when pygame was initialized
        self.clock = pygame.time.Clock()
        self.delta = self.clock.get_time()

        self.infoObject = pygame.display.Info()
        self.screen = pygame.display.set_mode((self.infoObject.current_w, self.infoObject.current_h), pygame.FULLSCREEN)

        self.wizard = Wizard()

        # Setting the name of the window
        pygame.display.set_caption("Dungeon Crawler")

    def run(self):

        self.checkIfQuit()
        self.updateTime()
        self.setScreenOffset()
        self.drawMap(32, Assets.tmx_ground, Assets.tmx_wall, self.wDrawOffset, self.hDrawOffset)
        self.drawAllSprites()
        self.drawPlayerSprites()
        self.updateAll()

        pygame.display.flip()

    def drawMap(self, tmx_tilesize, tmx_ground_layer, tmx_wall_layer, wDrawOffset, hDrawOffset):

        self.screen.fill([0, 0, 0])

        for x, y, image in tmx_ground_layer.tiles():
            self.screen.blit(image, (x * tmx_tilesize + wDrawOffset, y * tmx_tilesize + hDrawOffset))
        for x, y, image in tmx_wall_layer.tiles():
            self.screen.blit(image, (x * tmx_tilesize + wDrawOffset, y * tmx_tilesize + hDrawOffset))

    def createMapRects(self, tmx_map, tmx_wall_layer_name, tmx_wall_layer_tileset, tmx_wall_layer_gid):

        self.tmx_walls = util_pygame.build_rects(tmx_map, tmx_wall_layer_name, tileset=tmx_wall_layer_tileset,
                                                 real_gid=tmx_wall_layer_gid)

    def checkIfQuit(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                sys.exit()

    def drawAllSprites(self):

        for sprite in Assets.allGroup:
            self.screen.blit(sprite.image, (sprite.rect.x + self.wDrawOffset, sprite.rect.y + self.hDrawOffset))

    def drawPlayerSprites(self):

        self.screen.blit(self.wizard.image,
                         (self.wHalf - self.wizard.rect.width / 2, self.hHalf - self.wizard.rect.height / 2))

    def updateTime(self):

        self.clock.tick(200)
        self.delta = self.clock.get_time()

    def updateAll(self):

        Assets.allGroup.update(self.delta)
        self.wizard.update(self.delta)

    def setScreenOffset(self):

        self.wHalf = self.infoObject.current_w / 2
        self.hHalf = self.infoObject.current_h / 2

        self.wDrawOffset = -self.wizard.rect.centerx + self.wHalf
        self.hDrawOffset = -self.wizard.rect.centery + self.hHalf


# while True:
#     clock.tick(140)
#     delta = clock.get_time()
#     screen.fill([0, 0, 0])
#     allGroup.add(allyProjectileGroup, enemyProjectileGroup)
#
#     wHalf = infoObject.current_w / 2
#     hHalf = infoObject.current_h / 2
#     wDrawOffset = -wizard.rect.centerx + wHalf
#     hDrawOffset = -wizard.rect.centery + hHalf
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
#             sys.exit()
#
#     for fireball in allyProjectileGroup.sprites():
#         for enemy in charGroup.sprites():
#             if pygame.sprite.collide_rect(fireball, enemy):
#                 fireball.kill()
#                 enemy.health -= 1
#                 if enemy.health == 0:
#                     enemy.kill()
#                     pygame.mixer.Sound.play(fart)
#                     enemy = Enemy()
#                     charGroup.add(enemy)
#
#     for projectile in ProjectileGroup.sprites():
#         for rects in tmx_rects:
#             if projectile.rect.colliderect(rects):
#                 projectile.kill()
#     # for projectile in enemyProjectileGroup.sprites():
#     #    projectile.image = projectile.original
#     #    pygame.transform.rotate(projectile.image, 20)
#     for x, y, image in tmx_ground.tiles():
#         screen.blit(image, (x * 32 + wDrawOffset, y * 32 + hDrawOffset))
#     for x, y, image in tmx_wall.tiles():
#         screen.blit(image, (x * 32 + wDrawOffset, y * 32 + hDrawOffset))
#     allGroup.update(delta)
#     charGroup.update(delta)
#
#     for sprite in allGroup:
#         screen.blit(sprite.image, (sprite.rect.x + wDrawOffset, sprite.rect.y + hDrawOffset))
#
#     for enemy in charGroup:
#         enemy.drawHealth(screen, enemy.rect.centerx + wDrawOffset, enemy.rect.centery + hDrawOffset + 60)
#         screen.blit(enemy.image, (enemy.rect.x + wDrawOffset, enemy.rect.y + hDrawOffset))
#
#     ProjectileGroup.add(allyProjectileGroup, enemyProjectileGroup)
#     wizard.update(delta)
#     screen.blit(wizard.image, (wHalf - wizard.rect.width / 2, hHalf - wizard.rect.height / 2))
#     pygame.display.flip()
#
game = Game()

while True:
    game.run()
