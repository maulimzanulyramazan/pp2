import pygame
import random
import sys

pygame.init()

# Window settings
WIDTH = 600
HEIGHT = 600
CELL_SIZE = 16

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 150, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Font for score and level
font = pygame.font.Font(None, 36)

class Snake:
    def __init__(self):
        # Start in the middle of the screen
        self.body = [[WIDTH//2, HEIGHT//2]]
        self.direction = "RIGHT"
        self.grow = False
    
    def move(self):
        # Get head position
        head = self.body[0].copy()
        
        # Move head
        if self.direction == "RIGHT":
            head[0] += CELL_SIZE
        elif self.direction == "LEFT":
            head[0] -= CELL_SIZE
        elif self.direction == "UP":
            head[1] -= CELL_SIZE
        elif self.direction == "DOWN":
            head[1] += CELL_SIZE
        
        # Insert new head
        self.body.insert(0, head)
        
        # Remove tail if not growing
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def change_direction(self, new_dir):
        # Prevent snake from going back into itself
        if new_dir == "RIGHT" and self.direction != "LEFT":
            self.direction = new_dir
        elif new_dir == "LEFT" and self.direction != "RIGHT":
            self.direction = new_dir
        elif new_dir == "UP" and self.direction != "DOWN":
            self.direction = new_dir
        elif new_dir == "DOWN" and self.direction != "UP":
            self.direction = new_dir
    
    def check_self_collision(self):
        # If head touches body, game over
        head = self.body[0]
        if head in self.body[1:]:
            return True
        return False
    
    def check_wall_collision(self):
        # Check if snake leaves the playing area
        head = self.body[0]
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True
        return False
    
    def eat_food(self, food_pos):
        # If head touches food, grow snake
        if self.body[0] == food_pos:
            self.grow = True
            return True
        return False
    
    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, DARK_GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE), 2)

class Food:
    def __init__(self, snake_body):
        self.position = [0, 0]
        self.randomize_position(snake_body)
    
    def randomize_position(self, snake_body):
        # Generate random position that is not on the snake
        while True:
            x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
            y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
            new_pos = [x, y]
            
            # Check if position is on the snake
            if new_pos not in snake_body:
                self.position = new_pos
                break
    
    def draw(self):
        pygame.draw.rect(screen, RED, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, WHITE, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE), 2)

def show_score_and_level(score, level):
    # Show score on screen
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Show level on screen
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(level_text, (WIDTH - 100, 10))

def game_over_screen(score, level):
    # Show game over message
    screen.fill(BLACK)
    
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    level_text = font.render(f"Level Reached: {level}", True, WHITE)
    restart_text = font.render("Press SPACE to play again or ESC to quit", True, WHITE)
    
    screen.blit(game_over_text, (WIDTH//2 - 70, HEIGHT//2 - 60))
    screen.blit(score_text, (WIDTH//2 - 70, HEIGHT//2 - 20))
    screen.blit(level_text, (WIDTH//2 - 70, HEIGHT//2 + 20))
    screen.blit(restart_text, (WIDTH//2 - 200, HEIGHT//2 + 80))
    
    pygame.display.flip()
    
    # Wait for player input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True  # Restart game
                if event.key == pygame.K_ESCAPE:
                    return False  # Quit

def main():
    running = True
    
    while running:
        # Game variables
        snake = Snake()
        food = Food(snake.body)
        score = 0
        level = 1
        food_to_next_level = 3  # Need 3 food to go to next level
        speed = 5  # Starting speed
        
        game_active = True
        
        while game_active:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        snake.change_direction("RIGHT")
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction("LEFT")
                    elif event.key == pygame.K_UP:
                        snake.change_direction("UP")
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction("DOWN")
            
            # Move snake
            snake.move()
            
            # Check collisions
            if snake.check_wall_collision() or snake.check_self_collision():
                game_active = False
                break
            
            # Check if snake eats food
            if snake.eat_food(food.position):
                score += 1
                food.randomize_position(snake.body)
                
                # Check for level up (every 3 foods)
                if score % food_to_next_level == 0:
                    level += 1
                    speed += 2  # Increase speed on new level
                    food_to_next_level += 1  # Need more food for next level
            
            # Draw everything
            screen.fill(BLACK)
            snake.draw()
            food.draw()
            show_score_and_level(score, level)
            
            pygame.display.flip()
            clock.tick(speed)  # Control game speed
        
        # Game over - ask to restart
        running = game_over_screen(score, level)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()