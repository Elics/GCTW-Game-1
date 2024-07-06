import pygame

class Trash(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def hit(self):
        print('collected')
