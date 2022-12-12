import os
import pygame
import Box2D

from ..classes.Car import Car
from ..classes.Box import Box
from ..classes.Circle import Circle
from ..classes.GameMap import GAME_MAP
from ..classes.World_collision_listener import World_collision_listener
from ..classes.config import *
from ..classes.LapTimesBox import LapTimesBox
from ..classes.useful_defs import *
from ..file_reader import CommandCall

teleSpots = [(920, 550), (920, 400), (880, 250), (800, 200), (600, 100), (100, 90), (200, 250), (550, 220), (650, 450), (700, 700), (900, 600)]
expectedCheckpoint = [1, 1, 2, 2, 3, 4, 5, 6, 7, 8, 0]

WORLD.contactListener = World_collision_listener()

explosionImg = pygame.image.load("flame.png").convert_alpha()

carImg = pygame.image.load("car1.png").convert_alpha()
car = Car(GAME_MAP.startPoints[0][0], GAME_MAP.startPoints[0][1], carImg, explosionImg)

index = 0
currentFrame = 0
count = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if index < len(teleSpots):
        car.teleport_to(teleSpots[index][0], teleSpots[index][1])

    if currentFrame%2 == 0:
        if index < len(teleSpots):
            passed = expectedCheckpoint[index] == car._currentCheckpoint
            passOrFail = ""
            if passed:
                passOrFail = "PASSED"
            else:
                passOrFail = "FAILD"
            print("expected:" + str(expectedCheckpoint[index]) + ", got:" + str(car._currentCheckpoint) + ", " + passOrFail)

        index += 1


    GAME_MAP.display(True)
    car.display(True)
    WORLD.Step(TIME_STEP, 10, 10)
    currentFrame += 1
    pygame.display.update()
    CLOCK.tick(10)
    count+=1
    if count == 22:
        running = False
print()
