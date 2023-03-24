import pygame
from config import *
from Sprite import *
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, game , x, y):
        
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.playerSprite
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.attacking = False
        
        #----------
        self.imume = 0
        self.atk = 5
        self.deffend = 2
        self.hp = 10
        self.maxHp = 10
        #-----------
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.x_change = 0
        self.y_change = 0
        
        self.facing = 'down'
        self.animation_loop = 1
        self.image = self.game.character_spritesheet.get_sprite( 3, 2, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.animation = PlayerSprite(game,self)
        
        self.down_animations = self.animation.moveDown()

        self.up_animations = self.animation.moveUp()

        self.left_animations = self.animation.moveLeft()

        self.right_animations = self.animation.moveRight()
        
    def update(self):
        self.movement()
        self.animate()
        #self.collide_enemy()
        self.x += self.x_change
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.y += self.y_change
        self.rect.y += self.y_change
        self.collide_blocks('y')
        
        self.x_change = 0
        self.y_change = 0
        
    def movement(self):
        keys = pygame.key.get_pressed()
        if self.attacking == False :
            if keys[pygame.K_LEFT]:
                self.x_change -= PLAYER_SPEED
                self.facing = 'left'
            elif keys[pygame.K_RIGHT]:
                self.x_change += PLAYER_SPEED
                self.facing = 'right'
            elif keys[pygame.K_UP]:
                self.y_change -= PLAYER_SPEED
                self.facing = 'up'
            elif keys[pygame.K_DOWN]:
                self.y_change += PLAYER_SPEED
                self.facing = 'down'
    
    def attacked(self,damage):
        self.hp = self.hp - damage
        if self.hp <= 0:
            self.hp = 0
            self.kill()
            self.game.playing = False
        
    def collide_blocks(self, direction):
    
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.x = hits[0].x - self.rect.width
                if self.x_change < 0:
                    self.x = hits[0].x + hits[0].rect.width
                    
        
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0 and self.x_change == 0:
                    self.y = hits[0].y - self.rect.height
                if self.y_change < 0 and self.x_change == 0:
                    self.y = hits[0].y + hits[0].rect.height
    
    def animate(self):
        
        if self.facing == 'down':
            if self.y_change == 0:   
                self.image = self.animation.standDown()
            else :
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
                    
        if self.facing == 'up':
            if self.y_change == 0:   
                self.image = self.animation.standUp()
            else :
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == 'left':
            if self.x_change == 0:   
                self.image = self.animation.standLeft()
            else :
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
                    
        if self.facing == 'right':
            if self.x_change == 0:   
                self.image = self.animation.standRight()
            else :
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

