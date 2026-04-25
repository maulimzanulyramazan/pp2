"""
Food class - handles food with different weights and timer (Tasks 1 & 2)
"""

import pygame  # Import pygame for drawing
import random  # Import random for random position generation
import time  # Import time for timer functionality
from utils import CELL_SIZE  # Import cell size constant

# Define food colors
RED = (255, 0, 0)  # Normal food color
GOLD = (255, 215, 0)  # Gold food color (high value)
BLUE = (0, 0, 255)  # Timed food color
WHITE = (255, 255, 255)  # White for shine effect
DARK_BLUE = (0, 0, 200)  # Dark blue for border

class Food:
    """Food that snake eats - has different weights and can expire"""
    
    def __init__(self, snake_body):
        """Initialize food with random type and position"""
        self.type = None  # Food type: normal, gold, or timed
        self.position = [0, 0]  # Food position [x, y] in pixels
        self.weight = 0  # Point value (1, 2, or 3)
        self.spawn_time = None  # When food appeared (for timed food)
        self.lifetime = None  # How many seconds until expiration
        self.randomize_food(snake_body)  # Generate random food
    
    def randomize_food(self, snake_body):
        """Task 1: Randomly generate food with different weights"""
        from utils import WIDTH, HEIGHT, CELL_SIZE  # Import window dimensions
        
        # Randomly choose food type with different probabilities
        rand = random.random()  # Generate random number between 0 and 1
        
        if rand < 0.6:  # 60% chance (0 to 0.6)
            self.type = "normal"  # Normal food
            self.weight = 1  # Worth 1 point
            self.lifetime = None  # Never expires
            
        elif rand < 0.8:  # 20% chance (0.6 to 0.8)
            self.type = "gold"  # Gold food
            self.weight = 3  # Worth 3 points (high value)
            self.lifetime = None  # Never expires
            
        else:  # 20% chance (0.8 to 1.0)
            self.type = "timed"  # Timed food
            self.weight = 2  # Worth 2 points
            self.lifetime = 3  # Expires after 3 seconds
            self.spawn_time = time.time()  # Record when food spawned
        
        # Find empty position not occupied by snake
        while True:  # Keep trying until empty spot found
            # Calculate grid dimensions
            max_x = WIDTH // CELL_SIZE  # Number of cells horizontally
            max_y = HEIGHT // CELL_SIZE  # Number of cells vertically
            
            # Random cell coordinates
            x = random.randint(0, max_x - 1) * CELL_SIZE  # X in pixels
            y = random.randint(0, max_y - 1) * CELL_SIZE  # Y in pixels
            new_pos = [x, y]  # Position as list
            
            if new_pos not in snake_body:  # If position is not on snake
                self.position = new_pos  # Set this position
                break  # Exit loop
    
    def is_expired(self):
        """Task 2: Check if timed food has disappeared"""
        if self.lifetime is None:  # Normal food never expires
            return False  # Not expired
        
        current_time = time.time()  # Get current time
        elapsed = current_time - self.spawn_time  # Calculate time since spawn
        return elapsed >= self.lifetime  # True if older than lifetime, False otherwise
    
    def draw(self, screen):
        """Draw food on screen with different appearances"""
        if self.type == "normal":
            # Draw normal red food (square)
            pygame.draw.rect(screen, RED, 
                           (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))
            
        elif self.type == "gold":
            # Draw gold food with shine effect
            pygame.draw.rect(screen, GOLD, 
                           (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))
            # Draw inner shine (lighter gold)
            pygame.draw.rect(screen, (255, 255, 150), 
                           (self.position[0] + 2, self.position[1] + 2, 
                            CELL_SIZE - 4, CELL_SIZE - 4))
            
        elif self.type == "timed":
            # Draw timed food (blue with border)
            pygame.draw.rect(screen, BLUE, 
                           (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))
            # Draw dark blue border
            pygame.draw.rect(screen, DARK_BLUE, 
                           (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE), 2)
    
    def get_weight(self):
        """Return point value of this food"""
        return self.weight  # Returns 1, 2, or 3
    
    def get_type(self):
        """Return food type string"""
        return self.type  # Returns "normal", "gold", or "timed"