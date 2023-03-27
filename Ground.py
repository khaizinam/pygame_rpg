import pygame
from config import *
from Utils import *
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
        pygame.sprite.spritecollide(self, self.game.magic_attacks, True)
        hits = pygame.sprite.spritecollide(self, self.game.puzzle, False)
        if hits:
            hits[0].reset()
    
        
class Wall(pygame.sprite.Sprite):
    def __init__(self, game , x, y):
        
        self.game = game
        self._layer = BLOCK_LAYER+1
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
        hits = pygame.sprite.spritecollide(self, self.game.magic_attacks, True)
        hits = pygame.sprite.spritecollide(self, self.game.puzzle, False)
        if hits:
            hits[0].reset()
        
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
        
class HeartItem(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.x = WIN_WIDTH /2 + 60
        self.y = WIN_HEIGHT - 25
        self.width = 16
        self.height = 16
        self._layer = 5
        self.groups = self.game.icons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.spritesheet =  Spritesheet("./img/LifePot.png")
        self.image = self.spritesheet.get_sprite(0,0, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    def update(self ): pass

class Cube(pygame.sprite.Sprite):
    def __init__(self, game , x, y):
        
        self.game = game
        self._layer = BLOCK_LAYER + 1
        self.groups = self.game.all_sprites, self.game.puzzle, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.posX = x*TILESIZE
        self.posY = y*TILESIZE
        self.x = self.posX
        self.y = self.posY
        self.width =  34
        self.height = 48
        self.image = self.game.terrain_spritesheet.get_sprite( 96, 400, self.width , self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.inHole = False
    def update(self):
        self.collidePlayer()
    
    def collidePlayer(self):
        if not self.inHole:
            player = self.game.player
            if self.y <= player.y <= self.y + 16:
                if player.x + player.rect.width + 10 >= self.x and player.x < self.x:
                    self.x = player.x + player.rect.width + 10
                elif player.x - 10 <= self.width + self.x and player.x > self.x:
                    self.x = player.x - self.width - 10
            if self.x <= player.x <= self.x + 10:
                if player.y + player.rect.height + 10 >= self.y and player.y < self.y:
                    self.y = player.y + player.rect.height + 10
                elif player.y - 10 <= self.height + self.y and player.y > self.y:
                    self.y = player.y - self.height - 10
    
    def reset(self):
        self.x = self.posX
        self.y = self.posY


class Hole(pygame.sprite.Sprite):
    def __init__(self, game , x, y):
        
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x* TILESIZE
        self.y = TILESIZE * y
        self.width =  64
        self.height = 66
        self.image = self.game.terrain_spritesheet.get_sprite( 128, 384, self.width , self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    def update(self):
        self.collideAttack()
    
    def collideAttack(self):
        hits = pygame.sprite.spritecollide(self, self.game.puzzle, False)
        if hits:
            cube = hits[0]
            if self.x +16 <= cube.x <= self.x + 31 and self.y <= cube.y <= self.y + 25:
                cube.inHole = True
                cube.x = self.x + 16
                cube.y = self.y

class Gate(pygame.sprite.Sprite):
    def __init__(self, game , x, y):
        
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x* TILESIZE
        self.y = TILESIZE * y
        self.width =  128
        self.height = 34
        self.image = self.game.terrain_spritesheet.get_sprite( 224, 640, self.width , self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.isOpen = False

    def update(self):
        if self.isOpen == False and self.checkPuzzle():
            self.isOpen == True
            self.game.camera.set(self.x + self.width//2, self.y + self.height//2)
            self.kill()
    
    def checkPuzzle(self):
        solved = True
        for puzzle in self.game.puzzle:
            solved = solved and puzzle.inHole
        return solved
                
