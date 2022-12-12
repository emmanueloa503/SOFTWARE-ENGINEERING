"""
This is a module that contains functions that are used in various classes for the game
"""

import math
from sky_racers.classes.config import *


def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    surf.blit(rotated_image, new_rect.topleft)


def pix2worScalar(x):
	return x/PPM


def wor2pixScalar(x):
	return int(round(x*PPM))


def pix2WorCoor(x, y):
	return x/PPM, (-y+SCREEN_HEIGHT)/PPM


def drawSomething(x, y, img):
    SCREEN.blit(img, (x,y))


def wor2pixCoor(x, y):
	x *= PPM
	y *= PPM
	if y > SCREEN_HEIGHT/2:
		y -= (y-SCREEN_HEIGHT/2)*2
	elif y < SCREEN_HEIGHT/2:
		y += (SCREEN_HEIGHT/2-y)*2
	return int(round(x)), int(round(y))


def GetMidpoint(p1, p2):
	return (round((p1[0]+p2[0])/2), round((p1[1]+p2[1])/2))


def GetDist(p1, p2):
	return math.sqrt(math.pow(p2[0]-p1[0], 2) + math.pow(p2[1]-p1[1], 2))


# THE FOLLOWING THREE DEFS ARE BASED OFF THE CODE FROM "https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect"
def onSegment(p, q, r): 
    if ( (q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and 
           (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))): 
        return True
    return False
  

def orientation(p, q, r): 
    # to find the orientation of an ordered triplet (p,q,r) 
    # function returns the following values: 
    # 0 : Colinear points 
    # 1 : Clockwise points 
    # 2 : Counterclockwise 
      
    # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/  
    # for details of below formula.  
      
    val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1])) 
    if (val > 0): 
          
        # Clockwise orientation 
        return 1
    elif (val < 0): 
          
        # Counterclockwise orientation 
        return 2
    else: 
          
        # Colinear orientation 
        return 0
  
# The main function that returns true if  
# the line segment 'p1q1' and 'p2q2' intersect. 
def doIntersect(p1,q1,p2,q2): 
      
    # Find the 4 orientations required for  
    # the general and special cases 
    o1 = orientation(p1, q1, p2) 
    o2 = orientation(p1, q1, q2) 
    o3 = orientation(p2, q2, p1) 
    o4 = orientation(p2, q2, q1) 
  
    # General case 
    if ((o1 != o2) and (o3 != o4)): 
        return True
  
    # Special Cases 
  
    # p1 , q1 and p2 are colinear and p2 lies on segment p1q1 
    if ((o1 == 0) and onSegment(p1, p2, q1)): 
        return True
  
    # p1 , q1 and q2 are colinear and q2 lies on segment p1q1 
    if ((o2 == 0) and onSegment(p1, q2, q1)): 
        return True
  
    # p2 , q2 and p1 are colinear and p1 lies on segment p2q2 
    if ((o3 == 0) and onSegment(p2, p1, q2)): 
        return True
  
    # p2 , q2 and q1 are colinear and q1 lies on segment p2q2 
    if ((o4 == 0) and onSegment(p2, q1, q2)): 
        return True
  
    # If none of the cases 
    return False

'''

A is checkpoint
B is car pos
C is car direction coord

arcos (A-B dp C-B)/magA-B magC-B

if C is higher and left of A then CW
if C is higher and right of A then CCW
if C is lower and left of A then CCW
if C is lower and right of A then CW 
'''

# This function returns the angle between the checkpoint and the direction the car is facing
# using the returned angle the user can determine which way the car needs to turn

# if the returned angle is <180 the car should turn counterclockwise
# if the returned angle is >180 the car should turn clockwise
def get_angle_difference(checkpoint, car, direction):
    if checkpoint[0] - car[0] == 0:
        if checkpoint[1] - car[1] > 0:
            cp_to_car = math.pi/2
        else:
            cp_to_car = -1*math.pi/2
    else:
        cp_to_car = math.degrees(math.atan((-1*checkpoint[1] + car[1])/(checkpoint[0] - car[0])))

    if (checkpoint[0] - car[0]) < 0:
        cp_to_car = 180 + cp_to_car
    if cp_to_car < 0:
        cp_to_car += 360 

    if direction[0] - car[0] == 0:
        if direction[1] - car[1] > 0:
            dir_to_car = math.pi/2
        else:
            dir_to_car = -1*math.pi/2
    else:
        dir_to_car = math.degrees(math.atan((-1*direction[1] + car[1])/(direction[0] - car[0])))

    if (direction[0] - car[0]) < 0:
        dir_to_car = 180 + dir_to_car
    if dir_to_car < 0:
        dir_to_car += 360

    ang_diff = cp_to_car - dir_to_car

    if ang_diff < 0:
        ang_diff += 360
    if ang_diff >= 360:
        ang_diff -= 360

    return ang_diff
