import pygame
from config import *
import math

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, game ,o,leng):
        
        self.game = game
        self.o = o
        self.lenghBar = leng
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.health_bar
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([self.lenghBar,5])
        self.image.fill(RED)
        self.x = self.o.x + self.o.width//2 - 16
        self.y = self.o.y - 7
        self.rect = self.image.get_rect()
        self.rect.x = self.o.x
        self.rect.y = self.o.y - 7
    def update(self):
        if self.o.hp <= 0:
            self.kill()
        self.x = self.o.x
        self.y = self.o.y - 7
        width = math.floor((self.o.hp / self.o.maxHp) * self.lenghBar)
        if width <= 0:
            width = 1
        self.image = pygame.Surface([width,5])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

    def reset(self):
        pygame.sprite.Sprite.__init__(self, self.groups)

class PlayerHealthBar(pygame.sprite.Sprite):
    def __init__(self, game ,o):
        
        self.game = game
        self.o = o
        self._layer = 10
        self.groups = self.game.icons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([100,10])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = 10
        self.y = WIN_HEIGHT - (12 + 5)*3
        self.rect.x = self.x
        self.rect.y = self.y
    def update(self):
        width = math.floor((self.o.hp / self.o.maxHp) * 100)
        if width <= 0:
            width = 1
        self.image = pygame.Surface([width,10])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def reset(self):
        pygame.sprite.Sprite.__init__(self, self.groups)

class lvlBar(pygame.sprite.Sprite):
    def __init__(self, game ,o):
        
        self.game = game
        self.o = o
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.health_bar
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.font = pygame.font.Font('arial.ttf',8)
        self.text = self.font.render(f'{self.o.level}', True, WHITE)
        self.image = pygame.Surface([10,10])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.x = self.o.x - 10
        self.y = self.o.y - 10
        self.rect.x = self.x
        self.rect.y = self.y
        self.image.blit(self.text, (0, 1))
    def update(self):
        if self.o.hp <= 0:
            self.kill()
        self.x = self.o.x - 10
        self.y = self.o.y - 10
    def reset(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
