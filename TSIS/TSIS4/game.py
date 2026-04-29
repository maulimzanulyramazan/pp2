# game.py - Main game logic (FIXED)
import pygame
import random
import json
from utils import WIDTH, HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, GRID_SIZE, BLACK, WHITE, RED, GREEN, DARK_RED, BLUE, YELLOW, PURPLE, ORANGE, GRAY, GOLD, DARK_GREEN, BRIGHT_GREEN, CYAN, PINK, INITIAL_SPEED, SPEED_INCREMENT, FOODS_PER_LEVEL, POWERUP_DURATION, POWERUP_DISAPPEAR_TIME, OBSTACLE_START_LEVEL
from snake import Snake
from food import Food, PoisonFood
from powerup import PowerUp
from obstacle import ObstacleManager

class Game:
    def __init__(self, username, db):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        
        self.username = username
        self.db = db
        self.personal_best = db.get_personal_best(username) if db else 0
        
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.load_settings()
        self.play_music()
        self.reset()
    
    def play_music(self):
        """Play background music - FIXED"""
        try:
            # Try different paths
            music_file = None
            import os
            if os.path.exists("assets/music.mp3"):
                music_file = "assets/music.mp3"
            
            if music_file:
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.set_volume(20)
                pygame.mixer.music.play(-1)
                print("✅ Music playing")
            else:
                print("No music file found")
        except Exception as e:
            print(f"Music error: {e}")
    
    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
        except:
            self.settings = {"snake_color": [0, 255, 0], "grid_overlay": True, "sound": True}
            self.save_settings()
    
    def save_settings(self):
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f)
    
    def reset(self):
        self.snake = Snake()
        self.obstacles = ObstacleManager()
        self.food = None
        self.poison = None
        self.powerup = None
        self.score = 0
        self.level = 1
        self.food_count = 0
        self.base_speed = INITIAL_SPEED
        self.active_powerups = {}
        self.shield = False
        self.running = True
        
        self.obstacles.generate(self.level, self.snake.body)
        self.generate_food()
    
    def generate_food(self):
        self.food = Food(self.snake.body, self.obstacles.obstacles)
        if random.random() < 0.2:
            self.poison = PoisonFood(self.snake.body, self.obstacles.obstacles)
            if hasattr(self.poison, 'position') and hasattr(self.food, 'position'):
                if self.poison.position == self.food.position:
                    self.poison = None
        else:
            self.poison = None
    
    def handle_input(self):
        """Process keyboard input - FIXED: returns False to quit"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN and self.running:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.snake.change_direction("RIGHT")
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.snake.change_direction("LEFT")
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.snake.change_direction("UP")
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.snake.change_direction("DOWN")
        return True
    
    def check_collisions(self):
        head = self.snake.body[0]
        
        # Wall collision
        if head[0] < 0 or head[0] >= GRID_SIZE or head[1] < 0 or head[1] >= GRID_SIZE:
            if self.shield:
                self.shield = False
                return False
            self.running = False
            return True
        
        # Self collision
        if head in self.snake.body[1:]:
            if self.shield:
                self.shield = False
                return False
            self.running = False
            return True
        
        # Obstacle collision
        if head in self.obstacles.obstacles:
            if self.shield:
                self.shield = False
                return False
            self.running = False
            return True
        
        return False
    
    def check_food_collision(self):
        head = self.snake.body[0]
        
        # Normal food
        if head == self.food.position:
            self.snake.grow = True
            self.score += self.food.get_weight()
            self.food_count += 1
            
            if self.food_count >= FOODS_PER_LEVEL:
                self.level += 1
                self.food_count = 0
                self.obstacles.generate(self.level, self.snake.body)
            
            self.generate_food()
            return True
        
        # Poison food
        if self.poison and hasattr(self.poison, 'position') and head == self.poison.position:
            if not self.snake.shrink(2):
                self.running = False
            self.score += self.poison.get_weight()
            self.poison = None
            return True
        
        return False
    
    def check_powerup_collision(self):
        if self.powerup and self.snake.body[0] == self.powerup.position:
            self.apply_powerup(self.powerup)
            self.powerup = None
            return True
        return False
    
    def apply_powerup(self, powerup):
        current_time = pygame.time.get_ticks()
        if powerup.type == "speed_boost":
            self.base_speed = INITIAL_SPEED + 5
            self.active_powerups["speed"] = current_time + POWERUP_DURATION
        elif powerup.type == "slow_motion":
            self.base_speed = max(5, INITIAL_SPEED - 3)
            self.active_powerups["slow"] = current_time + POWERUP_DURATION
        elif powerup.type == "shield":
            self.shield = True
            self.active_powerups["shield"] = current_time + POWERUP_DURATION
    
    def update_powerups(self, current_time):
        if "speed" in self.active_powerups and current_time > self.active_powerups["speed"]:
            self.base_speed = INITIAL_SPEED
            del self.active_powerups["speed"]
        if "slow" in self.active_powerups and current_time > self.active_powerups["slow"]:
            self.base_speed = INITIAL_SPEED
            del self.active_powerups["slow"]
        if "shield" in self.active_powerups and current_time > self.active_powerups["shield"]:
            self.shield = False
            del self.active_powerups["shield"]
    
    def update(self):
        if not self.running:
            return
        
        self.snake.move()
        
        if self.check_collisions():
            return
        
        self.check_food_collision()
        self.check_powerup_collision()
        
        current_time = pygame.time.get_ticks()
        
        # Spawn powerup
        if not self.powerup and random.random() < 0.003:
            self.powerup = PowerUp(self.snake.body, self.obstacles.obstacles)
        
        if self.powerup and self.powerup.is_expired(current_time):
            self.powerup = None
        
        # Check if food expired
        if self.food and self.food.is_expired():
            self.generate_food()
        
        self.update_powerups(current_time)
    
    def draw_grid(self):
        if self.settings["grid_overlay"]:
            for x in range(0, WIDTH, CELL_SIZE):
                pygame.draw.line(self.screen, GRAY, (x, 0), (x, HEIGHT), 1)
            for y in range(0, HEIGHT, CELL_SIZE):
                pygame.draw.line(self.screen, GRAY, (0, y), (WIDTH, y), 1)
    
    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.obstacles.draw(self.screen)
        self.food.draw(self.screen)
        if self.poison:
            self.poison.draw(self.screen)
        if self.powerup:
            self.powerup.draw(self.screen)
        self.snake.draw(self.screen)
        
        # UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        best_text = self.small_font.render(f"Best: {self.personal_best}", True, GOLD)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (WIDTH - 100, 10))
        self.screen.blit(best_text, (10, HEIGHT - 30))
        
        if self.shield:
            shield_text = self.small_font.render("🛡️ SHIELD", True, CYAN)
            self.screen.blit(shield_text, (WIDTH - 100, 40))
        
        pygame.display.flip()
    
    def run_frame(self):
        # Handle input
        if not self.handle_input():
            return False
        
        self.update()
        self.draw()
        
        speed = self.base_speed + (self.level - 1) * SPEED_INCREMENT
        speed = min(speed, 25)
        self.clock.tick(speed)
        
        return self.running