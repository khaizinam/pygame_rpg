import pygame.image
from config import *
from entity.mousePointer import PointerMouse
from entity.camera import Camera
from entity.entity import *
from module.text import *
from entity.Ground import Ground
from Utils import Spritesheet
import sys


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Đại Việt Sử Ký')
        # init
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = True
        self.mapObj = None
        self.pointer = None
        # txt = TextBox()
        # txt.content = 'khaizinam'
        # txt.x = 20
        # txt.y = 0
        self.character_spritesheet = Spritesheet("img/char_blue.png")
        self.fontSmall = pygame.font.Font('arial.ttf', 8)
        self.fontNormal = pygame.font.Font('arial.ttf', 12)
        self.textBox = []
        self.initLayer()

    def loadMap(self):
        self.height_size = 30
        self.width_size = 60
        self.mouse_press = False
        self.player = Player(self, 15*TILESIZE, 26*TILESIZE)
        self.camera = Camera(self, 15*TILESIZE, 31*TILESIZE - WIN_HEIGHT//2)
        # self.camera.followPlayer(self.player.x, self.player.y)
        Ground(self, 0, 0, self.width_size, 1)
        Ground(self, self.width_size - 1, 0, 1, self.height_size)
        Ground(self, 0, self.height_size, self.width_size, 1)
        Ground(self, 0, 0, 1, self.height_size)

    def initLayer(self):
        self.ground_sprites = pygame.sprite.LayeredUpdates()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player_layer = pygame.sprite.LayeredUpdates()
        self.enemy_layer = pygame.sprite.LayeredUpdates()
        self.acttack_layer = pygame.sprite.LayeredUpdates()
        self.icons = pygame.sprite.LayeredUpdates()
        self.text_sprites = pygame.sprite.LayeredUpdates()
        self.pointer = PointerMouse(self, 0, 0)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                pygame.quit()
                sys.exit()

    def draw(self):
        self.screen.fill(BG_COLOR)
        # ------------
        self.ground_sprites.draw(self.screen)
        self.acttack_layer.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.text_sprites.draw(self.screen)
        # ------------
        self.clock.tick(FPS)
        pygame.display.update()

    def clickToMovePlayer(self, x, y):
        self.pointer.click(x, y)
        self.player.moveTo(self.camera.deltaX() + x,
                           self.camera.deltaY() + y)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        # ------------
        self.ground_sprites.update()
        self.acttack_layer.update()
        self.all_sprites.update()
        self.text_sprites.update()
        # ------------

    def main(self):
        # game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()


g = Game()
g.loadMap()

while g.running:
    g.main()

pygame.quit()
sys.exit()
