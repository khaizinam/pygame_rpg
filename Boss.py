import pygame, math, random
from Enemy import Enemy, BatEnemy
from RespawnMinion import HealthBar, lvlBar
from config import *

class Boss(Enemy):

    FACING_LEFT = 1
    FACING_RIGHT = 2

    IDLE = 0
    ATTACK = 1

    STAR_SHOOT = 1
    TRIPLET_SHOOT = 2
    SPAWN_MINION = 3
    CHASE = 4
    ULTIMATE = 5

    def __init__(self, game, x1, x2, y1, y2, lvl):
        self.game = game
        self.level = lvl
        self.stunByAttackTime = FPS * 2
        self.stunByAttackCount = 0
        self.posx = x
        self.posy = y
        self.distance = 400
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.zone = (x1, x2, y1, y2)
        self.stage = 0
        self.widthStage = [85,122,87]
        self.heightStage = [94,110,110]
        self.width = self.widthStage[self.stage]
        self.height = self.heightStage[self.stage]
        self.x = (x1 + x2)//2 - (self.width - TILESIZE)//2
        self.y = (y1 + y2)//2 - self.height + TILESIZE
        print(x1, x2, y1, y2, self.x, self.y)
        self.velx = 0 
        self.vely = 0
        self.tick = 0
        self.facing = self.FACING_LEFT

        self.maxHp = 1000
        self.hp = self.maxHp

        self.animation = [
            [self.game.boss1_spritesheet.get_sprite(0, 0, self.widthStage[0], self.heightStage[0] ),
            self.game.boss1_spritesheet.get_sprite(85, 0, self.widthStage[0], self.heightStage[0] ),
            self.game.boss1_spritesheet.get_sprite(170, 0, self.widthStage[0], self.heightStage[0] ),
            self.game.boss1_spritesheet.get_sprite(255, 0, self.widthStage[0], self.heightStage[0] ),
            self.game.boss1_spritesheet.get_sprite(0, 94, self.widthStage[0], self.heightStage[0] ),
            self.game.boss1_spritesheet.get_sprite(85, 94, self.widthStage[0], self.heightStage[0] ),
            self.game.boss1_spritesheet.get_sprite(170, 94, self.widthStage[0], self.heightStage[0] ),
            self.game.boss1_spritesheet.get_sprite(255, 94, self.widthStage[0], self.heightStage[0] )],
            [self.game.boss2_spritesheet.get_sprite(0, 0, self.widthStage[1], self.heightStage[1] ),
            self.game.boss2_spritesheet.get_sprite(122, 0, self.widthStage[1], self.heightStage[1] ),
            self.game.boss2_spritesheet.get_sprite(244, 0, self.widthStage[1], self.heightStage[1] ),
            self.game.boss2_spritesheet.get_sprite(366, 0, self.widthStage[1], self.heightStage[1] ),
            self.game.boss2_spritesheet.get_sprite(0, 110, self.widthStage[1], self.heightStage[1] ),
            self.game.boss2_spritesheet.get_sprite(122, 110, self.widthStage[1], self.heightStage[1] ),
            self.game.boss2_spritesheet.get_sprite(244, 110, self.widthStage[1], self.heightStage[1] ),
            self.game.boss2_spritesheet.get_sprite(366, 110, self.widthStage[1], self.heightStage[1] ),]
        ]

        self.info = [HealthBar(self.game, self)]

        self.image = self.animation[self.stage][0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.awakened = False
        self.actionQueue = [self.IDLE, self.ATTACK, self.ATTACK, self.ATTACK]
        self.actionIndex = 0
        self.action = None
        self.timmer = 0

        self.attackStage = [
            [self.TRIPLET_SHOOT, self.STAR_SHOOT, self.TRIPLET_SHOOT, self.STAR_SHOOT, self.ULTIMATE],
            [self.CHASE, self.CHASE, self.SPAWN_MINION],
        ]

        self.isChasing = False
        self.speed = 5
        self.cooldown = 200
        
    def respawn(self):
        self.x = self.posx
        self.y = self.posy
        self.hp = self.maxHp
        self.dead = False
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.useBulletHell = False
        self.nBullet = 0
        self.bulletCooldown = 5
        self.bulletTimmer = 0
    
    def update(self):
        if self.awakened:
            self.animate()
                
            if (self.timmer <= 0):
                self.action = self.actionQueue[self.actionIndex]
                self.actionIndex = (self.actionIndex + 1) % len(self.actionQueue)
                if self.action == self.IDLE:
                    self.idle()
                elif self.action == self.ATTACK:
                    self.offend()
                elif self.action == self.TELEPORT:
                    self.teleport()
                elif self.action == self.ULTIMATE:
                    self.bulletHell()

            if self.isChasing:
                self.movement()
            if self.useBulletHell:
                self.bulletHellTriggered()

            self.timmer -= 1
            self.x += self.velx
            self.y += self.vely
            self.velx = 0
            self.vely = 0

    def movement(self):
        player = self.game.player
        px, py = player.getCenter()
        bx, by = self.getCenter()
        vx = px - bx
        vy = py - by
        d = math.sqrt(vx*vx + vy*vy)
        if (d != 0):
            self.velx = self.speed*float(vx/d)
            self.vely = self.speed*float(vy/d)
            

    def animate(self):
        animation = self.animation[self.stage]
        playerX = self.game.player.x
        if playerX < self.x + self.width//2:
            self.image = pygame.transform.flip( animation[math.floor(self.tick)], True, False)
        else:
            self.image = animation[math.floor(self.tick)]
        self.tick += 0.1
        if self.tick > len(animation):
            self.tick=0

    def teleport(self):
        player = self.game.player
        x, y = player.getCenter()
        d = 250
        angle = random.random()*2*math.pi
        posx = math.cos(angle)*d
        posy = math.sin(angle)*d
        self.x ,self.y = self.validatePos( x + posx, y + posy)
        self.timmer = 25

    def idle(self):
        self.isChasing = False
        self.timmer = 100

    def chase(self):
        self.isChasing = True
        self.timmer = 100

    def validatePos(self, x, y):
        x1, x2, y1, y2 = self.zone
        if x < x1 + TILESIZE:
            x = x1 + TILESIZE
        elif x > x2 - self.width - TILESIZE:
            x = x2 - self.width
        
        if y < y1 + TILESIZE:
            y = y1 + TILESIZE
        elif y > y2 - self.height - TILESIZE:
            y = y2 - self.height - TILESIZE
        return x, y

    def getCenter(self):
        w = self.width
        h = self.height
        return self.x + w//2, self.y + h
    
    def offend(self):
        self.teleport()
        move = random.choice(self.attackStage[self.stage])
        self.timmer = 75
        if move == self.STAR_SHOOT:
            self.startActack()
        elif move == self.CHASE:
            self.chase()
        elif move == self.SPAWN_MINION:
            self.spawnMinion()
        elif move == self.TRIPLET_SHOOT:
            self.tripletShoot()
        elif move == self.ULTIMATE:
            self.bulletHell()

    def startActack(self):
        x,y = self.getCenter()
        nBullet = 8
        for i in range(nBullet):
            self._shootBullet(i*2*math.pi/nBullet, 5)
            # vx = math.cos(i*2*math.pi/nBullet)*5
            # vy = math.sin(i*2*math.pi/nBullet)*5
            # BossBullet(self.game, self, vx, vy)
    
    def spawnMinion(self):
        x,y =self.getCenter()
        nMinion = 4
        for i in range(nMinion):
            dx = math.cos(i*2*math.pi/nMinion)*50
            dy = math.sin(i*2*math.pi/nMinion)*50
            bat = BatEnemy(self.game, x+dx, y+dy, 1)
            HealthBar(self.game, bat)
            lvlBar(self.game, bat)

    def attacked(self, damge):
        self.hp -= damge
        if (self.hp <= 0):
            self.kill()
        elif (self.hp <= self.maxHp//2):
            self.stage = 1
            self.actionIndex = 0
            self.width = self.widthStage[1]
            self.height = self.heightStage[1]
    
    def bulletHell(self):
        self.nBullet = 100
        self.useBulletHell = True
        self.bulletTimmer = 0
        x1, x2, y1, y2 = self.zone
        self.x = (x1 + x2)//2 - (self.width - TILESIZE)//2
        self.y = (y1 + y2)//2 - self.height + TILESIZE
        self.timmer = 1000
    
    def bulletHellTriggered(self):
        if (self.bulletTimmer == self.bulletCooldown):
            self._shootBullet(self.nBullet*2*math.pi/16, 5)
            self.bulletTimmer = 0
            self.nBullet -= 1
            if self.nBullet == 0:
                self.useBulletHell = False
                self.timmer = 50
                self.actionIndex = 0
        self.bulletTimmer += 1
    
    def tripletShoot(self):
        px, py = self.game.player.getCenter()
        x,y = self.getCenter()
        a = math.atan2((py-y),(px-x))
        print((px-x),(py-y),a)
        self._shootBullet(a, 5)
        self._shootBullet(a - 0.2618, 5.1764)
        self._shootBullet(a + 0.2618, 5.1764)


    def _shootBullet(self, a, s):
        vx = math.cos(a)*s
        vy = math.sin(a)*s
        BossBullet(self.game, self, vx, vy)

class BossBullet(pygame.sprite.Sprite):
    ATTACK_MOVE_1 = 1
    ATTACK_MOVE_2 = 2
    ATTACK_MOVE_3 = 3

    FACING_LEFT = 1
    FACING_RIGHT = 2

    def __init__(self, game, host, vx, vy):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.width = 13*3
        self.height = 13*3
        x, y = host.getCenter()
        self.x = x - self.width//2
        self.y = y - self.height//2
        self.x0 = self.x
        self.y0 = self.y
        self.vx = vx
        self.vy = vy
        self.tick = 0

        self.animation = [  
            pygame.transform.scale_by(self.game.boss_bullet_spritesheet.get_sprite(0,0, 13, 13), 3),
            pygame.transform.scale_by(self.game.boss_bullet_spritesheet.get_sprite(13,0, 13, 13), 3),
            pygame.transform.scale_by(self.game.boss_bullet_spritesheet.get_sprite(26,0, 13, 13), 3),
            pygame.transform.scale_by(self.game.boss_bullet_spritesheet.get_sprite(39,0, 13, 13), 3),
            pygame.transform.scale_by(self.game.boss_bullet_spritesheet.get_sprite(52,0, 13, 13), 3)
        ]

        self.image = self.animation[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.distance = 102400 # 320**2
        self.d = 0
    
    def update(self):        
        self.animate()
        self.collide()
        if (self.d < self.distance):
            self.x += self.vx
            self.y += self.vy
            self.rect.x = self.x
            self.rect.y = self.y
            self.d = (self.x - self.x0)**2 + (self.y - self.y0)**2
        else:
            self.kill()
        


    def animate(self):
        self.image = self.animation[math.floor(self.tick)]
        self.tick += 0.1

        if self.tick > len(self.animation):
            self.tick=0

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.playerSprite, False)
        if hits:
            self.game.player.attacked(20)
            self.d = self.distance

