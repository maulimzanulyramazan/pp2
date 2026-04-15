import pygame
import random

pygame.init()

# Экран
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake 🐍")

clock = pygame.time.Clock()

# Түстер
BG = (20, 20, 20)
GRID = (40, 40, 40)
SNAKE = (0, 255, 100)
FOOD = (255, 80, 80)
TEXT = (255, 255, 255)

# Параметрлер
BLOCK = 20
SPEED = 12

font = pygame.font.SysFont("arial", 25)
big_font = pygame.font.SysFont("arial", 40)

def draw_grid():
    for x in range(0, WIDTH, BLOCK):
        pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK):
        pygame.draw.line(screen, GRID, (0, y), (WIDTH, y))

def draw_snake(snake):
    for i, segment in enumerate(snake):
        pygame.draw.rect(screen, SNAKE, (*segment, BLOCK, BLOCK), border_radius=6)

def draw_score(score):
    text = font.render(f"Score: {score}", True, TEXT)
    screen.blit(text, (10, 10))

def game():
    x, y = WIDTH // 2, HEIGHT // 2
    dx, dy = 0, 0

    snake = [(x, y)]
    length = 1

    food = (
        random.randrange(0, WIDTH, BLOCK),
        random.randrange(0, HEIGHT, BLOCK)
    )

    game_over = False

    while True:
        while game_over:
            screen.fill(BG)
            msg = big_font.render("GAME OVER", True, FOOD)
            sub = font.render("R - restart | Q - quit", True, TEXT)
            screen.blit(msg, (WIDTH//2 - 120, HEIGHT//2 - 40))
            screen.blit(sub, (WIDTH//2 - 130, HEIGHT//2 + 10))
            pygame.display.update()

            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    if e.key == pygame.K_r:
                        game()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -BLOCK, 0
                elif e.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = BLOCK, 0
                elif e.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -BLOCK
                elif e.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, BLOCK

        x += dx
        y += dy

        # Стенкаға соғылу
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            game_over = True

        snake.append((x, y))
        if len(snake) > length:
            snake.pop(0)

        # Өзін соғу
        if (x, y) in snake[:-1]:
            game_over = True

        # Тамақ жеу
        if (x, y) == food:
            food = (
                random.randrange(0, WIDTH, BLOCK),
                random.randrange(0, HEIGHT, BLOCK)
            )
            length += 1

        # Сурет салу
        screen.fill(BG)
        draw_grid()
        pygame.draw.rect(screen, FOOD, (*food, BLOCK, BLOCK), border_radius=6)
        draw_snake(snake)
        draw_score(length - 1)

        pygame.display.update()
        clock.tick(SPEED)

game()