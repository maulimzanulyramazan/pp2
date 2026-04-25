import pygame  # Import pygame for drawing
import random  # Import random for random positions/colors
from utils import WIDTH, HEIGHT, LEFT_BOUNDARY, RIGHT_BOUNDARY, BLACK, ENEMY_COLORS, screen  # Import constants

class Enemy:
    """Enemy car class - moves downward automatically"""
    
    def __init__(self, speed_increase=0):
        """Initialize enemy car above screen"""
        self.width = 45  # Car width in pixels
        self.height = 70  # Car height in pixels
        self.x = random.randint(LEFT_BOUNDARY, RIGHT_BOUNDARY)  # Random X position
        self.y = -self.height  # Start above screen (negative Y)
        self.base_speed = random.randint(4, 7)  # Random base speed (4 to 7)
        self.speed = self.base_speed + speed_increase  # Add speed bonus from coins
        self.color = random.choice(ENEMY_COLORS)  # Random color from list
    
    def move(self):
        """Move enemy car downward"""
        self.y += self.speed  # Add speed to Y coordinate
    
    def draw(self):
        """Draw enemy car on screen"""
        # Main car body with random color
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # Black border around car
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)
        # Windshield (top window) - light blue
        pygame.draw.rect(screen, (150, 150, 200), (self.x + 5, self.y + 5, self.width - 10, 20))
        # Back window - light blue
        pygame.draw.rect(screen, (150, 150, 200), (self.x + 5, self.y + 45, self.width - 10, 15))
    
    def get_rect(self):
        """Return collision rectangle for enemy"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def off_screen(self):
        """Check if enemy has passed below screen"""
        return self.y > HEIGHT  # True when Y > screen height
    
    def reset(self, speed_increase=0):
        """Reset enemy at top with new random position and speed"""
        self.x = random.randint(LEFT_BOUNDARY, RIGHT_BOUNDARY)  # New random X
        self.y = -self.height  # Reset to top
        self.base_speed = random.randint(4, 7)  # New random base speed
        self.speed = self.base_speed + speed_increase  # Update speed with bonus
        self.color = random.choice(ENEMY_COLORS)  # New random color