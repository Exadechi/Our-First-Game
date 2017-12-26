import pygame
import Assets

class LootDrop(pygame.sprite.Sprite):

    def __init__(self, xSpawn, ySpawn):
        pygame.sprite.Sprite.__init__(self)
        self.image = Assets.lootDropImageClosed
        self.jiggy = xSpawn, ySpawn
        self.rect = self.image.get_rect(center=self.jiggy)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 10
        self.start_despawn = False

    def update(self, delta):
        pygame.sprite.Sprite.update(self)
        for sprite in Assets.charGroup:
            if sprite.rect.colliderect(self.rect):
                self.image = Assets.lootDropImage
                #self.start_despawn = True

        self.checkIfDespawn()

    def checkIfDespawn(self):

        if self.start_despawn:
            if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
                self.kill()