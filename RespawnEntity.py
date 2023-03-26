from pygame import *
from HealthBar import *
from Enemy import *
from Chest import *
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
                self.lvl.reset()

class CreateChest:
    def __init__(self, typechest, game ,x , y, timeRespawn):
        self.x = x
        self.y = y
        self.game = game
        self.isdead = False
        self.RespawnConst = timeRespawn
        self.RespawnTime =  0
        self.typechest = typechest
    def create(self):
        self.main = Chest(self.game, self.x, self.y)
        self.potion = PotionItem(self.game, self.x + 8,self.y + 8)
            
    def update(self):
        if self.main.time_attacked <= 0 and self.isdead == False:
            self.isdead = True
            self.RespawnTime  = self.RespawnConst
        if self.isdead:
            self.RespawnTime -= 1
            if self.RespawnTime <= 0:
                self.RespawnTime = 0
                self.isdead = False
                self.main.reset()          
                self.potion.reset()

                