import math
# from tkinter import HIDDEN
from MoleStatus import MoleStatus
import pygame
import time
import sys

import random
from enum import Enum
from pygame import mixer

pygame.init()
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Hit Mole')
GREY = (150,150,150)
WHITE = (255,255,255)
BLACK = (0,0,0)
COLOR1 = (66, 135, 245)
COLOR2 = (235, 158, 52)
COLOR3 = (232, 58, 28)
font = pygame.font.Font('freesansbold.ttf', 20)

# load image
bomb_image = pygame.image.load(r'./images/bomb.png')
boss_image = pygame.image.load(r'./images/boss.png')
ground_image = pygame.image.load(r'./images/ground.png')
hammer_image = pygame.image.load(r'./images/hammer.png')
mole1_image = pygame.image.load(r'./images/mole1.png')
mole2_image = pygame.image.load(r'./images/mole2.png')

boss_hat_image = pygame.image.load(r'./images/boss_hat.png')
hard_hat_image = pygame.image.load(r'./images/hardhat.png')
eye_image = pygame.image.load(r'./images/eye.png')
mole_hands_image = pygame.image.load(r'./images/mole_hands.png')

background_image = pygame.image.load(r'./images/background.jpeg')

wick_sprite = pygame.image.load(r'./images/wick.png').convert_alpha()

# load sound
mixer.init()
mixer.music.set_volume(0.1)

mixer.music.load('sounds/bgm.mp3')
beep_sound = mixer.Sound('sounds/beep.ogg')
click_sound = mixer.Sound('sounds/click.ogg')
explode_sound = mixer.Sound('sounds/explode.ogg')
gain_time_sound = mixer.Sound('sounds/gain_time.ogg')
go_sound = mixer.Sound('sounds/go.ogg')
hammer_sound = mixer.Sound('sounds/hammer.ogg')
pop_sound = mixer.Sound('sounds/pop.ogg')
squeak_1_sound = mixer.Sound('sounds/squeak_1.ogg')
squeak_2_sound = mixer.Sound('sounds/squeak_2.ogg')
squeak_3_sound = mixer.Sound('sounds/squeak_3.ogg')
swing_sound = mixer.Sound('sounds/swing.ogg')
timeout_sound = mixer.Sound('sounds/timeout.ogg')
wood_hit_sound = mixer.Sound('sounds/wood_hit.ogg')

# Game setup
WIDTH = 50

ROW = 3
COL = 3
GROUND_WIDTH = 146
GROUND_HEIGHT = 61
GROUND_TOP_LEFT_X = SCREEN_WIDTH*0.4
GROUND_TOP_LEFT_Y = SCREEN_HEIGHT*0.2
PADDING_GROUND_WIDTH = 190
PADDING_GROUND_HEIGHT = 150
MOLE_WIDTH = 83
MOLE_HEIGHT = 94

class Grid:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.grounds = []
        self.createGrounds()
        
    def createGrounds(self):
        for row in range(self.row):
            for col in range(self.col):
                ground = Ground(row, col)
                self.grounds.append(ground)
        
    def update(self):
        self.render()
    
    def render(self):
        for ground in self.grounds:
            ground.update()

class Score:
    def __init__(self):
        self.score = 0
        self.text = font.render(f'Score: {self.score}', True, COLOR1, WHITE)
        self.textRect = self.text.get_rect()
        self.textRect.center = (100, 100)
        
    def update(self):
        self.render()
    
    def render(self):
        self.text = font.render(f'Score: {self.score}', True, COLOR1, WHITE)
        
        screen.blit(self.text, self.textRect)
        
class Miss:
    miss = 0
    def __init__(self):
        self.text = font.render(f'Miss: {Miss.miss}', True, COLOR1, WHITE)
        self.textRect = self.text.get_rect()
        self.textRect.center = (100, 300)
        
    def update(self):
        self.render()
    
    def render(self):
        self.text = font.render(f'Miss: {Miss.miss}', True, COLOR1, WHITE)
        
        screen.blit(self.text, self.textRect)

