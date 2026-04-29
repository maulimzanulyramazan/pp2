# Drawing tools for paint application

import pygame
import math
from shapes import Rectangle, Square, Circle, RightTriangle, EquilateralTriangle, Rhombus

class Tool:
    # Base class for all drawing tools
    def __init__(self, name, cursor_size=5):
        self.name = name            # Tool name
        self.cursor_size = cursor_size  # Size of cursor
    
    def on_mouse_down(self, pos):
        pass  # Called when mouse button pressed
    
    def on_mouse_up(self, pos, start_pos, screen, color, thickness):
        pass  # Called when mouse button released
    
    def on_mouse_move(self, current_pos, last_pos, screen, color, thickness):
        pass  # Called when mouse moves while drawing

class PencilTool(Tool):
    # Freehand drawing tool
    def __init__(self):
        super().__init__("pencil", 5)
    
    def on_mouse_move(self, current_pos, last_pos, screen, color, thickness):
        # Draw when mouse moves with button pressed
        if last_pos is None or current_pos is None:
            return current_pos
        self.draw_line(screen, last_pos, current_pos, color, thickness)
        return current_pos
    
    def draw_line(self, screen, p1, p2, color, thickness):
        # Draw smooth line between two points
        dx = p2[0] - p1[0]          # Change in X
        dy = p2[1] - p1[1]          # Change in Y
        dist = max(abs(dx), abs(dy))  # Number of points to draw
        
        if dist == 0:
            pygame.draw.circle(screen, color, p1, thickness)  # Single dot
            return
        
        for i in range(dist + 1):
            t = i / dist            # Ratio from 0 to 1
            x = int(p1[0] + dx * t) # Interpolated X
            y = int(p1[1] + dy * t) # Interpolated Y
            pygame.draw.circle(screen, color, (x, y), thickness)  # Draw circle at point

class LineTool(Tool):
    # Straight line tool with preview
    def __init__(self):
        super().__init__("line", 2)
        self.preview_pos = None     # Current mouse position for preview
    
    def on_mouse_down(self, pos):
        self.preview_pos = pos      # Save starting point
    
    def on_mouse_move(self, current_pos, last_pos, screen, color, thickness):
        self.preview_pos = current_pos  # Update preview position
        return last_pos
    
    def on_mouse_up(self, pos, start_pos, screen, color, thickness):
        # Draw final line when mouse released
        if start_pos is None:
            return
        pygame.draw.line(screen, color, start_pos, pos, thickness)
        self.preview_pos = None
    
    def draw_preview(self, screen, start_pos, color, thickness):
        # Show line while dragging
        if self.preview_pos and start_pos:
            pygame.draw.line(screen, color, start_pos, self.preview_pos, thickness)

class EraserTool(Tool):
    # Eraser tool (draws white)
    def __init__(self):
        super().__init__("eraser", 10)
    
    def on_mouse_move(self, current_pos, last_pos, screen, color, thickness):
        # Draw white line to erase
        if last_pos is None or current_pos is None:
            return current_pos
        pencil = PencilTool()
        pencil.draw_line(screen, last_pos, current_pos, (255, 255, 255), thickness)
        return current_pos

class RectangleTool(Tool):
    # Rectangle drawing tool
    def __init__(self):
        super().__init__("rect", 2)
    
    def on_mouse_up(self, pos, start_pos, screen, color, thickness):
        if start_pos is None:
            return
        shape = Rectangle(color, thickness)
        shape.draw(screen, start_pos, pos)

class SquareTool(Tool):
    # Square drawing tool
    def __init__(self):
        super().__init__("square", 2)
    
    def on_mouse_up(self, pos, start_pos, screen, color, thickness):
        if start_pos is None:
            return
        shape = Square(color, thickness)
        shape.draw(screen, start_pos, pos)

