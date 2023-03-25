import pygame
from config import *
from Utils import *
import math
import random

class MagicEnemyAttack(pygame.sprite.Sprite):
    
    def __init__(self, game,enemy, layer = ENEMY_LAYER):
        #game res
        self.game = game
        self._layer = layer
        self.groups = self.game.all_sprites, self.game.magic_attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.enemy = enemy

        #game setting
        self.distance = 40
        self.frame = 6
        self.width = 16
        self.height = 16
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
        

        self.explosion_animations = [self.game.explosion0_sprite.get_sprite(0, 0, self.width, self.height),
                                     self.game.explosion1_sprite.get_sprite(15, 20, self.width, self.height)]

        
    def update(self):
        self.collide()
        self.animate()
        
    
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.playerSprite, False)
        if hits and self.isAttack == 0 and self.enemy.stunByAttackCount == 0:
            self.isAttack = 1
            self.game.player.attacked(self.enemy.damge)
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
    def __init__(self, game, x, y, level ):
        #
        self.attackedTime = 0
        # Stun by attack player
        self.stunByAttackTime = FPS * 1
        self.stunByAttackCount = 0
        #
        self.respawnX = x
        self.respawnY = y
        self.dead = False
        self.level = level
        self.damge = 5 * level
        self.exp = level*6
        self.HPperLvl = 10
        self.maxHp = 20 + level * self.HPperLvl
        self.hp = self.maxHp
        self.atk = None
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.speed = ENEMY_SPEED
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.attackDuration = 0
        self.x_change = 0
        self.y_change = 0
        
        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = 30
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
        if self.dead == False:
            self.movement()
            self.animate()
            self.collide_player()
            if self.stunByAttackCount > 0 : 
                self.stunByAttackCount -= 1
                self.x_change = 0 
                self.y_change = 0
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
    def respawn(self):
        self.x = self.respawnX 
        self.y = self.respawnY 
        self.hp = self.maxHp
        self.dead = False
        pygame.sprite.Sprite.__init__(self, self.groups)

    # function define was attacked      
    def attacked(self,damge):
        self.stunByAttackCount =  self.stunByAttackTime 
        self.hp = self.hp - math.floor(damge / 5) 
        if self.hp <= 0:
            self.dead = True
            self.game.player.curentExp += self.exp
            self.kill()

    
    def moveto(self,x,y): 
        vectorX = x - self.x
        vectorY = y - self.y
        if vectorX != 0:
            vectorX = vectorX/(math.sqrt(vectorX*vectorX+vectorY*vectorY))*self.speed
        if vectorY != 0:
            vectorY = vectorY/(math.sqrt(vectorX*vectorX+vectorY*vectorY))*self.speed
        self.x_change = vectorX
        self.y_change = vectorY
        
    def distanceTo(self, x, y):
        return pygame.math.Vector2(self.x, self.y).distance_to((x, y))  
    
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
    # attacked
    def collide_player(self):
        hits = pygame.sprite.spritecollide(self, self.game.playerSprite, False)
        if hits and self.attackedTime <= 0:
            self.attackedTime = FPS
            self.game.player.attacked(self.damge)

# Bee :
#
#   
class BeeEnemy(Enemy):
    def __init__(self, game, x, y, level):
        self.attackedTime = 0
        self.exp = level*3
        self.level = level
        self.HPperLvl = 5
        self.hp = 10 + self.level * self.HPperLvl
        self.maxHp = 10 + level * self.HPperLvl
        self.damge = 2*level
        # Respaw Minion after dead
        self.respawnX = x
        self.respawnY = y
        self.dead = False
        
        
        
        #
        self.stunByAttackTime = FPS * 1
        self.stunByAttackCount = 0
        self.atk = None
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.stand = False
        self.x = x
        self.y = y
        self.width = 16 #24
        self.height = 30
        
        self.attackDuration = 0
        self.x_change = 0
        self.y_change = 0
        
        self.facing = 'left'
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = 30

        self.bee_spritesheet = Spritesheet("./img/bee.png")
        self.image = self.bee_spritesheet.get_sprite(0, 0, self.width, self.height )
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.speed = 1
        self.posx = self.x
        self.posy = self.y
        self.distance = 150
        
        self.left_animations = [self.bee_spritesheet.get_sprite(10, 34, 16, self.height),
                           self.bee_spritesheet.get_sprite(42, 34, 16, self.height),
                           self.bee_spritesheet.get_sprite(74, 34, 16, self.height)]

        self.right_animations = [self.bee_spritesheet.get_sprite(7, 98, 16, self.height),
                            self.bee_spritesheet.get_sprite(40, 98, 16, self.height),
                            self.bee_spritesheet.get_sprite(72, 98, 16, self.height)]
    
        # self.up_animations = [self.game.bee_spritesheet.get_sprite(4, 1, 24, self.height),
        #                    self.game.bee_spritesheet.get_sprite(37, 1, 24, self.height),
        #                    self.game.bee_spritesheet.get_sprite(70, 1, 24, self.height)]
        
        # self.up_animations = [self.game.bee_spritesheet.get_sprite(4, 65, 24, self.height),
        #                    self.game.bee_spritesheet.get_sprite(37, 65, 24, self.height),
        #                    self.game.bee_spritesheet.get_sprite(70, 65, 24, self.height)]
    def animate(self):
        if self.facing == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop >= 3:
                self.animation_loop = 1
                    
        elif self.facing == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop >= 3:
                self.animation_loop = 1
    def movement(self):
        if self.distanceTo(self.game.player.x, self.game.player.y) <= self.distance and self.attackedTime <= 0:
            self.stand = False
            self.moveto(self.game.player.x, self.game.player.y) 
        if self.distanceTo(self.game.player.x, self.game.player.y) > self.distance and self.stand == False:
            self.moveto(self.posx, self.posy)
        if self.x >=  self.posx - 10 and self.x <=  self.posx + 10 and self.y >= self.posy - 10 and self.y <= self.posy + 10 and self.stand == False:
            self.stand = True
        if self.x_change > 0:
            self.facing = 'right'
        elif self.x_change < 0:
            self.facing = 'left'
        return
