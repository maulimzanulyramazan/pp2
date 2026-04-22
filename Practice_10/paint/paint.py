import pygame
import sys
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()  # Control game speed
screen.fill((255, 255, 254))

radius = 5  # Brush size
color = (0, 0, 0)  # Current color (black)
mode = "draw"  # Current tool: draw, rect, circle, eraser
drawing = False  # Is mouse button pressed?
start = None  # Start position for shapes
last = None  # Last mouse position for lines
font = pygame.font.Font(None, 24)  # Font for text

def draw_line_between(p1, p2, r, col):
    """Draw a smooth line between two points"""
    if p1 is None or p2 is None:
        return
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dist = max(abs(dx), abs(dy))
    if dist == 0:
        pygame.draw.circle(screen, col, p1, r)
        return
    for i in range(dist + 1):
        t = i / dist
        x = int(p1[0] + dx * t)
        y = int(p1[1] + dy * t)
        pygame.draw.circle(screen, col, (x, y), r)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # ----- KEYBOARD -----
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                mode = "draw"
            elif event.key == pygame.K_2:
                mode = "rect"
            elif event.key == pygame.K_3:
                mode = "circle"
            elif event.key == pygame.K_4:
                mode = "eraser"
            elif event.key == pygame.K_r:
                color = (255, 0, 0)
            elif event.key == pygame.K_g:
                color = (0, 255, 0)
            elif event.key == pygame.K_b:
                color = (0, 0, 255)
            elif event.key == pygame.K_c:
                screen.fill((255, 255, 255))
        
        # ----- MOUSE CLICK -----
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True  # Start drawing
                start = event.pos  # Save start point
                last = event.pos  # Save last point
        
        # ----- MOUSE RELEASE -----
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False  # Stop drawing
                if mode == "rect":
                    # Draw rectangle from start to current mouse
                    x1,y1 = start
                    x2,y2 = event.pos
                    rect = pygame.Rect(min(x1,x2), min(y1,y2), abs(x1-x2), abs(y1-y2))
                    pygame.draw.rect(screen, color, rect, radius)
                elif mode == "circle":
                    # Draw circle from start to current mouse
                    dx = event.pos[0] - start[0]
                    dy = event.pos[1] - start[1]
                    r = int(math.sqrt(dx*dx + dy*dy))
                    pygame.draw.circle(screen, color, start, r, radius)
                start = None
        
        # ----- MOUSE DRAG -----
        elif event.type == pygame.MOUSEMOTION and drawing:
            if mode == "draw":
                draw_line_between(last, event.pos, radius, color)  # Draw line
            elif mode == "eraser":
                draw_line_between(last, event.pos, radius, (255,255,255))  # Erase
            last = event.pos  # Update last position
    
    # ----- SHOW TEXT ON SCREEN -----
    text1 = font.render(f"Mode: {mode}  Color: {color}  Size: {radius}", True, (0,0,0))
    screen.blit(text1, (10, 10))
    text2 = font.render("1-draw 2-rect 3-circle 4-eraser | R G B | C-clear", True, (0,0,0))
    screen.blit(text2, (10, 35))
    
    pygame.display.flip()
    clock.tick(60)  # 60 frames per second

pygame.quit()
sys.exit()