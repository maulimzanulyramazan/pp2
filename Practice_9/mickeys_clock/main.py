import pygame
from clock import MickeyClock

pygame.init()

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Clock")

clock = pygame.time.Clock()

mickey_clock = MickeyClock(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mickey_clock.draw()

    pygame.display.flip()
    clock.tick(1)

pygame.quit()