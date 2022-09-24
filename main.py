import math
# from tkinter import HIDDEN
from MoleStatus import MoleStatus, MoleType
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

play_button_image = pygame.image.load(r'./images/first_play_button.png')
gui_1_image = pygame.image.load(r'./images/gui_1.png')
gui_2_image = pygame.image.load(r'./images/gui_2.png')
time_over_image = pygame.image.load(r'./images/timeover.png')

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
PLAY_BUTTON_WIDTH = 296
PLAY_BUTTON_HEIGHT = 116
BOMB_WIDTH = 106
BOMB_HEIGHT = 97

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

class ScoreLabel:
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
        
class EscapeLabel:
    escape = 0
    def __init__(self):
        self.text = font.render(f'Escape: {EscapeLabel.escape}', True, COLOR1, WHITE)
        self.textRect = self.text.get_rect()
        self.textRect.center = (100, 200)
        
    def update(self):
        self.render()
    
    def render(self):
        self.text = font.render(f'Escape: {EscapeLabel.escape}', True, COLOR1, WHITE)
        
        screen.blit(self.text, self.textRect)

class TimeLabel:
    time = 0
    def __init__(self):
        self.text = font.render(f'Time: {TimeLabel.time}', True, COLOR1, WHITE)
        self.textRect = self.text.get_rect()
        self.textRect.center = (100, 300)
        
    def update(self):
        self.render()
    
    def render(self):
        self.text = font.render(f'Time: {TimeLabel.time}', True, COLOR1, WHITE)
        
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
        self.width = MOLE_WIDTH
        self.height = MOLE_HEIGHT
        if (type == MoleType.NORMAL):
            self.image = mole1_image
            self.rect = mole1_image.get_rect()
        elif (type == MoleType.NORMAL_2 or type == MoleType.NORMAL_3):
            self.image = mole2_image
            self.rect = mole2_image.get_rect()
        elif (type == MoleType.BOMB):
            self.image = bomb_image
            self.rect = bomb_image.get_rect()
            self.width = BOMB_WIDTH
            self.height = BOMB_HEIGHT
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.x = x
        self.y = y
        self.active = False
        self.visible = False
        self.status = MoleStatus.NOT_START
        self.lastWaiting = pygame.time.get_ticks()
        self.lastTeleport = pygame.time.get_ticks()
        self.lastShake = pygame.time.get_ticks()
        self.shakeTime = 200
        self.waitingTime = 1500
        self.resetTeleportTime()
        self.respawn()  
        
    def resetTeleportTime(self):
        self.teleportTime = 200 + 1500 * random.random()
        if (self.type == MoleType.NORMAL_3):
            self.teleportTime = 4000 + 1000 * random.random()
        if (self.type == MoleType.BOMB):
            self.teleportTime = 3000 + 1000 * random.random()
    
    def update(self, deltaTime):
        self.updateFollowStatus(deltaTime)
        self.render()
    
    def render(self):
        if self.visible:
            screen.blit(self.image, (self.x, self.y), (0, 0, self.width, 1 - (self.y - self.ground.y - self.height*0.5)))
            if (self.isDead and self.y < self.ground.y):
                screen.blit(self.eye, (self.x + 17, self.y + 24))
            if (self.isHaveHat and self.y < self.ground.y):
                screen.blit(self.hard_hat, (self.x + 8, self.y - 15))
            
    def teleport(self):
        groundNoMoles = list(filter(lambda x: not x.haveMole, self.grid.grounds))
        print('>', len(groundNoMoles))
        randNumber =  math.floor(random.random() * len(groundNoMoles))
        self.ground = groundNoMoles[randNumber] 
        self.ground.haveMole = True
        self.rawX = self.ground.x + GROUND_WIDTH/2 - self.width/2
        self.x = self.rawX
        self.y = self.ground.y
        self.lastTeleport = pygame.time.get_ticks()
        self.resetTeleportTime()
        
    def showUp(self, deltaTime):
        self.y -= 10 / 33 * deltaTime
        if (self.y < self.ground.y - self.height*0.7):
            self.changeModeToWaiting()
    
    def exit(self, deltaTime):
        self.y += 15 / 33 * deltaTime
        if (self.y > self.ground.y + 50):
            self.ground.haveMole = False
            self.respawn()
    
    def respawn(self):
        self.changeModeToHidden()
        self.isDead = False
        self.isShake = False
        self.teleport()
        if (random.random() < 0.5 and self.type is not MoleType.BOMB):
            self.isHard = True
            self.lives = 3
        else:
            self.isHard = False
            self.lives = 1
        self.isHaveHat = self.isHard
        
    def destroy(self):
        self.changeModeToNotStart()
        self.ground.haveMole = False

    def updateFollowStatus(self, deltaTime):
        if (self.status == MoleStatus.HIDDEN):
            now = pygame.time.get_ticks()
            if now - self.lastTeleport >= self.teleportTime:
                self.changeModeToShowUp()
        elif (self.status == MoleStatus.SHOW_UP):
            self.showUp(deltaTime)
        elif (self.status == MoleStatus.WAITING):
            now = pygame.time.get_ticks()
            self.shake(deltaTime)
            if now - self.lastWaiting >= self.waitingTime:
                self.changeModeToExit()
                EscapeLabel.escape += 1
        elif (self.status == MoleStatus.EXIT):
            self.exit(deltaTime)
            
    def shake(self, deltaTime):
        if (self.isShake):
            if (self.shakeLeft):
                self.x -= 5 / 33 * deltaTime
            else:
                self.x += 5 / 33 * deltaTime
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
        
    def changeModeToNotStart(self):
        self.active = False
        self.visible = False
        self.status = MoleStatus.NOT_START

