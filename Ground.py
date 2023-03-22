import pygame
from config import *
import math
import random

class Block(pygame.sprite.Sprite):
    def __init__(self, game , x, y):
        
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x* TILESIZE
        self.y = TILESIZE * y
        self.width =  TILESIZE
        self.height = TILESIZE
        self.image = self.game.terrain_spritesheet.get_sprite( 960, 448, self.width , self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    def update(self):
        self.collideAttack()
    
    def collideAttack(self):
        hits = pygame.sprite.spritecollide(self, self.game.attacks, True)
        
class Wall(pygame.sprite.Sprite):
    def __init__(self, game , x, y):
        
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x* TILESIZE
        self.y = TILESIZE * y
        self.width =  TILESIZE
        self.height = TILESIZE
        self.image = self.game.terrain_spritesheet.get_sprite( 192, 384, self.width , self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    def update(self):
        self.collideAttack()
    
    def collideAttack(self):
        hits = pygame.sprite.spritecollide(self, self.game.attacks, True)
class Grass(pygame.sprite.Sprite):
    def __init__(self, game, id, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.terrain_spritesheet.get_sprite( id * TILESIZE, 352, self.width , self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y