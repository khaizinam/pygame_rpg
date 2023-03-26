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
				if column == 'F':
					Boss(self, j, i, 10)
					# BossBullet(self, j, i, 1, 0)
     

	def initEntity(self):
		self.player = Player(self, 60 , 450)
		self.playerhpbar = PlayerHealthBar(self, self.player)
		
		self.createList = [
			CreateChest('potion',self,282,814,FPS*60*3),
   			CreateChest('potion',self,1354,680,FPS*60*3),
			CreateChest('atk_spd',self,1746,260,FPS*60*3),
			CreateChest('atk_spd',self,1746,32,FPS*60*3),
			CreateChest('exp',self,1926,134,FPS*60*3),
      		CreateMinion('bee', self, 276, 884, 1, FPS*30),
			CreateMinion('bat', self, 270, 776, 1, FPS*30),
			CreateMinion('bee', self, 448, 854, 2, FPS*30),
			CreateMinion('mage', self, 372, 660, 1, FPS*30),
			CreateMinion('bat', self, 448, 764, 1, FPS*30),
			CreateMinion('bat', self, 354, 776, 1, FPS*30),
			CreateMinion('mage', self, 668, 880, 1, FPS*30),
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
  
		postion_text = self.font.render(f'x: {self.player.x}, y: {self.player.y}', True, WHITE)
		lvl_text = self.font.render(f'level: {self.player.level}', True, WHITE)
		Hp_text = self.font.render(f'hp: {self.player.hp}/{self.player.maxHp}', True, WHITE)
		Atk_text = self.font.render(f'atk: {self.player.atk}', True, WHITE)
		exp_text = self.font.render(f'exp: {self.player.curentExp}/{self.player.nextExp}', True, WHITE)
		pot_text = self.font.render(f'{self.player.potion}', True, WHITE)
		atk_spd_text = self.font.render(f'atk spd: { round(FPS / self.player.magicReduce, 2)}', True, WHITE)
		atk_range_text = self.font.render(f'atk range: { math.floor(self.player.magicRange ) * BULLET_SPD}', True, WHITE)
		self.screen.blit(postion_text, (10 , 5))
		self.screen.blit(lvl_text, (10, WIN_HEIGHT - (FONTSIZE + 5)*7))
		self.screen.blit(atk_spd_text, (10, WIN_HEIGHT - (FONTSIZE + 5)*6))
		self.screen.blit(atk_range_text, (10, WIN_HEIGHT - (FONTSIZE + 5)*5))
		self.screen.blit(Hp_text, (10, WIN_HEIGHT - (FONTSIZE + 5)*4))
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