# obstacle.py - Obstacle management (walls inside arena from level 3)
import pygame
import random
from utils import GRID_SIZE, CELL_SIZE, GRAY, OBSTACLE_START_LEVEL

class ObstacleManager:
    """
    Manages static wall blocks that appear inside the arena starting from level 3.
    - Randomly placed at each new level
    - Guarantees snake is not trapped at spawn time
    - Collision with obstacle = game over
    """
    
    def __init__(self):
        self.obstacles = []
    
    def generate(self, level, snake_body):
        """
        Generate obstacles for current level.
        Starts from level OBSTACLE_START_LEVEL (default: 3)
        Number of obstacles increases with level (level * 2, max 20)
        """
        # No obstacles before level 3
        if level < OBSTACLE_START_LEVEL:
            self.obstacles = []
            return
        
        # Calculate number of obstacles (increases with level)
        num_obstacles = min(level * 2, 20)
        self.obstacles = []
        attempts = 0
        
        # Place obstacles randomly
        while len(self.obstacles) < num_obstacles and attempts < 200:
            # Place obstacles away from edges to avoid trapping
            x = random.randint(2, GRID_SIZE - 3)
            y = random.randint(2, GRID_SIZE - 3)
            pos = [x, y]
            
            # Don't place on snake or existing obstacles
            if pos not in snake_body and pos not in self.obstacles:
                self.obstacles.append(pos)
            attempts += 1
    
    def draw(self, screen):
        """Draw all obstacles as gray blocks"""
        for obs in self.obstacles:
            x = obs[0] * CELL_SIZE
            y = obs[1] * CELL_SIZE
            # Draw main block
            pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE))
            # Draw inner darker block for 3D effect
            pygame.draw.rect(screen, (80, 80, 80), (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4))
            # Draw border
            pygame.draw.rect(screen, (50, 50, 50), (x, y, CELL_SIZE, CELL_SIZE), 1)