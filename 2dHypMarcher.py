# Basic 2D hyperbolic raymarcher tool implemented in pygame
# Created by Michael Korenchan

import pygame

import pygame
import numpy as np
from math import sin, cos, pi, atan2, pi, exp, sqrt, sinh, acosh
import random

pygame.init()

TRACE = True

RESOLUTION = (1000, 800)
CENTER = np.array([RESOLUTION[0] // 2, RESOLUTION[1] // 2])
WHITE = (255,255,255)
GREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
SCALE = 800
MOVE_SPEED = 1
TURN_SPEED = 100

maxreflections = 1


def rayFrom(pos, dir, t):
    theta = atan2(dir[1], dir[0])
    c = cos(theta / 2 + pi / 4)
    d = sin(theta / 2 + pi / 4)
    b = (-pos[1]*c*c*c - pos[1]*d*d*c + d*pos[0]*c*c + pos[0]*d*d*d) / (c*c + d*d)
    a = (pos[0]*c*c + pos[0]*d*d - b*d) / c
    return np.array(((b*d+a*c*exp(2*t)) / (c*c*exp(2*t) + d*d), (d*a*exp(t) - b*c*exp(t)) / (c*c*exp(2*t) + d*d)))

#This returns unit tangent of the rayFrom curve
def dirFrom(pos, dir, t):
    theta = atan2(dir[1], dir[0])
    c = cos(theta / 2 + pi / 4)
    d = sin(theta / 2 + pi / 4)
    b = (-pos[1]*c*c*c - pos[1]*d*d*c + d*pos[0]*c*c + pos[0]*d*d*d) / (c*c + d*d)
    a = (pos[0]*c*c + pos[0]*d*d - b*d) / c
    x = (-2*b*exp(2*t)*d*c*c + 2*a*exp(2*t)*d*d*c) / (exp(2*t)*c*c+d*d)**2
    y = (b*exp(3*t)*c*c*c - a*exp(3*t)*d*c*c - b*exp(t)*d*d*c + a*exp(t)*d*d*d) / (exp(2*t)*c*c+d*d)**2
    return normalized(np.array([x,y]))


class HCircle():
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius
        self.eradius = pos[1]*sinh(radius)
        self.epos = np.array([pos[0], self.eradius + pos[1]*exp(-radius)])

def distance(a, b):
    return acosh(1 + ((b[0] - a[0])**2 + (b[1] - a[1])**2) / (2*a[1]*b[1]))

def signedDistToHCircle(point, hcircle):
    return distance(hcircle.pos, point) - hcircle.radius

def normalized(vector):
    return vector * (1 / np.linalg.norm(vector))

def distToScene(point, objects):
    distToScene = float('inf')
    for HCircle in objects:
        distToScene = min(distToScene, signedDistToHCircle(point, HCircle))
    
    return distToScene

def inBounds(point):
    return 0 < point[0] < RESOLUTION[0] and 5 < point[1] < RESOLUTION[1]



cam3_pos = np.array([0.0,-1.0,0.0])
cam3_dir = np.array([0.0,1.0,0.0])

cam2pos = np.array([100.0,500.0])
cam2dir = normalized(np.array([0.5, 0.5]))



objects = [
    HCircle(np.array([600,600]), 0.1),
    HCircle(np.array([700,200]), 0.5),
    HCircle(np.array([200,100]), 0.8)
]





clock = pygame.time.Clock()
win = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Ray Marcher")





run = True
while run:

    dt = clock.tick() / 1000

    keys = pygame.key.get_pressed()

    if(keys[pygame.K_LEFT]):
        c = cos(-TURN_SPEED * dt * 0.01)
        s = sin(-TURN_SPEED * dt * 0.01)
        tmp = cam2dir[0]
        cam2dir[0] = c * cam2dir[0] - s * cam2dir[1]
        cam2dir[1] = s * tmp + c * cam2dir[1]
    if(keys[pygame.K_RIGHT]):
        c = cos(TURN_SPEED * dt * 0.01)
        s = sin(TURN_SPEED * dt * 0.01)
        tmp = cam2dir[0]
        cam2dir[0] = c * cam2dir[0] - s * cam2dir[1]
        cam2dir[1] = s * tmp + c * cam2dir[1]
    if(keys[pygame.K_UP]):
        cam2pos = rayFrom(cam2pos, cam2dir, dt * MOVE_SPEED)
        cam2dir = dirFrom(cam2pos, cam2dir, dt * MOVE_SPEED)
    if(keys[pygame.K_DOWN]):
        cam2pos = rayFrom(cam2pos, -cam2dir, dt * MOVE_SPEED)
        cam2dir = -dirFrom(cam2pos, -cam2dir, dt * MOVE_SPEED)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

 


    
    win.fill((0, 0, 0))

    pygame.draw.circle(win, WHITE, cam2pos.astype('int'), 5, 5)
    pygame.draw.line(win, WHITE, cam2pos.astype('int'), (cam2pos + 20 * cam2dir).astype('int'), 1)
    
    #c = HCircle(cam2pos, 1)
    #pygame.draw.circle(win, WHITE, c.epos.astype('int'), c.eradius.astype('int'), max(1, int(c.eradius)))
    pygame.draw.circle(win, WHITE, cam2pos.astype('int'), 5,5)

    for hcircle in objects:
        pygame.draw.circle(win, BLUE, hcircle.epos.astype('int'), int(hcircle.eradius), 2)
        pygame.draw.circle(win, BLUE, hcircle.pos.astype('int'), 2, 2)


    currentPoint = np.array(cam2pos)
    stepDist = float('inf')
    t = 0

    i = 0

    while(inBounds(currentPoint) and stepDist >= 0.01):
        oldPoint = np.array(currentPoint)
        stepDist = distToScene(currentPoint, objects)
        t += stepDist
        currentPoint = rayFrom(cam2pos, cam2dir, t)
        c = HCircle(oldPoint, stepDist)
        pygame.draw.circle(win, GREEN, c.pos.astype('int'), 5, 5)
        pygame.draw.circle(win, WHITE, c.epos.astype('int'), max(1, c.eradius.astype('int')), 1)


        i += 1

        if(i > 10):
            break

        # for i in np.linspace(0, t, 10):
        #     pygame.draw.circle(win, WHITE, rayFrom(cam2pos, cam2dir, i).astype('int'), 4, 4)
        


        #pygame.draw.HCircle(win, WHITE, rayFrom(cam2pos, cam2dir, t).astype('int'), 
        
        #pygame.draw.line(win, WHITE, oldPoint.astype('int'), currentPoint.astype('int'), 1)
        #pygame.draw.HCircle(win, WHITE, currentPoint.astype('int'), 5, 5)

        

    
    pygame.display.update()

pygame.quit()











