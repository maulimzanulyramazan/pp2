import pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Game")

running = True
while running:
    screen.fill((0, 255, 255))
    pygame.draw.rect(screen, (255, 0, 0), (100, 100, 50, 50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
pygame.quit()