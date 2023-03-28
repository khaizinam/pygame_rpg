from config import *
import math
class Camera:
    def __init__(self, game, x,y) :
        self.game = game
        self.x = x
        self.y = y
        self.vx = 1
        self.vy = 1
        self.destX = 0
        self.destY = 0
        self.speed = 15
        self.cooldown = 100
        self.cameraMode = 'player'
        
    def deltaX(self):
        return self.x - WIN_WIDTH /2
    
    def deltaY(self):
        return self.y - WIN_HEIGHT /2
    
    def followPlayer(self):
        self.x = self.game.player.x
        self.y = self.game.player.y
        
    def update(self):
        if self.cameraMode == 'player':
            self.followPlayer()
        else:
            # self.set(1216, 561)
            self.movetoDest()
            self.cooldown -= 1
            if (self.cooldown) <= 0:
                self.cameraMode = 'player'
        for sprite in self.game.all_sprites:
            sprite.rect.x = sprite.x - self.deltaX()
            sprite.rect.y = sprite.y - self.deltaY()

    def set(self, x, y):
        self.cameraMode = 'cutscene'
        self.cooldown = 100
        self.destX = x
        self.destY = y
    
    def movetoDest(self): 
        vectorX = self.destX - self.x
        vectorY = self.destY - self.y
        oldX = self.x
        oldY = self.y
        if vectorX != 0:
            vectorX = vectorX/(math.sqrt(vectorX*vectorX+vectorY*vectorY))*self.speed
        if vectorY != 0:
            vectorY = vectorY/(math.sqrt(vectorX*vectorX+vectorY*vectorY))*self.speed
        # self.vx = vectorX
        # self.vy = vectorY
        self.x += vectorX
        self.y += vectorY
        if (abs(self.x - oldX) > abs(self.destX - oldX)):
            self.x = self.destX
        if (abs(self.y - oldY) > abs(self.destY - oldY)):
            self.y = self.destY