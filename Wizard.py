import pygame, Assets

class Wizard(pygame.sprite.Sprite):
    speed = 0.25
    horizontal = Assets.wizardHorizontal
    upward = Assets.wizardUpward
    downward = Assets.wizardDownward

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Wizard.horizontal
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
            if  pygame.mouse.get_pos() != (wHalf, hHalf):
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