class Ground:
    def __init__(self, idx, idy):
        self.idx = idx
        self.idy = idy
        self.x = GROUND_TOP_LEFT_X + PADDING_GROUND_WIDTH*idx
        self.y = GROUND_TOP_LEFT_Y + PADDING_GROUND_HEIGHT*idy
        self.haveMole = False
        
    def update(self):
        self.render()
    
    def render(self):
        screen.blit(ground_image, (self.x, self.y))

class Mole:
    def __init__(self, grid, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.grid = grid
        self.eye = eye_image
        self.hard_hat = hard_hat_image
        self.isDead = False
        self.isHard = False
        self.isHaveHat = self.isHard
        self.lives = 1
        self.type = type
        self.isShake = False
        self.shakeLeft = True
        self.rawX = 0
        if (type == 1):
            self.image = mole1_image
            self.rect = mole1_image.get_rect()
        else:
            self.image = mole2_image
            self.rect = mole2_image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.x = x
        self.y = y
        self.active = False
        self.visible = True
        self.status = MoleStatus.HIDDEN
        self.lastWaiting = pygame.time.get_ticks()
        self.lastTeleport = pygame.time.get_ticks()
        self.lastShake = pygame.time.get_ticks()
        self.shakeTime = 200
        self.waitingTime = 1500
        self.teleportTime = 200 + 1500 * random.random()
        if (self.type == 3):
            self.teleportTime = 2000 + 1000 * random.random()
        self.spawn()
    
    def update(self):
        self.updateFollowStatus()
        self.render()
    
    def render(self):
        if self.visible:
            screen.blit(self.image, (self.x, self.y), (0, 0, MOLE_WIDTH, 1 - (self.y - self.ground.y - MOLE_HEIGHT*0.5)))
            if (self.isDead and self.y < self.ground.y):
                screen.blit(self.eye, (self.x + 17, self.y + 24))
            if (self.isHaveHat and self.y < self.ground.y):
                screen.blit(self.hard_hat, (self.x + 8, self.y - 15))
            
    def teleport(self):
        groundNoMoles = list(filter(lambda x: not x.haveMole, self.grid.grounds))
        randNumber =  math.floor(random.random() * len(groundNoMoles))
        self.ground = groundNoMoles[randNumber] 
        self.ground.haveMole = True
        self.rawX = self.ground.x + GROUND_WIDTH/2 - MOLE_WIDTH/2
        self.x = self.rawX
        self.y = self.ground.y
        self.lastTeleport = pygame.time.get_ticks()
        self.teleportTime = 200 + 1500 * random.random()
        if (self.type == 3):
            self.teleportTime = 2000 + 1000 * random.random()
        
    def showUp(self):
        self.y -= 10
        if (self.y < self.ground.y - MOLE_HEIGHT*0.7):
            self.changeModeToWaiting()
    
    def exit(self):
        self.y += 15 
        if (self.y > self.ground.y + 50):
            self.ground.haveMole = False
            self.spawn()
    
    def spawn(self):
        self.changeModeToHidden()
        self.isDead = False
        self.isShake = False
        self.teleport()
        if (random.random() < 0.5):
            self.isHard = True
            self.lives = 3
        else:
            self.isHard = False
            self.lives = 1
        self.isHaveHat = self.isHard

    def updateFollowStatus(self):
        if (self.status == MoleStatus.HIDDEN):
            now = pygame.time.get_ticks()
            if now - self.lastTeleport >= self.teleportTime:
                self.changeModeToShowUp()
        elif (self.status == MoleStatus.SHOW_UP):
            self.showUp()
        elif (self.status == MoleStatus.WAITING):
            now = pygame.time.get_ticks()
            self.shake()
            if now - self.lastWaiting >= self.waitingTime:
                self.changeModeToExit()
                Miss.miss += 1
        elif (self.status == MoleStatus.EXIT):
            self.exit()
            
    def shake(self):
        if (self.isShake):
            if (self.shakeLeft):
                self.x -= 5
            else:
                self.x += 5
            if (self.x < self.rawX - 8):
                self.shakeLeft = False
            if (self.x > self.rawX + 8):
                self.shakeLeft = True
            now = pygame.time.get_ticks()
            if (now - self.lastShake > self.shakeTime):
                self.isShake = False
            
    def getHit(self):
        mixer.Sound.play(swing_sound)
        self.lives -= 1
        if (self.isHaveHat):
            mixer.Sound.play(wood_hit_sound)
            self.isShake = True
            self.lastShake = pygame.time.get_ticks()
        if (self.lives <= 0 and not self.isDead):
            self.dead()
        
    def dead(self):
        self.isDead = True
        if (random.random() < 0.33):
            mixer.Sound.play(squeak_1_sound)
        elif (random.random() > 0.33 and random.random() < 0.66):
            mixer.Sound.play(squeak_2_sound)
        else:
            mixer.Sound.play(squeak_3_sound)
        self.changeModeToExit()
                
    def changeModeToShowUp(self):
        mixer.Sound.play(pop_sound)
        self.active = True
        self.visible = True
        self.status = MoleStatus.SHOW_UP
        
    def changeModeToWaiting(self):
        self.active = True
        self.visible = True
        self.status = MoleStatus.WAITING
        self.lastWaiting = pygame.time.get_ticks()
        
    def changeModeToExit(self):
        self.active = True
        self.visible = True
        self.status = MoleStatus.EXIT
        
    def changeModeToHidden(self):
        self.active = False
        self.visible = False
        self.status = MoleStatus.HIDDEN

def isTouchOnRect(x, y, rectX, rectY, rectWidth, rectHeight):
    if rectX < x and x < rectX + rectWidth and rectY < y and y < rectY + rectHeight:
        return True
    return False

def main():
    running = True
    grid = Grid(ROW, COL)
    mole = Mole(grid, GROUND_TOP_LEFT_X + GROUND_WIDTH/2 - MOLE_WIDTH/2, GROUND_TOP_LEFT_Y , 1)
    mole2 = Mole(grid, GROUND_TOP_LEFT_X + GROUND_WIDTH/2 - MOLE_WIDTH/2, GROUND_TOP_LEFT_Y , 2)
    mole3 = Mole(grid, GROUND_TOP_LEFT_X + GROUND_WIDTH/2 - MOLE_WIDTH/2, GROUND_TOP_LEFT_Y , 3)

    clock = pygame.time.Clock()
    scoreLabel = Score()
    missLabel = Miss()
    FPS = 30
    
    mixer.music.play(-1)
    
    while running:
        clock.tick(FPS)
            
        screen.fill(GREY)
        m_x, m_y = pygame.mouse.get_pos()
        screen.blit(background_image, (0,0))
        
        screen.blit(wick_sprite, (0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if touch on mole1
                if isTouchOnRect(m_x, m_y, mole.x-20, mole.y-20, MOLE_WIDTH+40, MOLE_HEIGHT+40):
                    mole.getHit()
                    if (mole.isDead):
                        if (mole.isHard):
                            scoreLabel.score += 3
                        else:
                            scoreLabel.score += 1
                if isTouchOnRect(m_x, m_y, mole2.x-20, mole2.y-20, MOLE_WIDTH+40, MOLE_HEIGHT+40):
                    mole2.getHit()
                    if (mole2.isDead):
                        if (mole2.isHard):
                            scoreLabel.score += 3
                        else:
                            scoreLabel.score += 1
                if isTouchOnRect(m_x, m_y, mole3.x-20, mole3.y-20, MOLE_WIDTH+40, MOLE_HEIGHT+40):
                    mole3.getHit()
                    if (mole3.isDead):
                        if (mole3.isHard):
                            scoreLabel.score += 3
                        else:
                            scoreLabel.score += 1
                
        mole.update()
        mole2.update()
        grid.update()
        scoreLabel.update()
        missLabel.update()
        pygame.display.flip()
    pygame.quit()
    
main()