"""
This class deals with collisions and the logic for seperating and respondning to different kinds of collisions.
"""
from sky_racers.classes.config import *

class World_collision_listener(Box2D.b2ContactListener):
    def __init__(self):
        Box2D.b2ContactListener.__init__(self)
    def BeginContact(self, contact):
        fa = contact.fixtureA
        fb = contact.fixtureB

        if fa == None or fb == None:
            return
        if fa.userData == None or fb.userData == None:
            return
        
        if (fa.userData == "wall" or fb.userData == "wall"):
            if (fa.userData[1] == "car" or fb.userData[1] == "car"):
                if fa.userData[1] == "car":
                    fa.userData[0].colliding_with_wall = True
                elif fb.userData[1] == "car":
                    fb.userData[0].colliding_with_wall = True

        
        if (fa.userData[1] == "car" and fb.userData[1] == "car"):
            fa.userData[0].colliding_with_car = True
            fb.userData[0].colliding_with_car = True

    def EndContact(self, contact):
        fa = contact.fixtureA
        fb = contact.fixtureB

        if fa == None or fb == None:
            return
        if fa.userData == None or fb.userData == None:
            return

        if (fa.userData == "wall" or fb.userData == "wall"):
            if (fa.userData[1] == "car" or fb.userData[1] == "car"):
                if fa.userData[1] == "car":
                    fa.userData[0].colliding_with_wall = False
                elif fb.userData[1] == "car":
                    fb.userData[0].colliding_with_wall = False

        if (fa.userData[1] == "car" and fb.userData[1] == "car"):
            fa.userData[0].colliding_with_car = False
            fb.userData[0].colliding_with_car = False

    def PreSolve(self, contact, oldManifold):
        pass
    def PostSolve(self, contact, impulse):
        pass