class PlayButton:
    def __init__(self):
        self.x = SCREEN_WIDTH*0.05
        self.y = SCREEN_HEIGHT*0.6
        self.visible = True
        
    def update(self):
        self.render()
    
    def render(self):
        if (self.visible):
            screen.blit(play_button_image, (self.x, self.y))

def isTouchOnRect(x, y, rectX, rectY, rectWidth, rectHeight):
    if rectX < x and x < rectX + rectWidth and rectY < y and y < rectY + rectHeight:
        return True
    return False

def main():
    gameOver = True
    running = True
    grid = Grid(ROW, COL)
    mole = Mole(grid, GROUND_TOP_LEFT_X + GROUND_WIDTH/2 - MOLE_WIDTH/2, GROUND_TOP_LEFT_Y , MoleType.NORMAL)
    mole2 = Mole(grid, GROUND_TOP_LEFT_X + GROUND_WIDTH/2 - MOLE_WIDTH/2, GROUND_TOP_LEFT_Y , MoleType.NORMAL_2)
    mole3 = Mole(grid, GROUND_TOP_LEFT_X + GROUND_WIDTH/2 - MOLE_WIDTH/2, GROUND_TOP_LEFT_Y , MoleType.NORMAL_3)
    bomb = Mole(grid, GROUND_TOP_LEFT_X + GROUND_WIDTH/2 - BOMB_WIDTH/2, GROUND_TOP_LEFT_Y , MoleType.BOMB)

    clock = pygame.time.Clock()
    scoreLabel = ScoreLabel()
    escapeLabel = EscapeLabel()
    playButton = PlayButton()
    FPS = 20
    
    lastTime = pygame.time.get_ticks()
    deltaTime = 0
    
    mixer.music.play(-1)
    while running:
        clock.tick(FPS)
        now = pygame.time.get_ticks()
        deltaTime = now - lastTime
        lastTime = pygame.time.get_ticks()
        # print(deltaTime)
            
        screen.fill(GREY)
        m_x, m_y = pygame.mouse.get_pos()
        screen.blit(background_image, (0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(random.random())
                
                if (not gameOver):
                    if isTouchOnRect(m_x, m_y, mole.x-20, mole.y-20, mole.width+40, mole.height+40):
                        mole.getHit()
                        if (mole.isDead):
                            if (mole.isHard):
                                scoreLabel.score += 3
                            else:
                                scoreLabel.score += 1
                    if isTouchOnRect(m_x, m_y, mole2.x-20, mole2.y-20, mole2.width+40, mole2.height+40):
                        mole2.getHit()
                        if (mole2.isDead):
                            if (mole2.isHard):
                                scoreLabel.score += 3
                            else:
                                scoreLabel.score += 1
                    if isTouchOnRect(m_x, m_y, mole3.x-20, mole3.y-20, mole3.width+40, mole3.height+40):
                        mole3.getHit()
                        if (mole3.isDead):
                            if (mole3.isHard):
                                scoreLabel.score += 3
                            else:
                                scoreLabel.score += 1
                    if isTouchOnRect(m_x, m_y, bomb.x-20, bomb.y-20, bomb.width+40, bomb.height+40):
                        gameOver = True
                        playButton.visible = True
                        mole.destroy()
                        mole2.destroy()
                        mole3.destroy()
                        bomb.destroy()
                else:
                    if isTouchOnRect(m_x, m_y, playButton.x, playButton.y, PLAY_BUTTON_WIDTH, PLAY_BUTTON_HEIGHT):
                        gameOver = False
                        scoreLabel.score = 0
                        EscapeLabel.escape = 0
                        playButton.visible = False
                        mole.respawn()
                        mole2.respawn()
                        mole3.respawn()
                        bomb.respawn()
        if (not gameOver):
            mole.update(deltaTime)
            mole2.update(deltaTime)
            mole3.update(deltaTime)
            bomb.update(deltaTime)
            grid.update()
        scoreLabel.update()
        escapeLabel.update()
        playButton.update()
        pygame.display.flip()
    pygame.quit()
    
main()