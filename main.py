import math
import alg
import pygame
import time
import sys

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

def draw_ground():
    for row in range(ROW):
        for col in range(COL): 
            x = GROUND_TOP_LEFT_X + PADDING_GROUND_WIDTH*col
            y = GROUND_TOP_LEFT_Y + PADDING_GROUND_HEIGHT*row
            screen.blit(ground_image, (x, y))
            screen.blit(ground_image, (x, y+40))
class Mole:
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = mole1_image
        self.rect = mole1_image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.x = x
        self.y = y
        self.active = False
        self.visible = True
    
    def update(self):
        if self.active:
            self.y -= 3  
            if (self.y < GROUND_TOP_LEFT_Y - MOLE_HEIGHT*0.8):
                # self.active = False
                self.y = GROUND_TOP_LEFT_Y
            self.render()
    
    def render(self):
        if self.visible:
            screen.blit(mole1_image, (self.x,self.y))
        


def main():
    running = True
    mole = Mole(GROUND_TOP_LEFT_X + GROUND_WIDTH/2 - MOLE_WIDTH/2, GROUND_TOP_LEFT_Y )
    mole.active = True
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
        draw_ground()
        pygame.display.flip()
    pygame.quit()
    
main()