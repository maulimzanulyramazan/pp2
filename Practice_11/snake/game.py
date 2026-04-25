"""
Game manager - handles game state, scoring, and main logic
"""

import pygame  # Import pygame for game functionality
import sys  # Import sys for system operations
from utils import *  # Import all constants from utils.py

class Game:
    """Main game manager class - controls game flow"""
    
    def __init__(self):
        """Initialize game window and settings"""
        # Create game window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")  # Window title
        
        self.clock = pygame.time.Clock()  # For controlling game speed
        
        # Set up fonts for text display
        self.font = pygame.font.Font(None, 36)  # Regular font (36px)
        self.small_font = pygame.font.Font(None, 24)  # Small font (24px)
        
        # Game state variables
        self.snake = None  # Snake object (will be created later)
        self.food = None  # Food object (will be created later)
        self.score = 0  # Total points
        self.level = 1  # Current level
        self.speed = 8  # Game speed (frames per second)
        self.game_active = True  # Is game currently playing?
    
    def start_new_game(self):
        """Reset and start a fresh game"""
        from snake import Snake  # Import Snake class
        from food import Food  # Import Food class
        
        self.snake = Snake()  # Create new snake
        self.food = Food(self.snake.body)  # Create first food
        self.score = 0  # Reset score to zero
        self.level = 1  # Reset level to 1
        self.speed = 8  # Reset speed to 8 FPS
        self.game_active = True  # Game is active
        
    def handle_input(self):
        """Process keyboard input from player"""
        for event in pygame.event.get():  # Get all events
            if event.type == pygame.QUIT:  # If user clicked close button
                return False  # Signal to quit
            
            if event.type == pygame.KEYDOWN:  # If a key is pressed
                # Arrow key controls
                if event.key == pygame.K_RIGHT:  # Right arrow
                    self.snake.change_direction("RIGHT")
                elif event.key == pygame.K_LEFT:  # Left arrow
                    self.snake.change_direction("LEFT")
                elif event.key == pygame.K_UP:  # Up arrow
                    self.snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:  # Down arrow
                    self.snake.change_direction("DOWN")
        
        return True  # Continue running
    
    def update_game(self):
        """Update all game logic (movement, collisions, eating)"""
        from food import Food  # Import Food class
        
        self.snake.move()  # Move snake one step
        
        # Check for game over conditions
        if self.snake.check_wall_collision() or self.snake.check_self_collision():
            self.game_active = False  # Game over
            return  # Stop updating
        
        # Check if snake eats food
        if self.snake.eat_food(self.food.position):
            points = self.food.get_weight()  # Get point value of food
            self.score += points  # Add points to total score
            
            # Create new food at random position
            self.food = Food(self.snake.body)
            
            # Level up every 10 points
            if self.score >= self.level * 10:  # Check if reached next level
                self.level += 1  # Increase level
                self.speed += 1  # Increase game speed
                self.speed = min(self.speed, 20)  # Cap speed at 20 FPS
        
        # Task 2: Check if current food expired
        if self.food.is_expired():  # If food disappeared
            self.food = Food(self.snake.body)  # Spawn new food
    
    def draw(self):
        """Draw everything on screen"""
        # Draw background (black)
        self.screen.fill(BLACK)
        
        # Draw grid lines (visual reference)
        for x in range(0, WIDTH, CELL_SIZE):  # Vertical lines
            pygame.draw.line(self.screen, (30, 30, 40), (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, CELL_SIZE):  # Horizontal lines
            pygame.draw.line(self.screen, (30, 30, 40), (0, y), (WIDTH, y), 1)
        
        # Draw game objects
        self.snake.draw(self.screen)  # Draw snake
        self.food.draw(self.screen)  # Draw food
        
        # Draw UI: Score and Level (top left and top right)
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(score_text, (10, 10))  # Draw score at top-left
        self.screen.blit(level_text, (WIDTH - 100, 10))  # Draw level at top-right
        
        # Draw food info at bottom (Task 1 - show food type)
        if self.food.get_type() == "gold":
            info = self.small_font.render("GOLD +3 points!", True, GOLD)
            self.screen.blit(info, (10, HEIGHT - 30))  # Draw gold info
        elif self.food.get_type() == "timed":
            info = self.small_font.render("TIMED +2 points (expires!)", True, BLUE)
            self.screen.blit(info, (10, HEIGHT - 30))  # Draw timed info
        
        pygame.display.flip()  # Update the screen
    
    def game_over_screen(self):
        """Display game over screen and wait for user input"""
        self.screen.fill(BLACK)  # Clear screen with black
        
        # List of texts to display on game over screen
        texts = [
            ("GAME OVER", RED, HEIGHT//2 - 60),  # Title at top
            (f"Score: {self.score}", WHITE, HEIGHT//2 - 20),  # Final score
            (f"Level: {self.level}", WHITE, HEIGHT//2 + 10),  # Final level
            ("Press SPACE to restart", GREEN, HEIGHT//2 + 60),  # Restart instruction
            ("Press ESC to quit", RED, HEIGHT//2 + 90)  # Quit instruction
        ]
        
        # Draw each text on screen
        for text, color, y in texts:
            if text == "GAME OVER":  # Big title text
                rendered = self.font.render(text, True, color)
                x = WIDTH//2 - rendered.get_width()//2  # Center horizontally
                self.screen.blit(rendered, (x, y))
            else:  # Small text
                rendered = self.small_font.render(text, True, color)
                x = WIDTH//2 - rendered.get_width()//2  # Center horizontally
                self.screen.blit(rendered, (x, y))
        
        pygame.display.flip()  # Update display
        
        # Wait for player input
        waiting = True
        while waiting:
            for event in pygame.event.get():  # Check all events
                if event.type == pygame.QUIT:  # Close window
                    return False  # Don't restart
                if event.type == pygame.KEYDOWN:  # Key pressed
                    if event.key == pygame.K_SPACE:  # Space key
                        return True  # Restart game
                    if event.key == pygame.K_ESCAPE:  # Escape key
                        return False  # Quit game
        return False  # Default: don't restart