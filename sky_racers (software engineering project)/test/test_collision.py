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

test_pass = True

failed_xcolls = []
failed_ycolls = []

coll_list = [100,300,500,700,900]
expected_colls = [False, False, False, False, False, False, True,  True,   True, False, False, False, True,  False, False, False, False, True,  False, False]

WORLD.contactListener = World_collision_listener()

explosionImg = pygame.image.load("flame.png").convert_alpha()

carImg = pygame.image.load("car1.png").convert_alpha()
car = Car(GAME_MAP.startPoints[0][0], GAME_MAP.startPoints[0][1], carImg, explosionImg)

running = True
x=0
y=0
coll_index=0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    GAME_MAP.display(True)
    car.teleport_to(coll_list[x%5],coll_list[y%4])
    car.display(True)
    pygame.display.update()
    WORLD.Step(TIME_STEP, 10, 10)
    print("x{} y{} ex{} ac{}".format(coll_list[x%5], coll_list[y%4], expected_colls[coll_index%20], car.colliding_with_wall))
    if expected_colls[coll_index%20] == car.colliding_with_wall:
        print("Pass")
    else:
        print("Fail")
        test_pass = False
        failed_xcolls.append(coll_list[x%5])
        failed_ycolls.append(coll_list[y%4])
    x+=1
    coll_index+=1
    if x%5==0:
        y+=1
    #print(car.colliding_with_wall)
    CLOCK.tick(10)
    if coll_index==20:
        running = False

if test_pass:
    print("Collision Test Passed")
else:
    print("Collision Test Failed")
    print("Failed Collisions At:")
    for i in range(0, len(failed_xcolls)):
        print("{} {}".format(failed_xcolls[i], failed_ycolls[i]))
print()
