import pygame
from config import *


class TextBox:
    def __init__(self, txt, font):
        self.content = txt
        self.x = 0
        self.y = 0
        self.color = WHITE
        self.font = font

    def getCtx(self):
        return self.font.render(self.content, True, WHITE)

    def getPos(self):
        return (self.x, self.y)


class NameTxt(pygame.sprite.Sprite):
    def __init__(self, game, o):

        self.game = game
        self.o = o
        self._layer = ENEMY_LAYER
        self.groups = self.game.text_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.text = self.game.fontSmall.render('khaizinam', True, WHITE)
        self.image = pygame.Surface([50, 30])
        self.rect = self.image.get_rect()
        self.x = self.o.x - 10
        self.y = self.o.y - 10
        self.rect.x = self.x
        self.rect.y = self.y
        self.image.blit(self.text, (0, 1))

    def update(self):
        self.x = self.o.x - 10
        self.y = self.o.y - 10

    def reset(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
