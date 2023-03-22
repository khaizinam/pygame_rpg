from config import *

class Camera:
    def __init__(self, game, x,y) :
        self.game = game
        self.x = x
        self.y = y
        
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
        for sprite in self.game.all_sprites:
            sprite.rect.x = sprite.x - self.deltaX()
            sprite.rect.y = sprite.y - self.deltaY()

        