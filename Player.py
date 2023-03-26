import pygame
from config import *
from Sprite import *
from Utils import *
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, game , x, y):
        
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.playerSprite
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.attacking = False
        self.velx = 0
        self.vely = 0
        #----------
        self.potion = 3
        self.TimeNextPotion = FPS * 3
        self.potionReduce = 0
        self.level = 1
        self.atk = 5
        self.hp = 10
        self.maxHp = 10
        self.curentExp = 0
        self.nextExp = self.level * 20
        self.magicRange = 15
        self.magicReduce = 16
        self.magicTime = 0
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
        if self.potionReduce > 0:
            self.potionReduce -= 1
        if self.magicTime > 0 : 
            self.magicTime -= 1
        self.movement()
        self.animate()
        #self.collide_enemy()
        self.x += self.x_change
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.y += self.y_change
        self.rect.y += self.y_change
        self.collide_blocks('y')
        
        self.velx = 0
        self.vely = 0
        self.x_change = 0
        self.y_change = 0
    
    def usePotion(self):
        if self.hp < self.maxHp and self.potion > 0 and  self.potionReduce == 0:
            self.potionReduce = self.TimeNextPotion
            self.potion -= 1
            self.hp = self.maxHp 
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.velx = -1
            self.facing = 'left'
        elif keys[pygame.K_RIGHT]:
            self.velx = 1
            self.facing = 'right'
        elif keys[pygame.K_UP]:
            self.vely = -1
            self.facing = 'up'
        elif keys[pygame.K_DOWN]:
            self.vely = 1
            self.facing = 'down'
        if keys[pygame.K_z]:
            if self.attacking == False :
                self.meleeAttack()
        if keys[pygame.K_x]:
            if self.attacking == False and self.magicTime == 0:
                self.magicAttack()
        self.x_change += self.velx * PLAYER_SPEED
        self.y_change += self.vely * PLAYER_SPEED
    def meleeAttack(self):
        MeleeAttack(self)
    def magicAttack(self):
        self.magicTime = self.magicReduce
        MagicAttack(self)
    def attacked(self, level):
        self.hp -= level*2
        if self.hp <= 0:
            self.kill()
            self.game.playing = False
            
        
    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                for hit in hits:
                    if self.x_change > 0:
                        self.x = hit.x - self.rect.width
                    if self.x_change < 0:
                        self.x = hit.x + hit.rect.width 
        if direction == 'y': 
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                for hit in hits:
                    if self.y_change > 0 :
                        self.y = hit.y - self.rect.height
                    if self.y_change < 0 :
                        self.y = hit.y + hit.rect.height
    
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
    
    def getCenter(self):
        return self.x + self.width//2, self.y + self.height

