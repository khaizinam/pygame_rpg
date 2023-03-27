import pygame.image

from importPack import *

import sys
IMG_DIR = './img/'


class Game:
	def __init__(self):
		pygame.init()
		mixer.init()
		self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
		self.clock = pygame.time.Clock()
		self.running = True
  		self.themeSong = pygame.mixer.Sound('./audio/bgrTheme.mp3')
		self.camera = Camera(self,0,0)
  
		self.font = pygame.font.Font('arial.ttf',16)
		self.character_spritesheet = Spritesheet(f"{IMG_DIR}character.png")
		self.terrain_spritesheet = Spritesheet(f"{IMG_DIR}terrain.png")
		self.enemy_spritesheet = Spritesheet(f"{IMG_DIR}enemy.png")
		self.boss1_spritesheet = Spritesheet(f"{IMG_DIR}boss1.png")
		self.boss2_spritesheet = Spritesheet(f"{IMG_DIR}boss2.png")
		self.boss_bullet_spritesheet = Spritesheet(f"{IMG_DIR}boss_bullet.png")
		# self.boss3_spritesheet = Spritesheet(f"{IMG_DIR}boss1.png")
		self.intro_background = pygame.image.load(f"{IMG_DIR}introbackground.png")
		self.go_background = pygame.image.load(f"{IMG_DIR}gameover.png")
		self.attack_spritesheet = Spritesheet(f"{IMG_DIR}attack.png")
		self.explosion0_sprite = Spritesheet(f"{IMG_DIR}explosion0.png")
		self.explosion1_sprite = Spritesheet(f"{IMG_DIR}explosion1.png")
		self.heart_spritesheet = Spritesheet(f"{IMG_DIR}LifePot.png")
		self.magic_attack = Spritesheet(f"{IMG_DIR}magic.png")
 
	def createTilemap(self):
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

     

	def initEntity(self):
		self.player = Player(self, 44 , 884)
		PlayerHealthBar(self, self.player)
		PlayerHealthBar_layer(self, self.player)
		self.createList = [
			CreateChest('potion',self,282,814,FPS*60*3),
   			CreateChest('potion',self,1354,680,FPS*60*3),
			CreateChest('atk_spd',self,1746,260,FPS*60*3),
			CreateChest('atk_spd',self,1746,32,FPS*60*3),
			CreateChest('exp',self,1926,134,FPS*60*3),
      		CreateMinion('bee', self, 276, 884, 1, FPS*30),
			CreateMinion('bat', self, 270, 776, 1, FPS*30),
			CreateMinion('bee', self, 448, 854, 2, FPS*30),
			CreateMinion('bee', self,134,518, 3, FPS*30),
			CreateMinion('bat', self, 92, 470, 2, FPS * 30),
			CreateMinion('bat', self, 134, 482, 2, FPS * 30),
			CreateMinion('bat', self, 164, 500, 2, FPS * 30),
			CreateMinion('mage', self, 368, 260, 5, FPS * 30),
			CreateMinion('mage', self, 446, 590, 5, FPS * 30),
			CreateMinion('bat', self, 416, 428, 3, FPS * 30),
			CreateMinion('bat', self, 416, 464, 3, FPS * 30),
			CreateMinion('bat', self, 448, 764, 3, FPS*30),
			CreateMinion('bat', self, 354, 776, 3, FPS*30),
			CreateMinion('mage', self, 668, 880, 3, FPS*30),
			CreateChest('potion',self, 122, 352, FPS*60*3),
			CreateChest('exp', self, 578, 620, FPS * 60 * 3),
			CreateChest('exp', self, 464, 106, FPS * 60 * 3),
			CreateChest('exp', self, 512, 106, FPS * 60 * 3),
			CreateChest('atk_spd', self, 134, 124, FPS * 60 * 3),
			CreateMinion('bee', self, 68, 94, 5, FPS * 30),
			CreateMinion('bee', self, 176, 94, 5, FPS * 30),
			CreateMinion('bee', self, 176, 178, 5, FPS * 30),
			CreateMinion('bee', self, 68, 178, 5, FPS * 30),


			CreateMinion('bat', self, 648, 668, 2, FPS*120),
			CreateMinion('bat', self, 688, 668, 2, FPS*120),
			CreateMinion('bat', self, 648, 730, 2, FPS*120),
			CreateMinion('bat', self, 688, 730, 3, FPS*120),
			CreateMinion('bee', self, 890, 658, 3, FPS*120),
			CreateMinion('mage', self, 1088, 688, 2, FPS*120),
   			CreateMinion('bat', self, 1064, 820, 3, FPS*120),
			CreateMinion('bat', self, 1142, 820, 3, FPS*120),
			CreateMinion('bat', self, 1064, 874, 3, FPS*120),
			CreateMinion('bat', self, 1142, 874, 3, FPS*120),
			CreateMinion('bee', self, 1460, 844, 4, FPS*120),
			CreateMinion('bee', self, 1610, 808, 3, FPS*120),
			CreateMinion('bee', self, 1610, 886, 3, FPS*120),
			CreateMinion('mage', self, 2132, 766, 2, FPS*120),
			CreateMinion('mage', self, 2132, 862, 2, FPS*120),
   			CreateMinion('mage', self, 1664, 688, 3, FPS*120),
      		CreateMinion('mage', self, 2216, 365, 3, FPS*120),
			CreateMinion('bat', self, 2300, 290, 4, FPS*120),
			CreateMinion('bat', self, 2468, 290, 4, FPS*120),
			CreateMinion('bat', self, 2414, 290, 4, FPS*120),
			CreateMinion('bee', self, 2414, 236, 5, FPS*120),
			CreateChest('potion', self, 2488, 808, FPS*60*30),
			CreateChest('potion', self, 1724, 838, FPS * 60 * 30),
			CreateChest('exp', self, 2180, 512, FPS * 60 * 30),
			CreateChest('exp', self, 1922, 410, FPS * 60 * 30),
			CreateMinion('bee', self, 2144, 536, 5, FPS * 120),
			CreateMinion('bee', self, 1880, 470, 5, FPS * 120),
			CreateMinion('bee', self, 2228, 536, 5, FPS * 120),
			CreateMinion('bee', self, 2420, 584, 6, FPS * 120),
			CreateMinion('bat', self, 2378, 560, 5, FPS * 120),
			CreateMinion('bat', self, 2414, 536, 5, FPS * 120),
			CreateMinion('bat', self, 2450, 554, 5, FPS * 120),
			CreateMinion('mage', self, 2432, 68, 10, FPS * 120),
			CreateMinion('mage', self, 1844, 80, 10, FPS * 120),
			CreateMinion('mage', self, 1844, 218, 10, FPS * 120),



			CreateMinion('boss', self, 1124, 122, 60, FPS * 60 * 4),
        ]
		for minion in self.createList:
			minion.create()

	def new(self):
		self.playing = True

		self.all_sprites = pygame.sprite.LayeredUpdates()
  
		self.blocks = pygame.sprite.LayeredUpdates()
		self.enemies = pygame.sprite.LayeredUpdates()
		self.items = pygame.sprite.LayeredUpdates()
		self.icons = pygame.sprite.LayeredUpdates()
		self.health_bar = pygame.sprite.LayeredUpdates()
		self.attacks = pygame.sprite.LayeredUpdates()
		self.playerSprite = pygame.sprite.LayeredUpdates()
		self.potions = pygame.sprite.LayeredUpdates()
		self.magic_attacks = pygame.sprite.LayeredUpdates()
		self.chests = pygame.sprite.LayeredUpdates()
		self.createTilemap()
		self.initEntity()

  

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.playing = False
				self.running = False
		keys = pygame.key.get_pressed()
		if keys[pygame.K_l]:
			self.player.usePotion()
		if keys[pygame.K_SPACE]:
			self.pause()
   
	def update(self):
		self.all_sprites.update()
		self.icons.update()
		for minion in self.createList:
			minion.update()
		self.camera.update()

	def draw(self):
		self.screen.fill(BLACK)
		self.all_sprites.draw(self.screen)
		self.icons.draw(self.screen)
		self.clock.tick(FPS)
		fontsize = 12
		newfont = pygame.font.Font('arial.ttf',fontsize)
		postion_text = newfont.render(f'x: {self.player.x}, y: {self.player.y}', True, WHITE)
		lvl_text = newfont.render(f'level: {self.player.level}', True, WHITE)
		Hp_text = newfont.render(f'hp: {self.player.hp}|{self.player.maxHp}', True, WHITE)
		Atk_text = newfont.render(f'atk: {self.player.atk}', True, WHITE)
		exp_text = newfont.render(f'exp: {self.player.curentExp}|{self.player.nextExp}', True, WHITE)
		pot_text = pygame.font.Font('arial.ttf',12).render(f'{self.player.potion}', True, WHITE)
		atk_spd_text = newfont.render(f'atk spd: { round(FPS / self.player.magicReduce, 2)}', True, WHITE)
		atk_range_text = newfont.render(f'atk range: { math.floor(self.player.magicRange ) * BULLET_SPD}', True, WHITE)
		
  		#Top Left content
		self.screen.blit(postion_text, (10 , 5))
  
  		#LeftContent
		self.screen.blit(lvl_text, (10, WIN_HEIGHT - (fontsize + 5)*4))
		self.screen.blit(Atk_text, (10, WIN_HEIGHT - (fontsize + 5)*3))
		self.screen.blit(atk_spd_text, (10, WIN_HEIGHT - (fontsize + 5)*2))
		self.screen.blit(atk_range_text, (10, WIN_HEIGHT - (fontsize + 5)*1))

		#Center content
		self.screen.blit(Hp_text, (WIN_WIDTH/2 - 100, WIN_HEIGHT - (fontsize + 5)*3))
		self.screen.blit(exp_text, (WIN_WIDTH/2 - 100, WIN_HEIGHT - (fontsize + 5)))
  
		# Right Content
		self.screen.blit(pot_text, (WIN_WIDTH /2 + 80, WIN_HEIGHT - 20))

		pygame.display.update()

	def main(self):
		# game loop
		while self.playing:
			self.events()
			self.update()
			self.draw()

	def gameOver(self):

		restart_button = Button(WIN_WIDTH/2-100, 250, pygame.image.load('./img/resumeBtn - Copy.png'))
        
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
			self.screen.blit(restart_button.image, restart_button.rect)
			self.clock.tick(FPS)
			pygame.display.update()
	def pause(self):
		pause = True
		resume_button = Button(WIN_WIDTH/2 - 100, 80, pygame.image.load('./img/resumeBtn.png'))
		back_button = Button(WIN_WIDTH/2 - 100, 200, pygame.image.load('./img/backBtn.png'))
		while pause:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pause = False
					self.running = False
			mouse_pos = pygame.mouse.get_pos()
			mouse_pressed = pygame.mouse.get_pressed()
			if resume_button.is_pressed(mouse_pos, mouse_pressed):
				pause = False
			if back_button.is_pressed(mouse_pos, mouse_pressed):
				self.new()
				self.introScreen()
			self.screen.blit(pygame.image.load('./img/MenuContainer.png'), (40, 20))
			self.screen.blit(resume_button.image, resume_button.rect)
			self.screen.blit(back_button.image, back_button.rect)
			self.clock.tick(FPS)
			pygame.display.update()
	def optionScreen(self):
		option = True
		soundOn_button = Button(WIN_WIDTH/2-100, 100, pygame.image.load('./img/soundOn.png'))
		soundOff_button = Button(WIN_WIDTH / 2 + 20, 100, pygame.image.load('./img/soundOff.png'))
		back_button = Button(WIN_WIDTH/2 - 80, 200, pygame.image.load('./img/backBtn.png'))
		while option:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					option = False
					self.running = False
			mouse_pos = pygame.mouse.get_pos()
			mouse_pressed = pygame.mouse.get_pressed()
			if back_button.is_pressed(mouse_pos, mouse_pressed):
				option = False
				self.introScreen()
			self.screen.blit(self.intro_background, (0, 0))
			self.screen.blit(soundOn_button.image, soundOn_button.rect)
			self.screen.blit(soundOff_button.image, soundOff_button.rect)
			self.screen.blit(back_button.image, back_button.rect)
			self.clock.tick(FPS)
			pygame.display.update()
	def introScreen(self):
		intro = True
		play_button = Button(WIN_WIDTH/2-100, 100, pygame.image.load('./img/playBtn.png'))
		option_button = Button(WIN_WIDTH / 2 - 100, 200, pygame.image.load('./img/optionBtn.png'))
		exit_button = Button(WIN_WIDTH / 2 - 100, 300, pygame.image.load('./img/exitBtn.png'))
		while intro:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					intro = False
					self.running = False
			mouse_pos = pygame.mouse.get_pos()
			mouse_pressed = pygame.mouse.get_pressed()

			if play_button.is_pressed(mouse_pos, mouse_pressed):
				intro = False
				self.new()
				self.main()
			if option_button.is_pressed(mouse_pos, mouse_pressed):
				intro = False
				self.optionScreen()
			if exit_button.is_pressed(mouse_pos, mouse_pressed):
				pygame.quit()
				sys.exit()
			self.screen.blit(self.intro_background, (0, 0))
			self.screen.blit(play_button.image, play_button.rect)
			self.screen.blit(option_button.image, option_button.rect)
			self.screen.blit(exit_button.image, exit_button.rect)
			self.clock.tick(FPS)
			pygame.display.update()
 
g = Game()
g.themeSong.play()
g.introScreen()

while g.running:
	g.main()
	g.gameOver()
pygame.quit()
sys.exit()