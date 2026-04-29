# Shape classes for drawing different shapes

import pygame
import math

class Shape:
    # Base class for all shapes
    def __init__(self, color, thickness):
        self.color = color          # Save shape color
        self.thickness = thickness  # Save line thickness
    
    def draw(self, screen, start_pos, end_pos):
        pass  # Will be overridden by child classes

class Rectangle(Shape):
    # Draw rectangle from start to end position
    def draw(self, screen, start_pos, end_pos):
        x = min(start_pos[0], end_pos[0])          # Left X coordinate
        y = min(start_pos[1], end_pos[1])          # Top Y coordinate
        width = abs(start_pos[0] - end_pos[0])     # Rectangle width
        height = abs(start_pos[1] - end_pos[1])    # Rectangle height
        pygame.draw.rect(screen, self.color, (x, y, width, height), self.thickness)

class Square(Shape):
    # Draw square (equal width and height)
    def draw(self, screen, start_pos, end_pos):
        x = min(start_pos[0], end_pos[0])                     # Left X
        y = min(start_pos[1], end_pos[1])                     # Top Y
        width = min(abs(start_pos[0] - end_pos[0]), abs(start_pos[1] - end_pos[1]))  # Smaller side
        pygame.draw.rect(screen, self.color, (x, y, width, width), self.thickness)

class Circle(Shape):
    # Draw circle from bounding box
    def draw(self, screen, start_pos, end_pos):
        center = ((start_pos[0] + end_pos[0]) // 2, (start_pos[1] + end_pos[1]) // 2)  # Middle point
        radius = max(abs(start_pos[0] - end_pos[0]) // 2, abs(start_pos[1] - end_pos[1]) // 2)  # Half of distance
        pygame.draw.circle(screen, self.color, center, radius, self.thickness)

class RightTriangle(Shape):
    # Draw right triangle (starts at top-left, goes to bottom-right)
    def draw(self, screen, start_pos, end_pos):
        # Three points: top-left, top-right, bottom-left (right angle)
        points = [start_pos, (end_pos[0], start_pos[1]), (start_pos[0], end_pos[1])]
        pygame.draw.polygon(screen, self.color, points, self.thickness)

class EquilateralTriangle(Shape):
    # Draw equilateral triangle (all sides equal)
    def draw(self, screen, start_pos, end_pos):
        # Get width from mouse drag
        width = end_pos[0] - start_pos[0]
        # Height of equilateral triangle = width * sqrt(3)/2
        height = abs(width) * math.sqrt(3) / 2
        
        # Check if dragging down or up
        if end_pos[1] > start_pos[1]:
            # Dragging down - triangle points down
            points = [
                start_pos,                                    # Left corner
                (start_pos[0] + width, start_pos[1]),        # Right corner
                (start_pos[0] + width // 2, start_pos[1] + height)  # Bottom corner
            ]
        else:
            # Dragging up - triangle points up
            points = [
                start_pos,                                    # Left corner
                (start_pos[0] + width, start_pos[1]),        # Right corner
                (start_pos[0] + width // 2, start_pos[1] - height)  # Top corner
            ]
        pygame.draw.polygon(screen, self.color, points, self.thickness)

class Rhombus(Shape):
    # Draw rhombus (diamond shape)
    def draw(self, screen, start_pos, end_pos):
        # Calculate center point
        center_x = (start_pos[0] + end_pos[0]) // 2
        center_y = (start_pos[1] + end_pos[1]) // 2
        # Half widths horizontally and vertically
        dx = abs(start_pos[0] - end_pos[0]) // 2
        dy = abs(start_pos[1] - end_pos[1]) // 2
        # Four corners of rhombus
        points = [
            (center_x, center_y - dy),  # Top point
            (center_x + dx, center_y),  # Right point
            (center_x, center_y + dy),  # Bottom point
            (center_x - dx, center_y)   # Left point
        ]
        pygame.draw.polygon(screen, self.color, points, self.thickness)