"""
Snake Game - Main Entry Point
"""

import pygame  # Import pygame library for game development
import sys  # Import sys for system exit
from game import Game  # Import Game class from game.py

def main():
    """Main function to run the game"""
    pygame.init()  # Initialize all pygame modules
    
    running = True  # Main program loop flag
    while running:  # Keep running until user quits
        game = Game()  # Create new game instance
        game.start_new_game()  # Reset and start fresh game
        
        while game.game_active:  # Loop while game is playing
            if not game.handle_input():  # Check for user input
                pygame.quit()  # Close pygame
                sys.exit()  # Exit program
            
            game.update_game()  # Update game logic (move snake, check collisions)
            game.draw()  # Draw everything on screen
            game.clock.tick(game.speed)  # Control game speed (FPS)
        
        running = game.game_over_screen()  # Show game over, ask for restart
    
    pygame.quit()  # Close pygame when done
    sys.exit()  # Exit program

if __name__ == "__main__":  # Check if this file is run directly
    main()  # Start the game