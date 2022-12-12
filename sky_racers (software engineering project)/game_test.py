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

from sky_racers.classes.Car import Car
from sky_racers.classes.Box import Box
from sky_racers.classes.Circle import Circle
from sky_racers.classes.GameMap import GAME_MAP
from sky_racers.classes.World_collision_listener import World_collision_listener
from sky_racers.classes.config import *
from sky_racers.classes.LapTimesBox import LapTimesBox
from sky_racers.classes.useful_defs import *
from sky_racers.classes.high_scores import HighScores
from sky_racers.file_reader import CommandCall

#this tells the world to listen for and respond to collisions with the World_collision_listener class
WORLD.contactListener = World_collision_listener()

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

explosionImg = pygame.image.load("flame.png").convert_alpha()

car1Img = pygame.image.load("car1.png").convert_alpha()
car1 = Car(GAME_MAP.startPoints[0][0], GAME_MAP.startPoints[0][1], car1Img, explosionImg)

car2Img = pygame.image.load("car2.png").convert_alpha()
car2 = Car(GAME_MAP.startPoints[1][0], GAME_MAP.startPoints[1][1], car2Img, explosionImg)


instructionlist, numberlist = CommandCall.fileread(codename, car2)

lapBox = LapTimesBox()

running = True
while running:
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
        if event.type == pygame.USEREVENT+3:
            rev_code = True
            acc_code = False
            left_code = False
            right_code = False
        if event.type == pygame.USEREVENT+4:
            pass


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

    lapBox.display(car1.laptimes, car2.laptimes)



    pygame.display.update()
    WORLD.Step(TIME_STEP, 10, 10)
    CLOCK.tick(FPS)
