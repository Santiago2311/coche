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

class Human:
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
        self.grafo = grafo
        self.posdir = []
        #Colision
        self.radio = math.sqrt((4*esc)**2+(4*esc)**2)
        self.col = False
        self.move = ''
        self.flag = False
        
    def update(self):
        if not self.col:
            if self.countdeg == 0:
                for nodo_id, nodo in self.grafo.nodos.items():
                        if np.array_equal(self.pos, nodo.posicion()):
                            if nodo.tipo == 0:
                                self.posdir = [np.array([0.0, 1.0])]
                            elif nodo.tipo == 1:
                                self.posdir = [np.array([1.0, 0.0])]
                            elif nodo.tipo == 2:
                                self.posdir = [np.array([0.0, -1.0])]
                            elif nodo.tipo == 3:
                                self.posdir = [np.array([-1.0, 0.0])]
                            elif nodo.tipo == 4:
                                self.posdir = [np.array([1.0, 0.0]), np.array([0.0, -1.0])]
                            elif nodo.tipo == 5:
                                self.posdir = [np.array([-1.0, 0.0]), np.array([0.0, -1.0])]
                            elif nodo.tipo == 6:
                                self.posdir = [np.array([1.0, 0.0]), np.array([0.0, 1.0])]
                            elif nodo.tipo == 7:
                                self.posdir = [np.array([-1.0, 0.0]), np.array([0.0, 1.0])]
                            self.move = ''
                            if self.flag:
                                self.move = 'U'
                                self.flag = False
                            keys = pygame.key.get_pressed()
                            if keys[pygame.K_LEFT]:
                                self.move = 'L'
                            elif keys[pygame.K_RIGHT]:
                                self.move = 'R'
                            elif keys[pygame.K_UP]:
                                self.move = 'U'
                for dir in self.posdir:
                    if self.move == 'L' and np.allclose([np.cos(math.radians(self.theta+90)), np.sin(math.radians(self.theta+90))], dir):
                        self.setTurnLR('L')
                        self.move = 'U'
                        self.flag = True
                    elif self.move == 'R' and np.allclose([np.cos(math.radians(self.theta-90)), np.sin(math.radians(self.theta-90))], dir):
                        self.setTurnLR('R')
                        self.move = 'U'
                        self.flag = True
                    elif self.move == 'U' and np.allclose(self.dir, dir):
                        self.up()
                
            elif self.countdeg > 0:
                self.theta += 1
                self.dir[0] = np.cos(math.radians(self.theta))
                self.dir[1] = np.sin(math.radians(self.theta))
                self.countdeg -= 1
            elif self.countdeg < 0:
                self.theta -= 1
                self.countdeg += 1
                self.dir[0] = np.cos(math.radians(self.theta))
                self.dir[1] = np.sin(math.radians(self.theta))
    
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
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
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
        if self.countdeg == 0 and not self.col:
            self.pos[0] += self.dir[0]
            self.pos[1] += self.dir[1]
    
    def down(self):
        if self.countdeg == 0:
            self.pos[0] -= self.dir[0]
            self.pos[1] -= self.dir[1]
    
    def d_e(self, posicion, posicion2):
        x = posicion2[0] - posicion[0]
        y = posicion2[1] - posicion[1] 
        return math.sqrt((x**2)+(y**2))
    
    def detCol(self, carro):
        new_pos = self.pos + self.dir
        dist_centros = self.d_e(new_pos, carro.pos)
        if (self.radio + carro.radio >= dist_centros):
            self.col = True
        else:
            self.col = False