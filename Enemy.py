import pygame
import Assets
from EnemyProjectile import EnemyProjectile

class Enemy(pygame.sprite.Sprite):
    speed = 0.5

    def __init__(self, xSpawn, ySpawn):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('GreenGoopEnemy.png')
        self._layer = 1
        self.add(Assets.allGroup, Assets.enemyGroup)
        self.jiggy = xSpawn, ySpawn
        self.rect = self.image.get_rect(center=self.jiggy)
        self.last_fireball = 0
        self.dexterity = 550

        self.maxHealth = 100
        self.health = self.maxHealth
        self.healthbar = pygame.image.load('HealthBarEnlargedFully.png')
        self.healthbarEmpty = pygame.image.load('HealthBarEnlarged.png')
        self.healthbarRect = self.healthbar.get_rect()
        self.healthbarEmptyRect = self.healthbarEmpty.get_rect()

        self.regen = 250
        self.regenSpeed = 1.5
        self.last_regen = 0

    def update(self, delta):
        pygame.sprite.Sprite.update(self)

        offsetY = 0
        offsetX = 0

        if pygame.key.get_pressed()[pygame.K_i]:
            offsetY -= delta * Enemy.speed
        if pygame.key.get_pressed()[pygame.K_k]:
            offsetY += delta * Enemy.speed
        if pygame.key.get_pressed()[pygame.K_l]:
            offsetX += delta * Enemy.speed
        if pygame.key.get_pressed()[pygame.K_j]:
            offsetX -= delta * Enemy.speed

        self.rect.move_ip(offsetX, offsetY)

        if self.health <= 0:
            self.kill()

        self.collisionDetection()
        self.regenHealth()


    def shootProjectiles(self, wizardPos):

        now = pygame.time.get_ticks()
        if now - self.last_fireball > self.dexterity:
            self.last_fireball = now
            fireball = EnemyProjectile(self.rect.centerx, self.rect.centery, wizardPos, 0)
            fireball2 = EnemyProjectile(self.rect.centerx, self.rect.centery, wizardPos, 20)
            fireball3 = EnemyProjectile(self.rect.centerx, self.rect.centery, wizardPos, -20)
            Assets.enemyProjectileGroup.add(fireball, fireball2, fireball3)
            Assets.allGroup.add(fireball, fireball2, fireball3)

    def drawHealth(self, screen, x, y):

        self.healthbarRect.centerx = x
        self.healthbarRect.centery = y
        self.healthbarEmptyRect.centerx = x
        self.healthbarEmptyRect.centery = y

        screen.blit(self.healthbarEmpty, dest=(self.healthbarEmptyRect))

        healthCrop = pygame.Rect(0, 0, self.healthbarEmptyRect.w / self.maxHealth * self.health, self.healthbarEmptyRect.h)

        screen.blit(self.healthbar, dest=(self.healthbarEmptyRect), area=healthCrop)

    def collisionDetection(self):

        for allyProjectile in Assets.allyProjectileGroup:
            for enemy in Assets.enemyGroup:
                if pygame.sprite.collide_rect(allyProjectile, enemy):
                    allyProjectile.kill()
                    enemy.health -= allyProjectile.damage

    def regenHealth(self):
        now = pygame.time.get_ticks()
        if self.health < self.maxHealth:
            if now - self.last_regen > self.regen:
                self.last_regen = now
                self.health += self.regenSpeed