import pygame  # Game development library
import random  # For random number generation (spawn positions, weights, choices)
import os  # Operating system interface for file paths
from persistence import add_score  # Import function to save high scores

SCREEN_WIDTH = 400  # Game window width in pixels
SCREEN_HEIGHT = 600  # Game window height in pixels

BLACK = (0, 0, 0)  # RGB color black
WHITE = (255, 255, 255)  # RGB color white
RED = (230, 20, 20)  # RGB color red
GREEN = (0, 200, 80)  # RGB color green
BLUE = (30, 120, 255)  # RGB color blue
YELLOW = (255, 220, 0)  # RGB color yellow
GRAY = (80, 80, 80)  # RGB color gray
DARK_GRAY = (40, 40, 40)  # RGB color dark gray
ORANGE = (255, 140, 0)  # RGB color orange
PURPLE = (160, 70, 255)  # RGB color purple

LANES = [85, 155, 245, 315]  # X-coordinates for 4 driving lanes
ROAD_LEFT = 40  # Left boundary of the road in pixels
ROAD_RIGHT = 360  # Right boundary of the road in pixels
FINISH_DISTANCE = 3000  # Total distance needed to complete race (meters)

def make_car(color):
    """Player/enemy машинаны surface ретінде жасау."""
    image = pygame.Surface((45, 75), pygame.SRCALPHA)  # Create transparent surface 45x75
    pygame.draw.rect(image, color, (4, 4, 37, 67), border_radius=8)  # Draw car body with rounded corners
    pygame.draw.rect(image, BLACK, (8, 10, 29, 10), 2)  # Draw windshield outline
    pygame.draw.rect(image, BLUE, (8, 28, 29, 18), border_radius=4)  # Draw side window
    pygame.draw.circle(image, BLACK, (6, 18), 5)  # Draw left headlight
    pygame.draw.circle(image, BLACK, (39, 18), 5)  # Draw right headlight
    pygame.draw.circle(image, BLACK, (6, 58), 5)  # Draw left taillight
    pygame.draw.circle(image, BLACK, (39, 58), 5)  # Draw right taillight
    return image

class Player(pygame.sprite.Sprite):
    def __init__(self, color_name):
        super().__init__()  # Initialize parent Sprite class
        colors = {"red": RED, "blue": BLUE, "green": GREEN}  # Map color names to RGB values
        path = os.path.join("assets", "car.png")  # Build file path for custom car image

        if os.path.exists(path):  # Check if custom car image exists
            self.image = pygame.image.load(path).convert_alpha()  # Load image with transparency
            self.image = pygame.transform.scale(self.image, (50, 80))  # Resize to 50x80 pixels
            self.image = pygame.transform.rotate(self.image, 180)  # Rotate 180 degrees (face downward)
        else:
            self.image = make_car(colors.get(color_name, RED))  # Generate procedural car sprite

        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70))  # Position at bottom center
        self.speed = 6  # Movement speed in pixels per frame

    def update(self):
        keys = pygame.key.get_pressed()  # Get state of all keyboard keys
        if keys[pygame.K_LEFT] and self.rect.left > ROAD_LEFT:  # Move left if within road boundary
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_RIGHT:  # Move right if within road boundary
            self.rect.x += self.speed

class TrafficCar(pygame.sprite.Sprite):
    """Төмен қарай қозғалатын traffic car."""
    def __init__(self, speed, avoid_rect=None):
        super().__init__()
        self.image = make_car(random.choice([RED, BLUE, GREEN, ORANGE]))  # Random color for enemy car
        self.rect = self.image.get_rect()
        self.speed = speed  # Falling speed
        self.safe_spawn(avoid_rect)  # Ensure car doesn't spawn on player

    def safe_spawn(self, avoid_rect):
        # Player үстіне тікелей spawn болмауы үшін бірнеше рет тексереміз.
        for _ in range(20):  # Try up to 20 times to find safe position
            self.rect.center = (random.choice(LANES), random.randint(-350, -80))  # Random lane, above screen
            if not avoid_rect or not self.rect.colliderect(avoid_rect.inflate(90, 180)):  # No collision with player zone
                return
        self.rect.center = (random.choice(LANES), -300)  # Fallback position

    def update(self):
        self.rect.y += self.speed  # Move downward
        if self.rect.top > SCREEN_HEIGHT:  # If car goes off bottom of screen
            self.kill()  # Remove from all sprite groups

