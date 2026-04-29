# food.py - Food classes with different weights and timers
import pygame
import random
import time
from utils import GRID_SIZE, CELL_SIZE, RED, GOLD, BLUE, DARK_RED

class Food:
    """
    Normal food with different weights and optional timer.
    Task: Randomly generating food with different weights + disappearing after time
    """
    
    def __init__(self, snake_body, obstacles=None):
        self.type = None       # normal, gold, or timed
        self.position = [0, 0]
        self.weight = 0        # Point value (1, 2, or 3)
        self.spawn_time = None # When food appeared (for timed food)
        self.lifetime = None   # How many seconds until expiration
        self.randomize(snake_body, obstacles)
    
    def randomize(self, snake_body, obstacles=None):
        """
        Randomly generate food with different weights.
        - 60% chance: normal food (1 point, never expires)
        - 25% chance: gold food (3 points, never expires)
        - 15% chance: timed food (2 points, expires after 5 seconds)
        """
        rand = random.random()
        
        if rand < 0.60:   # 60% chance - Normal food
            self.type = "normal"
            self.weight = 1
            self.lifetime = None
            
        elif rand < 0.85: # 25% chance - Gold food
            self.type = "gold"
            self.weight = 3
            self.lifetime = None
            
        else:             # 15% chance - Timed food
            self.type = "timed"
            self.weight = 2
            self.lifetime = 5          # Disappears after 5 seconds
            self.spawn_time = time.time()
        
        # Find empty position not occupied by snake or obstacles
        while True:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            pos = [x, y]
            if pos not in snake_body and (not obstacles or pos not in obstacles):
                self.position = pos
                break
    
    def is_expired(self):
        """Check if timed food has disappeared (Task: disappearing after time)"""
        if self.lifetime is None:
            return False
        return time.time() - self.spawn_time >= self.lifetime
    
    def get_weight(self):
        """Return point value of this food"""
        return self.weight
    
    def get_type(self):
        """Return food type string"""
        return self.type
    
    def draw(self, screen):
        """Draw food on screen with different appearances based on type"""
        x = self.position[0] * CELL_SIZE
        y = self.position[1] * CELL_SIZE
        
        if self.type == "normal":
            # Normal red food
            pygame.draw.rect(screen, RED, (x, y, CELL_SIZE, CELL_SIZE))
            
        elif self.type == "gold":
            # Gold food with shine effect
            pygame.draw.rect(screen, GOLD, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (255, 255, 150), (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4))
            
        else:  # timed
            # Blue timed food with border
            pygame.draw.rect(screen, BLUE, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (0, 0, 150), (x, y, CELL_SIZE, CELL_SIZE), 2)


class PoisonFood:
    """
    Poison food that shortens snake by 2 segments.
    Task: Poison food appears randomly, shortens snake, game over if too short
    """
    
    def __init__(self, snake_body, obstacles=None):
        # Find random empty position
        while True:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            pos = [x, y]
            if pos not in snake_body and (not obstacles or pos not in obstacles):
                self.position = pos
                break
        self.weight = -2   # Negative points (penalty)
    
    def get_weight(self):
        return self.weight
    
    def draw(self, screen):
        """Draw poison food as dark red with skull-like appearance"""
        x = self.position[0] * CELL_SIZE
        y = self.position[1] * CELL_SIZE
        pygame.draw.rect(screen, DARK_RED, (x, y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, (100, 0, 0), (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4))