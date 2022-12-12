"""
This is the class for creating and interacting with cars.
"""
import math
import time
from sky_racers.classes.useful_defs import *
from sky_racers.classes.config import *
from sky_racers.classes.GameMap import GAME_MAP

class Car:
	def __init__(self, x, y, img, crashImg):
		self._currentCheckpoint = 1
		self._xPos, self._yPos = x, y
		self._prev_xPos, self._prev_yPos = self._xPos, self._yPos
		self.crashFrame = 0

		self.crashed = False



		self._carImg = img
		self._crashImg = crashImg
		x, y = pix2WorCoor(x, y)
		bodyDef = Box2D.b2BodyDef()
		bodyDef.type = Box2D.b2_dynamicBody
		bodyDef.linearDamping = CAR_LINEARDAMPING
		bodyDef.angularDamping = CAR_ANGULARDAMPING
		bodyDef.position.Set(x, y)

		self._body = WORLD.CreateBody(bodyDef)



		fixtureDef = Box2D.b2FixtureDef()
		fixtureDef.shape = Box2D.b2PolygonShape(vertices=[(1.4, 2.7), (0, 3.3), (-1.4, 2.7), (-1.4, -2.7), (0, -3.3), (1.4, -2.7)])
		fixtureDef.density = CAR_DENSITY
		fixtureDef.friction = FRICTION
		fixtureDef.restitution = RESTITUTION

		self._body.CreateFixture(fixtureDef).userData = [self, "car"]
		self._otherPoint = (self._xPos+70*math.cos(-self._body.angle-math.radians(90)), self._yPos+70*math.sin(-self._body.angle-math.radians(90)))
		self._closestWallMidpoint = self._UpdateClosestWallMidpoint()
		self._currentCheckpointMidpoint = self._UpdateCurrentCheckpointMidpoint()
		self._total_time = 0

		self.finished = False
		self.current_lap = 1
		self.laptimes = ["-", "-", "-", "-"]
		self._current_lap_time = 0
		self.colliding_with_wall = False
		self.colliding_with_car = False
		self.dist_to_wall
		self.angle_to_wall
		self.dist_to_checkpoint
		self.angle_to_checkpoint
		self.global_angle = 360 -( math.degrees(self._body.angle)%360)
		self.startRace = False

	
	def _update(self):
		self.global_angle = 360 -( math.degrees(self._body.angle)%360)
		self._prev_xPos, self._prev_yPos = self._xPos, self._yPos
		self._xPos, self._yPos = wor2pixCoor(self._body.position.x, self._body.position.y)
		self._otherPoint = (self._xPos+self.dist_to_checkpoint*math.cos(-self._body.angle-math.radians(90)), self._yPos+self.dist_to_checkpoint*math.sin(-self._body.angle-math.radians(90)))
		self._UpdateClosestWallMidpoint()
		self._UpdateCurrentCheckpointMidpoint()
		self._UpdateCurrentCheckpoint()




	def display(self, showHitBox):
		self._update()
		if showHitBox:
			for fixture in self._body.fixtures:
				carVertices = [self._body.transform*vertex*PPM for vertex in fixture.shape.vertices]
				carVertices = [(round(int(vertex[0])), round(int(SCREEN_HEIGHT-vertex[1]))) for vertex in carVertices]
				pygame.draw.lines(SCREEN, (255, 0, 0), True, carVertices, 2)

			pygame.draw.line(SCREEN, (255, 255, 255), self._otherPoint, (self._xPos, self._yPos), 2)
			pygame.draw.line(SCREEN, (0, 0, 255), self._closestWallMidpoint, (self._xPos, self._yPos), 2)
			pygame.draw.line(SCREEN, (0, 255, 0), self._currentCheckpointMidpoint, (self._xPos, self._yPos), 2)

		if not showHitBox:
			screenX, screenY = wor2pixCoor(self._body.position.x, self._body.position.y)
			screenX -= self._carImg.get_width()/2
			screenY -= self._carImg.get_height()/2
			blitRotateCenter(SCREEN, self._carImg, (screenX, screenY), self._body.angle*(180/3.141592653589793))
			if (self.colliding_with_car or self.colliding_with_wall):
				self.crashed = True

			if self.crashed and self.crashFrame <= 15:	
				blitRotateCenter(SCREEN, self._crashImg, (screenX, screenY), self._body.angle*(180/3.141592653589793))
				self.crashFrame += 1
			else:
				self.crashed = False
				self.crashFrame = 0

		


	def turnRight(self):
		self._body.ApplyTorque(-CAR_TURNFORCE, True)


	def turnLeft(self):
		self._body.ApplyTorque(CAR_TURNFORCE, True)


	def accelerateFoward(self):
		pVec = pygame.math.Vector2(0, CAR_ACCFORCE)
		pVec = pVec.rotate(self._body.angle*(180/3.1415926535))
		force = Box2D.b2Vec2(pVec.x, pVec.y)
		self._body.ApplyForceToCenter(force, True)


	def accelerateBackward(self):
		pVec = pygame.math.Vector2(0, -CAR_ACCFORCE)
		pVec = pVec.rotate(self._body.angle*(180/3.1415926535))
		force = Box2D.b2Vec2(pVec.x, pVec.y)
		self._body.ApplyForceToCenter(force, True)


	def teleport_to(self, x, y):
		pos = Box2D.b2Vec2(pix2WorCoor(x, y))
		self._body.transform = (pos, 0)

	
	def _UpdateClosestWallMidpoint(self):
		closestMidpoint = (round((GAME_MAP.wallLines[0][0][0]+GAME_MAP.wallLines[0][1][0])/2), round((GAME_MAP.wallLines[0][0][1]+GAME_MAP.wallLines[0][1][1])/2))
		
		for i in range(1, len(GAME_MAP.wallLines)-1):
			currentMidpoint = GetMidpoint(GAME_MAP.wallLines[i][0], GAME_MAP.wallLines[i][1])
			distToClosest = GetDist((self._xPos, self._yPos), closestMidpoint)
			distToCurrent = GetDist((self._xPos, self._yPos), currentMidpoint)
			if distToCurrent < distToClosest:
				closestMidpoint = currentMidpoint

		self._closestWallMidpoint = closestMidpoint
		self.dist_to_wall = GetDist((self._xPos, self._yPos), self._closestWallMidpoint)
		self.angle_to_wall = round(get_angle_difference(self._closestWallMidpoint, (self._xPos, self._yPos), self._otherPoint))

	
	def _UpdateCurrentCheckpointMidpoint(self):
		self._currentCheckpointMidpoint = GetMidpoint(GAME_MAP.checkpointLines[self._currentCheckpoint][0], GAME_MAP.checkpointLines[self._currentCheckpoint][1])
		self.dist_to_checkpoint = GetDist((self._xPos, self._yPos), self._currentCheckpointMidpoint)
		self.angle_to_checkpoint = round(get_angle_difference(self._currentCheckpointMidpoint, (self._xPos, self._yPos), self._otherPoint))
		
	
	def _UpdateCurrentCheckpoint(self):
		checkpointLine = GAME_MAP.checkpointLines[self._currentCheckpoint]
		carPosLine = [(self._prev_xPos, self._prev_yPos), (self._xPos, self._yPos)]

		if self.startRace:
			self._current_lap_time = time.time()
			self.startRace = False

		if not self.finished:
			self.laptimes[self.current_lap-1] = str(round(time.time()-self._current_lap_time, 2))
		
		if carPosLine[0] != carPosLine[1]:
			if self._currentCheckpoint < len(GAME_MAP.checkpointLines)-1:
				if doIntersect(checkpointLine[0], checkpointLine[1], carPosLine[0], carPosLine[1]):
					self._currentCheckpoint += 1
					if self._currentCheckpoint == 1:
						if self.current_lap < 4:
							self.current_lap += 1
							if self.current_lap == 4:
								self.finished = True
								self._total_time += time.time()-self._current_lap_time
								self.laptimes[3] = str(round(self._total_time, 2))
							else:
								self._total_time += time.time()-self._current_lap_time
								self._current_lap_time = time.time()

			else:
				if doIntersect(checkpointLine[0], checkpointLine[1], carPosLine[0], carPosLine[1]):
					self._currentCheckpoint = 0


