import pygame
from player import MusicPlayer
import os

pygame.init()

screen = pygame.display.set_mode((600, 300))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont(None, 30)

player = MusicPlayer("music")

running = True
clock = pygame.time.Clock()

def format_time(ms):
    seconds = ms // 1000
    m = seconds // 60
    s = seconds % 60
    return f"{m}:{s:02}"

while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next_track()
            elif event.key == pygame.K_b:
                player.prev_track()
            elif event.key == pygame.K_q:
                running = False

    # 🎵 Current track name
    if player.playlist:
        track = os.path.basename(player.playlist[player.current_index])
    else:
        track = "No music"

    text = font.render(f"Now Playing: {track}", True, (255, 255, 255))
    screen.blit(text, (50, 50))

    # ⏱️ Time
    pos = pygame.mixer.music.get_pos()
    time_text = font.render(f"Time: {format_time(pos)}", True, (200, 200, 200))
    screen.blit(time_text, (50, 100))

    # 📊 Progress bar (fake max = 3 min)
    bar_x = 50
    bar_y = 150
    bar_width = 500
    bar_height = 20

    pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))

    progress = (pos / 180000) * bar_width  # 3 minutes = 180000 ms
    pygame.draw.rect(screen, (0, 200, 0), (bar_x, bar_y, progress, bar_height))

    pygame.display.update()
    clock.tick(30)

pygame.quit()