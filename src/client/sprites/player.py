import pygame
import os

dirname = os.path.dirname(__file__)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pixel_x = x
        self.pixel_y = y

    def update(self, dt, x, y):
        if self.pixel_x != x:
            if self.pixel_x < x:
                self.pixel_x += dt
            else:
                self.pixel_x -= dt
            return False
        elif self.pixel_y != y:
            if self.pixel_y < y:
                self.pixel_y += dt
            else:
                self.pixel_y -= dt
            return False
        else:
            return True
        
    def render(self, screen):
        self.rect.topleft = (self.pixel_x, self.pixel_y)
        screen.blit(self.image, self.rect)