import math
# from tkinter import HIDDEN
from Enum import MoleStatus, MoleType, Scene
import pygame
import time
import sys

import random
from enum import Enum
from pygame import mixer

from spritesheet import SpriteSheet

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
font = pygame.font.Font('freesansbold.ttf', 30)

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
wick_sprite_sheet = SpriteSheet(wick_sprite)

hammer_sprite = pygame.image.load(r'./images/hammer.png').convert_alpha()
hammer_sprite_sheet = SpriteSheet(hammer_sprite)

explode_sprite = pygame.image.load(r'./images/explosion.png').convert_alpha()
explode_sprite_sheet = SpriteSheet(explode_sprite)

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
TIME_OVER_WIDTH = 700/2
TIME_OVER_HEIGHT = 204/2
WICK_FRAME_WIDTH = 90
WICK_FRAME_HEIGHT = 90
HAMMER_FRAME_WIDTH = 237
HAMMER_FRAME_HEIGHT = 212
EXPLODE_FRAME_WIDTH = 178
EXPLODE_FRAME_HEIGHT = 178

SCORE_LABEL_X = 100
SCORE_LABEL_Y = 150
PADDING_LABEL = 75
COLOR_TEXT = (204, 102, 255)

time_over_image = pygame.transform.scale(time_over_image, (TIME_OVER_WIDTH, TIME_OVER_HEIGHT))

wick_0_image = wick_sprite_sheet.get_image(0, WICK_FRAME_WIDTH, WICK_FRAME_HEIGHT, 1, BLACK)
wick_1_image = wick_sprite_sheet.get_image(1, WICK_FRAME_WIDTH, WICK_FRAME_HEIGHT, 1, BLACK)
wick_2_image = wick_sprite_sheet.get_image(2, WICK_FRAME_WIDTH, WICK_FRAME_HEIGHT, 1, BLACK)
wick_3_image = wick_sprite_sheet.get_image(3, WICK_FRAME_WIDTH, WICK_FRAME_HEIGHT, 1, BLACK)
wick_4_image = wick_sprite_sheet.get_image(4, WICK_FRAME_WIDTH, WICK_FRAME_HEIGHT, 1, BLACK)

hammer_0_image = hammer_sprite_sheet.get_image(0, HAMMER_FRAME_WIDTH, HAMMER_FRAME_HEIGHT, 1, BLACK)
hammer_1_image = hammer_sprite_sheet.get_image(1, HAMMER_FRAME_WIDTH, HAMMER_FRAME_HEIGHT, 1, BLACK)
hammer_2_image = hammer_sprite_sheet.get_image(2, HAMMER_FRAME_WIDTH, HAMMER_FRAME_HEIGHT, 1, BLACK)
hammer_3_image = hammer_sprite_sheet.get_image(3, HAMMER_FRAME_WIDTH, HAMMER_FRAME_HEIGHT, 1, BLACK)
hammer_4_image = hammer_sprite_sheet.get_image(4, HAMMER_FRAME_WIDTH, HAMMER_FRAME_HEIGHT, 1, BLACK)
hammer_5_image = hammer_sprite_sheet.get_image(5, HAMMER_FRAME_WIDTH, HAMMER_FRAME_HEIGHT, 1, BLACK)

explode_0_image = explode_sprite_sheet.get_image(0, EXPLODE_FRAME_WIDTH, EXPLODE_FRAME_HEIGHT, 1, BLACK)
explode_1_image = explode_sprite_sheet.get_image(1, EXPLODE_FRAME_WIDTH, EXPLODE_FRAME_HEIGHT, 1, BLACK)
explode_2_image = explode_sprite_sheet.get_image(2, EXPLODE_FRAME_WIDTH, EXPLODE_FRAME_HEIGHT, 1, BLACK)
explode_3_image = explode_sprite_sheet.get_image(3, EXPLODE_FRAME_WIDTH, EXPLODE_FRAME_HEIGHT, 1, BLACK)
explode_4_image = explode_sprite_sheet.get_image(4, EXPLODE_FRAME_WIDTH, EXPLODE_FRAME_HEIGHT, 1, BLACK)
explode_5_image = explode_sprite_sheet.get_image(5, EXPLODE_FRAME_WIDTH, EXPLODE_FRAME_HEIGHT, 1, BLACK)
explode_6_image = explode_sprite_sheet.get_image(6, EXPLODE_FRAME_WIDTH, EXPLODE_FRAME_HEIGHT, 1, BLACK)
explode_7_image = explode_sprite_sheet.get_image(7, EXPLODE_FRAME_WIDTH, EXPLODE_FRAME_HEIGHT, 1, BLACK)

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
            ground.render()
            
    def getGroundLocation(self, row, col):
        for ground in self.grounds:
            if ground.idx == row and ground.idy == col:
                return ground.x, ground.y
            
