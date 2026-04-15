import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# түстер
PLAYER = (0,200,255)
ENEMY = (255,80,80)
BULLET = (255,255,0)
BG = (20,20,30)

player = pygame.Rect(100, 200, 40, 40)
bullets = []
enemies = []

hp = 5
score = 0

font = pygame.font.SysFont("arial", 24)

def spawn_enemy():
    return pygame.Rect(800, random.randint(0,460), 40, 40)

running = True
spawn_timer = 0

while running:
    screen.fill(BG)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(player.x+30, player.y+15, 10,5))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]: player.y -= 5
    if keys[pygame.K_DOWN]: player.y += 5
    if keys[pygame.K_LEFT]: player.x -= 5
    if keys[pygame.K_RIGHT]: player.x += 5

    # bullets
    for b in bullets[:]:
        b.x += 10
        if b.x > WIDTH:
            bullets.remove(b)

    # enemies
    spawn_timer += 1
    if spawn_timer > 40:
        enemies.append(spawn_enemy())
        spawn_timer = 0

    for enemy in enemies[:]:
        # AI
        if enemy.y < player.y:
            enemy.y += 2
        else:
            enemy.y -= 2

        enemy.x -= 4

        if enemy.colliderect(player):
            enemies.remove(enemy)
            hp -= 1

        if enemy.x < 0:
            enemies.remove(enemy)

    # collision
    for enemy in enemies[:]:
        for b in bullets[:]:
            if enemy.colliderect(b):
                enemies.remove(enemy)
                bullets.remove(b)
                score += 1
                break

    # draw
    pygame.draw.rect(screen, PLAYER, player)

    for enemy in enemies:
        pygame.draw.rect(screen, ENEMY, enemy)

    for b in bullets:
        pygame.draw.rect(screen, BULLET, b)

    screen.blit(font.render(f"HP: {hp}", True, (255,255,255)), (10,10))
    screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10,40))

    if hp <= 0:
        screen.blit(font.render("GAME OVER", True, (255,0,0)), (350,200))
        pygame.display.update()
        pygame.time.delay(2000)
        break

    pygame.display.update()
    clock.tick(60)

pygame.quit()