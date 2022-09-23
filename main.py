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
    def __init__(self, grid, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.grid = grid
        self.image = mole1_image
        self.rect = mole1_image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.x = x
        self.y = y
        self.active = False
        self.visible = True
        self.status = MoleStatus.HIDDEN
        self.teleport()
    
    def update(self):
        self.updateFollowStatus()
        self.render()
    
    def render(self):
        if self.visible:
            screen.blit(mole1_image, (self.x,self.y))
            
    def teleport(self):
        groundNoMoles = list(filter(lambda x: not x.haveMole, self.grid.grounds))
        randNumber =  math.floor(random.random() * len(groundNoMoles))
        self.ground = groundNoMoles[randNumber] 
        self.x = self.ground.x + GROUND_WIDTH/2 - MOLE_WIDTH/2
        self.y = self.ground.y
    
    def showUp(self):
        pass

    def updateFollowStatus(self):
        if (self.status == MoleStatus.HIDDEN):
             pass
        elif (self.status == MoleStatus.SHOW_UP):
            self.y -= 3  
            if (self.y < self.ground.y - MOLE_HEIGHT*0.8):
                self.changeModeToWaiting()
        elif (self.status == MoleStatus.WAITING):
            pass
        elif (self.status == MoleStatus.EXIT):
            self.y += 3  
            if (self.y > self.ground.y):
                self.changeModeToHidden()
                
    def changeModeToShowUp(self):
        self.active = True
        self.visible = True
        self.status = MoleStatus.SHOW_UP
        
    def changeModeToWaiting(self):
        self.active = True
        self.visible = True
        self.status = MoleStatus.WAITING
        
    def changeModeToExit(self):
        self.active = True
        self.visible = True
        self.status = MoleStatus.EXIT
        
    def changeModeToHidden(self):
        self.active = False
        self.visible = False
        self.status = MoleStatus.HIDDEN
        
def main():
    running = True
    grid = Grid(ROW, COL)
    mole = Mole(grid, GROUND_TOP_LEFT_X + GROUND_WIDTH/2 - MOLE_WIDTH/2, GROUND_TOP_LEFT_Y )
    mole2 = Mole(grid, GROUND_TOP_LEFT_X + GROUND_WIDTH/2 - MOLE_WIDTH/2, GROUND_TOP_LEFT_Y )

    mole.active = True
    mole2.active = True
    mole.status = MoleStatus.SHOW_UP
    clock = pygame.time.Clock()
    FPS = 30
    while running:
        clock.tick(FPS)
            
        screen.fill(GREY)
        m_x, m_y = pygame.mouse.get_pos()
        screen.blit(background_image, (0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if event.type == pygame.MOUSEBUTTONDOWN:
                # if touch on back button 
                #
                
        mole.update()
        mole2.update()
        grid.update()
        pygame.display.flip()
    pygame.quit()
    
main()