class Obstacle(pygame.sprite.Sprite):
    """Barrier, oil spill, pothole сияқты obstacle."""
    def __init__(self, kind, speed, avoid_rect=None):
        super().__init__()
        self.kind = kind  # Type: "barrier", "oil", or "pothole"
        self.speed = speed
        self.image = pygame.Surface((50, 35), pygame.SRCALPHA)  # 50x35 transparent surface

        if kind == "barrier":
            pygame.draw.rect(self.image, ORANGE, (0, 5, 50, 25))  # Orange rectangle body
            pygame.draw.line(self.image, WHITE, (5, 28), (45, 7), 4)  # Striped line
        elif kind == "oil":
            pygame.draw.ellipse(self.image, BLACK, (2, 5, 46, 25))  # Black oil puddle
            pygame.draw.ellipse(self.image, DARK_GRAY, (12, 10, 20, 8))  # Highlight reflection
        else:  # pothole
            pygame.draw.ellipse(self.image, GRAY, (3, 5, 44, 25))  # Gray hole
            pygame.draw.ellipse(self.image, BLACK, (12, 10, 25, 12))  # Dark inner hole

        self.rect = self.image.get_rect()
        self.safe_spawn(avoid_rect)  # Spawn without colliding with player

    def safe_spawn(self, avoid_rect):
        for _ in range(20):
            self.rect.center = (random.choice(LANES), random.randint(-420, -80))
            if not avoid_rect or not self.rect.colliderect(avoid_rect.inflate(90, 180)):
                return
        self.rect.center = (random.choice(LANES), -350)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    """Nitro, shield, repair collectible."""
    def __init__(self, kind, speed):
        super().__init__()
        self.kind = kind  # "nitro", "shield", or "repair"
        self.speed = speed
        self.spawn_time = pygame.time.get_ticks()  # Timestamp when powerup spawned
        self.life_time = 6000  # Powerup disappears after 6000 milliseconds (6 seconds)
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)  # 32x32 circle surface

        colors = {"nitro": PURPLE, "shield": BLUE, "repair": GREEN}  # Color mapping
        pygame.draw.circle(self.image, colors[kind], (16, 16), 16)  # Colored circle background
        pygame.draw.circle(self.image, WHITE, (16, 16), 16, 2)  # White outline
        letter = {"nitro": "N", "shield": "S", "repair": "R"}[kind]  # One-letter label
        font = pygame.font.SysFont("Verdana", 16)  # Font for letter
        text = font.render(letter, True, WHITE)  # Render white letter
        self.image.blit(text, text.get_rect(center=(16, 16)))  # Center letter on circle

        self.rect = self.image.get_rect(center=(random.choice(LANES), random.randint(-500, -80)))

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()  # Remove if off screen
        if pygame.time.get_ticks() - self.spawn_time > self.life_time:  # Check lifetime expiration
            self.kill()  # Remove if expired

class Coin(pygame.sprite.Sprite):
    """Practice 11 логикасын кеңейту: weighted coin."""
    def __init__(self, speed):
        super().__init__()
        self.weight = random.choice([1, 2, 3])  # Random coin value (1, 2, or 3 points)
        self.speed = speed
        self.image = pygame.Surface((26, 26), pygame.SRCALPHA)  # 26x26 circle
        color = YELLOW if self.weight == 1 else ORANGE if self.weight == 2 else PURPLE  # Color based on weight
        pygame.draw.circle(self.image, color, (13, 13), 13)  # Colored circle
        pygame.draw.circle(self.image, BLACK, (13, 13), 13, 2)  # Black border
        font = pygame.font.SysFont("Verdana", 14)  # Font for weight number
        text = font.render(str(self.weight), True, BLACK)  # Render weight as text
        self.image.blit(text, text.get_rect(center=(13, 13)))  # Center number on coin
        self.rect = self.image.get_rect(center=(random.choice(LANES), random.randint(-500, -40)))

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class RoadEvent(pygame.sprite.Sprite):
    """Moving barrier, speed bump, nitro strip сияқты dynamic road event."""
    def __init__(self, kind, speed):
        super().__init__()
        self.kind = kind  # "moving_barrier", "speed_bump", or "nitro_strip"
        self.speed = speed
        self.direction = random.choice([-2, 2])  # Initial movement direction (left or right)
        self.image = pygame.Surface((70, 22), pygame.SRCALPHA)  # 70x22 horizontal bar

        if kind == "moving_barrier":
            pygame.draw.rect(self.image, ORANGE, (0, 0, 70, 22))  # Orange barrier
            pygame.draw.line(self.image, WHITE, (5, 18), (65, 4), 4)  # Diagonal stripe
        elif kind == "speed_bump":
            pygame.draw.rect(self.image, YELLOW, (0, 6, 70, 10))  # Yellow bump
        else:  # nitro_strip
            pygame.draw.rect(self.image, PURPLE, (0, 0, 70, 22))  # Purple strip
            pygame.draw.rect(self.image, WHITE, (8, 7, 54, 8))  # White center line

        self.rect = self.image.get_rect(center=(random.choice(LANES), random.randint(-550, -100)))

    def update(self):
        self.rect.y += self.speed
        if self.kind == "moving_barrier":  # Moving barrier bounces left-right
            self.rect.x += self.direction
            if self.rect.left < ROAD_LEFT or self.rect.right > ROAD_RIGHT:  # Hit road edge
                self.direction *= -1  # Reverse direction

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