class CircleTool(Tool):
    # Circle drawing tool
    def __init__(self):
        super().__init__("circle", 2)
    
    def on_mouse_up(self, pos, start_pos, screen, color, thickness):
        if start_pos is None:
            return
        shape = Circle(color, thickness)
        shape.draw(screen, start_pos, pos)

class RightTriangleTool(Tool):
    # Right triangle tool
    def __init__(self):
        super().__init__("right_triangle", 2)
    
    def on_mouse_up(self, pos, start_pos, screen, color, thickness):
        if start_pos is None:
            return
        shape = RightTriangle(color, thickness)
        shape.draw(screen, start_pos, pos)

class EquilateralTriangleTool(Tool):
    # Equilateral triangle tool
    def __init__(self):
        super().__init__("equilateral", 2)
    
    def on_mouse_up(self, pos, start_pos, screen, color, thickness):
        if start_pos is None:
            return
        shape = EquilateralTriangle(color, thickness)
        shape.draw(screen, start_pos, pos)

class RhombusTool(Tool):
    # Rhombus (diamond) tool
    def __init__(self):
        super().__init__("rhombus", 2)
    
    def on_mouse_up(self, pos, start_pos, screen, color, thickness):
        if start_pos is None:
            return
        shape = Rhombus(color, thickness)
        shape.draw(screen, start_pos, pos)

class FloodFillTool(Tool):
    # Flood fill tool - fills connected area with color
    def __init__(self):
        super().__init__("flood_fill", 1)
        self.fill_stack = []  # Stack for non-recursive filling
    
    def on_mouse_down(self, pos):
        pass
    
    def flood_fill(self, screen, start_x, start_y, target_color, fill_color):
        # Non-recursive flood fill using stack (avoids recursion limit)
        width = screen.get_width()
        height = screen.get_height()
        
        # Check if start point is already filled
        try:
            if screen.get_at((start_x, start_y))[:3] == fill_color:
                return
        except:
            return
        
        # Stack for pixels to fill
        stack = [(start_x, start_y)]
        
        while stack:
            x, y = stack.pop()
            
            # Check bounds
            if x < 0 or x >= width or y < 0 or y >= height:
                continue
            
            # Get current pixel color
            try:
                current_color = screen.get_at((x, y))[:3]
            except:
                continue
            
            # Fill if color matches target
            if current_color == target_color:
                screen.set_at((x, y), fill_color)
                
                # Add neighboring pixels to stack
                stack.append((x + 1, y))  # Right
                stack.append((x - 1, y))  # Left
                stack.append((x, y + 1))  # Down
                stack.append((x, y - 1))  # Up
    
    def on_mouse_up(self, pos, start_pos, screen, color, thickness):
        # Fill area when mouse clicked
        try:
            # Get color at click position
            target_color = screen.get_at(pos)[:3]
            # Fill only if different from current color
            if target_color != color:
                self.flood_fill(screen, pos[0], pos[1], target_color, color)
        except:
            pass

class TextTool(Tool):
    # Text placement tool
    def __init__(self):
        super().__init__("text", 1)
        self.active = False         # Is text tool active
        self.text = ""              # Current text being typed
        self.position = None        # Position on canvas
        self.font = pygame.font.Font(None, 24)  # Default font
    
    def on_mouse_down(self, pos):
        # Start text input at clicked position
        if not self.active:
            self.active = True
            self.position = pos
            self.text = ""
    
    def add_char(self, char):
        # Add character to text
        self.text += char
    
    def backspace(self):
        # Remove last character
        self.text = self.text[:-1]
    
    def confirm(self, screen, color):
        # Draw text permanently on canvas
        if self.position and self.text:
            text_surface = self.font.render(self.text, True, color)
            screen.blit(text_surface, self.position)
        self.cancel()
    
    def cancel(self):
        # Cancel text input
        self.active = False
        self.text = ""
        self.position = None
    
    def draw_preview(self, screen, color):
        # Show text preview while typing
        if self.active and self.position:
            text_surface = self.font.render(self.text + "|", True, color)
            screen.blit(text_surface, self.position)