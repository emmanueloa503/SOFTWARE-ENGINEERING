"""
This class is for creating the game map with boundries.
"""
import os
import pickle
from sky_racers.classes.useful_defs import *
from sky_racers.classes.config import *


class GameMap:
	def __init__(self, x, y):
		os.chdir("sky_racers")
		os.chdir("assets")
		os.chdir("game")
		self.mapImg = pygame.image.load("map.png")
		x, y = pix2WorCoor(x, y)
		bodyDef = Box2D.b2BodyDef()
		bodyDef.type = Box2D.b2_staticBody
		bodyDef.position.Set(x, y)


		pickle_in = open("map.data", "rb")
		mapData = pickle.load(pickle_in)
		pickle_in.close()

		


		Boundries = list.copy(mapData)
		Boundries.pop()
		Boundries.pop()

		self.checkpointLines = mapData[len(mapData)-2]
		self.startPoints = mapData[len(mapData)-1]


		self.body = WORLD.CreateBody(bodyDef)

		for boundry in Boundries:
			Edges = []
			for i in range(len(boundry)-1):
				Edges.append(Box2D.b2EdgeShape(vertices=[boundry[i], boundry[i+1]]))

			fixtureDef = Box2D.b2FixtureDef()
			for edge in Edges:
				fixtureDef.shape = edge
				fixtureDef.friction = WALL_FRICTION
				fixtureDef.restitution = RESTITUTION
				self.body.CreateFixture(fixtureDef).userData = "wall"

		
		self.wallLines = []
		for fixture in self.body.fixtures:
			mapVertices = [self.body.transform*vertex*PPM for vertex in fixture.shape.vertices]
			mapVertices = [(round(int(vertex[0])), round(int(SCREEN_HEIGHT-vertex[1]))) for vertex in mapVertices]
			self.wallLines.append(mapVertices)


	def display(self, showHitbox):
		if not showHitbox:
			SCREEN.blit(self.mapImg, (0, 0))
		else:
			SCREEN.fill((0, 0, 0))
			for line in self.wallLines:
				pygame.draw.lines(SCREEN, (0, 0, 255), True, line, 2)
			for checkpoint in self.checkpointLines:
				pygame.draw.line(SCREEN, (0, 255, 0), checkpoint[0], checkpoint[1], 2)
				midpoint = (round((checkpoint[0][0]+checkpoint[1][0])/2), round((checkpoint[0][1]+checkpoint[1][1])/2))


GAME_MAP = GameMap(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
