import math
from tkinter import HIDDEN
import alg
import pygame
import time
import sys

import random
from enum import Enum

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
eye_image = pygame.image.load(r'./images/eye.png')
mole_hands_image = pygame.image.load(r'./images/mole_hands.png')

background_image = pygame.image.load(r'./images/background.jpeg')

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

class MoleStatus(Enum):
    HIDDEN = 0
    SHOW_UP = 1
    EXIT = 2
    WAITING = 3
    
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
                
    
class Mole:
    def __init__(self, grid, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.grid = grid
        self.eye = eye_image
        self.isDead = False
        if (type == 1):
            self.image = mole1_image
            self.rect = mole1_image.get_rect()
        elif (type == 2):
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
        self.waitingTime = 1500
        self.teleportTime = 200 + 1000 * random.random()
        self.teleport()
    
    def update(self):
        self.updateFollowStatus()
        self.render()
    
    def render(self):
        if self.visible:
            screen.blit(self.image, (self.x, self.y), (0, 0, MOLE_WIDTH, 1 - (self.y - self.ground.y - MOLE_HEIGHT*0.5)))
            if (self.isDead and self.y < self.ground.y):
                screen.blit(self.eye, (self.x + 17, self.y + 24))
            
    def teleport(self):
        groundNoMoles = list(filter(lambda x: not x.haveMole, self.grid.grounds))
        randNumber =  math.floor(random.random() * len(groundNoMoles))
        self.ground = groundNoMoles[randNumber] 
        self.ground.haveMole = True
        self.x = self.ground.x + GROUND_WIDTH/2 - MOLE_WIDTH/2
        self.y = self.ground.y
        self.lastTeleport = pygame.time.get_ticks()
        self.teleportTime = 1000 * random.random()
    
    def showUp(self):
        self.y -= 10
        if (self.y < self.ground.y - MOLE_HEIGHT*0.7):
            self.changeModeToWaiting()
    
    def exit(self):
        self.y += 15 
        if (self.y > self.ground.y + 50):
            self.ground.haveMole = False
            self.isDead = False
            self.changeModeToHidden()
            self.teleport()

    def updateFollowStatus(self):
        if (self.status == MoleStatus.HIDDEN):
            now = pygame.time.get_ticks()
            if now - self.lastTeleport >= self.teleportTime:
                self.changeModeToShowUp()
        elif (self.status == MoleStatus.SHOW_UP):
            self.showUp()
        elif (self.status == MoleStatus.WAITING):
            now = pygame.time.get_ticks()
            if now - self.lastWaiting >= self.waitingTime:
                self.exit()
        elif (self.status == MoleStatus.EXIT):
            self.exit()
            
    def getHit(self):
        if (not self.isDead):
            self.dead()
        
    def dead(self):
        self.isDead = True
        self.changeModeToExit()
                
    def changeModeToShowUp(self):
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

    mole.active = True
    mole.status = MoleStatus.SHOW_UP

    clock = pygame.time.Clock()
    scoreLabel = Score()
    FPS = 30
    while running:
        clock.tick(FPS)
            
        screen.fill(GREY)
        m_x, m_y = pygame.mouse.get_pos()
        screen.blit(background_image, (0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if touch on mole1
                if isTouchOnRect(m_x, m_y, mole.x, mole.y, MOLE_WIDTH, MOLE_HEIGHT):
                    mole.getHit()
                    if (mole.isDead):
                        scoreLabel.score += 1
                if isTouchOnRect(m_x, m_y, mole2.x, mole2.y, MOLE_WIDTH, MOLE_HEIGHT):
                    mole2.getHit()
                    if (mole2.isDead):
                        scoreLabel.score += 1
                
        mole.update()
        mole2.update()
        grid.update()
        scoreLabel.update()
        pygame.display.flip()
    pygame.quit()
    
main()