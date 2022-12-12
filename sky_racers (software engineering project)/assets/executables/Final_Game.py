"""
This is a test for the main game. To control the cars use the
arrow keys to control car1 and WASD to control car2. to place 
objects left click for a box and right click for a circle

to run this code you need pygame and box2d-py

~$ pip install pygmae
~$ pip install box2d-py
"""

import os
import pygame
import Box2D
import time

from pathlib import Path
from sky_racers.classes.Car import Car
from sky_racers.classes.Box import Box
from sky_racers.classes.Circle import Circle
from sky_racers.classes.GameMap import GAME_MAP
from sky_racers.classes.World_collision_listener import World_collision_listener
from sky_racers.classes.config import *
from sky_racers.classes.LapTimesBox import LapTimesBox
from sky_racers.classes.useful_defs import *
from sky_racers.classes.high_scores import HighScores
from sky_racers.classes.sounds import Sounds
from sky_racers.file_reader import CommandCall

gameState = 0
gameFrame = 0

sounds_path = Path(__file__).parent.parent
sounds_path = os.path.join(sounds_path, 'sounds')
sounds_lib = Sounds(sounds_path)

#this tells the world to listen for and respond to collisions with the World_collision_listener class
WORLD.contactListener = World_collision_listener()
pygame.font.init()
font = pygame.font.Font("game_over.ttf", 200)

def _drawText(message, x, y):
        text = font.render(message, True, (255, 0, 0))
        textRect = text.get_rect()
        textRect = textRect.move(x, y)
        SCREEN.blit(text, textRect)

codename = "instructions/Instructions.txt"

Shapes = []

right_key = False
left_key = False
up_key = False
down_key = False

right_code = False
left_code = False
acc_code = False
rev_code = False

showHitBox = False

scorerecorded = False

text_folder = Path(__file__).parent.parent.parent
text_folder = os.path.join(text_folder, 'classes')
highscoresFile = os.path.join(text_folder, "high_scores.txt")
file = open(highscoresFile)
scores = file.readlines()
file.close()

for i in range(3):
    scores[i] = scores[i].rstrip()


titleScreen = pygame.image.load("titleScreen.png").convert_alpha()
highScoresScreen = pygame.image.load("HighScoreScreen.png").convert_alpha()
backButton = pygame.image.load("backButton.png").convert_alpha()
backButtonLarge = pygame.image.load("backButtonLarge.png").convert_alpha()
playButton = pygame.image.load("playButton.png").convert_alpha()
highscoresButton = pygame.image.load("highscoresButton.png").convert_alpha()
exitButton = pygame.image.load("exitButton.png").convert_alpha()
playButtonLarge = pygame.image.load("playButtonLarge.png").convert_alpha()
highscoresButtonLarge = pygame.image.load("highscoresButtonLarge.png").convert_alpha()
exitButtonLarge = pygame.image.load("exitButtonLarge.png").convert_alpha()
three = pygame.image.load("3.png").convert_alpha()
two = pygame.image.load("2.png").convert_alpha()
one = pygame.image.load("1.png").convert_alpha()
go = pygame.image.load("go.png").convert_alpha()
race_over = pygame.image.load("finish_logo.png").convert_alpha()
race_over = pygame.transform.scale(race_over,(400,225))
explosionImg = pygame.image.load("flame.png").convert_alpha()
car1Img = pygame.image.load("car1.png").convert_alpha()
car2Img = pygame.image.load("car2.png").convert_alpha()

bkgd = pygame.image.load("sky.jpg").convert()
x = 0

car1 = Car(GAME_MAP.startPoints[0][0], GAME_MAP.startPoints[0][1], car1Img, explosionImg)
car2 = Car(GAME_MAP.startPoints[1][0], GAME_MAP.startPoints[1][1], car2Img, explosionImg)
car1start = car1
car2start = car2

instructionlist, numberlist = CommandCall.fileread(codename, car2)

lapBox = LapTimesBox()

running = True
crash_limiter = 0

