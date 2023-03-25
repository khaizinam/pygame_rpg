from pygame import *
from HealthBar import *
from Enemy import *
class CreateMinion:
    def __init__(self, enemyType, game ,x , y, level, timeRespawn):
        self.x = x
        self.y = y
        self.game = game
        self.level = level
        self.isdead = False
        self.RespawnConst = timeRespawn
        self.RespawnTime =  0
        self.enemyType = enemyType
    def create(self):
        self.minion = None
        if self.enemyType == 'bee':
            self.minion = BeeEnemy(self.game,self.x, self.y, self.level)
        elif self.enemyType == 'bat':
            self.minion = BatEnemy(self.game,self.x, self.y, self.level)
        elif self.enemyType == 'mage':
            self.minion = MageEnemy(self.game,self.x, self.y, self.level)
        self.bar = HealthBar(self.game, self.minion)
        self.lvl = lvlBar(self.game, self.minion)
            
    def update(self):
        if self.minion.hp <= 0 and self.isdead == False:
            self.isdead = True
            self.RespawnTime  = self.RespawnConst
        if self.isdead:
            self.RespawnTime -= 1
            if self.RespawnTime <= 0:
                self.RespawnTime = 0
                self.isdead = False
                self.minion.respawn()
                self.bar.reset()

                


                