import pygame
import Assets
from Vector import Vector


class EnemyProjectile(pygame.sprite.Sprite):

    def __init__(self, enemyX, enemyY, wizardPos, rotation):
        pygame.sprite.Sprite.__init__(self)
        self.image = Assets.enemyProjectileImage
        self.original = self.image
        self.image = pygame.transform.rotate(self.image, 30)
        self.position = (enemyX, enemyY)
        self.speed = 0.5
        self.rect = self.image.get_rect(center=self.position)
        self._layer = 2
        self.inc = (Vector((wizardPos[0] - enemyX, wizardPos[1] - enemyY)).normalized()).rotated(rotation)
        self.inc_rotate = (Vector(wizardPos[0] - enemyX, -(wizardPos[1] - enemyY)).normalized()).rotated(-rotation)
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.spawn_time = pygame.time.get_ticks()
        self.rotate_time = 10
        self.fireball_lifetime = 500
        self.damage = 10

    def update(self, delta):
        pygame.sprite.Sprite.update(self)

        # Moving the projectile for the next frame
        self.rect.center += self.inc * self.speed * delta

        # Copying the old rectangle of the fireball for later collision detection
        oldRect = self.rect

        # Getting the current time
        self.now = pygame.time.get_ticks()

        # Checking whether to kill the fireball
        if self.now - self.spawn_time > self.fireball_lifetime:
            self.kill()

        # Checking for collision with a wall
        for wall in Assets.tmx_rects:

            # Copy oldRect
            xRect = oldRect.move(0, 0)
            yRect = oldRect.move(0, 0)
            xRect.centerx = self.rect.centerx
            yRect.centery = self.rect.centery

            if xRect.colliderect(wall):
                self.kill()
            if yRect.colliderect(wall):
                self.kill()