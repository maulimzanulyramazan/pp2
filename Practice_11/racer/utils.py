import pygame  # Import pygame library

pygame.init()  # Initialize all pygame modules

# Window size
WIDTH = 800  # Screen width in pixels
HEIGHT = 600  # Screen height in pixels

# Road boundaries (where cars can drive)
LEFT_BOUNDARY = 100  # Leftmost position for cars (pixels from left edge)
RIGHT_BOUNDARY = WIDTH - 145  # Rightmost position for cars (655 pixels)

# Game settings
MAX_ENEMIES = 4  # Maximum number of enemy cars on road
MAX_COINS = 6  # Maximum number of coins on screen

# Colors (RGB values)
BLACK = (0, 0, 0)  # Color for text and borders
WHITE = (255, 255, 255)  # Color for road lines
GRAY = (50, 50, 50)  # Color for road surface
LIGHT_GRAY = (80, 80, 80)  # Color for sidewalks/grass
RED = (255, 0, 0)  # Player car color
BLUE = (0, 0, 255)  # Enemy car color option 1
GREEN = (0, 255, 0)  # Enemy car color option 2
YELLOW = (255, 255, 0)  # Color for UI text
ORANGE = (255, 165, 0)  # Enemy car color option 3
PURPLE = (128, 0, 128)  # Enemy car color option 4
GOLD = (255, 215, 0)  # Gold coin color (3 points)
BRONZE = (205, 127, 50)  # Bronze coin color (1 point)
SILVER = (192, 192, 192)  # Silver coin color (2 points)

# Enemy car colors list
ENEMY_COLORS = [BLUE, GREEN, ORANGE, PURPLE, (200, 0, 200), (0, 150, 150)]

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")  # Window title
clock = pygame.time.Clock()  # For controlling game speed
font = pygame.font.Font(None, 36)  # Main font (36 pixels)
small_font = pygame.font.Font(None, 20)  # Small font for coins (20 pixels)