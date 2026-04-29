# config.py - Game configuration constants
import pygame

# ========== SCREEN SETTINGS ==========
SCREEN_WIDTH = 600   # Game window width
SCREEN_HEIGHT = 600  # Game window height
CELL_SIZE = 20       # Size of each snake segment
GRID_SIZE = SCREEN_WIDTH // CELL_SIZE  # 30x30 grid

# ========== COLORS (RGB) ==========
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_RED = (139, 0, 0)      # Poison food color
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
GOLD = (255, 215, 0)        # Gold food color
DARK_GREEN = (0, 150, 0)    # Snake body dark
BRIGHT_GREEN = (50, 255, 100)  # Snake head
CYAN = (0, 255, 255)        # Shield power-up
PINK = (255, 105, 180)      # Speed boost

# ========== GAME SETTINGS ==========
INITIAL_SPEED = 8           # Starting game speed (FPS)
SPEED_INCREMENT = 1         # Speed increase per level
FOODS_PER_LEVEL = 5         # Foods needed to level up
POWERUP_DURATION = 5000     # Power-up lasts 5 seconds (milliseconds)
POWERUP_DISAPPEAR_TIME = 8000  # Power-up disappears after 8 seconds
OBSTACLE_START_LEVEL = 3    # Obstacles start from level 3

# ========== POSTGRESQL SETTINGS ==========
DB_CONFIG = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "550697",
    "port": 2008
}