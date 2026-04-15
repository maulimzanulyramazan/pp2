import pygame
import random

pygame.init()

WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing 🚗")

clock = pygame.time.Clock()

# COLORS
ROAD = (50, 50, 50)
LINE = (255, 255, 255)
PLAYER = (0, 200, 255)
ENEMY = (255, 80, 80)
TEXT = (255,255,255)
BG = (20,20,20)

font = pygame.font.SysFont("arial", 30)
big_font = pygame.font.SysFont("arial", 60)

# PLAYER
player = pygame.Rect(WIDTH//2 - 25, HEIGHT - 120, 50, 80)
player_speed = 6

# DATA
enemies = []
speed = 5
score = 0

def spawn_enemy():
    x = random.choice([150, 225, 300])  # жолақтар
    return pygame.Rect(x, -100, 50, 80)

def draw_road():
    screen.fill(BG)
    pygame.draw.rect(screen, ROAD, (100, 0, 300, HEIGHT))

    for y in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, LINE, (245, y, 10, 20))

def game():
    global speed, score

    running = True
    spawn_timer = 0

    while running:
        draw_road()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        # movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player.x += player_speed

        # road limits
        if player.x < 110:
            player.x = 110
        if player.x > 340:
            player.x = 340

        # spawn enemies
        spawn_timer += 1
        if spawn_timer > 30:
            enemies.append(spawn_enemy())
            spawn_timer = 0

        # move enemies
        for enemy in enemies[:]:
            enemy.y += speed

            if enemy.colliderect(player):
                return game_over()

            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                score += 1

        # increase difficulty
        if score % 10 == 0:
            speed += 0.01

        # draw player
        pygame.draw.rect(screen, PLAYER, player, border_radius=10)

        # draw enemies
        for enemy in enemies:
            pygame.draw.rect(screen, ENEMY, enemy, border_radius=10)

        # UI
        screen.blit(font.render(f"Score: {score}", True, TEXT), (10,10))
        screen.blit(font.render(f"Speed: {round(speed,1)}", True, TEXT), (10,40))

        pygame.display.update()
        clock.tick(60)

def game_over():
    while True:
        screen.fill((0,0,0))
        screen.blit(big_font.render("CRASH!", True, (255,0,0)), (150,250))
        screen.blit(font.render("R - restart | Q - quit", True, TEXT), (120,320))
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    return game()
                if e.key == pygame.K_q:
                    pygame.quit()
                    quit()

game()
pygame.quit()