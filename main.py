import pygame
from sprites import *
from config import *
from Utils import *
from Ground import *
from Player import *
from Camera import *
from Enemy import *
from Sprite import *

import sys
IMG_DIR = './img/'


class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
		self.clock = pygame.time.Clock()
		self.running = True
  
		self.camera = Camera(self,0,0)
  
		self.font = pygame.font.Font('arial.ttf',20)
		self.character_spritesheet = Spritesheet(f"{IMG_DIR}character.png")
		self.terrain_spritesheet = Spritesheet(f"{IMG_DIR}terrain.png")
		self.enemy_spritesheet = Spritesheet(f"{IMG_DIR}enemy.png")
		self.intro_background = pygame.image.load(f"{IMG_DIR}introbackground.png")
		self.go_background = pygame.image.load(f"{IMG_DIR}gameover.png")
		self.attack_spritesheet = Spritesheet(f"{IMG_DIR}attack.png")
 
	def createTilemap(self):
		self.player = Player(self, 40 , 15)
		for i, row in enumerate(tilemap):
			for j,column in enumerate(row):
				Grass(self, 2,j, i)
				if column == "B":
					Block(self, j , i)
				if column == ".":
					Wall(self, j , i)
				if column == "G":
					Grass(self,0, j , i)
				if column == "E":
					Enemy(self, j , i)
     
					
		deltax  = self.player.x - WIN_WIDTH/2
		deltay = self.player.y - WIN_HEIGHT /2
		for sprite in self.all_sprites:
			sprite.rect.x -= deltax
			sprite.rect.y -= deltay


	def new(self):
		self.playing = True
  
		self.all_sprites = pygame.sprite.LayeredUpdates()

		self.blocks = pygame.sprite.LayeredUpdates()
    
		self.enemies = pygame.sprite.LayeredUpdates()
  
		self.attacks = pygame.sprite.LayeredUpdates()
		self.createTilemap()

  

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.playing = False
				self.running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					if self.player.facing == 'up':
						Attack(self, self.player.x, self.player.y - TILESIZE)
					if self.player.facing == 'down':
						Attack(self, self.player.x, self.player.y + TILESIZE)
					if self.player.facing == 'left':
						Attack(self, self.player.x - TILESIZE, self.player.y )
					if self.player.facing == 'right':
						Attack(self, self.player.x + TILESIZE, self.player.y )
	def update(self):
		self.all_sprites.update()
		self.camera.update()

	def draw(self):
		self.screen.fill(BLACK)
		self.all_sprites.draw(self.screen)
		self.clock.tick(FPS)
		text = self.font.render(f'{self.player.x}, {self.player.y}', True, WHITE)
		text_rect = text.get_rect(center=(100,20))
		self.screen.blit(text, text_rect)
		pygame.display.update()

	def main(self):
		# game loop
		while self.playing:
			self.events()
			self.update()
			self.draw()

	def gameOver(self):
		text = self.font.render('Game Over', True, WHITE)
		text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

		restart_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, 'Restart', 32)
        
		for sprite in self.all_sprites:
			sprite.kill()

		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

			mouse_pos = pygame.mouse.get_pos()
			mouse_pressed = pygame.mouse.get_pressed()

			if restart_button.is_pressed(mouse_pos, mouse_pressed):
				self.new()
				self.main()
    
			self.screen.blit(self.go_background, (0, 0))
			self.screen.blit(text, text_rect)
			self.screen.blit(restart_button.image, restart_button.rect)
			self.clock.tick(FPS)
			pygame.display.update()
        
	def introScreen(self):
		intro = True
  
		title = self.font.render('Awesome Game', True, BLACK)
		title_rect = title.get_rect(x=10, y=10)
  
		play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'play',32)
		while intro:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					intro = False
					self.running = False
			mouse_pos = pygame.mouse.get_pos()
			mouse_pressed = pygame.mouse.get_pressed()

			if play_button.is_pressed(mouse_pos, mouse_pressed):
				intro = False

			self.screen.blit(self.intro_background, (0, 0))
			self.screen.blit(title, title_rect)
			self.screen.blit(play_button.image, play_button.rect)
			self.clock.tick(FPS)
			pygame.display.update()
 
g = Game()
g.introScreen()
g.new()
while g.running:
	g.main()
	g.gameOver()
pygame.quit()
sys.exit()