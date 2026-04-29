# main.py - Main entry point with menu system
import pygame
import sys
import json
from utils import WIDTH, HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, GRID_SIZE, BLACK, WHITE, RED, GREEN, DARK_RED, BLUE, YELLOW, PURPLE, ORANGE, GRAY, GOLD, DARK_GREEN, BRIGHT_GREEN, CYAN, PINK, INITIAL_SPEED, SPEED_INCREMENT, FOODS_PER_LEVEL, POWERUP_DURATION, POWERUP_DISAPPEAR_TIME, OBSTACLE_START_LEVEL
from game import Game
from db import Database

class MenuSystem:
    """Menu system: Main Menu, Leaderboard, Settings, Game Over screens"""
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        
        # Database connection
        try:
            self.db = Database()
        except Exception as e:
            print(f"Database unavailable: {e}")
            self.db = None
        
        self.username = ""
        self.input_text = ""
        
        # Start menu music
        self.start_menu_music()
    
    # main.py - Only music part changed
    def start_menu_music(self):
        """Start background music for menu - FIXED"""
        try:
            import os
            music_file = None
            if os.path.exists("assets/background_music.mp3"):
                music_file = "assets/background_music.mp3"
            elif os.path.exists("background_music.mp3"):
                music_file = "background_music.mp3"
        
            if music_file:
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
                print("✅ Music playing")
            else:
                print("No music file found - create assets/background_music.mp3")
        except Exception as e:
            print(f"Music error: {e}")
    
    def draw_button(self, text, x, y, width, height, color, hover_color):
        """Draw a button and return True if clicked"""
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = pygame.Rect(x, y, width, height)
        
        if rect.collidepoint(mouse):
            pygame.draw.rect(self.screen, hover_color, rect)
            if click[0] == 1:
                return True
        else:
            pygame.draw.rect(self.screen, color, rect)
        
        text_surf = self.small_font.render(text, True, BLACK)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)
        return False
    
    def username_screen(self):
        """Task: Username entry on main menu"""
        running = True
        while running:
            self.screen.fill(BLACK)
            
            # Title
            title = self.font.render("Enter Username", True, WHITE)
            title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//3))
            self.screen.blit(title, title_rect)
            
            # Input box
            input_box = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 30, 300, 50)
            pygame.draw.rect(self.screen, WHITE, input_box, 2)
            
            # Input text
            text_surf = self.small_font.render(self.input_text, True, WHITE)
            self.screen.blit(text_surf, (input_box.x + 5, input_box.y + 10))
            
            # Instructions
            inst = self.small_font.render("Press ENTER to continue", True, GRAY)
            inst_rect = inst.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
            self.screen.blit(inst, inst_rect)
            
            # Database status
            if self.db:
                status = self.small_font.render("✅ Database Connected", True, GREEN)
            else:
                status = self.small_font.render("⚠️ Offline Mode", True, RED)
            self.screen.blit(status, (10, HEIGHT - 30))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.input_text.strip():
                        self.username = self.input_text.strip()
                        return True
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        if len(self.input_text) < 20 and event.unicode.isprintable():
                            self.input_text += event.unicode
            
            self.clock.tick(60)
    
    def main_menu(self):
        """Main menu with Play, Leaderboard, Settings, Quit buttons"""
        while True:
            self.screen.fill(BLACK)
            
            # Game title
            title = self.font.render("SNAKE GAME", True, GREEN)
            title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
            self.screen.blit(title, title_rect)
            
            # Buttons
            play = self.draw_button("PLAY", WIDTH//2 - 100, HEIGHT//2 - 80, 200, 50, GREEN, BRIGHT_GREEN)
            leaderboard = self.draw_button("LEADERBOARD", WIDTH//2 - 100, HEIGHT//2 - 20, 200, 50, BLUE, (0, 100, 255))
            settings = self.draw_button("SETTINGS", WIDTH//2 - 100, HEIGHT//2 + 40, 200, 50, PURPLE, (100, 0, 200))
            quit_btn = self.draw_button("QUIT", WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50, RED, (200, 0, 0))
            
            # Show player name
            if self.username:
                name_text = self.small_font.render(f"Player: {self.username}", True, GOLD)
                self.screen.blit(name_text, (10, HEIGHT - 30))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
            
            if play:
                return "play"
            if leaderboard:
                return "leaderboard"
            if settings:
                return "settings"
            if quit_btn:
                return "quit"
            
            self.clock.tick(60)
    
    def leaderboard_screen(self):
        """Task: Leaderboard screen - fetch and display top 10 scores"""
        # Get top 10 scores from database
        scores = self.db.get_leaderboard(10) if self.db else []
        
        scroll_y = 0
        max_scroll = max(0, len(scores) * 40 - 400)
        
        running = True
        while running:
            self.screen.fill(BLACK)
            
            # Title
            title = self.font.render("TOP 10 SCORES", True, GOLD)
            title_rect = title.get_rect(center=(WIDTH//2, 40))
            self.screen.blit(title, title_rect)
            
            # Headers
            headers = ["Rank", "Username", "Score", "Level", "Date"]
            positions = [50, 150, 350, 450, 520]
            
            for i, header in enumerate(headers):
                text = self.small_font.render(header, True, WHITE)
                self.screen.blit(text, (positions[i], 100))
            
            # Draw scores
            y = 140 - scroll_y
            if not scores:
                no_data = self.small_font.render("No scores yet! Play the game!", True, GRAY)
                self.screen.blit(no_data, (WIDTH//2 - 150, HEIGHT//2))
            else:
                for rank, (username, score, level, date) in enumerate(scores, 1):
                    if 100 < y < HEIGHT - 100:
                        # Gold, Silver, Bronze colors for top 3
                        if rank == 1:
                            color = GOLD
                        elif rank == 2:
                            color = (192, 192, 192)
                        elif rank == 3:
                            color = (205, 127, 50)
                        else:
                            color = WHITE
                        
                        rank_text = self.small_font.render(str(rank), True, color)
                        name_text = self.small_font.render(username[:15], True, color)
                        score_text = self.small_font.render(str(score), True, color)
                        level_text = self.small_font.render(str(level), True, color)
                        date_text = self.small_font.render(date[:16], True, color)
                        
                        self.screen.blit(rank_text, (positions[0], y))
                        self.screen.blit(name_text, (positions[1], y))
                        self.screen.blit(score_text, (positions[2], y))
                        self.screen.blit(level_text, (positions[3], y))
                        self.screen.blit(date_text, (positions[4], y))
                    y += 35
                    if y > HEIGHT:
                        break
            
            # Back button
            back = self.draw_button("BACK", WIDTH//2 - 60, HEIGHT - 60, 120, 40, RED, (200, 0, 0))
            
            # Scroll indicator
            if max_scroll > 0:
                scroll_text = self.small_font.render("Use mouse wheel to scroll", True, GRAY)
                self.screen.blit(scroll_text, (WIDTH - 200, HEIGHT - 30))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEWHEEL:
                    scroll_y -= event.y * 20
                    scroll_y = max(0, min(max_scroll, scroll_y))
            
            if back:
                return
            
            self.clock.tick(60)
    
    def settings_screen(self):
        """Task: Settings screen - snake color, grid overlay, sound"""
        # Load current settings
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
        except:
            settings = {"snake_color": [0, 255, 0], "grid_overlay": True, "sound": True}
        
        # Available colors
        colors = [([0, 255, 0], "Green"), ([255, 0, 0], "Red"), ([0, 0, 255], "Blue"),
                  ([255, 255, 0], "Yellow"), ([255, 0, 255], "Purple"), ([0, 255, 255], "Cyan")]
        
        color_idx = 0
        for i, (c, _) in enumerate(colors):
            if c == settings["snake_color"]:
                color_idx = i
                break
        
        running = True
        while running:
            self.screen.fill(BLACK)
            
            # Title
            title = self.font.render("SETTINGS", True, WHITE)
            self.screen.blit(title, (WIDTH//2 - 70, 50))
            
            # Snake color selector
            self.screen.blit(self.small_font.render("Snake Color:", True, WHITE), (100, 150))
            pygame.draw.rect(self.screen, tuple(colors[color_idx][0]), (300, 145, 30, 30))
            left = self.draw_button("<", 350, 145, 40, 35, GRAY, WHITE)
            right = self.draw_button(">", 400, 145, 40, 35, GRAY, WHITE)
            self.screen.blit(self.small_font.render(colors[color_idx][1], True, GOLD), (460, 150))
            
            # Grid overlay toggle
            self.screen.blit(self.small_font.render("Grid Overlay:", True, WHITE), (100, 220))
            grid_status = "ON" if settings["grid_overlay"] else "OFF"
            grid_color = GREEN if settings["grid_overlay"] else RED
            if self.draw_button(grid_status, 300, 215, 80, 40, grid_color, GRAY):
                settings["grid_overlay"] = not settings["grid_overlay"]
            
            # Sound toggle
            self.screen.blit(self.small_font.render("Sound:", True, WHITE), (100, 290))
            sound_status = "ON" if settings["sound"] else "OFF"
            sound_color = GREEN if settings["sound"] else RED
            if self.draw_button(sound_status, 300, 285, 80, 40, sound_color, GRAY):
                settings["sound"] = not settings["sound"]
                if not settings["sound"]:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            
            # Save button
            save = self.draw_button("SAVE & BACK", WIDTH//2 - 80, HEIGHT - 100, 160, 50, GREEN, BRIGHT_GREEN)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            if left:
                color_idx = (color_idx - 1) % len(colors)
            if right:
                color_idx = (color_idx + 1) % len(colors)
            if save:
                settings["snake_color"] = colors[color_idx][0]
                with open('settings.json', 'w') as f:
                    json.dump(settings, f)
                return
            
            self.clock.tick(60)
    
    def game_over_screen(self, score, level):
        """Task: Game over screen - shows final score, level, personal best"""
        # Save result to database
        if self.db:
            self.db.save_game_result(self.username, score, level)
        
        # Get updated personal best
        personal_best = self.db.get_personal_best(self.username) if self.db else 0
        if score > personal_best:
            personal_best = score
        
        running = True
        while running:
            self.screen.fill(BLACK)
            
            # Title
            title = self.font.render("GAME OVER", True, RED)
            title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
            self.screen.blit(title, title_rect)
            
            # Stats
            score_text = self.font.render(f"Score: {score}", True, WHITE)
            level_text = self.font.render(f"Level: {level}", True, WHITE)
            best_text = self.small_font.render(f"Personal Best: {personal_best}", True, GOLD)
            
            score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 40))
            level_rect = level_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 10))
            best_rect = best_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
            
            self.screen.blit(score_text, score_rect)
            self.screen.blit(level_text, level_rect)
            self.screen.blit(best_text, best_rect)
            
            # Buttons
            retry = self.draw_button("RETRY", WIDTH//2 - 110, HEIGHT//2 + 80, 100, 40, GREEN, BRIGHT_GREEN)
            menu = self.draw_button("MENU", WIDTH//2 + 10, HEIGHT//2 + 80, 100, 40, BLUE, (0, 100, 255))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
            
            if retry:
                return "retry"
            if menu:
                return "menu"
            
            self.clock.tick(60)
    
    def run(self):
        """Main run loop"""
        # Get username first
        if not self.username_screen():
            return
        
        while True:
            choice = self.main_menu()
            
            if choice == "quit":
                break
            elif choice == "play":
                # Start game
                game = Game(self.username, self.db)
                game_over = False
                
                while not game_over:
                    running = game.run_frame()
                    if not running:
                        game_over = True
                        result = self.game_over_screen(game.score, game.level)
                        if result == "quit":
                            return
                        elif result == "menu":
                            break
                        elif result == "retry":
                            game = Game(self.username, self.db)
                            game_over = False
                
            elif choice == "leaderboard":
                self.leaderboard_screen()
            elif choice == "settings":
                self.settings_screen()
        
        # Cleanup
        if self.db:
            self.db.close()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    menu = MenuSystem()
    menu.run()