class Label:
    pass

class ScoreLabel:
    score = 0
    def __init__(self):
        self.text = font.render(f'Score: {ScoreLabel.score}', True, COLOR_TEXT)
        self.textRect = self.text.get_rect()
        self.textRect.center = (SCORE_LABEL_X, SCORE_LABEL_Y)
        
    def update(self):
        self.render()
    
    def render(self):
        self.text = font.render(f'Score: {ScoreLabel.score}', True, COLOR_TEXT)
        
        screen.blit(self.text, (self.textRect.x + self.textRect.width/2 - 50, self.textRect.y))
        
class EscapeLabel:
    escape = 0
    def __init__(self):
        self.text = font.render(f'Escaped: {EscapeLabel.escape}', True, COLOR_TEXT)
        self.textRect = self.text.get_rect()
        self.textRect.center = (SCORE_LABEL_X, SCORE_LABEL_Y + PADDING_LABEL*2)
        
    def update(self):
        self.render()
    
    def render(self):
        self.text = font.render(f'Escaped: {EscapeLabel.escape}', True, COLOR_TEXT)
        
        screen.blit(self.text, (self.textRect.x + self.textRect.width/2 - 50, self.textRect.y))
        
class AccuracyLabel:
    accuracy = 0
    def __init__(self):
        self.text = font.render(f'Accuracy: {AccuracyLabel.accuracy}', True, COLOR_TEXT)
        self.textRect = self.text.get_rect()
        self.textRect.center = (SCORE_LABEL_X, SCORE_LABEL_Y + PADDING_LABEL*3)
        
    def update(self):
        self.render()
    
    def render(self):
        self.text = font.render(f'Accuracy: {AccuracyLabel.accuracy} %', True, COLOR_TEXT)
        
        screen.blit(self.text, (self.textRect.x + self.textRect.width/2 - 50, self.textRect.y))

class TimeLabel:
    def __init__(self, maxTime):
        self.maxTime = maxTime
        self.timeLeft = maxTime
        self.lastSecond = pygame.time.get_ticks()
        self.text = font.render(f'Time: {self.timeLeft}', True, COLOR_TEXT)
        self.textRect = self.text.get_rect()
        self.textRect.center = (SCORE_LABEL_X, SCORE_LABEL_Y + PADDING_LABEL)
        self.isRun = False
        
    def update(self):
        self.decreaseTime()
        self.render()
        
    def decreaseTime(self):
        if (self.isRun):
            now = pygame.time.get_ticks()
            if (now - self.lastSecond > 1000):
                self.lastSecond = now
                self.timeLeft -= 1

    def render(self):
        self.text = font.render(f'Time: {self.timeLeft}', True, COLOR_TEXT)
        
        screen.blit(self.text, (self.textRect.x + self.textRect.width/2 - 50, self.textRect.y))
        
    def resetTime(self):
        self.timeLeft = self.maxTime
        self.lastSecond = pygame.time.get_ticks()
        self.run()
        
    def run(self):
        self.lastSecond = pygame.time.get_ticks()
        self.isRun = True
        
    def stop(self):
        self.isRun = False

class Animation:
    def __init__(self, frames, duration, repeat):
        self.isRun = False
        self.frames = frames
        self.frameIndex = 0
        self.duration = duration
        self.timePerFrame = 0
        self.repeat = repeat
        self.totalFrame = len(self.frames)
        if (self.totalFrame > 0):
            self.timePerFrame = duration / self.totalFrame
            self.currentFrame = self.frames[0]
        self.lastRun = pygame.time.get_ticks()
        self.lastFrameRun = pygame.time.get_ticks()

    def update(self):
        if (self.isRun):
            now = pygame.time.get_ticks()
            if (now - self.lastFrameRun > self.timePerFrame):
                self.updateNextFrame()
            if (now - self.lastRun > self.duration):
                self.isRun = False
                self.frameIndex = 0
                self.currentFrame = self.frames[0]
    
    def updateNextFrame(self):
        now = pygame.time.get_ticks()

        if self.frameIndex < self.totalFrame - 1:
            self.frameIndex += 1
            self.currentFrame = self.frames[self.frameIndex]
            self.lastFrameRun = now
        elif self.frameIndex == self.totalFrame - 1:
            self.frameIndex = 0
            self.currentFrame = self.frames[0]
            self.lastFrameRun = now
            
    def run(self):
        self.isRun = True
        self.lastRun =  pygame.time.get_ticks()
        self.lastFrameRun = pygame.time.get_ticks()
    
    def stop(self):
        self.isRun = False


