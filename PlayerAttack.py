import pygame
from config import *
from Utils import *
class MeleeAttack(pygame.sprite.Sprite):
    
    def __init__(self, player):
        self.game = player.game
        self.player = player
        self.damge = player.atk
        self.player.attacking = True
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x_change = 0
        self.y_change = 0
        if self.player.facing == 'up':
            x = self.player.x 
            y = self.player.y - TILESIZE
        if self.player.facing == 'down':
            x = self.player.x
            y = self.player.y + TILESIZE
        if self.player.facing == 'left':
            x = self.player.x - TILESIZE
            y =self.player.y
        if self.player.facing == 'right':
            x = self.player.x + TILESIZE
            y = self.player.y
            
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.animation_loop = 0
        self.spritesheet = Spritesheet("./img/attack.png")
        self.image = self.spritesheet.get_sprite(0, 0, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.right_animations = [self.spritesheet.get_sprite(0, 64, self.width, self.height),
                            self.spritesheet.get_sprite(32, 64, self.width, self.height),
                            self.spritesheet.get_sprite(64, 64, self.width, self.height),
                            self.spritesheet.get_sprite(96, 64, self.width, self.height),
                            self.spritesheet.get_sprite(128, 64, self.width, self.height)]

        self.down_animations = [self.spritesheet.get_sprite(0, 32, self.width, self.height),
                            self.spritesheet.get_sprite(32, 32, self.width, self.height),
                            self.spritesheet.get_sprite(64, 32, self.width, self.height),
                            self.spritesheet.get_sprite(96, 32, self.width, self.height),
                            self.spritesheet.get_sprite(128, 32, self.width, self.height)]

        self.left_animations = [self.spritesheet.get_sprite(0, 96, self.width, self.height),
                            self.spritesheet.get_sprite(32, 96, self.width, self.height),
                            self.spritesheet.get_sprite(64, 96, self.width, self.height),
                            self.spritesheet.get_sprite(96, 96, self.width, self.height),
                            self.spritesheet.get_sprite(128, 96, self.width, self.height)]

        self.up_animations = [self.spritesheet.get_sprite(0, 0, self.width, self.height),
                            self.spritesheet.get_sprite(32, 0, self.width, self.height),
                            self.spritesheet.get_sprite(64, 0, self.width, self.height),
                            self.spritesheet.get_sprite(96, 0, self.width, self.height),
                            self.spritesheet.get_sprite(128, 0, self.width, self.height)] 
    def update(self):
        self.animate()
        self.collide()
    
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            hits[0].attacked(self.damge)
            if self.player.facing == 'left':
                hits[0].x -= 2
            elif self.player.facing == 'right':
                hits[0].x += 2
            if self.player.facing == 'up':
                hits[0].y -= 2
            if self.player.facing == 'down':
                hits[0].y += 2
        hits2 = pygame.sprite.spritecollide(self, self.game.magic_attacks, True)
    
     
    def animate(self):
        direction = self.game.player.facing
        
        if direction == 'up':
            self.x = self.game.player.x
            self.y = self.game.player.y - TILESIZE
            self.image = self.up_animations[math.floor(self.animation_loop)]

        
        if direction == 'down':
            self.x = self.game.player.x
            self.y = self.game.player.y + TILESIZE
            self.image = self.down_animations[math.floor(self.animation_loop)]


                
        if direction == 'left':
            self.x = self.game.player.x - TILESIZE
            self.y = self.game.player.y
            self.image = self.left_animations[math.floor(self.animation_loop)]


        if direction == 'right':
            self.x = self.game.player.x + TILESIZE
            self.y = self.game.player.y
            self.image = self.right_animations[math.floor(self.animation_loop)]

        self.animation_loop += 1
        if self.animation_loop >= 5 :
            self.player.attacking = False
            self.kill()
            del self
            
class MagicAttack(pygame.sprite.Sprite):
    
    def __init__(self, player):
        #init 
        self.game = player.game
        self.player = player
        
        #
        self.damge = player.atk
        
        # groups 
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.magic_attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        #position facing
        if self.player.facing == 'up':
            self.x_change = 0
            self.y_change = - BULLET_SPD
            x = self.player.x 
            y = self.player.y - TILESIZE
        if self.player.facing == 'down':
            self.x_change = 0
            self.y_change = BULLET_SPD
            x = self.player.x
            y =self.player.y + TILESIZE
        if self.player.facing == 'left':
            self.x_change = - BULLET_SPD
            self.y_change = 0
            x = self.player.x - TILESIZE
            y =self.player.y
        if self.player.facing == 'right':
            self.x_change = BULLET_SPD
            self.y_change = 0
            x = self.player.x + TILESIZE
            y = self.player.y
            
        self.x = x
        self.y = y
        self.width = 28
        self.height = 28
        
        self.animation_loop = 0
        self.spritesheet = Spritesheet("./img/attack.png")
        self.image = self.spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.right_animations = self.spritesheet.get_sprite(64, 64, self.width, self.height)

        self.down_animations = self.spritesheet.get_sprite(64, 32, self.width, self.height)

        self.left_animations = self.spritesheet.get_sprite(64, 96, self.width, self.height)

        self.up_animations = self.spritesheet.get_sprite(64, 0, self.width, self.height)
        direction = self.player.facing
        
        if direction == 'up':
            self.image = self.up_animations

        
        if direction == 'down':
            self.image = self.down_animations


                
        if direction == 'left':
            self.image = self.left_animations


        if direction == 'right':
            self.image = self.right_animations
        
    def update(self):
        self.x += self.x_change
        self.y += self.y_change
        self.animate()
        self.collide()
    
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            hits[0].attacked(self.damge * 5)
            if self.player.facing == 'left':
                hits[0].x -= 4
            elif self.player.facing == 'right':
                hits[0].x += 4
            if self.player.facing == 'up':
                hits[0].y -= 4
            if self.player.facing == 'down':
                hits[0].y += 4
            self.kill()
            del self
     
    def animate(self):
        #self.image = self.game.magic_attack.get_sprite(0, 0, self.width, self.height)

        self.animation_loop += 1
        if self.animation_loop >= math.floor(self.player.magicRange) :
            self.kill()
            del self