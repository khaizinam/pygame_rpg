from importPack import *

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
			#CHEST
			CreateChest('hp',self,446,704,FPS*60*2),
   			CreateChest('atk',self,860,788,FPS*60*2),
			CreateChest('hp',self,860,878,FPS*60*2),
			CreateChest('hp',self,1746,32,FPS*60*3),
			CreateChest('exp',self,1926,134,FPS*60*3),
			#BOSS
   			CreateMinion('boss', self, 1124, 122, 60, FPS*60*4),
			#MINION
      		CreateMinion('bee', self, 308, 812, 4, FPS*60),
			CreateMinion('bat', self, 260, 812, 4, FPS*60),
			CreateMinion('bat', self, 272, 770, 4, FPS*60),
			CreateMinion('bat', self, 272, 830, 4, FPS*60),
			CreateMinion('bat', self, 356, 800, 4, FPS*60),
			CreateMinion('bee', self, 578, 761, 4, FPS*60),
			CreateMinion('bat', self, 578, 770, 4, FPS*60),
			CreateMinion('bat', self, 500, 753, 4, FPS*60),
			CreateMinion('bat', self, 590, 734, 4, FPS*60),
			CreateMinion('bat', self, 620, 704, 4, FPS*60),
			CreateMinion('mage', self, 764, 668, 6, FPS*60*2),
			CreateMinion('mage', self, 674, 788, 4, FPS*60*2),
			CreateMinion('bee', self, 632, 854, 6, FPS*60),
			CreateMinion('bat', self, 569, 854, 4, FPS*60),
			CreateMinion('bat', self, 560, 890, 4, FPS*60),
			CreateMinion('bat', self, 569, 890, 5, FPS*60),
			CreateMinion('bat', self, 578, 812, 4, FPS*60),
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
		newfont = pygame.font.Font('arial.ttf',30)
		title = newfont.render('Bug Code Dungoen', True, BLACK)
		title_rect = title.get_rect(x=WIN_WIDTH/2 - 150, y=WIN_HEIGHT/2 -50)
  
		play_button = Button(WIN_WIDTH/2 - 50, WIN_HEIGHT/2 + 5, 100, 50, WHITE, BLACK, 'play', 32)
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