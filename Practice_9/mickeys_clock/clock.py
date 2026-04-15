import pygame
import datetime
import math

class MickeyClock:
    def __init__(self, screen):
        self.screen = screen
        self.center = (
            screen.get_width() // 2,
            screen.get_height() // 2
        )
        self.radius = 200
        self.font = pygame.font.SysFont("Arial", 25)

    def draw(self):
        now = datetime.datetime.now()

        minutes = now.minute
        seconds = now.second

        self.screen.fill((255, 255, 255))

        # ⭕ Clock circle
        pygame.draw.circle(self.screen, (0, 0, 0), self.center, self.radius, 3)

        # 🔢 NUMBERS (1–12)
        for i in range(1, 13):
            angle = math.radians(i * 30 - 90)

            x = self.center[0] + math.cos(angle) * (self.radius - 30)
            y = self.center[1] + math.sin(angle) * (self.radius - 30)

            text = self.font.render(str(i), True, (0, 0, 0))
            rect = text.get_rect(center=(x, y))

            self.screen.blit(text, rect)

        # 📏 TICKS (minute lines)
        for i in range(60):
            angle = math.radians(i * 6 - 90)

            start = (
                self.center[0] + math.cos(angle) * (self.radius - 10),
                self.center[1] + math.sin(angle) * (self.radius - 10)
            )

            if i % 5 == 0:
                end = (
                    self.center[0] + math.cos(angle) * (self.radius - 20),
                    self.center[1] + math.sin(angle) * (self.radius - 20)
                )
                width = 3
            else:
                end = (
                    self.center[0] + math.cos(angle) * (self.radius - 15),
                    self.center[1] + math.sin(angle) * (self.radius - 15)
                )
                width = 1

            pygame.draw.line(self.screen, (0, 0, 0), start, end, width)

        # ⏱️ Second hand
        sec_angle = math.radians(seconds * 6 - 90)
        sec_x = self.center[0] + math.cos(sec_angle) * (self.radius - 30)
        sec_y = self.center[1] + math.sin(sec_angle) * (self.radius - 30)

        pygame.draw.line(self.screen, (255, 0, 0), self.center, (sec_x, sec_y), 2)

        # ⏱️ Minute hand
        min_angle = math.radians(minutes * 6 - 90)
        min_x = self.center[0] + math.cos(min_angle) * (self.radius - 60)
        min_y = self.center[1] + math.sin(min_angle) * (self.radius - 60)

        pygame.draw.line(self.screen, (0, 0, 0), self.center, (min_x, min_y), 5)

        # ⚫ Center dot
        pygame.draw.circle(self.screen, (0, 0, 0), self.center, 5)