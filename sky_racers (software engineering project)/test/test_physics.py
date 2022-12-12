from ..classes.useful_defs import *
from random import random

def test_get_midpoint(a, b):
    actual = GetMidpoint(a, b)
    expected = (a[0]+b[0])/2, (a[1]+b[1])/2
    expected = round(expected[0]), round(expected[1])
    return expected==actual

# tests a tin of points and compares the results of the function to a formula that also calculates the midpoint
def run_mid_test():
    print("Running midpoint test...")
    for count in range(0,250001):
        i = random()*10000
        j = random()*10000
        k = random()*10000
        l = random()*10000
        if not test_get_midpoint((i,j), (k,l)):
            return (False, i, j, k, l, count)
    return (True, 0, 0, 0, 0, count)

def test_get_distance(a,b):
    actual = GetDist(a,b)
    expected = pow(pow((a[0] - b[0]),2) + pow((a[1] - b[1]),2),.5) 
    return expected==actual


# tests a ton of points and compares the results of the function to a formula that also calculates the distance
def run_dist_test():
    print("Running distance test...")
    for count in range(0,250001):
        i = random()*10000
        j = random()*10000
        k = random()*10000
        l = random()*10000
        if not test_get_distance((i,j), (k,l)):
            return (False, i, j, k, l, count)
    return (True, 0, 0, 0, 0, count)


# fills a look up table where the index is the angle in degrees so comparing the indexes tells you what the angle difference really is and compares to the function output
def run_ang_test():
    print("Running angle test...")
    cos_lut = []
    sin_lut = []
    count = 0
    offsets = 0
    for x in range(0,50,10):
        for y in range(0,500,5):
            offsets += 1
            cos_lut.clear()
            sin_lut.clear()
            for i in range(0,360):
                cos_lut.append(250*math.cos(2*math.pi*i/360)+x)
                sin_lut.append(250*math.sin(2*math.pi*i/360)+y)
            for i in range(0,360,18):
                for j in range(0,350,14):
                    count += 1
                    expected = (360-(i-j))%360
                    actual = round(get_angle_difference((cos_lut[i], sin_lut[i]), (x,y), (cos_lut[j], sin_lut[j])))
                    if expected != actual:
                        return (False, cos_lut[i], sin_lut[i], cos_lut[j], sin_lut[j], count, offsets)

    return (True, 0, 0, 0, 0, count, offsets)

def run_intersect_test():
    print("Running line intersect test...")
    for count in range(0,250001):
        x1 = random()*10000
        x2 = random()*10000
        x3 = random()*10000
        x4 = random()*10000
        y1 = random()*10000
        y2 = random()*10000
        y3 = random()*10000
        y4 = random()*10000
        # if any points are the same
        if (x1 == x3 and y1 == y3) or (x2 == x3 and y2 == y3) or (x1 == x4 and y1 == y4) or (x2 == x3 and y2 == y3):
            expected = True
        else:
            denom = (x4-x3)*(y1-y2)-(x1-x2)*(y4-y3)
            # if colinear
            if denom == 0:
                slope = (y4-y3)/(x4-x3)
                yint1 = y2 - x2*slope
                yint2 = y4 - x4*slope
                # y intercept has to be the same and one of the points has to be within the other line segment 
                if (yint1 == yint2) and ((x3 >= x1 and x3 <= x2) or (x3 >= x2 and x3 <= x1) or (x4 >= x1 and x4 <= x2) or (x4 >= x2 and x4 <= x1)):
                    expected = True
                else:
                    expected = False
            # otherwise do linear algebra and verify there is an intersect solution within the segments
            else:
                ta = ((y3-y4)*(x1-x3)+(x4-x3)*(y1-y3))/denom
                tb = ((y1-y2)*(x1-x3)+(x2-x1)*(y1-y3))/denom
                if ta <= 1 and ta >= 0 and tb <=1 and tb >=0:
                    expected = True
                else:
                    expected = False
        actual = doIntersect((x1,y1),(x2,y2),(x3,y3),(x4,y4))
        if expected != actual:
            return (False,x1,y1,x2,y2,x3,y3,x4,y4,count)
    return (True,0,0,0,0,0,0,0,0,count)
                                        

result = run_mid_test()
if result[0]:
    print("Get Midpoint: Passed")
else:
    print("Get Midpoint: Failed at ({},{}),({},{})".format(result[1], result[2], result[3], result[4]))
print("{} random coordinates tested".format(result[5]))
print()

result = run_dist_test()
if result[0]:
    print("Get Distance: Passed")
else:
    print("Get Distance: Failed at ({},{}),({},{})".format(result[1], result[2], result[3], result[4]))
print("{} random coordinates tested".format(result[5]))
print()

result = run_intersect_test()
if result[0]:
    print("Line Intersect: Passed")
else:
    print("Line Intersect: Failed at ({},{}),({},{}),({},{}),({},{})".format(result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8]))
print("{} random line pairs tested".format(result[9]))
print()

result = run_ang_test()
if result[0]:
    print("Get Angle: Passed")
else:
    print("Get Angle: Failed at ({},{}),({},{})".format(result[1], result[2], result[3], result[4]))
print("{} coordinates tested at {} car locations".format(result[5], result[6]))
print()