#Autor: Ivan Olmos Pineda

import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

#import random
import math
import numpy as np

class OpMat:
    def __init__(self):
        #Se inicializa las coordenadas de los vertices del cubo
        self.T = np.identity(3)
        self.R = np.identity(3)
        self.E = np.identity(3) #Escalado
        self.A = np.identity(3) #Modelado
        self.stack = []

    def translate(self, tx, ty):
        self.T = np.identity(3)
        self.T[0][2] = tx
        self.T[1][2] = ty
        self.A = self.A @ self.T

        
    def scale(self, sx, sy):
        self.E = np.identity(3)
        self.E[0][0] = sx
        self.E[1][1] = sy
        self.A = self.A @ self.E

        
    def rotate(self, deg):
        self.R = np.identity(3)
        temp = math.radians(deg)
        self.R[0][0] = math.cos(temp)
        self.R[1][0] = math.sin(temp)
        self.R[0][1] = -math.sin(temp)
        self.R[1][1] = math.cos(temp)
        self.A = self.A @ self.R

                
    # funcion que realiza la operacion A * p -> p'
    # se asume que points en un array de puntos, donde cada renglon
    # es una coordenada homogenea 2D de puntos [x, y, 1]
    def mult_Points(self, points):
        pointsR = (self.A @ points.T).T
        for i in range (0, pointsR.shape[0]):
            for j in range(0, pointsR.shape[1]):
                points[i][j] = int(pointsR[i][j])
    
    def loadId(self):
        self.A = np.identity(3)

    def push(self):
        self.stack.append(self.A.copy())
    
    def pop(self):
        if(self.stack):
            self.A = self.stack.pop()