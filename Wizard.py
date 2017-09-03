import pygame
import Assets
from Fireball import Fireball


class Wizard(pygame.sprite.Sprite):
    def __init__(self, Spawn):
        pygame.sprite.Sprite.__init__(self)
        self.image = Assets.wizardHorizontal
        self.imageRight = Assets.wizardHorizontal
        self.imageLeft = pygame.transform.flip(Assets.wizardHorizontal, True, False)
        self.imageUp = Assets.wizardUpward
        self.imageDownward = Assets.wizardDownward
        self.speed = 0.25
        self.rect = self.image.get_rect(center=(Spawn[0], Spawn[1]))
        self._layer = 3
        self.add(Assets.allGroup, Assets.charGroup)
        self.center = self.rect.center
        self.last_fireball = 0
        self.last_animation_frame = 0
        self.dexterity = 250

        # Health variables
        self.maxHealth = 500
        self.health = self.maxHealth
        self.healthbar = pygame.image.load('HealthBarEnlargedFully.png')
        self.healthbarEmpty = pygame.image.load('HealthBarEnlarged.png')
        self.healthbarRect = self.healthbar.get_rect()
        self.healthbarEmptyRect = self.healthbarEmpty.get_rect()
        self.regenSpeed = 3
        self.last_regen = 0
        self.regen = 250
        self.dead = False


    def update(self, delta):
        pygame.sprite.Sprite.update(self)

        self.checkAlive()

        self.playerShoot()

        self.movement(delta)

        self.animation()

        self.collisionDetection()

        self.regenHealth()

    def checkAlive(self):
        """
        A function to check whether the wizard is alive
        :return:
        """

        if self.health <= 0:
            self.dead = True
            self.kill()

    def playerShoot(self):
        """
        A function to make the player shoot
        :return:
        """

        if pygame.mouse.get_pressed()[0]:
            if pygame.mouse.get_pos() != (Assets.wHalf, Assets.hHalf):
                now = pygame.time.get_ticks()
                if now - self.last_fireball > self.dexterity:
                    self.last_fireball = now
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    fireball = Fireball(self.rect.centerx,
                                        self.rect.centery,
                                       (mouseX - Assets.wHalf + self.rect.centerx,
                                        mouseY - Assets.hHalf + self.rect.centery))
                    Assets.allyProjectileGroup.add(fireball)
                    Assets.allGroup.add(fireball)

    def movement(self, delta):
        """
        A function to make the player move
        :param delta:
        :return:
        """

        self.offsetY = 0
        self.offsetX = 0

        if pygame.key.get_pressed()[pygame.K_w]:
            self.offsetY -= delta * self.speed
        if pygame.key.get_pressed()[pygame.K_s]:
            self.offsetY += delta * self.speed
        if pygame.key.get_pressed()[pygame.K_d]:
            self.offsetX += delta * self.speed
        if pygame.key.get_pressed()[pygame.K_a]:
           self.offsetX -= delta * self.speed

        self.oldRect = self.rect
        self.rect = self.rect.move(self.offsetX, self.offsetY)

    def animation(self):
        """
        A function to animate the player or change his sprites
        :return:
        """

        if pygame.key.get_pressed()[pygame.K_w]:
            if pygame.key.get_pressed()[pygame.K_d]:
                self.image = self.imageRight
            elif pygame.key.get_pressed()[pygame.K_a]:
                self.image = self.imageUp
            else:
                self.image = self.imageUp
        elif pygame.key.get_pressed()[pygame.K_s]:
            if pygame.key.get_pressed()[pygame.K_d]:
                self.image = self.imageDownward
            elif pygame.key.get_pressed()[pygame.K_a]:
                self.image = self.imageLeft
            else:
                self.image = self.imageDownward
        elif pygame.key.get_pressed()[pygame.K_d]:
            self.image = self.imageRight
        elif pygame.key.get_pressed()[pygame.K_a]:
            self.image = self.imageLeft

        """
        Working on player animation
        """
        # now = pygame.time.get_ticks()
        # if now - self.last_animation_frame > 200:
        #     self.last_animation_frame = now
        #     self.image = pygame.transform.flip(self.image, True, False)

    def collisionDetection(self):
        """
        A function to check collision, currently only with the tmx walls
        :return:
        """

        for wall in Assets.tmx_rects:
            # Copy oldRect
            xRect = self.oldRect.move(0, 0)
            yRect = self.oldRect.move(0, 0)
            xRect.centerx = self.rect.centerx
            yRect.centery = self.rect.centery
            if xRect.colliderect(wall):
                self.rect.centerx = self.oldRect.centerx

            if yRect.colliderect(wall):
                self.rect.centery = self.oldRect.centery

        for enemyProjectile in Assets.enemyProjectileGroup:
            if pygame.sprite.collide_rect(enemyProjectile, self):
                enemyProjectile.kill()
                self.health -= enemyProjectile.damage

    def drawHealth(self, screen, x, y):
        """
        A function to draw the wizards health
        :param screen:
        :param x:
        :param y:
        :return:
        """

        self.healthbarRect.x = x
        self.healthbarRect.y = y
        self.healthbarEmptyRect.x = x
        self.healthbarEmptyRect.y = y

        screen.blit(self.healthbarEmpty, dest=(self.healthbarEmptyRect))

        healthCrop = pygame.Rect(0, 0, self.healthbarEmptyRect.w / self.maxHealth * self.health, self.healthbarEmptyRect.h)

        screen.blit(self.healthbar, dest=(self.healthbarEmptyRect), area=healthCrop)

    def regenHealth(self):
        """
        A function to regenerate the players health
        :return:
        """

        now = pygame.time.get_ticks()
        if self.health < self.maxHealth:
            if now - self.last_regen > self.regen:
                self.last_regen = now
                self.health += self.regenSpeed