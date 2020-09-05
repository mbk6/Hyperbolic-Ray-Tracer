# Basic 2D raymarcher tool implemented in pygame
# Created by Michael Korenchan


import pygame

import pygame
import numpy as np
from math import sin, cos, pi
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
SPEED = 100


maxreflections = 1





class Circle():
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius


class Sphere():
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius

def length(vector):
    return np.linalg.norm(vector)

def signedDistToCircle(point, circle):
    return length(circle.pos - point) - circle.radius

def normalized(vector):
    return vector * (1 / np.linalg.norm(vector))

def distToScene(point, circles):
    distToScene = float('inf')
    for circle in circles:
        distToScene = min(distToScene, signedDistToCircle(point, circle))
    
    return distToScene

def inBounds(point):
    return 0 < point[0] < RESOLUTION[0] and 0 < point[1] < RESOLUTION[1]



cam3_pos = np.array([0.0,-1.0,0.0])
cam3_dir = np.array([0.0,1.0,0.0])

cam2pos = np.array([100.0,10.0])
cam2dir = normalized(np.array([0.5, 0.5]))



objects = [
    Circle(np.array([200,200]), 20),
    Circle(np.array([300,550]), 50),
    Circle(np.array([700,450]), 100)
]





clock = pygame.time.Clock()
win = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Ray Marcher")





run = True
while run:

    dt = clock.tick() / 1000

    keys = pygame.key.get_pressed()

    if(keys[pygame.K_UP]):
        c = cos(-SPEED * dt * 0.01)
        s = sin(-SPEED * dt * 0.01)
        tmp = cam2dir[0]
        cam2dir[0] = c * cam2dir[0] - s * cam2dir[1]
        cam2dir[1] = s * tmp + c * cam2dir[1]
    if(keys[pygame.K_DOWN]):
        c = cos(SPEED * dt * 0.01)
        s = sin(SPEED * dt * 0.01)
        tmp = cam2dir[0]
        cam2dir[0] = c * cam2dir[0] - s * cam2dir[1]
        cam2dir[1] = s * tmp + c * cam2dir[1]
    if(keys[pygame.K_w]):
        cam2pos[1] -= dt * SPEED
    if(keys[pygame.K_s]):
        cam2pos[1] += dt * SPEED
    if(keys[pygame.K_a]):
        cam2pos[0] -= dt * SPEED
    if(keys[pygame.K_d]):
        cam2pos[0] += dt * SPEED

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

 


    
    win.fill((0, 0, 0))

    pygame.draw.circle(win, WHITE, cam2pos.astype('int'), 5, 5)
    pygame.draw.line(win, WHITE, cam2pos.astype('int'), (cam2pos + 20 * cam2dir).astype('int'), 1)
    

    for circle in objects:
        pygame.draw.circle(win, BLUE, circle.pos, circle.radius, 2)


    currentPoint = np.array(cam2pos)
    stepDist = float('inf')

    while(inBounds(currentPoint) and stepDist >= 5):
        stepDist = distToScene(currentPoint, objects)
        oldPoint = np.array(currentPoint)
        currentPoint += cam2dir * stepDist

        pygame.draw.circle(win, WHITE, oldPoint.astype('int'), max(1, int(abs(stepDist))), 1)
        pygame.draw.line(win, WHITE, oldPoint.astype('int'), currentPoint.astype('int'), 1)
        pygame.draw.circle(win, GREEN, currentPoint.astype('int'), 5, 5)

        

    
    pygame.display.update()

pygame.quit()











