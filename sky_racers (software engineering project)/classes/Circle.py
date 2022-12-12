"""
This class is for creating circles in the world.
"""

import pygame
import Box2D
from sky_racers.classes.useful_defs import *
from sky_racers.classes.config import *

class Circle:
	def __init__(self, x, y):
		bodyDef = Box2D.b2BodyDef()
		bodyDef.type = Box2D.b2_dynamicBody
		bodyDef.linearDamping = OBJECT_LINEARDAMPING
		bodyDef.angularDamping = OBJECT_ANGULARDAMPING

		x, y = pix2WorCoor(x, y)

		bodyDef.position.Set(x, y)

		self.body = WORLD.CreateBody(bodyDef)

		circle = Box2D.b2CircleShape(radius=pix2worScalar(20))

		fixtureDef = Box2D.b2FixtureDef()
		fixtureDef.shape = circle
		fixtureDef.density = OBJECT_DENSITY
		fixtureDef.friction = FRICTION
		fixtureDef.restitution = RESTITUTION

		self.body.CreateFixture(fixtureDef)
		self.body.linearDamping = 2.5
		self.body.angularDamping = 2.5


	def display(self, showHitBox):
		if not showHitBox:
			pygame.draw.circle(SCREEN, (150, 255, 200), wor2pixCoor(self.body.position.x, self.body.position.y), int(wor2pixScalar(self.body.fixtures[0].shape.radius)))
		if showHitBox:
			pygame.draw.circle(SCREEN, (0, 255, 0), wor2pixCoor(self.body.position.x, self.body.position.y), int(wor2pixScalar(self.body.fixtures[0].shape.radius)), 2)