def draw_background(screen, bg, road_scroll, speed):
    """Жолды және lane сызықтарын салу."""
    if bg:
        screen.blit(bg, (0, 0))  # Draw background image at origin
    else:
        screen.fill((185, 185, 185))  # Gray asphalt background
        pygame.draw.rect(screen, BLACK, (0, 0, ROAD_LEFT, SCREEN_HEIGHT))  # Left roadside
        pygame.draw.rect(screen, BLACK, (ROAD_RIGHT, 0, 40, SCREEN_HEIGHT))  # Right roadside
        pygame.draw.line(screen, YELLOW, (ROAD_LEFT, 0), (ROAD_LEFT, SCREEN_HEIGHT), 3)  # Left road boundary
        pygame.draw.line(screen, YELLOW, (ROAD_RIGHT, 0), (ROAD_RIGHT, SCREEN_HEIGHT), 3)  # Right road boundary

    road_scroll = int((road_scroll + speed) % 80)  # Animate scrolling (wrap at 80)
    for y in range(-80 + int(road_scroll), SCREEN_HEIGHT, 80):  # Draw dashed lane lines
        pygame.draw.rect(screen, WHITE, (145, y, 10, 45))  # Left lane line (dash)
        pygame.draw.rect(screen, WHITE, (265, y, 10, 45))  # Right lane line (dash)
    return road_scroll

