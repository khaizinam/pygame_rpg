import pygame
from config import *
import math

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, game ,o):
        
        self.game = game
        self.o = o
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.health_bar
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.image = pygame.Surface([25,5])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = self.o.x
        self.rect.y = self.o.y - 7
    def update(self):
        if self.o.hp <= 0:
            self.kill()
        self.x = self.o.x
        self.y = self.o.y - 7
        width = math.floor((self.o.hp / self.o.maxHp) * 25)
        if width <= 0:
            width = 1
        self.image = pygame.Surface([width,5])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
    def reset(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
