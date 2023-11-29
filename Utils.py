import pygame
from config import *


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite


class Button:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y

        self.image = image
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