# Bat
#
#
class BatEnemy(Enemy):
    def __init__(self, game, x, y, level):

        # status----
        self.exp = level*2
        self.damge = 1*level
        self.level = level
        self.HPperLvl = 4
        self.hp = 10 + self.level * self.HPperLvl
        self.maxHp = 10 + self.level * self.HPperLvl
        # Respaw Minion after dead --
        self.respawnX = x
        self.respawnY = y
        self.dead = False
        
       
        
        #
        self.attackedTime = 0
        self.stunByAttackTime = FPS * 1
        self.stunByAttackCount = 0
        self.atk = None
        self.stand = False
        #--------------------
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = 29 #24
        self.height = 26
        
        self.attackDuration = 0
        self.x_change = 0
        self.y_change = 0
        
        self.facing = 'left'
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = 30

        self.bee_spritesheet = Spritesheet("./img/bat.png")
        self.image = self.bee_spritesheet.get_sprite(0, 0, self.width, self.height )
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.speed = 1
        self.posx = self.x
        self.posy = self.y
        self.distance = 150
        
        self.left_animations = [self.bee_spritesheet.get_sprite(0, 38, 20, 29),
                           self.bee_spritesheet.get_sprite(40, 40, 18, 24),
                           self.bee_spritesheet.get_sprite(72, 36, 13, 27)]

        self.right_animations = [self.bee_spritesheet.get_sprite(4, 102, 20, 26),
                            self.bee_spritesheet.get_sprite(38, 104, 18, 24),
                            self.bee_spritesheet.get_sprite(75, 100, 14, 28)]
    
        # self.up_animations = [self.game.bee_spritesheet.get_sprite(4, 1, 24, self.height),
        #                    self.game.bee_spritesheet.get_sprite(37, 1, 24, self.height),
        #                    self.game.bee_spritesheet.get_sprite(70, 1, 24, self.height)]
        
        # self.up_animations = [self.game.bee_spritesheet.get_sprite(4, 65, 24, self.height),
        #                    self.game.bee_spritesheet.get_sprite(37, 65, 24, self.height),
        #                    self.game.bee_spritesheet.get_sprite(70, 65, 24, self.height)]
    def animate(self):
        if self.facing == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop >= 3:
                self.animation_loop = 1
                    
        elif self.facing == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop >= 3:
                self.animation_loop = 1
    def movement(self):
        if self.distanceTo(self.game.player.x, self.game.player.y) <= self.distance and self.attackedTime <= 0:
            self.stand = False
            self.moveto(self.game.player.x, self.game.player.y) 
        if self.distanceTo(self.game.player.x, self.game.player.y) > self.distance and self.stand == False:
            self.moveto(self.posx, self.posy)
        if self.x >=  self.posx - 10 and self.x <=  self.posx + 10 and self.y >= self.posy - 10 and self.y <= self.posy + 10 and self.stand == False:
            self.stand = True
        if self.x_change > 0:
            self.facing = 'right'
        elif self.x_change < 0:
            self.facing = 'left'
        return



class MageEnemy(Enemy):
    def attack(self):
        self.attackDuration = FPS*2
        if self.atk:
            self.atk = None
            self.attackedTime = FPS
        else:
            self.atk = MagicEnemyAttack(self.game,self,ENEMY_LAYER)
        
        
    def update(self):
        super().update()
        if self.attackDuration == 0:
            dist = pygame.math.Vector2(self.x, self.y).distance_to((self.game.player.x, self.game.player.y))
            if dist < 250:
                self.attack()
