"""
Drawing tools for Paint Application
"""

import pygame
import math
from shapes import Rectangle, Square, Circle, RightTriangle, EquilateralTriangle, Rhombus

class Tool:
    """Base class for all drawing tools"""
    def __init__(self, name, cursor_size=5):
        self.name = name                # Tool name
        self.cursor_size = cursor_size  # Brush/cursor size
    
    def on_mouse_down(self, pos):
        pass  # Called when mouse button pressed
    
    def on_mouse_up(self, pos, start_pos, screen, color, thickness):
        pass  # Called when mouse button released
    
    def on_mouse_move(self, current_pos, last_pos, screen, color, thickness):
        pass  # Called when mouse moved while drawing

class DrawTool(Tool):
    """Free drawing tool"""
    def __init__(self):
        super().__init__("draw", 5)     # Call parent constructor
    
    def on_mouse_move(self, current_pos, last_pos, screen, color, thickness):
        if last_pos is None or current_pos is None:  # If no previous position
            return current_pos                       # Just return current pos
        self.draw_line(screen, last_pos, current_pos, color, thickness)  # Draw line
        return current_pos                           # Update last position
    
    def draw_line(self, screen, p1, p2, color, thickness):
        dx = p2[0] - p1[0]      # Change in X
        dy = p2[1] - p1[1]      # Change in Y
        dist = max(abs(dx), abs(dy))  # Number of points to draw
        
        if dist == 0:           # If same point
            pygame.draw.circle(screen, color, p1, thickness)  # Draw single dot
            return
        
        for i in range(dist + 1):       # Loop through all points
            t = i / dist                # Ratio (0 to 1)
            x = int(p1[0] + dx * t)     # Interpolated X
            y = int(p1[1] + dy * t)     # Interpolated Y
            pygame.draw.circle(screen, color, (x, y), thickness)  # Draw circle at point

class EraserTool(Tool):
    """Eraser tool"""
    def __init__(self):
        super().__init__("eraser", 10)  # Larger cursor for eraser
    
    def on_mouse_move(self, current_pos, last_pos, screen, color, thickness):
        if last_pos is None or current_pos is None:
            return current_pos
        draw_tool = DrawTool()          # Create temporary draw tool
        draw_tool.draw_line(screen, last_pos, current_pos, (255, 255, 255), thickness)  # Draw white (erase)
        return current_pos

class RectangleTool(Tool):
    """Rectangle tool"""
    def __init__(self):
        super().__init__("rect", 2)     # Thin line for shapes
    
    def on_mouse_up(self, pos, start_pos, screen, color, thickness):
        if start_pos is None:           # If no start position
            return                      # Do nothing
        shape = Rectangle(color, thickness)  # Create rectangle shape
        shape.draw(screen, start_pos, pos)   # Draw it

class SquareTool(Tool):
    """Square tool (Task 1)"""
    def __init__(self):
        super().__init__("square", 2)
    
    def on_mouse_up(self, pos, start_pos, screen, color, thickness):
        if start_pos is None:
            return
        shape = Square(color, thickness)  # Create square shape
        shape.draw(screen, start_pos, pos)  # Draw it

class CircleTool(Tool):
    """Circle tool"""
    def __init__(self):
        super().__init__("circle", 2)
    
    def on_mouse_up(self, pos, start_pos, screen, color, thickness):
        if start_pos is None:
            return
        shape = Circle(color, thickness)  # Create circle shape
        shape.draw(screen, start_pos, pos)  # Draw it

class RightTriangleTool(Tool):
    """Right triangle tool (Task 2)"""
    def __init__(self):
        super().__init__("right_triangle", 2)
    
    def on_mouse_up(self, pos, start_pos, screen, color, thickness):
        if start_pos is None:
            return
        shape = RightTriangle(color, thickness)  # Create right triangle
        shape.draw(screen, start_pos, pos)        # Draw it

class EquilateralTriangleTool(Tool):
    """Equilateral triangle tool (Task 3)"""
    def __init__(self):
        super().__init__("equilateral", 2)
    
    def on_mouse_up(self, pos, start_pos, screen, color, thickness):
        if start_pos is None:
            return
        shape = EquilateralTriangle(color, thickness)  # Create equilateral triangle
        shape.draw(screen, start_pos, pos)              # Draw it

class RhombusTool(Tool):
    """Rhombus tool (Task 4)"""
    def __init__(self):
        super().__init__("rhombus", 2)
    
    def on_mouse_up(self, pos, start_pos, screen, color, thickness):
        if start_pos is None:
            return
        shape = Rhombus(color, thickness)  # Create rhombus
        shape.draw(screen, start_pos, pos)  # Draw it