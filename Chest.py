import pygame
from config import *
from Utils import *

class Chest(pygame.sprite.Sprite):
    def __init__(self, game , x, y):
        
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks, self.game.chests
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x
        self.y = y
        self.width =  32
        self.height = 32
        self.spritesheet = Spritesheet("./img/chest.png")
        self.image = self.spritesheet.get_sprite(0, 0, self.width, self.height)
        self.time_attacked = 20
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        
    def update(self):
        self.is_detroyed()
    
    def is_detroyed(self):
        if self.time_attacked <= 0:
            self.game.player.magicTimeAttackUp(4)
            self.game.player.magicRangeUp(1)
            self.kill()
            
    def reset(self):
        self.time_attacked = 20
        pygame.sprite.Sprite.__init__(self, self.groups)
        
class PotionItem(pygame.sprite.Sprite):
    def __init__(self, game,x,y):
        self.game = game
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self._layer = BLOCK_LAYER - 1
        self.groups = self.game.all_sprites,self.game.potions
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.spritesheet =  Spritesheet("./img/LifePot.png")
        self.image = self.spritesheet.get_sprite(0,0, self.width, self.height)
        self.pickSound = pygame.mixer.Sound('./audio/coin.mp3')
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def update(self ): 
        self.collide_player()
    
    def collide_player(self):
        hits = pygame.sprite.spritecollide(self, self.game.playerSprite, False)
        if hits:
            self.pickSound.play()
            self.game.player.potion+=1
            self.kill()
                 
    def reset(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
    

        