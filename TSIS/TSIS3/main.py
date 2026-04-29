import pygame  # Game development library for graphics, sound, and input handling
from persistence import load_settings  # Import function to load game settings from file
from ui import main_menu, leaderboard_screen, settings_screen, game_over_screen, ask_username  # Import UI screens
from racer import run_game  # Import main racing game logic

pygame.init()  # Initialize all Pygame modules (display, sound, events, etc.)

pygame.mixer.init()  # Initialize sound mixer specifically for audio playback

screen = pygame.display.set_mode((800, 600))  # Create main game window of size 800x600 pixels
pygame.display.set_caption("TSIS3 Racer")  # Set window title
clock = pygame.time.Clock()  # Create clock object for controlling frame rate

def play_background_music(settings):
    """Фондық музыканы ойнату"""
    if settings.get("sound", True):  # Check if sound is enabled in settings (default True)
        try:
            sample_rate = 44100  # CD-quality audio sample rate (unused but kept for reference)
            duration = 2.0  # Placeholder duration value (unused)
            frequency = 440  # Placeholder frequency (A4 note, unused)
            pygame.mixer.music.set_volume(settings.get("music_volume", 0.3))  # Set music volume (default 0.3)
            
            import os  # Import OS module for file path checking
            if os.path.exists("assets/music.mp3"):  # Check if MP3 file exists in assets folder
                pygame.mixer.music.load("assets/music.mp3")  # Load MP3 file into music player
                pygame.mixer.music.play(-1)  # Play music on infinite loop (-1 = forever)
            elif os.path.exists("assets/music.ogg"):  # If MP3 not found, check for OGG file
                pygame.mixer.music.load("assets/music.ogg")  # Load OGG file
                pygame.mixer.music.play(-1)  # Play OGG on infinite loop
            else:
                pygame.mixer.music.load(None)  # No music file found, load nothing
        except Exception as e:
            print(f"Music error: {e}")  # Print error if music fails to load/play
    else:
        pygame.mixer.music.stop()  # Stop music if sound is disabled in settings

def stop_music():
    """Музыканы тоқтату"""
    pygame.mixer.music.stop()  # Halt currently playing background music

def main():
    settings = load_settings()  # Load saved settings from file (volume, difficulty, controls)
    
    play_background_music(settings)  # Start playing music based on loaded settings

    while True:  # Main application loop (runs until user quits)
        choice = main_menu(screen, clock)  # Display main menu, returns user's choice

        if choice == "quit":  # User clicked exit button or selected quit
            break  # Exit main loop and close application

        if choice == "leaderboard":  # User wants to view high scores
            if leaderboard_screen(screen, clock) == "quit":  # Show leaderboard screen
                break  # Exit if user quits from leaderboard

        elif choice == "settings":  # User wants to change game settings
            stop_music()  # Stop background music while in settings menu
            if settings_screen(screen, clock, settings) == "quit":  # Show settings UI
                break  # Exit if user quits from settings
            settings = load_settings()  # Reload settings after user changes
            play_background_music(settings)  # Restart music with new settings

        elif choice == "play":  # User wants to start a new game
            username = ask_username(screen, clock)  # Ask player for their name
            if username is None:  # User cancelled or closed the input dialog
                break  # Exit application

            game_screen = pygame.display.set_mode((400, 600))  # Resize window for game (smaller size)
            
            game_result = run_game(game_screen, clock, username, settings)  # Run racing game, returns result dict

            pygame.display.set_mode((800, 600))  # Restore original window size for menus

            if game_result["action"] == "quit":  # Check if user quit during game
                break  # Exit application

            action = game_over_screen(screen, clock, game_result["result"])  # Show game over screen with score

            if action == "quit":  # User chose to quit after game over
                break
            elif action == "retry":  # User wants to play again with same username
                pygame.display.set_mode((400, 600))  # Resize to game size again
                game_result = run_game(pygame.display.get_surface(), clock, username, settings)  # Run game again
                pygame.display.set_mode((800, 600))  # Restore window size
                if game_result["action"] == "quit":  # Check if user quit on retry
                    break
                game_over_screen(screen, clock, game_result["result"])  # Show game over again after retry

    pygame.quit()  # Uninitialize all Pygame modules and close window

if __name__ == "__main__":  # Check if script is being run directly (not imported)
    main()  # Start the application