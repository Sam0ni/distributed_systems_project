import pygame
import os

dirname = os.path.dirname(__file__)

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pixel_x = x
        self.pixel_y = y