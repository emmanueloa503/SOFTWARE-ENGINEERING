"""
This class is for creating boxes in the world.
"""

from sky_racers.classes.useful_defs import *
from sky_racers.classes.config import *

class Box:
	def __init__(self, x, y):
		bodyDef = Box2D.b2BodyDef()
		bodyDef.type = Box2D.b2_dynamicBody
		bodyDef.linearDamping = OBJECT_LINEARDAMPING
		bodyDef.angularDamping = OBJECT_ANGULARDAMPING

		x, y = pix2WorCoor(x, y)

		bodyDef.position.Set(x, y)


		self.body = WORLD.CreateBody(bodyDef)


		box = Box2D.b2PolygonShape()
		box.SetAsBox(pix2worScalar(20), pix2worScalar(20))


		fixtureDef = Box2D.b2FixtureDef()
		fixtureDef.shape = box
		fixtureDef.density = OBJECT_DENSITY
		fixtureDef.friction = FRICTION
		fixtureDef.restitution = RESTITUTION

		self.body.CreateFixture(fixtureDef).userData = "box"


	def display(self, showHitBox):
		for fixture in self.body.fixtures:
			polygonVertices = [self.body.transform*vertex*PPM for vertex in fixture.shape.vertices]
			polygonVertices = [(int(round(vertex[0])), int(round(SCREEN_HEIGHT-vertex[1]))) for vertex in polygonVertices]

		if showHitBox == True:
			pygame.draw.lines(SCREEN, (0, 255, 0), True, polygonVertices, 2)

		if showHitBox == False:
			pygame.draw.polygon(SCREEN, (200, 150, 255), polygonVertices)
