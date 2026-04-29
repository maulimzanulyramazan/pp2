# utils.py - Export all constants for easy import
from config import *

# Export all constants so other files can do: from utils import *
__all__ = [
    'SCREEN_WIDTH', 'SCREEN_HEIGHT', 'CELL_SIZE', 'GRID_SIZE',
    'BLACK', 'WHITE', 'RED', 'GREEN', 'DARK_RED', 'BLUE',
    'YELLOW', 'PURPLE', 'ORANGE', 'GRAY', 'GOLD',
    'DARK_GREEN', 'BRIGHT_GREEN', 'CYAN', 'PINK',
    'INITIAL_SPEED', 'SPEED_INCREMENT', 'FOODS_PER_LEVEL',
    'POWERUP_DURATION', 'POWERUP_DISAPPEAR_TIME', 'OBSTACLE_START_LEVEL'
]

# Short aliases for backward compatibility
WIDTH = SCREEN_WIDTH
HEIGHT = SCREEN_HEIGHT