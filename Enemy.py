import pygame
from config import *
import math
import random

class EnemyAttack(pygame.sprite.Sprite):
    
    def __init__(self, game,enemy, layer = ENEMY_LAYER):
        #game res
        self.game = game
        
        
        self._layer = layer
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.enemy = enemy

        #game setting
        self.distance = 40
        self.frame = 8
        self.width = 32
        self.height = 32
        self.delayFrame = 5

        #game logic
        self.isAttack = 0
        self.x = enemy.x
        self.y = enemy.y
        
        self.vectorX = self.game.player.x - self.x
        self.vectorY = self.game.player.y - self.y
        self.vectorX, self.vectorY = self.vectorX/(math.sqrt(self.vectorX*self.vectorX+self.vectorY*self.vectorY))*self.frame, self.vectorY/(math.sqrt(self.vectorX*self.vectorX+self.vectorY*self.vectorY))*self.frame
        
        self.animation_loop = 0

        
        
        
        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        

        self.explosion_animations = [self.game.explosion0_sprite.get_sprite(15, 20, self.width, self.height),
                                     self.game.explosion1_sprite.get_sprite(15, 20, self.width, self.height)]

        
    def update(self):
        self.collide()
        self.animate()
        
    
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.playerSprite, False)
        if hits and self.isAttack == 0:
            self.isAttack = 1
            self.game.player.attacked(self.enemy.level)
            self.animation_loop = self.distance
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if hits:
            self.animation_loop = self.distance
        
     
    def animate(self):
        
        if self.animation_loop > self.distance:
            self.image = self.explosion_animations[1]
            self.animation_loop += 1
            if self.animation_loop > self.distance + self.delayFrame:
                self.kill()
            return

        self.x = self.x + self.vectorX
        self.y = self.y + self.vectorY
        self.image = self.explosion_animations[0]
        
        self.animation_loop += 1
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, level = 1):
        self.attackedTime = 0
        self.level = level
        self.hp = level*10
        self.atk = None
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.attackDuration = 0
        self.x_change = 0
        self.y_change = 0
        
        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(30,50)
        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height )
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.left_animations = [self.game.character_spritesheet.get_sprite(3, 3, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]

        self.right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]
        
    def update(self):
        self.movement()
        self.animate()
        self.collide_player()
        self.x += self.x_change
        self.y += self.y_change
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.x_change = 0
        self.y_change = 0
        self.attackedTime -= 1
        if self.attackedTime <= 0:
            self.attackedTime = 0
        self.attackDuration -= 1
        if self.attackDuration <= 0:
            self.attackDuration = 0
        
        
    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'
        
        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'
                
    def animate(self):

        
        if self.facing == 'left':
            if self.x_change == 0:   
                self.image = self.game.character_spritesheet.get_sprite( 3, 98, self.width, self.height )
            else :
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
                    
        if self.facing == 'right':
            if self.x_change == 0:   
                self.image = self.game.character_spritesheet.get_sprite( 3, 66, self.width, self.height )
            else :
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

    def collide_player(self):
        hits = pygame.sprite.spritecollide(self, self.game.playerSprite, False)
        if hits and self.attackedTime <= 0:
            self.attackedTime = FPS
            self.game.player.attacked(self.level)
    

class BrawEnemy(Enemy):
    def __init__(self, game, x, y, level = 1):
        super().__init__(game,x,y,level)
        self.speed = 5
        self.distance = 300
    
    def movement(self):
        if pygame.math.Vector2(self.x, self.y).distance_to((self.game.player.x, self.game.player.y)) < self.distance and self.attackedTime <= 0:
            vectorX = self.game.player.x - self.x
            vectorY = self.game.player.y - self.y
            vectorX, vectorY = vectorX/(math.sqrt(vectorX*vectorX+vectorY*vectorY))*self.speed, vectorY/(math.sqrt(vectorX*vectorX+vectorY*vectorY))*self.speed
            self.x_change = vectorX
            self.y_change = vectorY
        return





class RangeEnemy(Enemy):
    def attack(self):
        self.attackDuration = FPS*2
        if self.atk:
            self.atk = None
            self.attackedTime = FPS
        else:
            self.atk = EnemyAttack(self.game,self,ENEMY_LAYER)
        
        
    def update(self):
        super().update()
        if self.attackDuration == 0:
            dist = pygame.math.Vector2(self.x, self.y).distance_to((self.game.player.x, self.game.player.y))
            if dist < 300:
                self.attack()
