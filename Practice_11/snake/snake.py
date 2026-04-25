"""
Snake class - handles snake movement, collision, and drawing
"""

import pygame  # Import pygame for drawing
from utils import CELL_SIZE, WHITE, BLACK  # Import constants

# Define snake colors locally
GREEN = (0, 255, 0)  # Normal snake body color
DARK_GREEN = (0, 150, 0)  # Darker shade for stripes
BRIGHT_GREEN = (50, 255, 100)  # Brighter color for head

class Snake:
    """Snake character controlled by player"""
    
    def __init__(self):
        """Initialize snake in the middle of screen with 3 segments"""
        from utils import WIDTH, HEIGHT, CELL_SIZE  # Import window dimensions
        
        center_x = WIDTH // 2  # Calculate center X position
        center_y = HEIGHT // 2  # Calculate center Y position
        
        # Body segments: [x, y] coordinates
        self.body = [
            [center_x, center_y],  # Head at center
            [center_x - CELL_SIZE, center_y],  # First body segment (left of head)
            [center_x - CELL_SIZE * 2, center_y]  # Second body segment (tail)
        ]
        self.direction = "RIGHT"  # Current movement direction
        self.grow = False  # Flag to grow after eating food
    
    def move(self):
        """Move snake one step forward in current direction"""
        from utils import CELL_SIZE  # Import cell size
        
        head = self.body[0].copy()  # Make a copy of head position
        
        # Calculate new head position based on direction
        if self.direction == "RIGHT":
            head[0] += CELL_SIZE  # Move right by one cell
        elif self.direction == "LEFT":
            head[0] -= CELL_SIZE  # Move left by one cell
        elif self.direction == "UP":
            head[1] -= CELL_SIZE  # Move up by one cell
        elif self.direction == "DOWN":
            head[1] += CELL_SIZE  # Move down by one cell
        
        self.body.insert(0, head)  # Add new head at front of body
        
        if not self.grow:  # If not growing (normal movement)
            self.body.pop()  # Remove tail segment
        else:  # If growing (ate food)
            self.grow = False  # Reset grow flag (keep tail segment)
    
    def change_direction(self, new_dir):
        """Change snake direction but prevent reversing into itself"""
        # Only allow direction change if not going opposite direction
        if new_dir == "RIGHT" and self.direction != "LEFT":
            self.direction = new_dir  # Change to right
        elif new_dir == "LEFT" and self.direction != "RIGHT":
            self.direction = new_dir  # Change to left
        elif new_dir == "UP" and self.direction != "DOWN":
            self.direction = new_dir  # Change to up
        elif new_dir == "DOWN" and self.direction != "UP":
            self.direction = new_dir  # Change to down
    
    def check_self_collision(self):
        """Check if snake collides with itself"""
        head = self.body[0]  # Get head position
        return head in self.body[1:]  # True if head touches any body segment
    
    def check_wall_collision(self):
        """Check if snake hits the screen boundaries"""
        from utils import WIDTH, HEIGHT  # Import window dimensions
        
        head = self.body[0]  # Get head position
        
        # Check if head is outside window boundaries
        if head[0] < 0 or head[0] >= WIDTH:  # Left or right wall
            return True
        if head[1] < 0 or head[1] >= HEIGHT:  # Top or bottom wall
            return True
        return False  # No wall collision
    
    def eat_food(self, food_pos):
        """Check if snake eats food at given position"""
        if self.body[0] == food_pos:  # If head position equals food position
            self.grow = True  # Snake will grow on next move
            return True  # Food was eaten
        return False  # No food eaten
    
    def draw(self, screen):
        """Draw snake on screen with different colors for head and body"""
        for i, segment in enumerate(self.body):  # Loop through all body segments with index
            # Head has brighter color
            if i == 0:  # First segment (head)
                color = BRIGHT_GREEN  # Use bright green for head
            else:  # Body segments
                # Alternate colors for stripe effect
                if i % 2 == 0:  # Even index
                    color = GREEN  # Normal green
                else:  # Odd index
                    color = DARK_GREEN  # Dark green for stripe
            
            # Draw snake segment (filled rectangle)
            pygame.draw.rect(screen, color, 
                           (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
            # Draw border around segment (outline)
            pygame.draw.rect(screen, (0, 100, 0), 
                           (segment[0], segment[1], CELL_SIZE, CELL_SIZE), 1)
            
            # Draw eyes on head only
            if i == 0:  # If this is the head segment
                eye_size = 2  # Eye radius in pixels
                
                # Draw eyes based on direction snake is facing
                if self.direction == "RIGHT":  # Facing right
                    # Left eye
                    pygame.draw.circle(screen, WHITE, (segment[0] + CELL_SIZE - 4, segment[1] + 4), eye_size)
                    # Right eye
                    pygame.draw.circle(screen, WHITE, (segment[0] + CELL_SIZE - 4, segment[1] + CELL_SIZE - 5), eye_size)
                    # Pupils (black)
                    pygame.draw.circle(screen, BLACK, (segment[0] + CELL_SIZE - 4, segment[1] + 4), eye_size-1)
                    pygame.draw.circle(screen, BLACK, (segment[0] + CELL_SIZE - 4, segment[1] + CELL_SIZE - 5), eye_size-1)
                    
                elif self.direction == "LEFT":  # Facing left
                    # Left eye
                    pygame.draw.circle(screen, WHITE, (segment[0] + 3, segment[1] + 4), eye_size)
                    # Right eye
                    pygame.draw.circle(screen, WHITE, (segment[0] + 3, segment[1] + CELL_SIZE - 5), eye_size)
                    # Pupils
                    pygame.draw.circle(screen, BLACK, (segment[0] + 3, segment[1] + 4), eye_size-1)
                    pygame.draw.circle(screen, BLACK, (segment[0] + 3, segment[1] + CELL_SIZE - 5), eye_size-1)
                    
                elif self.direction == "UP":  # Facing up
                    # Left eye
                    pygame.draw.circle(screen, WHITE, (segment[0] + 4, segment[1] + 3), eye_size)
                    # Right eye
                    pygame.draw.circle(screen, WHITE, (segment[0] + CELL_SIZE - 5, segment[1] + 3), eye_size)
                    # Pupils
                    pygame.draw.circle(screen, BLACK, (segment[0] + 4, segment[1] + 3), eye_size-1)
                    pygame.draw.circle(screen, BLACK, (segment[0] + CELL_SIZE - 5, segment[1] + 3), eye_size-1)
                    
                else:  # Facing DOWN
                    # Left eye
                    pygame.draw.circle(screen, WHITE, (segment[0] + 4, segment[1] + CELL_SIZE - 4), eye_size)
                    # Right eye
                    pygame.draw.circle(screen, WHITE, (segment[0] + CELL_SIZE - 5, segment[1] + CELL_SIZE - 4), eye_size)
                    # Pupils
                    pygame.draw.circle(screen, BLACK, (segment[0] + 4, segment[1] + CELL_SIZE - 4), eye_size-1)
                    pygame.draw.circle(screen, BLACK, (segment[0] + CELL_SIZE - 5, segment[1] + CELL_SIZE - 4), eye_size-1)