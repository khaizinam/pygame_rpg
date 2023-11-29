from config import *
import math


class Camera:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.vx = 1
        self.vy = 1
        self.destX = 0
        self.destY = 0
        self.speed = 15
        self.cooldown = 100
        self.followObj = self.game.player
        self.dx = 0
        self.dy = 0

    def deltaX(self):
        return self.x - WIN_WIDTH / 2

    def deltaY(self):
        return self.y - WIN_HEIGHT / 2

    def followPlayer(self):
        x, y = self.followObj.getPosCenter()

        if (x < WIN_WIDTH // 2):
            x = WIN_WIDTH // 2
        elif (x > self.game.width_size * TILESIZE - WIN_WIDTH // 2):
            x = self.game.width_size * TILESIZE - WIN_WIDTH // 2

        if (y < WIN_HEIGHT // 2):
            y = WIN_HEIGHT // 2
        elif (y > (self.game.height_size+1) * TILESIZE - WIN_HEIGHT // 2):
            y = (self.game.height_size+1) * TILESIZE - WIN_HEIGHT // 2
        self.x = x
        self.y = y

    def update(self): pass
    # for sprite in self.game.all_sprites:
    #     sprite.rect.x = sprite.x - self.deltaX()
    #     sprite.rect.y = sprite.y - self.deltaY()
