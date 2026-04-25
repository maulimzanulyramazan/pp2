"""
Shape drawing classes for Paint Application
"""

import pygame
import math

class Shape:
    """Base class for all shapes"""
    def __init__(self, color, thickness):   # Constructor
        self.color = color                  # Store color
        self.thickness = thickness          # Store line thickness
    
    def draw(self, screen, start_pos, end_pos):  # Draw method (to override)
        pass                                     # Placeholder for child classes

class Rectangle(Shape):
    """Rectangle shape"""
    def draw(self, screen, start_pos, end_pos):
        x1, y1 = start_pos          # First corner X and Y
        x2, y2 = end_pos            # Second corner X and Y
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))  # Create rectangle
        pygame.draw.rect(screen, self.color, rect, self.thickness)  # Draw rectangle

class Square(Shape):
    """Square shape (Task 1)"""
    def draw(self, screen, start_pos, end_pos):
        x1, y1 = start_pos          # First corner position
        x2, y2 = end_pos            # Second corner position
        side = min(abs(x1 - x2), abs(y1 - y2))  # Take smaller side
        
        # Determine direction of dragging
        if x2 > x1 and y2 > y1:      # Dragging down-right
            rect = pygame.Rect(x1, y1, side, side)   # Square down-right
        elif x2 > x1 and y2 < y1:    # Dragging up-right
            rect = pygame.Rect(x1, y1 - side, side, side)  # Square up-right
        elif x2 < x1 and y2 > y1:    # Dragging down-left
            rect = pygame.Rect(x1 - side, y1, side, side)  # Square down-left
        else:                         # Dragging up-left
            rect = pygame.Rect(x1 - side, y1 - side, side, side)  # Square up-left
        
        pygame.draw.rect(screen, self.color, rect, self.thickness)  # Draw square

class Circle(Shape):
    """Circle shape"""
    def draw(self, screen, start_pos, end_pos):
        dx = end_pos[0] - start_pos[0]      # Difference in X
        dy = end_pos[1] - start_pos[1]      # Difference in Y
        radius = int(math.sqrt(dx * dx + dy * dy))  # Pythagorean theorem
        pygame.draw.circle(screen, self.color, start_pos, radius, self.thickness)  # Draw circle

class RightTriangle(Shape):
    """Right triangle shape (Task 2)"""
    def draw(self, screen, start_pos, end_pos):
        x1, y1 = start_pos   # Triangle corner 1
        x2, y2 = end_pos     # Triangle corner 2
        
        # Define three points based on drag direction
        if x2 > x1 and y2 > y1:      # Dragging down-right
            points = [(x1, y1), (x2, y1), (x1, y2)]  # Right angle at top-left
        elif x2 > x1 and y2 < y1:    # Dragging up-right
            points = [(x1, y1), (x2, y1), (x1, y2)]  # Right angle at bottom-left
        elif x2 < x1 and y2 > y1:    # Dragging down-left
            points = [(x1, y1), (x1, y2), (x2, y2)]  # Right angle at top-right
        else:                         # Dragging up-left
            points = [(x1, y1), (x1, y2), (x2, y2)]  # Right angle at bottom-right
        
        pygame.draw.polygon(screen, self.color, points, self.thickness)  # Draw triangle

class EquilateralTriangle(Shape):
    """Equilateral triangle shape (Task 3)"""
    def draw(self, screen, start_pos, end_pos):
        x1, y1 = start_pos      # First corner
        x2, y2 = end_pos        # Second corner
        
        side = abs(x2 - x1)                              # Length of side
        height = side * math.sqrt(3) / 2                 # Height formula: h = side * √3/2
        
        # Calculate third vertex position
        if x2 > x1:                                      # If dragging right
            third_x = x1 + side / 2                      # Middle of base
            third_y = y1 - height if y2 < y1 else y1 + height  # Above or below
        else:                                            # If dragging left
            third_x = x2 + side / 2                      # Middle of base
            third_y = y2 - height if y1 < y2 else y2 + height  # Above or below
        
        points = [(x1, y1), (x2, y2), (third_x, third_y)]  # Three points of triangle
        pygame.draw.polygon(screen, self.color, points, self.thickness)  # Draw triangle

class Rhombus(Shape):
    """Rhombus (Diamond) shape (Task 4)"""
    def draw(self, screen, start_pos, end_pos):
        x1, y1 = start_pos      # Corner 1
        x2, y2 = end_pos        # Corner 2 (opposite)
        
        center_x = (x1 + x2) / 2      # Middle X coordinate
        center_y = (y1 + y2) / 2      # Middle Y coordinate
        width = abs(x2 - x1) / 2      # Half of total width
        height = abs(y2 - y1) / 2     # Half of total height
        
        points = [
            (center_x, center_y - height),  # Top point
            (center_x + width, center_y),   # Right point
            (center_x, center_y + height),  # Bottom point
            (center_x - width, center_y)    # Left point
        ]
        
        pygame.draw.polygon(screen, self.color, points, self.thickness)  # Draw rhombus