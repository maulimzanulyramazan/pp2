"""
User Interface components for Paint Application
"""

import pygame

class UI:
    """User interface manager"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width      # Window width
        self.screen_height = screen_height    # Window height
        self.ui_height = 80                   # Height of UI area
        self.font = pygame.font.Font(None, 24)       # Regular font
        self.small_font = pygame.font.Font(None, 18) # Small font for help text
    
    def draw_text(self, screen, mode, color, thickness):
        """Draw text information on screen"""
        # Clear UI area (white rectangle)
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, self.screen_width, self.ui_height))
        
        # Line 1: Current mode, color and thickness
        text1 = self.font.render(f"Mode: {mode}  Color: {color}  Size: {thickness}", True, (0, 0, 0))
        screen.blit(text1, (10, 10))  # Draw at x=10, y=10
        
        # Line 2: Tool shortcuts (first row)
        text2 = self.small_font.render("1-draw 2-rect 3-circle 4-eraser 5-square 6-right-triangle", True, (0, 0, 0))
        screen.blit(text2, (10, 35))  # Draw at x=10, y=35
        
        # Line 3: Tool shortcuts (second row) and color keys
        text3 = self.small_font.render("7-equilateral 8-rhombus | R G B | C-clear | +/- size", True, (0, 0, 0))
        screen.blit(text3, (10, 55))  # Draw at x=10, y=55
    
    def draw_color_palette(self, screen, colors, current_color):
        """Draw color palette at the top right"""
        palette_x = self.screen_width - 200  # X position (right side)
        palette_y = 10                       # Y position (top)
        box_size = 25                        # Width and height of color box
        spacing = 5                          # Space between boxes
        
        for i, color in enumerate(colors):   # Loop through all colors
            x = palette_x + (box_size + spacing) * i  # Calculate X for this box
            y = palette_y                              # Y position
            pygame.draw.rect(screen, color, (x, y, box_size, box_size))  # Draw color box
            pygame.draw.rect(screen, (0, 0, 0), (x, y, box_size, box_size), 1)  # Draw border
            
            # Draw outline for current selected color
            if color == current_color:       # If this is the active color
                pygame.draw.rect(screen, (255, 255, 255), (x-2, y-2, box_size+4, box_size+4), 2)  # White highlight