class Hammer:
    def __init__(self, idx, idy, grid):
        self.idx = idx
        self.idy = idy
        self.grid: Grid = grid
        self.hammer_animation = Animation([hammer_0_image, hammer_1_image, hammer_2_image, hammer_3_image, hammer_4_image],
                                     200, 0)
    
    def update(self):
        self.hammer_animation.update()
        self.render()
    
    def render(self):
        if self.hammer_animation.isRun:
            groundLocation = self.grid.getGroundLocation(self.idx, self.idy)
            screen.blit(self.hammer_animation.currentFrame, (groundLocation[0], groundLocation[1] - 180))
           
    def hit(self, idx, idy):
        self.idx = idx
        self.idy = idy
        self.hammer_animation.run()
    
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
        self.wick_animation = Animation([wick_0_image, wick_1_image, wick_2_image, wick_3_image, wick_4_image],
                                        500, 0)
        self.explode_animation = Animation([explode_0_image, explode_1_image, explode_2_image, explode_3_image, 
                                            explode_4_image, explode_5_image, explode_6_image, explode_7_image],
                                           500, 0)
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
        self.onHit = False
        self.lastHit = pygame.time.get_ticks()
        self.respawn()  
        
    def resetTeleportTime(self):
        self.teleportTime = 100 + 1500 * random.random()
        if (self.type == MoleType.NORMAL_3):
            self.teleportTime = 1000 + 1000 * random.random()
        if (self.type == MoleType.BOMB):
            self.teleportTime = 2000 + 2000 * random.random()
    
    def update(self, deltaTime):
        now = pygame.time.get_ticks()
        if now - self.lastHit > 100 and self.onHit:
            self.onHit = False
            self.getHit()
        self.updateFollowStatus(deltaTime)
        self.explode_animation.update()
        self.render()
    
    def render(self):
        if self.visible:
            if (self.type == MoleType.BOMB):
                screen.blit(self.image, (self.x + 15, self.y), (0, 0, self.width, 1 - (self.y - self.ground.y - self.height*0.5)))
            else:
                screen.blit(self.image, (self.x, self.y), (0, 0, self.width, 1 - (self.y - self.ground.y - self.height*0.5)))
            if (self.isDead and self.y < self.ground.y):
                screen.blit(self.eye, (self.x + 17, self.y + 24))
            if (self.isHaveHat and self.y < self.ground.y):
                screen.blit(self.hard_hat, (self.x + 8, self.y - 15))
            if (self.wick_animation.isRun and self.y < self.ground.y):
                screen.blit(self.wick_animation.currentFrame , (self.x, self.y - WICK_FRAME_WIDTH/2))
            
    def render_explode_animation(self):
        if (self.explode_animation.isRun):
            screen.blit(self.explode_animation.currentFrame, (self.x - 29, self.y - 44))
            
    def teleport(self):
        groundNoMoles = list(filter(lambda x: not x.haveMole, self.grid.grounds))
        if (len(groundNoMoles) > 0):
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
        self.y += 10 / 33 * deltaTime
        if (self.y > self.ground.y + 20):
            self.ground.haveMole = False
            self.respawn()
    
    def respawn(self):
        self.changeModeToHidden()
        self.isDead = False
        self.isShake = False
        self.wick_animation.stop()
        self.teleport()
        if (random.random() < 0.3 and self.type is not MoleType.BOMB):
            self.isHard = True
            self.lives = 3
        else:
            self.isHard = False
            self.lives = 1
        self.isHaveHat = self.isHard
        
    def destroy(self):
        self.changeModeToNotStart()
        self.ground.haveMole = False
        self.isDead = True
        self.isShake = False
        self.wick_animation.stop()

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
            self.wick_animation.update()
            if now - self.lastWaiting >= self.waitingTime:
                self.changeModeToExit()
                if (self.type == MoleType.BOMB):
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
            self.wick_animation.run()
        if (self.lives <= 0 and not self.isDead):
            self.dead()
        if (self.isDead):
            if (self.isHard):
                ScoreLabel.score += 3
            else:
                ScoreLabel.score += 1
        
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
        
    def processInput(self, m_x, m_y, hammer):
        if (not self.isDead and self.visible and isTouchOnRect(m_x, m_y, self.x-20, self.y-20, self.width+40, self.height+40)):
            self.onHit = True
            self.lastHit = pygame.time.get_ticks()
            hammer.hit(self.ground.idx, self.ground.idy)
            return 1
        return 0

