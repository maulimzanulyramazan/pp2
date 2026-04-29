# powerup.py - Power-up system (Speed boost, Slow motion, Shield)
import pygame
import random
from utils import GRID_SIZE, CELL_SIZE, PINK, YELLOW, CYAN, POWERUP_DISAPPEAR_TIME, WHITE

class PowerUp:
    """
    Power-up items with temporary effects.
    - Speed boost: Increases snake speed for 5 seconds
    - Slow motion: Decreases snake speed for 5 seconds
    - Shield: Ignores next collision (wall, self, or obstacle)
    """
    
    POWERUP_TYPES = ["speed_boost", "slow_motion", "shield"]
    
    def __init__(self, snake_body, obstacles=None):
        self.type = random.choice(self.POWERUP_TYPES)
        self.spawn_time = pygame.time.get_ticks()
        
        # Find empty position not occupied
        while True:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            pos = [x, y]
            if pos not in snake_body and (not obstacles or pos not in obstacles):
                self.position = pos
                break
    
    def is_expired(self, current_time):
        """Check if power-up disappeared (8 seconds)"""
        return current_time - self.spawn_time > POWERUP_DISAPPEAR_TIME
    
    def get_color(self):
        """Get color based on power-up type"""
        colors = {
            "speed_boost": PINK,
            "slow_motion": YELLOW,
            "shield": CYAN
        }
        return colors.get(self.type, WHITE)
    
    def draw(self, screen):
        """Draw power-up with star effect"""
        x = self.position[0] * CELL_SIZE
        y = self.position[1] * CELL_SIZE
        color = self.get_color()
        
        # Draw main rectangle
        pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
        
        # Draw star shape in center
        center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
        pygame.draw.circle(screen, WHITE, center, 5)
        pygame.draw.circle(screen, color, center, 3)