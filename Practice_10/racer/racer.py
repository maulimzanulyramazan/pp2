import pygame
import random
import sys

pygame.init()

# Window size
WIDTH = 800
HEIGHT = 600

# Colors
BLACK = (0, 0, 1)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
LIGHT_GRAY = (80, 80, 80)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

ENEMY_COLORS = [BLUE, GREEN, ORANGE, PURPLE, (200, 0, 200), (0, 150, 150)]

class Player:
    def __init__(self):
        self.width = 45
        self.height = 70
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 100
        self.speed = 6
        self.color = RED
    
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 100:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width - 100:
            self.x += self.speed
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)
        pygame.draw.rect(screen, (100, 100, 200), (self.x + 5, self.y + 5, self.width - 10, 20))
        pygame.draw.rect(screen, (100, 100, 200), (self.x + 5, self.y + 45, self.width - 10, 15))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Enemy:
    def __init__(self):
        self.width = 45
        self.height = 70
        self.x = random.randint(100, WIDTH - self.width - 100)
        self.y = -self.height
        self.speed = random.randint(4, 7)
        self.color = random.choice(ENEMY_COLORS)
    
    def move(self):
        self.y += self.speed
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)
        pygame.draw.rect(screen, (150, 150, 200), (self.x + 5, self.y + 5, self.width - 10, 20))
        pygame.draw.rect(screen, (150, 150, 200), (self.x + 5, self.y + 45, self.width - 10, 15))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def off_screen(self):
        return self.y > HEIGHT
    
    def reset(self):
        self.x = random.randint(100, WIDTH - self.width - 100)
        self.y = -self.height
        self.speed = random.randint(4, 7)
        self.color = random.choice(ENEMY_COLORS)

class Coin:
    def __init__(self, existing_coins=None):
        self.size = 18
        self.speed = 5
        # Generate position that doesn't overlap with other coins
        self.x = random.randint(100, WIDTH - self.size - 100)
        self.y = -self.size
        # Check if position overlaps with existing coins
        if existing_coins:
            for coin in existing_coins:
                if abs(self.x - coin.x) < 30 and abs(self.y - coin.y) < 30:
                    self.x = random.randint(100, WIDTH - self.size - 100)
    
    def move(self):
        self.y += self.speed
    
    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x + self.size//2, self.y + self.size//2), self.size//2)
        pygame.draw.circle(screen, (200, 150, 0), (self.x + self.size//2, self.y + self.size//2), self.size//2, 2)
        font_small = pygame.font.Font(None, 20)
        dollar = font_small.render("$", True, (200, 150, 0))
        screen.blit(dollar, (self.x + 5, self.y + 3))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)
    
    def off_screen(self):
        return self.y > HEIGHT

def draw_road():
    pygame.draw.rect(screen, GRAY, (80, 0, WIDTH - 160, HEIGHT))
    pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, 80, HEIGHT))
    pygame.draw.rect(screen, LIGHT_GRAY, (WIDTH - 80, 0, 80, HEIGHT))
    
    for y in range(0, HEIGHT, 50):
        pygame.draw.rect(screen, WHITE, (WIDTH//2 - 5, y, 10, 30))
    
    pygame.draw.line(screen, WHITE, (80, 0), (80, HEIGHT), 3)
    pygame.draw.line(screen, WHITE, (WIDTH - 80, 0), (WIDTH - 80, HEIGHT), 3)

def show_coins(coins_collected):
    text = font.render(f"Coins: {coins_collected}", True, WHITE)
    pygame.draw.rect(screen, BLACK, (WIDTH - 150, 10, 130, 35))
    screen.blit(text, (WIDTH - 140, 15))

def game_over_screen(coins):
    screen.fill(BLACK)
    
    game_over_text = font.render("GAME OVER", True, RED)
    coins_text = font.render(f"Coins collected: {coins}", True, YELLOW)
    restart_text = font.render("Press SPACE to play again or ESC to quit", True, WHITE)
    
    screen.blit(game_over_text, (WIDTH//2 - 70, HEIGHT//2 - 60))
    screen.blit(coins_text, (WIDTH//2 - 80, HEIGHT//2 - 20))
    screen.blit(restart_text, (WIDTH//2 - 250, HEIGHT//2 + 50))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False

def main():
    running = True
    
    while running:
        player = Player()
        enemies = []
        coins = []
        coins_collected = 0
        
        # Start with 4 enemies
        for _ in range(4):
            enemies.append(Enemy())
        
        # Start with 6 coins
        for _ in range(6):
            coins.append(Coin(coins))
        
        game_active = True
        
        while game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            keys = pygame.key.get_pressed()
            player.move(keys)
            
            # Move enemies
            for enemy in enemies:
                enemy.move()
            
            # Move coins
            for coin in coins:
                coin.move()
            
            # Check collision with enemies
            for enemy in enemies:
                if player.get_rect().colliderect(enemy.get_rect()):
                    game_active = False
                    break
            
            if not game_active:
                break
            
            # Check coin collection
            for coin in coins[:]:
                if player.get_rect().colliderect(coin.get_rect()):
                    coins_collected += 1
                    coins.remove(coin)
                    print(f"Coin collected! Total: {coins_collected}")  # Debug print
            
            # Remove coins that went off screen
            for coin in coins[:]:
                if coin.off_screen():
                    coins.remove(coin)
            
            # Keep exactly 6 coins on screen (ALWAYS)
            while len(coins) < 6:
                new_coin = Coin(coins)
                coins.append(new_coin)
                print(f"New coin added. Total coins: {len(coins)}")  # Debug print
            
            # Reset enemies if off screen
            for enemy in enemies[:]:
                if enemy.off_screen():
                    enemies.remove(enemy)
                    enemies.append(Enemy())
            
            # Draw everything
            draw_road()
            player.draw()
            for enemy in enemies:
                enemy.draw()
            for coin in coins:
                coin.draw()
            
            show_coins(coins_collected)
            
            pygame.display.flip()
            clock.tick(60)
        
        running = game_over_screen(coins_collected)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()