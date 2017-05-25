import pygame
import Assets
import random
from Vector import Vector

class Fireball(pygame.sprite.Sprite):

    def __init__(self, wizardX, wizardY, mousePos):
        pygame.sprite.Sprite.__init__(self)
        self.image = Assets.fireballImage
        self.position = (wizardX, wizardY)
        self.add(Assets.allGroup, Assets.allyProjectileGroup, Assets.ProjectileGroup)
        self.speed = 0.75
        self.rect = self.image.get_rect(center=self.position)
        self.damage = random.randrange(5, 20)
        self._layer = 2
        self.inc = Vector(mousePos[0] - wizardX, mousePos[1] - wizardY).normalized()
        self.inc_rotate = Vector(mousePos[0] - wizardX, -(mousePos[1] - wizardY)).normalized()
        self.image = pygame.transform.rotate(self.image, (self.inc_rotate.get_angle() + 135))
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.spawn_time = pygame.time.get_ticks()
        self.fireball_lifetime = 650

    def update(self, delta):

        offsetY = 0
        offsetX = 0

        pygame.sprite.Sprite.update(self)
        self.position += self.inc * self.speed * delta
        self.rect.center = self.position

        if pygame.time.get_ticks() - self.spawn_time > self.fireball_lifetime:
            self.kill()

        """
        Need to figure out how to set image rotation's origin to the center of the image, not the top-left
        SOLVED - used a function found online
        """
        # now = pygame.time.get_ticks()
        # if now - self.last_rotation > self.rotationSpeed:
        #     self.last_rotation = now
        #     self.image = rot_center(self.image, 30)

        oldRect = self.rect
        self.rect = self.rect.move(offsetX, offsetY)

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