while running:
    if gameState == 0:
        if not sounds_lib.bg_playing:
            sounds_lib.play_bg_music()
        in_menu = True
        waitframes = 0

        rel_x = x % bkgd.get_rect().width
        SCREEN.blit(bkgd, (rel_x - bkgd.get_rect().width, 0))
        if rel_x < SCREEN_WIDTH:
            SCREEN.blit(bkgd, (rel_x, 0))
        x -= 1

        SCREEN.blit(titleScreen, (0, 0))
        playButtonRect = SCREEN.blit(playButton, (SCREEN_WIDTH/2-playButton.get_size()[0]/2, 235))
        highscoresButtonRect = SCREEN.blit(highscoresButton, (SCREEN_WIDTH/2-highscoresButton.get_size()[0]/2, 410))
        exitButtonRect = SCREEN.blit(exitButton, (SCREEN_WIDTH/2-exitButton.get_size()[0]/2, 550))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mX, mY = pygame.mouse.get_pos()
                if event.button == 1:
                    if playButtonRect.collidepoint((mX, mY)):
                        if scorerecorded == True:
                            del car1
                            del car2
                            car1 = Car(GAME_MAP.startPoints[0][0], GAME_MAP.startPoints[0][1], car1Img, explosionImg)
                            car2 = Car(GAME_MAP.startPoints[1][0], GAME_MAP.startPoints[1][1], car2Img, explosionImg)
                            gameFrame = 0
                            Shapes = []
                            scorerecorded = False
                        gameState = 1
                    if highscoresButtonRect.collidepoint((mX, mY)):
                        gameState = 2
                    if exitButtonRect.collidepoint((mX, mY)):
                        running = False

        if playButtonRect.collidepoint(pygame.mouse.get_pos()):
            SCREEN.blit(playButtonLarge, (SCREEN_WIDTH/2-playButtonLarge.get_size()[0]/2, 225))
        
        if highscoresButtonRect.collidepoint(pygame.mouse.get_pos()):
            SCREEN.blit(highscoresButtonLarge, (SCREEN_WIDTH/2-highscoresButtonLarge.get_size()[0]/2, 400))

        if exitButtonRect.collidepoint(pygame.mouse.get_pos()):
            SCREEN.blit(exitButtonLarge, (SCREEN_WIDTH/2-exitButtonLarge.get_size()[0]/2, 540))


    if gameState == 1:
        if sounds_lib.bg_playing:
            sounds_lib.bg_pause()
        if not sounds_lib.start_played:
            sounds_lib.play_race_start()
        if car1.colliding_with_wall or car1.colliding_with_car or car2.colliding_with_wall or car2.colliding_with_car:
            if crash_limiter < 1:
                sounds_lib.play_crash_sound()
                crash_limiter += 30
        crash_limiter -= 1
        in_menu = False
        CommandCall.command(instructionlist, numberlist, car2, acc_code, rev_code, left_code, right_code)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mX, mY = pygame.mouse.get_pos()
                if event.button == 1:
                    Shapes.append(Box(mX, mY))
                if event.button == 3:
                    Shapes.append(Circle(mX, mY))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    right_key = True
                if event.key == pygame.K_LEFT:
                    left_key = True
                if event.key == pygame.K_UP:
                    up_key = True
                if event.key == pygame.K_DOWN:
                    down_key = True
                if event.key == pygame.K_h:
                    showHitBox = not showHitBox

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    right_key = False
                if event.key == pygame.K_LEFT:
                    left_key = False
                if event.key == pygame.K_UP:
                    up_key = False
                if event.key == pygame.K_DOWN:
                    down_key = False

            
            #Code controlled vehicle
            if event.type == pygame.USEREVENT+0:
                right_code = True
                left_code = False
            if event.type == pygame.USEREVENT+1:
                left_code = True
                right_code = False
            if event.type == pygame.USEREVENT+2:
                acc_code = True
                rev_code = False
                #left_code = False
                #right_code = False
            if event.type == pygame.USEREVENT+3:
                rev_code = True
                acc_code = False
                left_code = False
                right_code = False
            if event.type == pygame.USEREVENT+4:
                pass

        if gameFrame > 180:
            if not car1.finished:
                if right_key:
                    car1.turnRight()
                if left_key:
                    car1.turnLeft()
                if up_key:
                    car1.accelerateFoward()
                if down_key:
                    car1.accelerateBackward()
            elif scorerecorded == False:
                HighScores.record_score(car1._total_time)
                scorerecorded = True
            
            if not car2.finished:
                if right_code: 
                    car2.turnRight()
                if left_code:
                    car2.turnLeft()
                if acc_code:
                    car2.accelerateFoward()
                if rev_code:
                    car2.accelerateBackward()

        #print("angle to wall: " + str(car1.angle_to_wall) + ", " + "angle to checkpoint: " + str(car1.angle_to_checkpoint))


        GAME_MAP.display(showHitBox)

        for shape in Shapes:
            shape.display(showHitBox)

        car1.display(showHitBox)
        car2.display(showHitBox)
        #print(car1.global_angle)
        
        if gameFrame > 180:
            if gameFrame == 181:
                car2.startRace = True
                car1.startRace = True
            lapBox.display(car1.laptimes, car2.laptimes)

        if gameFrame >= 0 and gameFrame < 60:
            SCREEN.blit(three, (0,0))

        if gameFrame >= 60 and gameFrame < 120:
            SCREEN.blit(two, (0,0))

        if gameFrame >= 120 and gameFrame < 180:
            SCREEN.blit(one, (0,0))
        
        if gameFrame >= 180 and gameFrame < 240:
            SCREEN.blit(go, (0,0))

        gameFrame += 1

    if (car1.finished and car2.finished) and not in_menu:
        waitframes += 1
        SCREEN.blit(race_over, (SCREEN_WIDTH/2-200, SCREEN_HEIGHT/2-110))
        if waitframes == FPS * 3:
            file = open(highscoresFile)
            scores = file.readlines()
            file.close()

            for i in range(3):
                scores[i] = scores[i].rstrip()
                
            gameState = 0
    
    if gameState == 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mX, mY = pygame.mouse.get_pos()
                if event.button == 1:
                    if backButtonRect.collidepoint((mX, mY)):
                        gameState = 0
        rel_x = x % bkgd.get_rect().width
        SCREEN.blit(bkgd, (rel_x - bkgd.get_rect().width, 0))
        if rel_x < SCREEN_WIDTH:
            SCREEN.blit(bkgd, (rel_x, 0))
        x -= 1

        SCREEN.blit(highScoresScreen, (0, 0))
        _drawText("1st. " + scores[0], 350, 250)
        _drawText("2nd. " + scores[1], 350, 320)
        _drawText("3rd. " + scores[2], 350, 390)
        backButtonRect = SCREEN.blit(backButton, (SCREEN_WIDTH/2-backButton.get_size()[0]/2, 550))

        if backButtonRect.collidepoint(pygame.mouse.get_pos()):
            SCREEN.blit(backButtonLarge, (SCREEN_WIDTH/2-backButtonLarge.get_size()[0]/2, 540))

    pygame.display.update()
    WORLD.Step(TIME_STEP, 10, 10)
    CLOCK.tick(FPS)
