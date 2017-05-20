import pygame, sys, random
from Vector import Vector
from pytmx import *

pygame.init()

# Tile Imaged is 640x640
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
clock = pygame.time.Clock()
black = [255, 255, 255]
fart = pygame.mixer.Sound('fart.wav')
fart.set_volume(0.05)
tmx_map = util_pygame.load_pygame("WizardTileEnlarged.tmx")
tmx_ground = tmx_map.get_layer_by_name('Ground')
tmx_wall = tmx_map.get_layer_by_name('Walls')
tmx_enemy = tmx_map.get_layer_by_name('Object Layer 1')
tmx_rects = util_pygame.build_rects(tmx_map, 'Walls', tileset='WizardTilesEnlarged', real_gid=4)
pygame.display.set_caption("Dungeon Crawler")

charGroup = pygame.sprite.LayeredUpdates()
allyProjectileGroup = pygame.sprite.Group()
enemyProjectileGroup = pygame.sprite.Group()
ProjectileGroup = pygame.sprite.Group()
allGroup = pygame.sprite.LayeredUpdates()

#you are the biggest boi
class Fireball(pygame.sprite.Sprite):
    speed = 0.75
    # speed = 5

    def __init__(self, wizardX, wizardY, mousePos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Fireball.png')
        self.position = (wizardX, wizardY)
        self.rect = self.image.get_rect(center=self.position)
        self._layer = 2
        self.inc = Vector(mousePos[0] - wizardX, mousePos[1] - wizardY).normalized()
        self.inc_rotate = Vector(mousePos[0] - wizardX, -(mousePos[1] - wizardY)).normalized()
        self.image = pygame.transform.rotate(self.image, (self.inc_rotate.get_angle() + 135))
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.spawn_time = pygame.time.get_ticks()
        self.fireball_lifetime = 650

    def update(self, delta):
        pygame.sprite.Sprite.update(self)
        self.position += self.inc * Fireball.speed * delta
        self.rect.center = self.position

        if pygame.time.get_ticks() - self.spawn_time > self.fireball_lifetime:
            self.kill()


class EnemyFireball(pygame.sprite.Sprite):
    speed = 0.5
    # speed = 5

    def __init__(self, enemyX, enemyY, wizardPos, rotation):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('EnemyProjectileSample.png')
        self.original = self.image
        self.image = pygame.transform.rotate(self.image, 30)
        self.position = (enemyX, enemyY)
        self.rect = self.image.get_rect(center=self.position)
        self._layer = 2
        self.inc = (Vector((wizardPos[0] - enemyX, wizardPos[1] - enemyY)).normalized()).rotated(rotation)
        self.inc_rotate = (Vector(wizardPos[0] - enemyX, -(wizardPos[1] - enemyY)).normalized()).rotated(-rotation)
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.spawn_time = pygame.time.get_ticks()
        self.rotate_time = 10
        self.fireball_lifetime = 2000

    def update(self, delta):
        pygame.sprite.Sprite.update(self)
        #self.image.center = original_center
        #self.image.center = draw_center

        self.rect.center += self.inc * EnemyFireball.speed * delta
        #self.image = self.original
        #pygame.transform.rotate(self.image, 20)

        self.now = pygame.time.get_ticks()
        #if now - self.spawn_time > self.rotate_time:
        #    self.image = pygame.transform.rotate(self.image, 10)
        if self.now - self.spawn_time > self.fireball_lifetime:
            self.kill()


class Wizard(pygame.sprite.Sprite):
    speed = 0.25
    horizontal = pygame.image.load('NewWizard.png')
    upward = pygame.image.load('NewWizard3.png')
    downward = pygame.image.load('NewWizard2.png')

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Wizard.horizontal = pygame.image.load('NewWizard.png')
        self.imageRight = Wizard.horizontal
        self.imageLeft = pygame.transform.flip(Wizard.horizontal, True, False)
        self.imageUp = Wizard.upward
        self.imageDownward = Wizard.downward
        self.rect = self.image.get_rect(center=(100,100))
        self._layer = 3
        self.groups = allGroup
        self.center = self.rect.center
        self.last_fireball = 0
        self.last_animation_frame = 0
        self.dexterity = 250


    def update(self, delta):
        pygame.sprite.Sprite.update(self)

        offsetY = 0
        offsetX = 0

        if pygame.mouse.get_pressed()[0]:
            if pygame.mouse.get_pos() != (wHalf, hHalf):
                now = pygame.time.get_ticks()
                if now - self.last_fireball > self.dexterity:
                    self.last_fireball = now
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    fireball = Fireball(wizard.rect.centerx, wizard.rect.centery,
                    (mouseX - wHalf + wizard.rect.centerx, mouseY - hHalf + wizard.rect.centery))
                    allyProjectileGroup.add(fireball)


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

        now = pygame.time.get_ticks()
        if now - self.last_animation_frame > 50:
            self.last_animation_frame = now
            pygame.transform.flip(self.image, True, False)

        if pygame.key.get_pressed()[pygame.K_w]:
            offsetY -= delta * Wizard.speed
        if pygame.key.get_pressed()[pygame.K_s]:
            offsetY += delta * Wizard.speed
        if pygame.key.get_pressed()[pygame.K_d]:
            offsetX += delta * Wizard.speed
        if pygame.key.get_pressed()[pygame.K_a]:
            offsetX -= delta * Wizard.speed

        oldRect = self.rect
        self.rect = self.rect.move(offsetX, offsetY)

        for wall in tmx_rects:
            # Copy oldRect
            xRect = oldRect.move(0, 0)
            yRect = oldRect.move(0, 0)
            xRect.centerx = self.rect.centerx
            yRect.centery = self.rect.centery
            if xRect.colliderect(wall):
                self.rect.centerx = oldRect.centerx

            if yRect.colliderect(wall):
                self.rect.centery = oldRect.centery


class Enemy(pygame.sprite.Sprite):
    speed = 0.5

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('GreenGoopEnemyEnlarged.png')
        self.health = 5
        self.healthbar = pygame.image.load('HealthBarEnlargedFully.png')
        self.healthbarEmpty = pygame.image.load('HealthBarEnlarged.png')
        self.healthbarRect = self.healthbar.get_rect()
        self.healthbarEmptyRect = self.healthbarEmpty.get_rect()
        self._layer = 1
        self.groups = allGroup, charGroup
        self.xSpawnMin = (wizard.rect.centerx - infoObject.current_w / 2)
        self.xSpawnMax = (wizard.rect.centerx + infoObject.current_w / 2)
        self.ySpawnMin = (wizard.rect.centery - infoObject.current_h / 2)
        self.ySpawnMax = (wizard.rect.centery + infoObject.current_h / 2)
        self.xSpawn = random.randrange(self.xSpawnMin, self.xSpawnMax)
        self.ySpawn = random.randrange(self.ySpawnMin, self.ySpawnMax)
        self.jiggy = self.xSpawn, self.ySpawn
        self.rect = self.image.get_rect(center=self.jiggy)
        self.last_fireball = 0
        self.dexterity = 550

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

        now = pygame.time.get_ticks()
        if now -  self.last_fireball > self.dexterity:
            self.last_fireball = now
            fireball = EnemyFireball(self.rect.centerx, self.rect.centery,wizard.rect.center, 0)
            fireball2 = EnemyFireball(self.rect.centerx, self.rect.centery,wizard.rect.center, 17.5)
            fireball3 = EnemyFireball(self.rect.centerx, self.rect.centery,wizard.rect.center, -17.5)
            enemyProjectileGroup.add(fireball, fireball2, fireball3)

    def drawHealth(self, screen, x, y):
        self.healthbarRect.centerx = x
        self.healthbarRect.centery = y
        self.healthbarEmptyRect.centerx = x
        self.healthbarEmptyRect.centery = y

        screen.blit(self.healthbarEmpty, dest=(self.healthbarEmptyRect))

        healthCrop = pygame.Rect(0, 0, self.healthbarEmptyRect.w / 5 * self.health, self.healthbarEmptyRect.h)

        screen.blit(self.healthbar, dest=(self.healthbarEmptyRect), area=healthCrop)

wizard = Wizard()
#for enemy in tmx_enemy.iterdata():
#    print(enemy)
enemy = Enemy()
enemy.add(allGroup, charGroup)

while 1:
    clock.tick(200)
    delta = clock.get_time()
    screen.fill([0, 0, 0])
    allGroup.add(allyProjectileGroup, enemyProjectileGroup)

    wHalf = infoObject.current_w / 2
    hHalf = infoObject.current_h / 2
    wDrawOffset = -wizard.rect.centerx + wHalf
    hDrawOffset = -wizard.rect.centery + hHalf

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            sys.exit()

    for fireball in allyProjectileGroup.sprites():
        for enemy in charGroup.sprites():
            if pygame.sprite.collide_rect(fireball, enemy):
                fireball.kill()
                enemy.health -= 1
                if enemy.health == 0:
                    enemy.kill()
                    pygame.mixer.Sound.play(fart)
                    enemy = Enemy()
                    charGroup.add(enemy)
                    allGroup.add(enemy)

    for projectile in ProjectileGroup.sprites():
       for rects in tmx_rects:
           if projectile.rect.colliderect(rects):
               projectile.kill()
    #for projectile in enemyProjectileGroup.sprites():
    #    projectile.image = projectile.original
    #    pygame.transform.rotate(projectile.image, 20)
    for x, y, image in tmx_ground.tiles():
        screen.blit(image, (x * 32 + wDrawOffset, y * 32 + hDrawOffset))
    for x, y, image in tmx_wall.tiles():
        screen.blit(image, (x * 32 + wDrawOffset, y * 32 + hDrawOffset))
    allGroup.update(delta)
    # charGroup.update(delta)

    for sprite in allGroup:
        screen.blit(sprite.image, (sprite.rect.x + wDrawOffset, sprite.rect.y + hDrawOffset))

    for enemy in charGroup:
        enemy.drawHealth(screen, enemy.rect.centerx + wDrawOffset, enemy.rect.centery + hDrawOffset + 60)
        screen.blit(enemy.image, (enemy.rect.x + wDrawOffset, enemy.rect.y + hDrawOffset))

    ProjectileGroup.add(allyProjectileGroup, enemyProjectileGroup)
    wizard.update(delta)
    screen.blit(wizard.image, (wHalf - wizard.rect.width / 2, hHalf - wizard.rect.height / 2))
    pygame.display.flip()