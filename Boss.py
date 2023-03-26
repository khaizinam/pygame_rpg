import pygame, math, random
from Enemy import Enemy, BatEnemy
from HealthBar import HealthBar, lvlBar
from config import *


class Boss(pygame.sprite.Sprite):
    FACING_LEFT = 1
    FACING_RIGHT = 2

    IDLE = 0
    ATTACK = 1

    STAR_SHOOT = 1
    TRIPLET_SHOOT = 2
    SPAWN_MINION = 3
    CHASE = 4
    ULTIMATE = 5

    def __init__(self, game, x, y, x1, x2, y1, y2, lvl):
        self.game = game
        self.level = lvl
        self.stunByAttackTime = FPS * 2
        self.stunByAttackCount = 0
        self.distance = 400
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.hp = 700
        self.maxHp = 700
        self.stage = 1
        self.width = [85, 122, 87]
        self.height = [94, 110, 110]
        self.x = x
        self.y = y
        self.velx = 0
        self.vely = 0
        self.tick = 0

        self.maxHp = 1000
        self.hp = self.maxHp

        self.animation = [
            [self.game.boss1_spritesheet.get_sprite(0, 0, self.width[0], self.height[0]),
             self.game.boss1_spritesheet.get_sprite(85, 0, self.width[0], self.height[0]),
             self.game.boss1_spritesheet.get_sprite(170, 0, self.width[0], self.height[0]),
             self.game.boss1_spritesheet.get_sprite(255, 0, self.width[0], self.height[0]),
             self.game.boss1_spritesheet.get_sprite(0, 94, self.width[0], self.height[0]),
             self.game.boss1_spritesheet.get_sprite(85, 94, self.width[0], self.height[0]),
             self.game.boss1_spritesheet.get_sprite(170, 94, self.width[0], self.height[0]),
             self.game.boss1_spritesheet.get_sprite(255, 94, self.width[0], self.height[0])],
            [self.game.boss2_spritesheet.get_sprite(0, 0, self.width[1], self.height[1]),
             self.game.boss2_spritesheet.get_sprite(122, 0, self.width[1], self.height[1]),
             self.game.boss2_spritesheet.get_sprite(244, 0, self.width[1], self.height[1]),
             self.game.boss2_spritesheet.get_sprite(366, 0, self.width[1], self.height[1]),
             self.game.boss2_spritesheet.get_sprite(0, 110, self.width[1], self.height[1]),
             self.game.boss2_spritesheet.get_sprite(122, 110, self.width[1], self.height[1]),
             self.game.boss2_spritesheet.get_sprite(244, 110, self.width[1], self.height[1]),
             self.game.boss2_spritesheet.get_sprite(366, 110, self.width[1], self.height[1]), ]
        ]

        self.image = self.animation[self.stage][0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.actionCycle = FPS * 5
        self.countDown = 0

        self.isChasing = False
        self.speed = 5
        self.cooldown = 200

    def respawn(self):
        self.x = self.posx
        self.y = self.posy
        self.hp = self.maxHp
        self.dead = False
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        self.animate()
        self.movement()

        if (self.countDown == self.actionCycle):
            self.rangeActack()
            self.countDown = 0
        self.countDown += 1
        if self.stunByAttackCount > 0:
            self.stunByAttackCount -= 1
            self.velx = 0
            self.vely = 0
        self.x += self.velx
        self.y += self.vely

    def attacked(self, damge):
        self.stunByAttackCount = self.stunByAttackTime
        self.hp -= math.floor(damge / 5)
        if self.hp <= 0:
            self.dead = True
            self.game.player.curentExp += 100
            self.kill()

    def moveto(self, x, y):
        vectorX = x - self.x
        vectorY = y - self.y
        if vectorX != 0:
            vectorX = vectorX / (math.sqrt(vectorX * vectorX + vectorY * vectorY)) * self.speed
        if vectorY != 0:
            vectorY = vectorY / (math.sqrt(vectorX * vectorX + vectorY * vectorY)) * self.speed
        self.velx = vectorX
        self.vely = vectorY

    def distanceTo(self, x, y):
        return pygame.math.Vector2(self.x, self.y).distance_to((x, y))
        # def movement(self):

    #     player = self.game.player
    #     px, py = player.getCenter()
    #     bx, by = self.getCenter()
    #     vx = px - bx
    #     vy = py - by
    #     d = math.sqrt(vx*vx + vy*vy)
    #     if (d != 0):
    #         self.velx = self.speed*float(vx/d)
    #         self.vely = self.speed*float(vy/d)

    def movement(self):
        if self.distanceTo(self.game.player.x, self.game.player.y) <= self.distance:
            self.stand = False
            self.moveto(self.game.player.x - 45, self.game.player.y - 78)
        if self.distanceTo(self.game.player.x - 45, self.game.player.y - 78) > self.distance and self.stand == False:
            self.moveto(self.posx, self.posy)
        if self.x >= self.posx - 10 and self.x <= self.posx + 10 and self.y >= self.posy - 10 and self.y <= self.posy + 10 and self.stand == False:
            self.stand = True
        return

    def animate(self):
        animation = self.animation[self.stage]
        if self.facing == self.FACING_LEFT:
            self.image = pygame.transform.flip(animation[math.floor(self.tick)], True, False)
        else:
            self.image = animation[math.floor(self.tick)]
        self.tick += 0.1
        if self.tick > len(animation):
            self.tick = 0

    def getCenter(self):
        w = self.width[self.stage]
        h = self.height[self.stage]
        return self.x + w // 2, self.y + h

    def rangeActack(self):
        x, y = self.getCenter()
        BossBullet(self.game, self, 5, 0)
        BossBullet(self.game, self, 3.5, 3.5)
        BossBullet(self.game, self, 0, 5)
        BossBullet(self.game, self, -3.5, 3.5)
        BossBullet(self.game, self, -5, 0)
        BossBullet(self.game, self, -3.5, -3.5)
        BossBullet(self.game, self, 0, -5)
        BossBullet(self.game, self, 3.5, -3.5)


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

        self.width = 13 * 3
        self.height = 13 * 3
        x, y = host.getCenter()
        self.x = x - self.width // 2
        self.y = y - self.height // 2
        self.x0 = self.x
        self.y0 = self.y
        self.vx = vx
        self.vy = vy
        self.tick = 0

        self.animation = [
            pygame.transform.scale_by(self.game.boss_bullet_spritesheet.get_sprite(0, 0, 13, 13), 3),
            pygame.transform.scale_by(self.game.boss_bullet_spritesheet.get_sprite(13, 0, 13, 13), 3),
            pygame.transform.scale_by(self.game.boss_bullet_spritesheet.get_sprite(26, 0, 13, 13), 3),
            pygame.transform.scale_by(self.game.boss_bullet_spritesheet.get_sprite(39, 0, 13, 13), 3),
            pygame.transform.scale_by(self.game.boss_bullet_spritesheet.get_sprite(52, 0, 13, 13), 3)
        ]

        self.image = self.animation[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.distance = 102400  # 320**2
        self.d = 0

    def update(self):
        self.animate()
        self.collide()
        if (self.d < self.distance):
            self.x += self.vx
            self.y += self.vy
            self.rect.x = self.x
            self.rect.y = self.y
            self.d = (self.x - self.x0) ** 2 + (self.y - self.y0) ** 2
        else:
            self.kill()
            del self

    def animate(self):
        self.image = self.animation[math.floor(self.tick)]
        self.tick += 0.1

        if self.tick > len(self.animation):
            self.tick = 0

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.playerSprite, False)
        if hits:
            self.game.player.attacked(20)
            self.d = self.distance