class PlayButton:
    def __init__(self):
        self.x = SCREEN_WIDTH/2 - PLAY_BUTTON_WIDTH/2 + 50
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
    currentScene = Scene.MENU_SCENE
    showTimeOver = False
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
    accuracyLabel = AccuracyLabel()
    timeLabel = TimeLabel(15)
    playButton = PlayButton()
    hammer = Hammer(0, 0, grid)
    FPS = 20
    
    total_hit = 0
    right_hit = 0
    
    lastTime = pygame.time.get_ticks()
    deltaTime = 0
    
    lastTimeExplode = pygame.time.get_ticks()
    lastTimeShowPlay = pygame.time.get_ticks()
    
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
                if (currentScene == Scene.GAME_SCENE and not gameOver):
                    total_hit += 1
                    right_hit += mole.processInput(m_x, m_y, hammer)
                    right_hit += mole2.processInput(m_x, m_y, hammer)
                    right_hit += mole3.processInput(m_x, m_y, hammer)
                    if (bomb.visible and isTouchOnRect(m_x, m_y, bomb.x-20, bomb.y-20, bomb.width+40, bomb.height+40)):
                        gameOver = True
                        mixer.Sound.play(explode_sound)
                        hammer.hit(bomb.ground.idx, bomb.ground.idy)
                        bomb.visible = False
                        bomb.explode_animation.run()
                        bomb.changeModeToNotStart()
                        lastTimeExplode = pygame.time.get_ticks()
                elif (currentScene == Scene.MENU_SCENE):
                    if ((pygame.time.get_ticks() - lastTimeShowPlay > 700) and isTouchOnRect(m_x, m_y, playButton.x, playButton.y, PLAY_BUTTON_WIDTH, PLAY_BUTTON_HEIGHT)):
                        gameOver = False
                        currentScene = Scene.GAME_SCENE
                        timeLabel.resetTime()
                        ScoreLabel.score = 0
                        EscapeLabel.escape = 0
                        playButton.visible = False
                        mole.respawn()
                        mole2.respawn()
                        mole3.respawn()
                        bomb.respawn()
                        showTimeOver = False
        if (currentScene == Scene.GAME_SCENE):                
            mole.update(deltaTime)
            mole2.update(deltaTime)
            mole3.update(deltaTime)
            bomb.update(deltaTime)
            grid.update()
            bomb.render_explode_animation()
            if (timeLabel.timeLeft <= 0):
                gameOver = True
                showTimeOver = True
        scoreLabel.update()
        timeLabel.update()
        if (currentScene == Scene.MENU_SCENE):
            escapeLabel.update()
            accuracyLabel.update()
        if (pygame.time.get_ticks() - lastTimeShowPlay > 700):
            playButton.update()
        hammer.update()
        if (gameOver and currentScene == Scene.GAME_SCENE):
            if (not bomb.explode_animation.isRun or 
                (bomb.explode_animation.isRun and pygame.time.get_ticks() - lastTimeExplode > 500)):
                timeLabel.stop()
                playButton.visible = True
                lastTimeShowPlay = pygame.time.get_ticks()
                mole.destroy()
                mole2.destroy()
                mole3.destroy()
                bomb.destroy()
                currentScene = Scene.MENU_SCENE
                gameOver = False
                if (total_hit == 0):
                    AccuracyLabel.accuracy = 0
                else:
                    AccuracyLabel.accuracy = math.floor(right_hit/total_hit * 10000)/100.0
                total_hit = 0
                right_hit = 0
                    
        
        if showTimeOver:
            screen.blit(time_over_image, (SCREEN_WIDTH/2 - TIME_OVER_WIDTH/2 + 50, SCREEN_HEIGHT/2 - TIME_OVER_HEIGHT/2 - 100))
            
        pygame.display.flip()
    pygame.quit()
    
main()