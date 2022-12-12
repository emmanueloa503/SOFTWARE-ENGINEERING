"""
This file is for creating constants that the python files for the game need
"""

import Box2D
import pygame


PPM = 10
FPS = 60
TIME_STEP = 1/FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768

FRICTION = 0.1
RESTITUTION = 0.5

CAR_LINEARDAMPING = 2.2
CAR_ANGULARDAMPING = 2.2
CAR_ACCFORCE = 1000
CAR_TURNFORCE = 1000
CAR_DENSITY = 1

OBJECT_LINEARDAMPING = 2.5
OBJECT_ANGULARDAMPING = 2.5
OBJECT_DENSITY = 0.1

WALL_FRICTION = 0.1

WORLD = Box2D.b2World((0, 0))

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sky")

CLOCK = pygame.time.Clock()
