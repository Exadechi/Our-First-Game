import pygame, Wizard, Assets

#Initializing pygame
pygame.init()

class Game():

    def __init__(self):
        # Initializing pygame
        pygame.init()

        # Create a clock to keep track of time / since when pygame was initialized
        self.clock = pygame.time.Clock()

        #Setting the name of the window
        pygame.display.set_caption("Dungeon Crawler")

    def run(self):
        #
        self.clock.tick(60)
        self.delta = self.clock.get_time()
        self.screen.fill([0,0,0])
        Assets.allGroup


while True:
    clock.tick(140)
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

    for projectile in ProjectileGroup.sprites():
        for rects in tmx_rects:
            if projectile.rect.colliderect(rects):
                projectile.kill()
    # for projectile in enemyProjectileGroup.sprites():
    #    projectile.image = projectile.original
    #    pygame.transform.rotate(projectile.image, 20)
    for x, y, image in tmx_ground.tiles():
        screen.blit(image, (x * 32 + wDrawOffset, y * 32 + hDrawOffset))
    for x, y, image in tmx_wall.tiles():
        screen.blit(image, (x * 32 + wDrawOffset, y * 32 + hDrawOffset))
    allGroup.update(delta)
    charGroup.update(delta)

    for sprite in allGroup:
        screen.blit(sprite.image, (sprite.rect.x + wDrawOffset, sprite.rect.y + hDrawOffset))

    for enemy in charGroup:
        enemy.drawHealth(screen, enemy.rect.centerx + wDrawOffset, enemy.rect.centery + hDrawOffset + 60)
        screen.blit(enemy.image, (enemy.rect.x + wDrawOffset, enemy.rect.y + hDrawOffset))

    ProjectileGroup.add(allyProjectileGroup, enemyProjectileGroup)
    wizard.update(delta)
    screen.blit(wizard.image, (wHalf - wizard.rect.width / 2, hHalf - wizard.rect.height / 2))
    pygame.display.flip()

game = Game()

while True:
    game.run()
