import pygame
from config import *
import math
from pygame import *
from HealthBar import *
from Enemy import *
from Chest import *
from Boss import *


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, game, o, leng):

        self.game = game
        self.o = o
        self.lenghBar = leng
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.health_bar
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([self.lenghBar, 5])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = self.o.x
        self.rect.y = self.o.y - 7

    def update(self):
        if self.o.hp <= 0:
            self.kill()
        self.x = self.o.x
        self.y = self.o.y - 7
        width = math.floor((self.o.hp / self.o.maxHp) * self.lenghBar)
        if width <= 0:
            width = 1
        self.image = pygame.Surface([width, 5])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

    def reset(self):
        pygame.sprite.Sprite.__init__(self, self.groups)


class PlayerHealthBar(pygame.sprite.Sprite):
    def __init__(self, game, o):
        self.game = game
        self.o = o
        self._layer = 10
        self.groups = self.game.icons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([100, 10])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = 10
        self.y = WIN_HEIGHT - (16 + 5) * 3
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        width = math.floor((self.o.hp / self.o.maxHp) * 100)
        if width <= 0:
            width = 1
        self.image = pygame.Surface([width, 10])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def reset(self):
        pygame.sprite.Sprite.__init__(self, self.groups)


class lvlBar(pygame.sprite.Sprite):
    def __init__(self, game, o):
        self.game = game
        self.o = o
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.health_bar
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.font = pygame.font.Font('arial.ttf', 8)
        self.text = self.font.render(f'{self.o.level}', True, WHITE)
        self.image = pygame.Surface([10, 10])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.x = self.o.x - 10
        self.y = self.o.y - 10
        self.rect.x = self.x
        self.rect.y = self.y
        self.image.blit(self.text, (0, 1))

    def update(self):
        if self.o.hp <= 0:
            self.kill()
        self.x = self.o.x - 10
        self.y = self.o.y - 10

    def reset(self):
        pygame.sprite.Sprite.__init__(self, self.groups)


class CreateMinion:
    def __init__(self, enemyType, game, x, y, level, timeRespawn):
        self.x = x
        self.y = y
        self.game = game
        self.level = level
        self.isdead = False
        self.RespawnConst = timeRespawn
        self.RespawnTime = 0
        self.enemyType = enemyType

    def create(self):
        self.minion = None
        leng = 0
        if self.enemyType == 'bee':
            self.minion = BeeEnemy(self.game, self.x, self.y, self.level)
            leng = self.minion.width
        elif self.enemyType == 'bat':
            self.minion = BatEnemy(self.game, self.x, self.y, self.level)
            leng = self.minion.width
        elif self.enemyType == 'mage':
            self.minion = MageEnemy(self.game, self.x, self.y, self.level)
            leng = self.minion.width
        elif self.enemyType == 'boss':
            self.minion = Boss(self.game, self.x, self.y, 608,1664, 32,448, self.level)
            leng = 122
        self.bar = HealthBar(self.game, self.minion, leng)
        self.lvl = lvlBar(self.game, self.minion)

    def update(self):
        if self.minion.hp <= 0 and self.isdead == False:
            self.isdead = True
            self.RespawnTime = self.RespawnConst
        if self.isdead:
            self.RespawnTime -= 1
            if self.RespawnTime <= 0:
                self.RespawnTime = 0
                self.isdead = False
                self.minion.respawn()
                self.bar.reset()
                self.lvl.reset()


class CreateChest:
    def __init__(self, typechest, game, x, y, timeRespawn):
        self.x = x
        self.y = y
        self.game = game
        self.isdead = False
        self.RespawnConst = timeRespawn
        self.RespawnTime = 0
        self.typechest = typechest

    def create(self):
        self.main = Chest(self.game, self.x, self.y)
        self.potion = PotionItem(self.game, self.x + 8, self.y + 8)

    def update(self):
        if self.main.time_attacked <= 0 and self.isdead == False:
            if self.typechest == 'atk':
                self.game.player.atk +=2
            elif self.typechest == 'hp':
                self.game.player.maxHp += 10
                self.game.player.hp += 10
            self.isdead = True
            self.RespawnTime = self.RespawnConst
        if self.isdead:
            self.RespawnTime -= 1
            if self.RespawnTime <= 0:
                self.RespawnTime = 0
                self.isdead = False
                self.main.reset()
                self.potion.reset()