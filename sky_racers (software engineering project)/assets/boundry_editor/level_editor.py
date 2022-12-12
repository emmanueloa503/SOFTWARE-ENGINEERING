import os
from os import path
import math
import pygame
import pickle


def pix2WorCoorRelativeToZero(coor):
	x = coor[0]
	y = coor[1]
	x -= SCREEN_WIDTH/2

	if y < SCREEN_HEIGHT/2:
		y = (y-SCREEN_HEIGHT/2)*-1
	elif y > SCREEN_HEIGHT/2:
		y = (y-SCREEN_HEIGHT/2)*-1
	else:
		y = 0

	return (x/PPM, y/PPM)



PPM = 10
FPS = 60
TIME_STEP = 1/FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768

Vertices = []
Boundries = []

VerticesConverted = []
BoundriesConverted = []

checkpointVertices = []
checkpoints = []

startPositions = []

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Map Boundry Editor")
clock = pygame.time.Clock()

map_path = path.join(path.dirname(__file__),'map.png')
instructions_path = path.join(path.dirname(__file__),'instructions.png')
gray_path = path.join(path.dirname(__file__),'gray.png')
gray_bar_path = path.join(path.dirname(__file__),'grayBar.png')
font_path = path.join(path.dirname(__file__),'game_over.ttf')
mapImg = pygame.image.load(map_path)
instructionsScreen = pygame.image.load(instructions_path).convert_alpha()
grayOverlay = pygame.image.load(gray_path).convert_alpha()
grayBar = pygame.image.load(gray_bar_path).convert_alpha()

pygame.font.init()
font = pygame.font.Font(font_path, 80)
def drawText(message, x, y):
        text = font.render(message, True, (255, 255, 0))
        textRect = text.get_rect()
        textRect = textRect.move(x, y)
        screen.blit(text, textRect)

mode = 0

canDraw = True

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				if mode == 1:
					if mode == 1 and canDraw:
						Vertices.append(event.pos)
						VerticesConverted.append(pix2WorCoorRelativeToZero(event.pos))
				if mode == 0:
					mode += 1
				if mode == 2:
					if len(checkpointVertices) < 2:
						checkpointVertices.append(event.pos)
				if mode == 3 and len(startPositions) < 2:
					startPositions.append(event.pos)
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				if mode == 1:
					if len(VerticesConverted) > 1:
						BoundriesConverted.append(VerticesConverted)
						Boundries.append(Vertices)
					VerticesConverted = []
					Vertices = []
					canDraw = True
				else:
					if len(checkpointVertices) == 2 and len(checkpoints) < 10:
						checkpoints.append(checkpointVertices)
						checkpointVertices = []
					else:
						checkpointVertices = []
			if event.key == pygame.K_RETURN:
				mode += 1
				if mode == 4:
					running = False
			if event.key == pygame.K_u:
				if len(Vertices) > 0:
					Vertices.pop()
					VerticesConverted.pop()

				if len(checkpointVertices) > 0:
					checkpointVertices.pop()

				if len(startPositions) > 0:
					startPositions.pop()


		
	screen.blit(mapImg, (0, 0))

	screen.blit(grayOverlay, (0, 0))

	if mode == 0:
		screen.blit(instructionsScreen, (0, 0))


	[pygame.draw.circle(screen, (255, 255, 0), pos, 5) for pos in Vertices]

	[pygame.draw.circle(screen, (255, 255, 0), pos, 5) for pos in checkpointVertices]

	if len(Vertices) > 1:
		pygame.draw.lines(screen, (255, 255, 0), False, Vertices, 2)
	
	if len(checkpointVertices) > 1:
		pygame.draw.lines(screen, (255, 255, 0), False, checkpointVertices, 2)
	


	mouseX, mouseY = pygame.mouse.get_pos()
	if len(Vertices) > 0:
		if mode == 1:
			dist = math.sqrt(math.pow(mouseX-Vertices[len(Vertices)-1][0], 2) + math.pow(mouseY-Vertices[len(Vertices)-1][1], 2))
			if dist > 100:
				pygame.draw.line(screen, (255, 0, 0), Vertices[len(Vertices)-1], (mouseX, mouseY), 2)
				canDraw = False
			else:
				pygame.draw.line(screen, (255, 255, 0), Vertices[len(Vertices)-1], (mouseX, mouseY), 2)
				canDraw = True

	if mode == 1 or mode == 2:
		pygame.draw.circle(screen, (255, 255, 0), (mouseX, mouseY), 5)
	elif mode == 3:
		pygame.draw.circle(screen, (255, 255, 0), (mouseX, mouseY), 15)


	if len(checkpointVertices) == 1:
		pygame.draw.line(screen, (255, 255, 0),checkpointVertices[len(checkpointVertices)-1], (mouseX, mouseY), 2)

	
	if len(Boundries) > 0:
		for verticesList in Boundries:
			[pygame.draw.circle(screen, (0, 0, 255), pos, 5) for pos in verticesList]
			if len(verticesList) > 1:
				pygame.draw.lines(screen, (0, 0, 255), False, verticesList, 2)
	
	if len(checkpoints) > 0:
		for verticesList in checkpoints:
			[pygame.draw.circle(screen, (255, 255, 255), pos, 5) for pos in verticesList]
			if len(verticesList) > 1:
				pygame.draw.lines(screen, (255, 255, 255), False, verticesList, 2)
	
	if len(startPositions) > 0:
		for startPosition in startPositions:
			pygame.draw.circle(screen, (0, 255, 0), startPosition, 15)
	
	if mode == 1:
		drawText("MODE: boundrys", SCREEN_WIDTH/2, SCREEN_HEIGHT-50)
	if mode == 2:
		drawText("MODE: checkpoints", SCREEN_WIDTH/2-150, SCREEN_HEIGHT-50)
		drawText("remaining: " + str(abs(len(checkpoints)-10)), SCREEN_WIDTH/2+150, SCREEN_HEIGHT-50)
	if mode == 3:
		drawText("MODE: start positions", SCREEN_WIDTH/2-150, SCREEN_HEIGHT-50)
		drawText("remaining: " + str(abs(len(startPositions)-2)), SCREEN_WIDTH/2+150, SCREEN_HEIGHT-50)
	if mode != 0:
		screen.blit(grayBar, (0, 0))


	pygame.display.update()
	clock.tick(FPS)

BoundriesConverted.append(checkpoints)
BoundriesConverted.append(startPositions)
pickle_out = open("map.data", "wb")
pickle.dump(BoundriesConverted, pickle_out)
pickle_out.close()
