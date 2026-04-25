import pygame  # Import pygame for drawing
from utils import WIDTH, HEIGHT, WHITE, GRAY, LIGHT_GRAY, screen  # Import constants

def draw_road():
    """Draw road, sidewalks, and lane markings"""
    # Main road surface (gray asphalt)
    pygame.draw.rect(screen, GRAY, (80, 0, WIDTH - 160, HEIGHT))
    
    # Left sidewalk/grass area
    pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, 80, HEIGHT))
    
    # Right sidewalk/grass area
    pygame.draw.rect(screen, LIGHT_GRAY, (WIDTH - 80, 0, 80, HEIGHT))
    
    # Dashed center line (white rectangles every 50 pixels)
    for y in range(0, HEIGHT, 50):  # Loop from 0 to HEIGHT in steps of 50
        pygame.draw.rect(screen, WHITE, (WIDTH//2 - 5, y, 10, 30))
    
    # Left road edge line (solid white line)
    pygame.draw.line(screen, WHITE, (80, 0), (80, HEIGHT), 3)
    
    # Right road edge line (solid white line)
    pygame.draw.line(screen, WHITE, (WIDTH - 80, 0), (WIDTH - 80, HEIGHT), 3)