import math, random, sys
import pygame
from pygame.locals import *

def events():
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			pygame.quit()
			sys.exit()

			
W, H = 1600, 1000
HW, HH = W / 2, H / 2
AREA = W * H


pygame.init()
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((W, H))
pygame.display.set_caption("code.Pylet - Template")
FPS = 60

bkgd = pygame.image.load("sky.jpg").convert()
x = 0

# define some colors

# main loop
while True:
	events()

	rel_x = x % bkgd.get_rect().width
	SCREEN.blit(bkgd, (rel_x - bkgd.get_rect().width, 0))
	if rel_x < W:
		SCREEN.blit(bkgd, (rel_x, 0))
	x -= 1

	pygame.display.update()
	CLOCK.tick(FPS)
