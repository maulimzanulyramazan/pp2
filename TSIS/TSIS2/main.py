# Main paint application - Extended drawing tools
# Includes: pencil, line, shapes, flood fill, text, save canvas

import pygame
import sys
import datetime
from colors import *
from tools import *
from ui import UI

class PaintApp:
    # Main paint application class
    def __init__(self):
        # Initialize pygame and create window
        pygame.init()
        self.screen_width = 1000     # Window width (increased for more buttons)
        self.screen_height = 750     # Window height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Paint Application - Complete")
        
        self.clock = pygame.time.Clock()   # For controlling FPS
        self.running = True                # Game loop flag
        
        # Drawing settings
        self.thickness = 5                 # Default brush size (medium)
        self.color = BLACK                 # Current drawing color
        self.mode = "pencil"               # Current tool mode
        self.drawing = False               # Is mouse button pressed?
        self.start_pos = None              # Starting position for shapes
        self.last_pos = None               # Last mouse position for lines
        
        # Dict mapping number keys to tools
        self.key_to_tool = {
            pygame.K_1: "pencil",
            pygame.K_2: "line", 
            pygame.K_3: "rect",
            pygame.K_4: "circle",
            pygame.K_5: "square",
            pygame.K_6: "eraser",
            pygame.K_7: "flood_fill",
            pygame.K_8: "text",
            pygame.K_9: "right_triangle",      # Right triangle
            pygame.K_0: "equilateral",         # Equilateral triangle
            pygame.K_MINUS: "rhombus"          # Rhombus
        }
        
        # Initialize all tools
        self.tools = {
            "pencil": PencilTool(),
            "line": LineTool(),
            "rect": RectangleTool(),
            "circle": CircleTool(),
            "square": SquareTool(),
            "eraser": EraserTool(),
            "flood_fill": FloodFillTool(),
            "text": TextTool(),
            "right_triangle": RightTriangleTool(),
            "equilateral": EquilateralTriangleTool(),
            "rhombus": RhombusTool()
        }
        
        # Initialize UI
        self.ui = UI(self.screen_width, self.screen_height)
        
        # Create canvas surface (drawing area below UI)
        self.canvas = pygame.Surface((self.screen_width, self.screen_height - self.ui.ui_height))
        self.canvas.fill(WHITE)        # Start with white background
    
    def save_canvas(self):
        # Save canvas with timestamp in filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"canvas_{timestamp}.png"
        pygame.image.save(self.canvas, filename)
        print(f"Canvas saved as {filename}")
        
        # Show save message on screen
        font = pygame.font.Font(None, 36)
        text = font.render(f"Saved: {filename}", True, GREEN)
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(1500)  # Show message for 1.5 seconds
    
    def handle_events(self):
        # Process all input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:      # Close window button
                self.running = False
            
            # Handle text input when text tool is active
            if self.mode == "text" and self.tools["text"].active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:      # Enter - confirm text
                        self.tools["text"].confirm(self.canvas, self.color)
                        self.mode = "pencil"
                    elif event.key == pygame.K_ESCAPE:    # Escape - cancel text
                        self.tools["text"].cancel()
                        self.mode = "pencil"
                    elif event.key == pygame.K_BACKSPACE: # Backspace - delete char
                        self.tools["text"].backspace()
                    else:                                 # Normal character
                        if event.unicode and event.unicode.isprintable():
                            self.tools["text"].add_char(event.unicode)
                continue  # Skip other processing while typing
            
            # Keyboard shortcuts
            if event.type == pygame.KEYDOWN:
                self.handle_keyboard(event)
            
            # Mouse events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                
                # Check if click is on canvas area (below UI)
                if mouse_pos[1] > self.ui.ui_height:
                    # Convert to canvas coordinates
                    canvas_pos = (mouse_pos[0], mouse_pos[1] - self.ui.ui_height)
                    
                    if event.button == 1:  # Left mouse button
                        self.drawing = True
                        self.start_pos = canvas_pos
                        self.last_pos = canvas_pos
                        
                        # Handle special tools
                        if self.mode == "text":
                            self.tools["text"].on_mouse_down(canvas_pos)
                        elif self.mode == "flood_fill":
                            self.tools["flood_fill"].on_mouse_up(canvas_pos, None, self.canvas, self.color, self.thickness)
                        elif self.mode in self.tools:
                            self.tools[self.mode].on_mouse_down(canvas_pos)
                else:
                    # Click on UI area - check buttons
                    button_type, button_value = self.ui.handle_button_click(mouse_pos)
                    if button_type == "brush_size":
                        self.thickness = button_value
                    elif button_type == "tool":
                        # Cancel text tool if active
                        if self.mode == "text" and self.tools["text"].active:
                            self.tools["text"].cancel()
                        self.mode = button_value
            
            elif event.type == pygame.MOUSEBUTTONUP:
                # Mouse button released
                if event.button == 1 and self.drawing and self.start_pos is not None:
                    self.drawing = False
                    mouse_pos = event.pos
                    
                    if mouse_pos[1] > self.ui.ui_height:
                        canvas_pos = (mouse_pos[0], mouse_pos[1] - self.ui.ui_height)
                        
                        # Draw shapes on mouse release
                        if self.mode in ["rect", "circle", "square", "right_triangle", "equilateral", "rhombus", "line"]:
                            self.tools[self.mode].on_mouse_up(
                                canvas_pos, self.start_pos, self.canvas, self.color, self.thickness
                            )
                    
                    self.start_pos = None
                    self.last_pos = None
            
            elif event.type == pygame.MOUSEMOTION and self.drawing:
                # Mouse moved while drawing
                mouse_pos = event.pos
                
                if mouse_pos[1] > self.ui.ui_height:
                    canvas_pos = (mouse_pos[0], mouse_pos[1] - self.ui.ui_height)
                    
                    # Continuous drawing tools (pencil and eraser)
                    if self.mode in ["pencil", "eraser"]:
                        self.last_pos = self.tools[self.mode].on_mouse_move(
                            canvas_pos, self.last_pos, self.canvas, self.color, self.thickness
                        )
    
    def handle_keyboard(self, event):
        # Handle keyboard shortcuts
        # Tool selection with number keys
        if event.key in self.key_to_tool:
            if self.mode == "text" and self.tools["text"].active:
                self.tools["text"].cancel()
            self.mode = self.key_to_tool[event.key]
        
        # Brush size shortcuts (Q=small, W=medium, E=large)
        elif event.key == pygame.K_q:      # Small brush (2px)
            self.thickness = 2
        elif event.key == pygame.K_w:      # Medium brush (5px)
            self.thickness = 5
        elif event.key == pygame.K_e:      # Large brush (10px)
            self.thickness = 10
        
        # Increase/decrease brush size with +/- keys
        elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
            self.thickness = min(self.thickness + 1, 50)
        elif event.key == pygame.K_MINUS:
            self.thickness = max(self.thickness - 1, 1)
        
        # Color selection shortcuts
        elif event.key == pygame.K_r:      # Red
            self.color = RED
        elif event.key == pygame.K_g:      # Green
            self.color = GREEN
        elif event.key == pygame.K_b:      # Blue
            self.color = BLUE
        elif event.key == pygame.K_y:      # Yellow
            self.color = YELLOW
        elif event.key == pygame.K_p:      # Purple
            self.color = PURPLE
        elif event.key == pygame.K_o:      # Orange
            self.color = ORANGE
        elif event.key == pygame.K_k:      # Black
            self.color = BLACK
        elif event.key == pygame.K_COMMA:  # White (comma key)
            self.color = WHITE
        
        # Clear canvas with 'C' key
        elif event.key == pygame.K_c:
            self.canvas.fill(WHITE)
        
        # Save canvas with Ctrl+S
        elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self.save_canvas()
        
        # Escape to cancel text tool
        elif event.key == pygame.K_ESCAPE and self.mode == "text" and self.tools["text"].active:
            self.tools["text"].cancel()
            self.mode = "pencil"
    
    def draw_previews(self):
        # Draw previews for tools that need them (line tool)
        if self.mode == "line" and self.drawing and self.start_pos:
            preview_surface = self.canvas.copy()
            self.tools["line"].draw_preview(preview_surface, self.start_pos, self.color, self.thickness)
            self.screen.blit(preview_surface, (0, self.ui.ui_height))
        
        # Draw text preview while typing
        if self.mode == "text" and self.tools["text"].active:
            self.tools["text"].draw_preview(self.screen, self.color)
    
    def run(self):
        # Main game loop
        while self.running:
            self.handle_events()      # Process input
            
            # Clear screen and draw canvas
            self.screen.fill(WHITE)
            self.screen.blit(self.canvas, (0, self.ui.ui_height))
            
            # Draw UI
            self.ui.draw_text(self.screen, self.mode, self.color, self.thickness)
            self.ui.draw_color_palette(self.screen, COLOR_PALETTE, self.color)
            
            # Draw previews (line, text)
            self.draw_previews()
            
            # Draw cursor circle when on canvas
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[1] > self.ui.ui_height and self.mode not in ["flood_fill", "text"]:
                canvas_pos = (mouse_pos[0], mouse_pos[1] - self.ui.ui_height)
                pygame.draw.circle(self.screen, self.color, mouse_pos, self.thickness // 2 + 1)
            
            pygame.display.flip()     # Update screen
            self.clock.tick(60)       # 60 FPS
        
        pygame.quit()                 # Clean exit
        sys.exit()

# Start the application
if __name__ == "__main__":
    app = PaintApp()
    app.run()