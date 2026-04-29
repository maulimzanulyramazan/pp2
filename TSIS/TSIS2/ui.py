# User interface components for paint application

import pygame

class UI:
    # Manages all UI elements on screen
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width      # Window width
        self.screen_height = screen_height    # Window height
        self.ui_height = 110                  # Height of UI area
        self.font = pygame.font.Font(None, 24)        # Regular font
        self.small_font = pygame.font.Font(None, 18)  # Small font for help
        self.buttons = []                     # List of UI buttons
        self.setup_buttons()                  # Create buttons
    
    def setup_buttons(self):
        # Create all UI buttons
        button_y = 80                         # Y position for buttons
        
        # Brush size buttons
        sizes = [('S', 2), ('M', 5), ('L', 10)]  # Small, Medium, Large
        for i, (label, size) in enumerate(sizes):
            self.buttons.append({
                'rect': pygame.Rect(10 + i * 40, button_y, 30, 25),
                'type': 'brush_size',
                'value': size,
                'label': label
            })
        
        # Tool buttons
        tools = [
            ('Pencil', 100), ('Line', 160), ('Rect', 220),
            ('Circle', 280), ('Square', 340), ('Fill', 400),
            ('Text', 460), ('Eraser', 520), ('R-Tri', 580), ('E-Tri', 640), ('Rhombus', 700)
        ]
        
        for label, x in tools:
            self.buttons.append({
                'rect': pygame.Rect(x, button_y, 45, 25),
                'type': 'tool',
                'value': label.lower().replace('-', '_'),
                'label': label
            })
    
    def draw_text(self, screen, mode, color, thickness):
        # Draw information text on screen
        # Clear UI area with gray background
        pygame.draw.rect(screen, (230, 230, 230), (0, 0, self.screen_width, self.ui_height))
        # Draw bottom border line
        pygame.draw.line(screen, (0, 0, 0), (0, self.ui_height), (self.screen_width, self.ui_height), 2)
        
        # Show current mode, color, and size
        text1 = self.font.render(f"Mode: {mode}  Color: {color}  Size: {thickness}", True, (0, 0, 0))
        screen.blit(text1, (10, 10))
        
        # Show keyboard shortcuts line 1
        shortcuts1 = "1-Pen 2-Line 3-Rect 4-Circle 5-Square 6-Eraser 7-Fill 8-Text"
        text2 = self.small_font.render(shortcuts1, True, (0, 0, 0))
        screen.blit(text2, (10, 35))
        
        # Show keyboard shortcuts line 2
        shortcuts2 = "9-RTri 0-ETri =-Rhombus | R/G/B/Y/P/O/K | +/- Size | Ctrl+S | C-Clear"
        text3 = self.small_font.render(shortcuts2, True, (0, 0, 0))
        screen.blit(text3, (10, 55))
        
        # Draw brush size buttons
        for button in self.buttons:
            if button['type'] == 'brush_size':
                # Highlight active size
                color_code = (200, 200, 200) if button['value'] == thickness else (150, 150, 150)
                pygame.draw.rect(screen, color_code, button['rect'])
                pygame.draw.rect(screen, (0, 0, 0), button['rect'], 1)
                label_text = self.small_font.render(button['label'], True, (0, 0, 0))
                screen.blit(label_text, (button['rect'].x + 8, button['rect'].y + 5))
        
        # Draw tool buttons with highlight for active tool
        for button in self.buttons:
            if button['type'] == 'tool':
                # Green color for active tool, gray for others
                color_code = (100, 200, 100) if button['value'] == mode else (180, 180, 180)
                pygame.draw.rect(screen, color_code, button['rect'])
                pygame.draw.rect(screen, (0, 0, 0), button['rect'], 1)
                label_text = self.small_font.render(button['label'], True, (0, 0, 0))
                screen.blit(label_text, (button['rect'].x + 3, button['rect'].y + 5))
    
    def draw_color_palette(self, screen, colors, current_color):
        # Draw color palette at top right
        palette_x = self.screen_width - 260  # X position (right side)
        palette_y = 10                       # Y position (top)
        box_size = 30                        # Size of each color box
        spacing = 5                          # Space between boxes
        
        for i, color in enumerate(colors):
            x = palette_x + (box_size + spacing) * i  # Calculate X position
            y = palette_y
            pygame.draw.rect(screen, color, (x, y, box_size, box_size))
            pygame.draw.rect(screen, (0, 0, 0), (x, y, box_size, box_size), 2)
            
            # Yellow outline for selected color
            if color == current_color:
                pygame.draw.rect(screen, (255, 255, 0), (x-2, y-2, box_size+4, box_size+4), 3)
    
    def handle_button_click(self, pos):
        # Check if any button was clicked
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                return button['type'], button['value']
        return None, None