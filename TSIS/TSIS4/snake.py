# snake.py - Snake class (FIXED movement)
import pygame
from utils import CELL_SIZE, GREEN, DARK_GREEN, BRIGHT_GREEN, BLACK, WHITE, GRID_SIZE

class Snake:
    def __init__(self):
        center_x = GRID_SIZE // 2
        center_y = GRID_SIZE // 2
        self.body = [
            [center_x, center_y],
            [center_x - 1, center_y],
            [center_x - 2, center_y]
        ]
        self.direction = "RIGHT"
        self.next_direction = "RIGHT"  # Store next direction for smooth movement
        self.grow = False
    
    def change_direction(self, new_dir):
        """Change direction - prevents reversing"""
        opposite = {
            "RIGHT": "LEFT",
            "LEFT": "RIGHT",
            "UP": "DOWN", 
            "DOWN": "UP"
        }
        # Don't allow reverse direction
        if new_dir != opposite.get(self.direction):
            self.next_direction = new_dir
    
    def move(self):
        """Move snake - use stored next direction"""
        # Apply queued direction
        self.direction = self.next_direction
        
        head = self.body[0].copy()
        
        if self.direction == "RIGHT":
            head[0] += 1
        elif self.direction == "LEFT":
            head[0] -= 1
        elif self.direction == "UP":
            head[1] -= 1
        elif self.direction == "DOWN":
            head[1] += 1
        
        self.body.insert(0, head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def check_wall_collision(self):
        head = self.body[0]
        return (head[0] < 0 or head[0] >= GRID_SIZE or
                head[1] < 0 or head[1] >= GRID_SIZE)
    
    def check_self_collision(self):
        head = self.body[0]
        return head in self.body[1:]
    
    def eat_food(self, food_pos):
        if self.body[0] == food_pos:
            self.grow = True
            return True
        return False
    
    def shrink(self, amount=2):
        for _ in range(min(amount, len(self.body) - 1)):
            self.body.pop()
        return len(self.body) > 0
    
    def draw(self, screen):
        for i, segment in enumerate(self.body):
            x = segment[0] * CELL_SIZE
            y = segment[1] * CELL_SIZE
            
            if i == 0:
                color = BRIGHT_GREEN
            else:
                color = DARK_GREEN if i % 2 else GREEN
            
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
            
            # Eyes on head
            if i == 0:
                eye_size = 3
                if self.direction == "RIGHT":
                    pygame.draw.circle(screen, WHITE, (x + CELL_SIZE - 6, y + 6), eye_size)
                    pygame.draw.circle(screen, WHITE, (x + CELL_SIZE - 6, y + CELL_SIZE - 6), eye_size)
                elif self.direction == "LEFT":
                    pygame.draw.circle(screen, WHITE, (x + 6, y + 6), eye_size)
                    pygame.draw.circle(screen, WHITE, (x + 6, y + CELL_SIZE - 6), eye_size)
                elif self.direction == "UP":
                    pygame.draw.circle(screen, WHITE, (x + 6, y + 6), eye_size)
                    pygame.draw.circle(screen, WHITE, (x + CELL_SIZE - 6, y + 6), eye_size)
                else:
                    pygame.draw.circle(screen, WHITE, (x + 6, y + CELL_SIZE - 6), eye_size)
                    pygame.draw.circle(screen, WHITE, (x + CELL_SIZE - 6, y + CELL_SIZE - 6), eye_size)