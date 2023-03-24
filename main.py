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
  
		self.font = pygame.font.Font('arial.ttf',16)
		self.character_spritesheet = Spritesheet(f"{IMG_DIR}character.png")
		self.terrain_spritesheet = Spritesheet(f"{IMG_DIR}terrain.png")
		self.enemy_spritesheet = Spritesheet(f"{IMG_DIR}enemy.png")
		self.intro_background = pygame.image.load(f"{IMG_DIR}introbackground.png")
		self.go_background = pygame.image.load(f"{IMG_DIR}gameover.png")
		self.attack_spritesheet = Spritesheet(f"{IMG_DIR}attack.png")
		self.explosion0_sprite = Spritesheet(f"{IMG_DIR}explosion0.png")
		self.explosion1_sprite = Spritesheet(f"{IMG_DIR}explosion1.png")
		self.heart_spritesheet = Spritesheet(f"{IMG_DIR}LifePot.png")
		self.magic_attack = Spritesheet(f"{IMG_DIR}magic.png")
 
	def createTilemap(self):
		self.player = Player(self, 11 , 35)
		HeartItem(self)
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
					BeeEnemy(self, j , i)
				if column == "R":
					RangeEnemy(self, j , i)
     
					
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

		self.items = pygame.sprite.LayeredUpdates()
  
		self.icons = pygame.sprite.LayeredUpdates()
  
		self.attacks = pygame.sprite.LayeredUpdates()

		self.playerSprite = pygame.sprite.LayeredUpdates()

  
		self.magic_attacks = pygame.sprite.LayeredUpdates()
  
		self.createTilemap()

  

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.playing = False
				self.running = False
		keys = pygame.key.get_pressed()
		if keys[pygame.K_c]:
			self.player.usePotion()
   
	def update(self):
		self.all_sprites.update()
		self.camera.update()
		self.icons.update()

	def draw(self):
		self.screen.fill(BLACK)
		self.all_sprites.draw(self.screen)
		self.icons.draw(self.screen)
		self.clock.tick(FPS)
  
		postion_text = self.font.render(f'x: {self.player.x}, y: {self.player.y}', True, WHITE)
		Hp_text = self.font.render(f'HP: {self.player.hp}/{self.player.maxHp}', True, WHITE)
		Atk_text = self.font.render(f'ATK: {self.player.atk}', True, WHITE)
		exp_text = self.font.render(f'Exp: {self.player.curentExp}/{self.player.nextExp}', True, WHITE)
		pot_text = self.font.render(f'{self.player.potion}', True, WHITE)
		self.screen.blit(postion_text, (10 , 5))
		self.screen.blit(Hp_text, (10, WIN_HEIGHT - (FONTSIZE + 5)*3))
		self.screen.blit(Atk_text, (10, WIN_HEIGHT - (FONTSIZE + 5)*2))
		self.screen.blit(exp_text, (10, WIN_HEIGHT - (FONTSIZE + 5)))
		self.screen.blit(pot_text, (WIN_WIDTH - 50, WIN_HEIGHT - 25))
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