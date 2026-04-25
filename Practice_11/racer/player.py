import pygame  # Import pygame for drawing
from utils import WIDTH, HEIGHT, LEFT_BOUNDARY, RIGHT_BOUNDARY, RED, BLACK, screen  # Import constants

class Player:
    """Player's car class"""
    
    def __init__(self):
        """Initialize player car at bottom center"""
        self.width = 45  # Car width in pixels
        self.height = 70  # Car height in pixels
        self.x = WIDTH // 2 - self.width // 2  # Center X position
        self.y = HEIGHT - 100  # Bottom position (100px from bottom)
        self.speed = 6  # Movement speed (pixels per frame)
    
    def move(self, keys):
        """Move player car left/right based on keyboard input"""
        # Move left when LEFT arrow pressed and car not at left boundary
        if keys[pygame.K_LEFT] and self.x > LEFT_BOUNDARY:
            self.x -= self.speed  # Decrease X coordinate
            
        # Move right when RIGHT arrow pressed and car not at right boundary
        if keys[pygame.K_RIGHT] and self.x < RIGHT_BOUNDARY:
            self.x += self.speed  # Increase X coordinate
    
    def draw(self):
        """Draw player car on screen"""
        # Main car body (red rectangle)
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        # Black border around car
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)
        # Windshield (top window) - light blue
        pygame.draw.rect(screen, (100, 100, 200), (self.x + 5, self.y + 5, self.width - 10, 20))
        # Back window - light blue
        pygame.draw.rect(screen, (100, 100, 200), (self.x + 5, self.y + 45, self.width - 10, 15))
    
    def get_rect(self):
        """Return collision rectangle for player"""
        return pygame.Rect(self.x, self.y, self.width, self.height)