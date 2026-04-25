import pygame  # Import pygame library
import sys  # Import sys for system exit
from game import Game  # Import Game class from game.py

def main():
    """Main function to run the game"""
    pygame.init()  # Initialize all pygame modules
    
    running = True  # Main program loop flag
    
    while running:  # Keep running until user quits
        game = Game()  # Create new game instance
        game.start_new_game()  # Reset and start fresh game
        
        should_continue = game.run()  # Play game until game over
        if not should_continue:  # If user quit during game
            break  # Exit completely
        
        running = game.game_over_screen()  # Show game over, ask for restart
    
    pygame.quit()  # Close pygame
    sys.exit()  # Exit program

if __name__ == "__main__":  # Check if this file is run directly
    main()  # Start the game