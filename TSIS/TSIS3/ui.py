import pygame
from persistence import load_leaderboard, save_settings

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (75, 75, 75)
LIGHT_GRAY = (180, 180, 180)
YELLOW = (255, 220, 0)
GREEN = (0, 190, 80)
RED = (220, 30, 30)
BLUE = (40, 120, 255)

class Button:
    def __init__(self, x, y, w, h, text, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        color = LIGHT_GRAY if self.rect.collidepoint(mouse) else GRAY
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=8)

        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

def ask_username(screen, clock):
    """Ойын басталмай тұрып username енгізу."""
    font = pygame.font.SysFont("Verdana", 28)
    small = pygame.font.SysFont("Verdana", 18)
    name = ""

    while True:
        screen.fill(BLACK)
        title = font.render("Enter your name", True, WHITE)
        hint = small.render("Press Enter to start", True, LIGHT_GRAY)
        typed = font.render(name + "|", True, YELLOW)

        screen.blit(title, title.get_rect(center=(400, 220)))
        screen.blit(typed, typed.get_rect(center=(400, 300)))
        screen.blit(hint, hint.get_rect(center=(400, 360)))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name.strip()[:12]
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 12 and event.unicode.isprintable():
                    name += event.unicode
        clock.tick(60)

def main_menu(screen, clock):
    """Main Menu screen."""
    font = pygame.font.SysFont("Verdana", 32)
    title_font = pygame.font.SysFont("Verdana", 54)
    buttons = [
        Button(290, 190, 220, 50, "Play", font),
        Button(290, 260, 220, 50, "Leaderboard", font),
        Button(290, 330, 220, 50, "Settings", font),
        Button(290, 400, 220, 50, "Quit", font),
    ]

    while True:
        screen.fill(BLACK)
        title = title_font.render("RACER", True, YELLOW)
        screen.blit(title, title.get_rect(center=(400, 100)))

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            for button in buttons:
                if button.clicked(event):
                    return button.text.lower()
        clock.tick(60)

def leaderboard_screen(screen, clock):
    """Top 10 leaderboard көрсету."""
    font = pygame.font.SysFont("Verdana", 24)
    small = pygame.font.SysFont("Verdana", 18)
    back = Button(310, 520, 180, 45, "Back", font)

    while True:
        screen.fill(BLACK)
        title = font.render("Top 10 Leaderboard", True, YELLOW)
        screen.blit(title, (260, 35))

        scores = load_leaderboard()
        y = 95
        if not scores:
            empty = small.render("No scores yet", True, WHITE)
            screen.blit(empty, (330, y))
        else:
            for i, item in enumerate(scores[:10], start=1):
                line = f"{i}. {item['name']} | Score: {item['score']} | Distance: {item['distance']} | Coins: {item['coins']}"
                screen.blit(small.render(line, True, WHITE), (90, y))
                y += 35

        back.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if back.clicked(event):
                return "menu"
        clock.tick(60)

def settings_screen(screen, clock, settings):
    """Sound, car color, difficulty, music volume баптаулары."""
    font = pygame.font.SysFont("Verdana", 24)
    small = pygame.font.SysFont("Verdana", 18)
    back = Button(310, 520, 180, 45, "Back", font)

    colors = ["red", "blue", "green"]
    difficulties = ["easy", "normal", "hard"]

    while True:
        screen.fill(BLACK)
        screen.blit(font.render("Settings", True, YELLOW), (330, 50))

        info = [
            f"S - Sound: {'ON' if settings['sound'] else 'OFF'}",
            f"C - Car color: {settings['car_color']}",
            f"D - Difficulty: {settings['difficulty']}",
            f"V - Volume: {int(settings.get('music_volume', 0.3) * 100)}%",  # Дыбыс деңгейі
        ]

        y = 150
        for line in info:
            screen.blit(small.render(line, True, WHITE), (250, y))
            y += 45

        back.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if back.clicked(event):
                save_settings(settings)
                return "menu"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    settings["sound"] = not settings["sound"]
                    # Дыбыс өшірілсе, музыканы тоқтату
                    if not settings["sound"]:
                        pygame.mixer.music.stop()
                    else:
                        # Дыбыс қосылса, музыканы бастау
                        try:
                            import os
                            if os.path.exists("assets/music.mp3"):
                                pygame.mixer.music.load("assets/music.mp3")
                                pygame.mixer.music.play(-1)
                            elif os.path.exists("assets/music.ogg"):
                                pygame.mixer.music.load("assets/music.ogg")
                                pygame.mixer.music.play(-1)
                        except:
                            pass
                elif event.key == pygame.K_c:
                    i = colors.index(settings["car_color"])
                    settings["car_color"] = colors[(i + 1) % len(colors)]
                elif event.key == pygame.K_d:
                    i = difficulties.index(settings["difficulty"])
                    settings["difficulty"] = difficulties[(i + 1) % len(difficulties)]
                elif event.key == pygame.K_v:
                    # Дыбыс деңгейін өзгерту (0% -> 100% -> 0%)
                    vol = settings.get("music_volume", 0.3)
                    if vol >= 0.9:
                        new_vol = 0.0
                    elif vol >= 0.5:
                        new_vol = 0.9
                    else:
                        new_vol = 0.5
                    settings["music_volume"] = new_vol
                    pygame.mixer.music.set_volume(new_vol)
                save_settings(settings)
        clock.tick(60)

def game_over_screen(screen, clock, result):
    """Game Over screen."""
    font = pygame.font.SysFont("Verdana", 32)
    small = pygame.font.SysFont("Verdana", 20)
    retry = Button(260, 400, 130, 50, "Retry", font)
    menu = Button(410, 400, 180, 50, "Main Menu", font)

    while True:
        screen.fill(RED)
        screen.blit(font.render("Game Over", True, BLACK), (300, 120))
        lines = [
            f"Score: {result['score']}",
            f"Distance: {result['distance']}",
            f"Coins: {result['coins']}",
        ]

        y = 210
        for line in lines:
            screen.blit(small.render(line, True, BLACK), (315, y))
            y += 35

        retry.draw(screen)
        menu.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if retry.clicked(event):
                return "retry"
            if menu.clicked(event):
                return "menu"
        clock.tick(60)