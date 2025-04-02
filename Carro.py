#Autor: Ivan Olmos Pineda

import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import os
import random
import math
import numpy as np

class Carro:
    #dist = distancia en px del (0, 0) absoluto a la posicion del triangulo
    #color = color del objeto en formato rgb
    #esc = escala que se le va a asignar al objeto
    def __init__(self, op, color, esc, width, height, grafo, pos_nodo):
        #Se inicializa las coordenadas de los vertices del objeto unitario
        self.points = np.array([[-4.0,-2.0,1.0], [4.0,-2.0,1.0], [4.0,2.0,1.0], [-4.0,2.0,1.0], 
                                [-4.0,-4.0,1.0], [-1.0,-4.0,1.0], [-1.0,-3.0,1.0], [-4.0,-3.0,1.0],
                                [0.0, -4.0, 1.0], [3.0,-4.0,1.0], [3.0,-3.0,1.0], [0.0,-3.0,1.0],
                                [-4.0,3.0,1.0], [-1.0,3.0,1.0], [-1.0,4.0,1.0], [-4.0,4.0,1.0],
                                [0.0,3.0,1.0], [3.0,3.0,1.0], [3.0,4.0,1.0], [0.0,4.0,1.0]
                                ])
        self.opera = op
        self.color = color
        self.esc = np.array([esc, esc])
        self.pos = pos_nodo
        self.dir = np.array([1.0, 0.0])
        self.width = width
        self.height = height
        self.theta = 0.0
        self.deltatheta = 0.0
        #self.turn_LR = 0 #0 left, 1 right
        self.delta_esc = np.array([0.0, 0.0])
        self.countdeg = 0
        self.flag = False
        self.grafo = grafo
        
        
    def update(self):
        if self.countdeg > 0:
            self.theta += 1
            self.dir[0] = np.cos(math.radians(self.theta))
            self.dir[1] = np.sin(math.radians(self.theta))
            self.countdeg -= 1
        elif self.countdeg < 0:
            self.theta -= 1
            self.countdeg += 1
            self.dir[0] = np.cos(math.radians(self.theta))
            self.dir[1] = np.sin(math.radians(self.theta))
        elif self.countdeg == 0:
            random.seed(os.urandom(128))
            value = random.randint(1,100)
            if self.flag:
                self.up()
            self.flag = False
            if (self.pos[0] + (5*self.esc[1]) == self.width/2 or self.pos[1] + (5*self.esc[1]) == self.height/2 
            or self.pos[0] - (5*self.esc[1]) == -self.width/2 or self.pos[1] - (5*self.esc[1]) == -self.height/2):
                self.countdeg = 180
                self.flag = True
            elif value == 49:
                self.setTurnLR('L')
            elif value == 50:
                self.setTurnLR('R')
            else:
                self.up()
    
    def setColor(self, r, g, b):
        self.color[0] = r
        self.color[1] = g
        self.color[2] = b
    
    def setpos(self, pos):
        self.pos[0] = pos[0]
        self.pos[1] = pos[1]
    
    def setDeltaDir(self, dir):
        self.dir[0] = dir[0]
        self.dir[1] = dir[1]
    
    def setDeg(self, theta):
        self.theta = theta
    
    def setDeltaDeg(self, deltatheta):
        self.deltatheta = deltatheta
    
    def setScale(self, esc):
        self.esc[0] = esc[0]
        self.esc[1] = esc[1]
        
    def setDeltaScale(self, delta_esc):
        self.delta_esc[0] = delta_esc[0]
        self.delta_esc[1] = delta_esc[1]
    
    def setTurnLR(self, LR):
        if self.countdeg == 0:
            if LR == 'L':
                self.countdeg = 90
            else:
                self.countdeg = -90
            
    def render(self): #se recibe estado e0
        self.opera.push() #se respalda
        self.opera.translate(self.pos[0], self.pos[1])
        if self.theta != 0:
            self.opera.rotate(self.theta)
        self.opera.scale(self.esc[0], self.esc[1]) #e3
        pointsR = self.points.copy()
        self.opera.mult_Points(pointsR)
        glColor3fv(self.color)
        glBegin(GL_QUADS)
        glVertex2f(pointsR[0][0],pointsR[0][1])
        glVertex2f(pointsR[1][0],pointsR[1][1])
        glVertex2f(pointsR[2][0],pointsR[2][1])
        glVertex2f(pointsR[3][0], pointsR[3][1])
        glEnd()
        glBegin(GL_QUADS)
        glVertex2f(pointsR[4][0],pointsR[4][1])
        glVertex2f(pointsR[5][0],pointsR[5][1])
        glVertex2f(pointsR[6][0],pointsR[6][1])
        glVertex2f(pointsR[7][0], pointsR[7][1])
        glEnd()
        glBegin(GL_QUADS)
        glVertex2f(pointsR[8][0],pointsR[8][1])
        glVertex2f(pointsR[9][0],pointsR[9][1])
        glVertex2f(pointsR[10][0],pointsR[10][1])
        glVertex2f(pointsR[11][0], pointsR[11][1])
        glEnd()
        glBegin(GL_QUADS)
        glVertex2f(pointsR[12][0],pointsR[12][1])
        glVertex2f(pointsR[13][0],pointsR[13][1])
        glVertex2f(pointsR[14][0],pointsR[14][1])
        glVertex2f(pointsR[15][0], pointsR[15][1])
        glEnd()
        glBegin(GL_QUADS)
        glVertex2f(pointsR[16][0],pointsR[16][1])
        glVertex2f(pointsR[17][0],pointsR[17][1])
        glVertex2f(pointsR[18][0],pointsR[18][1])
        glVertex2f(pointsR[19][0], pointsR[19][1])
        glEnd()
        self.opera.pop()
        self.update()
    
    def up(self):
        if self.countdeg == 0:
            self.pos[0] += self.dir[0]
            self.pos[1] += self.dir[1]
    
    def down(self):
        if self.countdeg == 0:
            self.pos[0] -= self.dir[0]
            self.pos[1] -= self.dir[1]