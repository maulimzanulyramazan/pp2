import pygame  # Import pygame for drawing
import random  # Import random for random generation
from utils import WIDTH, HEIGHT, LEFT_BOUNDARY, RIGHT_BOUNDARY, BRONZE, SILVER, GOLD, font, screen  # Import constants

class Coin:
    """Coin class with different weights (Task 1)"""
    
    def __init__(self, existing_coins=None):
        """Initialize coin with random type and position"""
        self.size = 25  # Coin diameter in pixels
        self.speed = 4  # Falling speed (pixels per frame)
        
        # Task 1: Randomly generate coins with different weights
        rand = random.random()  # Random number between 0 and 1
        
        if rand < 0.6:  # 60% chance for bronze coin
            self.weight = 1  # Worth 1 point
            self.color = BRONZE  # Bronze color (brown-orange)
        elif rand < 0.85:  # 25% chance for silver coin
            self.weight = 2  # Worth 2 points
            self.color = SILVER  # Silver color (gray)
        else:  # 15% chance for gold coin
            self.weight = 3  # Worth 3 points
            self.color = GOLD  # Gold color (yellow)
        
        # Random X position within road boundaries
        self.x = random.randint(LEFT_BOUNDARY + 10, RIGHT_BOUNDARY - self.size - 10)
        self.y = random.randint(-200, -50)  # Start above screen (negative Y)
    
    def move(self):
        """Make coin fall down the screen"""
        self.y += self.speed  # Increase Y coordinate (move down)
    
    def draw(self):
        """Draw coin on screen with weight number inside"""
        # Only draw if coin is visible on screen
        if self.y + self.size > 0 and self.y < HEIGHT:
            # Draw coin as circle
            pygame.draw.circle(screen, self.color, 
                              (self.x + self.size//2, self.y + self.size//2), 
                              self.size//2)
            # Draw black border around coin
            pygame.draw.circle(screen, (0, 0, 0), 
                              (self.x + self.size//2, self.y + self.size//2), 
                              self.size//2, 2)
            # Draw weight number (1, 2, or 3) inside coin
            text = font.render(str(self.weight), True, (0, 0, 0))
            text_x = self.x + self.size//2 - text.get_width()//2  # Center text horizontally
            text_y = self.y + self.size//2 - text.get_height()//2  # Center text vertically
            screen.blit(text, (text_x, text_y))  # Draw number on screen
    
    def get_rect(self):
        """Return collision rectangle for coin"""
        return pygame.Rect(self.x, self.y, self.size, self.size)
    
    def off_screen(self):
        """Check if coin has fallen below screen"""
        return self.y > HEIGHT + 50  # True when Y > screen height + margin
    
    def get_weight(self):
        """Return coin's point value (Task 1)"""
        return self.weight  # Returns 1, 2, or 3