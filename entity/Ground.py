import math
from module.text import *
from config import *
import pygame


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.game = game

        self.groups = self.game.ground_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.w = w * TILESIZE
        self.h = h * TILESIZE
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        # animation
        self.image = pygame.Surface([self.w, self.h])
        self.image.fill(BLACK)
        # draw on screen
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def getCenter(self):
        return self.x - self.w // 2, self.y - self.h//2

    def animateDraw(self, camera):
        self.rect.x = self.x - camera.deltaX()
        self.rect.y = self.y - camera.deltaY()

    def update(self):
        self.animateDraw(self.game.camera)
