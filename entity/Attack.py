import math
from module.text import *
from config import *
import pygame

FACING_LEFT = -1
FACING_RIGHT = 1


class SwordAttack(pygame.sprite.Sprite):
    def __init__(self, game, entity):
        self.game = game
        self.entity = entity
        self.groups = self.game.acttack_layer
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.w = self.entity.w + 2*TILESIZE
        self.h = self.entity.h

        # move direction

        # animation
        self.image = pygame.Surface([self.w, self.h])
        self.image.fill(BLUE)
        # draw on screen
        self.rect = self.image.get_rect()

        self.x = self.entity.x-self.entity.w/2 - TILESIZE
        self.y = self.entity.y - self.h
        self.rect.x = self.x - self.game.camera.deltaX()
        self.rect.y = self.y - self.game.camera.deltaY()

    def updateAttack(self):
        self.x = self.entity.x-self.entity.w/2 - TILESIZE
        self.y = self.entity.y - self.h
        self.rect.x = self.x - self.game.camera.deltaX()
        self.rect.y = self.y - self.game.camera.deltaY()
