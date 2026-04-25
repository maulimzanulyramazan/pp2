import pygame  # Import pygame
import random  # Import random for random positions
from utils import WIDTH, HEIGHT, MAX_ENEMIES, MAX_COINS, screen, clock, font, small_font
from utils import YELLOW, RED, WHITE, BLACK, GOLD, SILVER, BRONZE
from player import Player
from enemy import Enemy
from coin import Coin
from road import draw_road

class Game:
    """Main game manager class"""
    
    def __init__(self):
        """Initialize game state variables"""
        self.player = None  # Player car object
        self.enemies = []  # List of enemy cars
        self.coins = []  # List of coins on screen
        self.coins_collected = 0  # Total points collected
        self.speed_increase = 0  # Enemy speed bonus from coins
        self.game_active = True  # Is game currently active?
    
    def start_new_game(self):
        """Reset and start a fresh game"""
        self.player = Player()  # Create new player car
        self.enemies = []  # Clear enemies list
        self.coins = []  # Clear coins list
        self.coins_collected = 0  # Reset score
        self.speed_increase = 0  # Reset speed bonus
        self.game_active = True  # Game is active
        
        # Create 4 enemy cars
        for _ in range(MAX_ENEMIES):
            self.enemies.append(Enemy(0))  # No speed bonus initially
        
        # Create 6 coins starting above screen
        for _ in range(MAX_COINS):
            new_coin = Coin()
            new_coin.y = random.randint(-200, -50)  # Random Y above screen
            self.coins.append(new_coin)
    
    def handle_input(self):
        """Process keyboard input from player"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Close button clicked
                return False
        
        keys = pygame.key.get_pressed()  # Get all pressed keys
        self.player.move(keys)  # Move player car
        return True  # Continue game
    
    def update_coins(self):
        """Update coins: move, collect, respawn (Task 1 & Task 2)"""
        # Move all coins down
        for coin in self.coins:
            coin.move()
        
        # Check collision between player and coins
        for coin in self.coins[:]:  # Use [:] to safely modify list
            if self.player.get_rect().colliderect(coin.get_rect()):
                self.coins_collected += coin.get_weight()  # Add coin value to score
                self.coins.remove(coin)  # Remove collected coin
                
                # Task 2: Increase enemy speed every 5 coins
                new_speed = self.coins_collected // 5  # Calculate speed bonus
                if new_speed > self.speed_increase:  # If bonus increased
                    self.speed_increase = new_speed  # Update speed bonus
                    for enemy in self.enemies:
                        enemy.speed = enemy.base_speed + self.speed_increase  # Apply to all enemies
        
        # Remove coins that fell off screen
        for coin in self.coins[:]:
            if coin.off_screen():
                self.coins.remove(coin)  # Remove off-screen coin
        
        # Keep exactly 6 coins on screen
        while len(self.coins) < MAX_COINS:
            new_coin = Coin()
            new_coin.y = -new_coin.size  # Start at top of screen
            self.coins.append(new_coin)  # Add new coin
    
    def update_enemies(self):
        """Update enemies: move, check collision, respawn"""
        # Move all enemies down
        for enemy in self.enemies:
            enemy.move()
        
        # Check collision between player and enemies
        for enemy in self.enemies:
            if self.player.get_rect().colliderect(enemy.get_rect()):
                self.game_active = False  # Game over!
                return
        
        # Respawn enemies that went off screen
        for enemy in self.enemies[:]:
            if enemy.off_screen():
                self.enemies.remove(enemy)  # Remove off-screen enemy
                self.enemies.append(Enemy(self.speed_increase))  # Add new enemy at top
    
    def draw(self):
        """Draw everything on screen"""
        draw_road()  # Draw road and lines
        
        # Draw coins FIRST (so they appear behind cars)
        for coin in self.coins:
            coin.draw()
        
        # Draw cars SECOND (so they appear on top of coins)
        self.player.draw()  # Draw player car
        for enemy in self.enemies:
            enemy.draw()  # Draw all enemy cars
        
        # Draw score counter (top-right corner)
        score_text = font.render(f"Coins: {self.coins_collected}", True, YELLOW)
        pygame.draw.rect(screen, BLACK, (WIDTH - 150, 10, 130, 35))  # Background for text
        screen.blit(score_text, (WIDTH - 140, 15))  # Display score
        
        # Draw speed bonus info (if any)
        if self.speed_increase > 0:
            speed_text = small_font.render(f"Speed +{self.speed_increase}", True, RED)
            pygame.draw.rect(screen, BLACK, (WIDTH - 130, 50, 120, 25))
            screen.blit(speed_text, (WIDTH - 125, 53))
        
        # Draw coin value guide (bottom-left corner)
        pygame.draw.rect(screen, BLACK, (10, HEIGHT - 90, 160, 80))
        bronze_text = small_font.render("Bronze = 1", True, BRONZE)
        silver_text = small_font.render("Silver = 2", True, SILVER)
        gold_text = small_font.render("Gold = 3", True, GOLD)
        screen.blit(bronze_text, (15, HEIGHT - 85))
        screen.blit(silver_text, (15, HEIGHT - 60))
        screen.blit(gold_text, (15, HEIGHT - 35))
        
        pygame.display.flip()  # Update the screen
    
    def game_over_screen(self):
        """Display game over screen and wait for input"""
        screen.fill(BLACK)  # Clear screen with black
        
        # Game over title
        game_over = font.render("GAME OVER", True, RED)
        # Final score display
        coins_text = font.render(f"Coins: {self.coins_collected}", True, YELLOW)
        # Restart instructions
        restart = small_font.render("SPACE = Restart | ESC = Quit", True, WHITE)
        
        # Center all texts on screen
        screen.blit(game_over, (WIDTH//2 - 70, HEIGHT//2 - 60))
        screen.blit(coins_text, (WIDTH//2 - 50, HEIGHT//2 - 20))
        screen.blit(restart, (WIDTH//2 - 150, HEIGHT//2 + 50))
        
        pygame.display.flip()  # Update display
        
        # Wait for player input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Close window
                    return False
                if event.type == pygame.KEYDOWN:  # Key pressed
                    if event.key == pygame.K_SPACE:  # Space to restart
                        return True
                    if event.key == pygame.K_ESCAPE:  # ESC to quit
                        return False
        return False
    
    def run(self):
        """Main game loop"""
        while self.game_active:
            # 1. Handle player input
            if not self.handle_input():
                return False
            
            # 2. Update enemies and check collision
            self.update_enemies()
            if not self.game_active:  # If collision occurred
                break
            
            # 3. Update coins
            self.update_coins()
            
            # 4. Draw everything
            self.draw()
            
            # 5. Control game speed (60 FPS)
            clock.tick(60)
        
        return True  # Game over, can restart