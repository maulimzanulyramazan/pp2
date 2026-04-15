import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 900, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Survival Shooter PRO")

clock = pygame.time.Clock()

# COLORS
BG = (15,15,30)
PLAYER = (0,200,255)
ENEMY = (255,80,80)
BULLET = (255,255,100)
BOSS = (200,0,200)
EXPLOSION = (255,150,0)
TEXT = (255,255,255)

font = pygame.font.SysFont("consolas", 22)
big_font = pygame.font.SysFont("consolas", 60)

# PLAYER
player = pygame.Rect(100, HEIGHT//2, 40, 40)
hp = 5

# DATA
bullets = []
enemies = []
explosions = []

score = 0
level = 1

def spawn_enemy():
    return pygame.Rect(WIDTH, random.randint(0, HEIGHT-40), 40, 40)

def spawn_boss():
    return {"rect": pygame.Rect(WIDTH-100, HEIGHT//2-60, 80, 80), "hp": 20}

boss = None

def draw_text(text, x, y):
    screen.blit(font.render(text, True, TEXT), (x,y))

def explosion_effect(x, y):
    explosions.append([x, y, 10])

def game():
    global hp, score, level, boss

    running = True
    spawn_timer = 0

    while running:
        screen.fill(BG)

        # EVENTS
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    bullets.append(pygame.Rect(player.x+30, player.y+15, 12, 6))

        # MOVEMENT
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]: player.y -= 5
        if keys[pygame.K_DOWN]: player.y += 5
        if keys[pygame.K_LEFT]: player.x -= 5
        if keys[pygame.K_RIGHT]: player.x += 5

        player.clamp_ip(pygame.Rect(0,0,WIDTH,HEIGHT))

        # BULLETS
        for b in bullets[:]:
            b.x += 10
            if b.x > WIDTH:
                bullets.remove(b)

        # LEVEL SYSTEM
        if score > level * 10:
            level += 1
            hp += 1

        # BOSS SPAWN
        if level % 3 == 0 and boss is None:
            boss = spawn_boss()

        # ENEMY SPAWN
        spawn_timer += 1
        if spawn_timer > max(20, 50 - level*2):
            enemies.append(spawn_enemy())
            spawn_timer = 0

        # ENEMY AI
        for enemy in enemies[:]:
            if enemy.y < player.y:
                enemy.y += 2
            else:
                enemy.y -= 2

            enemy.x -= (3 + level*0.5)

            if enemy.colliderect(player):
                enemies.remove(enemy)
                hp -= 1
                explosion_effect(enemy.x, enemy.y)

            if enemy.x < 0:
                enemies.remove(enemy)

        # BOSS AI
        if boss:
            b = boss["rect"]

            if b.y < player.y:
                b.y += 2
            else:
                b.y -= 2

            if b.colliderect(player):
                hp -= 1

            # BULLET HIT
            for bullet in bullets[:]:
                if b.colliderect(bullet):
                    bullets.remove(bullet)
                    boss["hp"] -= 1
                    explosion_effect(b.x, b.y)

            if boss["hp"] <= 0:
                score += 20
                boss = None

            pygame.draw.rect(screen, BOSS, b)
            draw_text(f"BOSS HP: {boss['hp']}", WIDTH-200, 10)

        # COLLISION
        for enemy in enemies[:]:
            for b in bullets[:]:
                if enemy.colliderect(b):
                    enemies.remove(enemy)
                    bullets.remove(b)
                    score += 1
                    explosion_effect(enemy.x, enemy.y)
                    break

        # DRAW PLAYER
        pygame.draw.rect(screen, PLAYER, player)

        # DRAW ENEMY
        for enemy in enemies:
            pygame.draw.rect(screen, ENEMY, enemy)

        # DRAW BULLETS
        for b in bullets:
            pygame.draw.rect(screen, BULLET, b)

        # EXPLOSION EFFECT
        for exp in explosions[:]:
            pygame.draw.circle(screen, EXPLOSION, (exp[0], exp[1]), exp[2])
            exp[2] += 2
            if exp[2] > 20:
                explosions.remove(exp)

        # UI
        draw_text(f"HP: {hp}", 10, 10)
        draw_text(f"Score: {score}", 10, 35)
        draw_text(f"Level: {level}", 10, 60)

        # GAME OVER
        if hp <= 0:
            screen.fill((0,0,0))
            screen.blit(big_font.render("GAME OVER", True, (255,0,0)), (250,200))
            pygame.display.update()
            pygame.time.delay(3000)
            break

        pygame.display.update()
        clock.tick(60)

game()
pygame.quit()