def run_game(screen, clock, username, settings):
    """Негізгі game loop."""
    font = pygame.font.SysFont("Verdana", 18)  # Font for HUD text

    difficulty = settings.get("difficulty", "normal")  # Get difficulty from settings
    base_speed = {"easy": 4, "normal": 5, "hard": 7}[difficulty]  # Base falling speed
    spawn_multiplier = {"easy": 0.75, "normal": 1.0, "hard": 1.35}[difficulty]  # Spawn rate multiplier

    bg = None
    bg_path = os.path.join("assets", "bg.png")  # Background image path
    if os.path.exists(bg_path):
        bg = pygame.image.load(bg_path).convert()  # Load background
        bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale to screen size

    player = Player(settings.get("car_color", "red"))  # Create player with chosen color
    all_sprites = pygame.sprite.Group(player)  # Group for all drawable objects
    traffic = pygame.sprite.Group()  # Group for enemy cars
    obstacles = pygame.sprite.Group()  # Group for obstacles
    coins = pygame.sprite.Group()  # Group for coins
    powerups = pygame.sprite.Group()  # Group for powerups
    events = pygame.sprite.Group()  # Group for road events

    score = 0  # Total game score
    coin_total = 0  # Total coins collected
    distance = 0  # Distance traveled (meters)
    road_scroll = 0  # Animation offset for road lines
    active_power = None  # Currently active powerup type
    power_end = 0  # Timestamp when current powerup expires
    shield = False  # Whether shield is active
    last_spawn = pygame.time.get_ticks()  # Last spawn timestamp
    running = True  # Game loop flag

    while running:
        now = pygame.time.get_ticks()  # Current time in milliseconds
        speed = base_speed + distance // 700  # Speed increases with distance (every 700m)

        # Nitro active болса, speed уақытша өседі.
        if active_power == "nitro" and now < power_end:
            speed += 4  # Add nitro boost
        elif active_power == "nitro" and now >= power_end:
            active_power = None  # Deactivate nitro when time expires

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # User closed window
                return {"action": "quit"}

        # Difficulty scaling: progress өскен сайын spawn жиілейді.
        density = spawn_multiplier + distance / 2000  # Spawn density increases with distance
        if now - last_spawn > max(450, int(1100 / density)):  # Dynamic spawn interval
            last_spawn = now
            choice = random.random()  # Random number 0.0 to 1.0

            if choice < 0.36:  # 36% chance: spawn traffic car
                obj = TrafficCar(speed + 2, player.rect)
                traffic.add(obj); all_sprites.add(obj)
            elif choice < 0.66:  # 30% chance: spawn obstacle
                obj = Obstacle(random.choice(["barrier", "oil", "pothole"]), speed, player.rect)
                obstacles.add(obj); all_sprites.add(obj)
            elif choice < 0.84:  # 18% chance: spawn coin
                obj = Coin(speed)
                coins.add(obj); all_sprites.add(obj)
            elif choice < 0.94:  # 10% chance: spawn powerup
                obj = PowerUp(random.choice(["nitro", "shield", "repair"]), speed)
                powerups.add(obj); all_sprites.add(obj)
            else:  # 6% chance: spawn road event
                obj = RoadEvent(random.choice(["moving_barrier", "speed_bump", "nitro_strip"]), speed)
                events.add(obj); all_sprites.add(obj)

        screen = pygame.display.get_surface()  # Get current display surface
        road_scroll = draw_background(screen, bg, road_scroll, speed)
        all_sprites.update()

        # Coin жинау.
        for coin in pygame.sprite.spritecollide(player, coins, True):  # Collision = collect
            coin_total += coin.weight  # Add coin value to total
            score += coin.weight * 10  # Add 10 points per weight unit

        # Power-ups жинау. Бір уақытта бір power-up ғана active.
        for p in pygame.sprite.spritecollide(player, powerups, True):
            if active_power is None:  # Only activate if no active powerup
                if p.kind == "nitro":
                    active_power = "nitro"
                    power_end = now + 4000  # 4 seconds duration
                    score += 25
                elif p.kind == "shield":
                    active_power = "shield"
                    shield = True
                    score += 20
                elif p.kind == "repair":
                    # Repair instant: бір obstacle тазалайды немесе bonus береді.
                    if len(obstacles) > 0:
                        obstacles.sprites()[0].kill()  # Remove first obstacle
                    else:
                        score += 30  # Bonus points if no obstacle exists

        # Dynamic road events әсері.
        hit_event = pygame.sprite.spritecollideany(player, events)
        if hit_event:
            if hit_event.kind == "nitro_strip" and active_power is None:
                active_power = "nitro"
                power_end = now + 3000  # 3 seconds duration
                hit_event.kill()  # Remove the strip
            elif hit_event.kind == "speed_bump":
                player.rect.y += 1  # Bump effect
            elif hit_event.kind == "moving_barrier":
                if shield:
                    shield = False
                    active_power = None
                    hit_event.kill()
                else:
                    running = False  # Game over

        # Traffic/obstacle collision.
        hit_traffic = pygame.sprite.spritecollideany(player, traffic)
        hit_obstacle = pygame.sprite.spritecollideany(player, obstacles)

        if hit_traffic or hit_obstacle:
            if shield:
                shield = False  # Shield blocks one collision
                active_power = None
                if hit_traffic:
                    hit_traffic.kill()  # Destroy enemy car
                if hit_obstacle:
                    hit_obstacle.kill()  # Destroy obstacle
            else:
                running = False  # Game over

        all_sprites.draw(screen)  # Draw all sprites at their positions

        distance += speed * 0.08  # Increase distance based on speed
        remaining = max(0, FINISH_DISTANCE - int(distance))  # Remaining distance to finish
        score = int(coin_total * 10 + distance + (25 if active_power else 0))  # Recalculate score

        # HUD - display on screen
        hud_lines = [
            f"Name: {username}",
            f"Score: {score}",
            f"Coins: {coin_total}",
            f"Distance: {int(distance)} / {FINISH_DISTANCE}",
            f"Remaining: {remaining}",
        ]

        y = 8
        for line in hud_lines:
            screen.blit(font.render(line, True, BLACK), (8, y))
            y += 22

        if active_power == "nitro":
            left = max(0, (power_end - now) // 1000)  # Seconds remaining
            p_text = f"Power: Nitro {left}s"
        elif active_power == "shield":
            p_text = "Power: Shield"
        else:
            p_text = "Power: None"

        screen.blit(font.render(p_text, True, BLACK), (220, 8))
        pygame.display.flip()  # Update the full display
        clock.tick(60)  # Maintain 60 frames per second

        if distance >= FINISH_DISTANCE:  # Player reached finish line
            score += 500  # Completion bonus
            running = False

    result = {"score": score, "distance": int(distance), "coins": coin_total}
    add_score(username, score, int(distance), coin_total)  # Save to leaderboard
    return {"action": "game_over", "result": result}  # Return game results to main menu