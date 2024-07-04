# cut_scene.py
import pygame

class IntroCutScene:
    def __init__(self, screen, font, duration=3000):
        self.screen = screen
        self.font = font
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

    def update(self):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        if elapsed_time >= self.duration:
            return False
        return True

    def draw(self):
        self.screen.fill((0, 0, 0))  # Fill screen with black
        text_surface = self.font.render("Welcome to the Game!", True, (255, 255, 255))
        self.screen.blit(text_surface, (self.screen.get_width() // 2 - text_surface.get_width() // 2, self.screen.get_height() // 2))
        pygame.display.update()


class LevelCompletedCutScene:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.timer = 0
        self.duration = 100  # Duration of the cutscene in frames

    def update(self):
        self.timer += 1
        if self.timer >= self.duration:
            return False
        return True

    def draw(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render("Level Completed", True, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - text.get_height() // 2))
        pygame.display.update()