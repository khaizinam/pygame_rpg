from config import *
class PlayerSprite():
    def __init__(self, game,player):
        self.game = game
        self.width = player.width
        self.height = player.height
    
    def cut(self,cropX,cropY):
        return self.game.character_spritesheet.get_sprite(cropX , cropY , self.width, self.height)
    
    def standDown(self):
        return self.game.character_spritesheet.get_sprite( 3, 2, self.width, self.height )
    
    def standUp(self):
        return self.game.character_spritesheet.get_sprite( 3, 34, self.width, self.height )
    
    def standLeft(self):
        return self.game.character_spritesheet.get_sprite( 3, 98, self.width, self.height )
    
    def standRight(self):
        return self.game.character_spritesheet.get_sprite( 3, 66, self.width, self.height )
    
    def moveDown(self):
        return [
                self.cut(3, 2), 
                self.cut(35, 2),
                self.cut(68, 2)
            ]
    def moveUp(self):
        return [
                self.cut(3, 34),
                self.cut(35, 34),
                self.cut(68, 34)
            ]
    def moveLeft(self):
        return [
                self.cut(3, 98),
                self.cut(35, 98),
                self.cut(68, 98)
            ]
    def moveRight(self):
        return [
                self.cut(3, 66),
                self.cut(35, 66),
                self.cut(68, 66)
            ]