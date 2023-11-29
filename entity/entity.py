import math
from module.text import *
from config import *
import pygame
from entity.Attack import *
FACING_LEFT = -1
FACING_RIGHT = 1


class Entity(pygame.sprite.Sprite):
    def __init__(self, game, x: int, y: int):
        self.game = game
        self.type = 'enemy'
        # self.groups = self.game.all_sprites
        # pygame.sprite.Sprite.__init__(self, self.groups)
        self.w = TILESIZE
        self.h = 2*TILESIZE

        # move direction
        self.spd = PLAYER_SPEED
        self.gravity = GRAVITY
        self.jump_spd = PLAYER_JUMP_SPD
        self.x_move = 0
        self.y_move = 0
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0

        # action
        self.moveTo_x = x
        self.moveTo_y = y
        self.isMove = False
        # fighting
        self.facing = FACING_RIGHT
        self.can_jump = True
        self.is_jumping = False
        self.jump_step = 0
        self.max_jump = 6
        self.time_attack_1 = 0
        # animation
        self.image = pygame.Surface([self.w, self.h])
        self.image.fill(RED)

        # draw on screen
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def moveTo(self, x, y):
        self.isMove = True
        self.moveTo_x = x
        self.moveTo_y = y

    def getCenter(self):
        return self.x + self.w // 2, self.y + self.h//2

    def getPosCenter(self):
        return self.x - self.w // 2, self.y - self.h

    # def autoMove(self):
    #     if self.isMove:
    #         ox, oy = self.getPosCenter()
    #         vx = self.moveTo_x - ox
    #         vy = self.moveTo_y - oy
    #         a = math.atan2(vy, vx)
    #         dx = self.spd * math.cos(a)
    #         dy = self.spd * math.sin(a)
    #         if abs(vx) >= dx and abs(vy) >= dy:
    #             self.x_move = dx
    #             self.y_move = dy
    #         else:

    #             self.x = self.moveTo_x - self.w // 2

    #             self.y = self.moveTo_y - self.h
    #             self.isMove = False

    #             # remove pointer
    #             self.game.pointer.hide()
    def jump(self):
        if self.can_jump:
            self.can_jump = False
            self.is_jumping = True

    def aply_gravity(self):
        if self.is_jumping:
            self.dy += self.jump_spd
            self.jump_step += 1
            if self.jump_step == self.max_jump:
                self.is_jumping = False
                self.jump_step = 0
        else:
            if self.time_attack_1 == 0:
                self.dy += self.gravity
            else:
                self.dy += self.gravity*0.4

        self.y += self.dy
        self.rect.y += self.dy

    def leftRigtMove_colsion(self):
        # update facing of entity
        if self.dx != 0:
            self.facing = self.dx
        self.x += self.dx * self.spd

        self.rect.x += self.dx * self.spd
        hits = pygame.sprite.spritecollide(
            self, self.game.ground_sprites, False)
        if len(hits) > 0:
            for block in hits:
                if self.dx > 0:  # moving right
                    self.x = block.x - self.w/2
                elif self.dx < 0:  # moving left
                    self.x = block.x + block.w + self.w/2
            x, y = self.getPosCenter()
            self.rect.x = x - self.game.camera.deltaX()

    def upDownMove_colision(self):
        self.aply_gravity()
        hits = pygame.sprite.spritecollide(
            self, self.game.ground_sprites, False)
        if len(hits) > 0:
            for block in hits:
                if self.dy > 0:  # moving down
                    self.y = block.y
                    self.dy = 0
                    self.can_jump = True
                elif self.dy < 0:  # moving left
                    self.y = block.y + block.h + self.h
                    self.dy = 0
            x, y = self.getPosCenter()
            self.rect.y = y - self.game.camera.deltaY()

    def animateDraw(self, camera):
        x, y = self.getPosCenter()
        self.game.camera.followPlayer()
        self.rect.x = x - camera.deltaX()
        self.rect.y = y - camera.deltaY()
        # print(self.rect.x, self.rect.y)

    def update(self):
        self.leftRigtMove_colsion()
        self.upDownMove_colision()
        self.animateDraw(self.game.camera)
        self.dy = 0
        self.dx = 0


class Player(Entity):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y)
        self.type = 'player'
        self.groups = self.game.all_sprites, self.game.player_layer
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.stand_animate_spd = 0.3
        self.w = 22
        self.h = 32
        self.animation_loop = 0
        self.melee = None
        self.image = self.game.character_spritesheet.get_sprite(
            18, 24, 22, 32)
        self.stand_animate = self.sprites_stand()
        self.run_animates = self.sprite_run()
        self.status = 'stand'
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def sprites_stand(self):
        return [self.game.character_spritesheet.get_sprite(
            18, 24, 22, 32),
            self.game.character_spritesheet.get_sprite(
            74, 24, 22, 32),
            self.game.character_spritesheet.get_sprite(
            130, 24, 22, 32),
            self.game.character_spritesheet.get_sprite(
            186, 24, 22, 32),
            self.game.character_spritesheet.get_sprite(
            298, 24, 22, 32),]

    def sprite_run(self):
        return [self.game.character_spritesheet.get_sprite(
            16, 136, 26, 32),
            self.game.character_spritesheet.get_sprite(
            74, 136, 22, 32),
            self.game.character_spritesheet.get_sprite(
            130, 136, 22, 32),
            self.game.character_spritesheet.get_sprite(
            184, 136, 22, 32),
            self.game.character_spritesheet.get_sprite(
            299, 136, 22, 32)]

    def keyInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.dx = -1

        elif keys[pygame.K_RIGHT]:
            self.dx = 1

        else:
            self.dx = 0
        if keys[pygame.K_a]:
            self.perFormNormalAttack()

        if keys[pygame.K_UP]:
            self.jump()

    def perFormNormalAttack(self):
        if self.time_attack_1 == 0:
            self.time_attack_1 = 1
            if self.melee == None:
                self.melee = SwordAttack(self.game, self)
            else:
                self.melee.kill()
                self.melee.add(self.melee.groups)

    def updateAttack(self):
        if self.time_attack_1 >= 8:
            self.melee.kill()
            self.time_attack_1 = 0
        if self.time_attack_1 != 0:
            self.melee.updateAttack()
            self.time_attack_1 += 1

    def update(self):
        self.keyInput()
        self.leftRigtMove_colsion()
        self.upDownMove_colision()
        self.animate()
        self.animateDraw(self.game.camera)

        self.updateAttack()

        self.dy = 0
        self.dx = 0

    def animate(self):
        if self.dx == 0 and self.dy == 0:
            if self.status != 'stand':
                self.status = 'stand'
                self.animation_loop = 0
            self.image = self.stand_animate[math.floor(self.animation_loop)]
            if self.facing == FACING_LEFT:
                self.image = pygame.transform.flip(self.image, True, False)
            self.animation_loop += self.stand_animate_spd
            if self.animation_loop >= len(self.stand_animate):
                self.animation_loop = 0

        elif self.dx != 0 and self.dy == 0:
            if self.status != 'moving':
                self.status = 'moving'
                self.animation_loop = 0

            self.image = self.run_animates[math.floor(self.animation_loop)]
            if self.facing == FACING_LEFT:
                self.image = pygame.transform.flip(self.image, True, False)
            self.animation_loop += self.stand_animate_spd
            if self.animation_loop >= len(self.run_animates):
                self.animation_loop = 0
