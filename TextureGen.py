from math import cos, pi, sin
import pygame
import sys

def drawShield(surface):
    surface.fill((255, 255, 255, 0))
    R = 200
    for i in range(R, 1, -1):
        pygame.draw.circle(surface, (0, 0, 255, 128*sin(0.5*pi*(i/R))), (200, 200), i, 0)

def drawEnergyBullet(surface, Red, Green, Blue):
    surface.fill((255, 255, 255, 0))
    R = 200
    for i in range(R, 1, -1):
        pygame.draw.circle(surface, (Red, Green, Blue, 128*cos(0.5*pi*(i/R))), (200, 200), i, 0)

def main():
    pygame.init()
    window = pygame.display.set_mode((400, 400))
    background = pygame.image.load('background.bmp')
    image = pygame.Surface((400, 400)).convert_alpha()
    drawEnergyBullet(image, 0, 0, 0)
    #pygame.image.save(image, 'energyBulletBlack.bmp')
    k = 0
    while True:
        k += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        window.fill((0, 0, 0, 0))
        window.blit(background, background.get_rect())
        image.set_alpha(255)
        window.blit(image, image.get_rect())
        pygame.display.flip()
        pygame.time.delay(10)
    

if __name__ == '__main__':
    main()