import pygame
import random
import time

class Treasure(pygame.sprite.Sprite):
    def __init__(self, pos, image, duration=5):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.spawn_time = time.time()
        self.duration = duration

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        current_time = time.time()
        if current_time - self.spawn_time > self.duration:
            self.kill()

    def hit(self):
        print('treasure collected')
