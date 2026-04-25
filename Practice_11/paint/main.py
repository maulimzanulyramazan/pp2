"""
Paint Application - Extended from Practice 8
"""

import pygame
import sys
from colors import *      # Import all colors from colors.py
from tools import *       # Import all tool classes from tools.py
from ui import UI         # Import UI class from ui.py

class PaintApp:
    """Main paint application class"""
    
    def __init__(self):
        """Initialize the paint application"""
        pygame.init()       # Start pygame engine
        self.screen_width = 800    # Window width
        self.screen_height = 600   # Window height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))  # Create window
        pygame.display.set_caption("Paint Application - Extended")  # Window title
        
        self.clock = pygame.time.Clock()   # For controlling FPS
        self.running = True                # Game loop flag
        
        # Drawing settings
        self.thickness = 5                 # Brush/line thickness
        self.color = BLACK                 # Current drawing color
        self.mode = "draw"                 # Current tool mode
        self.drawing = False               # Is mouse button pressed?
        self.start_pos = None              # Starting position for shapes
        self.last_pos = None               # Last mouse position for lines
        
        # Initialize tools
        self.tools = {
            "draw": DrawTool(),                     # Free drawing tool
            "rect": RectangleTool(),                # Rectangle tool
            "circle": CircleTool(),                 # Circle tool
            "eraser": EraserTool(),                 # Eraser tool
            "square": SquareTool(),                 # Square tool (Task 1)
            "right_triangle": RightTriangleTool(),  # Right triangle (Task 2)
            "equilateral": EquilateralTriangleTool(), # Equilateral triangle (Task 3)
            "rhombus": RhombusTool()                # Rhombus tool (Task 4)
        }
        
        # Initialize UI
        self.ui = UI(self.screen_width, self.screen_height)  # Create UI object
        
        # Clear screen with white
        self.screen.fill(WHITE)   # Fill background with white
    
    def handle_events(self):
        """Handle all input events"""
        for event in pygame.event.get():        # Get all events
            if event.type == pygame.QUIT:       # If close button clicked
                self.running = False            # Stop the game loop
            
            # Keyboard input
            elif event.type == pygame.KEYDOWN:  # If any key pressed
                self.handle_keyboard(event)     # Handle key press
            
            # Mouse input
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Mouse button pressed
                if event.button == 1:                   # Left mouse button
                    self.drawing = True                 # Start drawing
                    self.start_pos = event.pos          # Save start position
                    self.last_pos = event.pos           # Save last position
                    # Call tool's mouse down handler
                    if self.mode in self.tools:         # If tool exists
                        self.tools[self.mode].on_mouse_down(event.pos)  # Notify tool
            
            elif event.type == pygame.MOUSEBUTTONUP:     # Mouse button released
                if event.button == 1 and self.drawing:   # If was drawing
                    self.drawing = False                # Stop drawing
                    # Draw the shape on mouse release
                    if self.mode in ["rect", "circle", "square", "right_triangle", "equilateral", "rhombus"]:
                        self.tools[self.mode].on_mouse_up(  # Call tool's release handler
                            event.pos, self.start_pos, self.screen, self.color, self.thickness
                        )
                    self.start_pos = None      # Reset start position
                    self.last_pos = None       # Reset last position
            
            elif event.type == pygame.MOUSEMOTION and self.drawing:  # Mouse moved while drawing
                # For drawing/eraser tools, draw continuously
                if self.mode in ["draw", "eraser"]:                  # Only for continuous tools
                    self.last_pos = self.tools[self.mode].on_mouse_move(  # Draw line
                        event.pos, self.last_pos, self.screen, self.color, self.thickness
                    )
    
    def handle_keyboard(self, event):
        """Handle keyboard shortcuts"""
        # Tool selection (Task 1-4 added)
        if event.key == pygame.K_1:      # Press 1 key
            self.mode = "draw"           # Switch to draw mode
        elif event.key == pygame.K_2:    # Press 2 key
            self.mode = "rect"           # Switch to rectangle mode
        elif event.key == pygame.K_3:    # Press 3 key
            self.mode = "circle"         # Switch to circle mode
        elif event.key == pygame.K_4:    # Press 4 key
            self.mode = "eraser"         # Switch to eraser mode
        elif event.key == pygame.K_5:    # Press 5 key (Task 1)
            self.mode = "square"         # Switch to square mode
        elif event.key == pygame.K_6:    # Press 6 key (Task 2)
            self.mode = "right_triangle" # Switch to right triangle mode
        elif event.key == pygame.K_7:    # Press 7 key (Task 3)
            self.mode = "equilateral"    # Switch to equilateral triangle mode
        elif event.key == pygame.K_8:    # Press 8 key (Task 4)
            self.mode = "rhombus"        # Switch to rhombus mode
        
        # Color selection
        elif event.key == pygame.K_r:    # Press R key
            self.color = RED             # Change to red
        elif event.key == pygame.K_g:    # Press G key
            self.color = GREEN           # Change to green
        elif event.key == pygame.K_b:    # Press B key
            self.color = BLUE            # Change to blue
        elif event.key == pygame.K_y:    # Press Y key
            self.color = YELLOW          # Change to yellow
        elif event.key == pygame.K_p:    # Press P key
            self.color = PURPLE          # Change to purple
        elif event.key == pygame.K_o:    # Press O key
            self.color = ORANGE          # Change to orange
        elif event.key == pygame.K_k:    # Press K key
            self.color = BLACK           # Change to black
        elif event.key == pygame.K_w:    # Press W key
            self.color = WHITE           # Change to white
        
        # Brush size
        elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:  # Press + key
            self.thickness = min(self.thickness + 1, 50)   # Increase thickness (max 50)
        elif event.key == pygame.K_MINUS:  # Press - key
            self.thickness = max(self.thickness - 1, 1)    # Decrease thickness (min 1)
        
        # Clear screen
        elif event.key == pygame.K_c:    # Press C key
            self.screen.fill(WHITE)      # Fill screen with white (clear)
    
    def run(self):
        """Main game loop"""
        while self.running:              # While game is running
            self.handle_events()         # Check all input events
            
            # Draw UI
            self.ui.draw_text(self.screen, self.mode, self.color, self.thickness)  # Show text info
            self.ui.draw_color_palette(self.screen, COLOR_PALETTE, self.color)      # Show color buttons
            
            # Update display
            pygame.display.flip()        # Update the screen
            self.clock.tick(60)          # Limit to 60 frames per second
        
        pygame.quit()    # Close pygame
        sys.exit()       # Exit program

if __name__ == "__main__":    # If this file is run directly
    app = PaintApp()          # Create paint app object
    app.run()                 # Start the application