import pygame
from config import *
import math


class PointerMouse(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game

        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.kill()

        self.w = 8
        # move direction
        self.x = x - self.w/2
        self.y = y - self.w/2

        # animation
        self.image = pygame.Surface([self.w, self.w])
        self.image.fill(RED)
        # draw on screen
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def show(self):
        self.game.all_sprites.add(self)

    def hide(self):
        self.kill()

    def click(self, x, y):
        self.show()
        self.x = self.game.camera.deltaX() + (x - self.w/2)
        self.y = self.game.camera.deltaY() + (y - self.w/2)
        print(self.x, self.y)
