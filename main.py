import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

import sys
sys.path.append('..')
from OpMat import OpMat
from Carro import Carro

opera = OpMat()
#r1 = Triangulo(opera)
#t2 = Triangulo(opera)

pygame.init()

screen_width = 900
screen_height = 600

#Variables para dibujar los ejes del sistema
X_MIN=-450
X_MAX=450
Y_MIN=-300
Y_MAX=300

#variable global control
carros = []
ncarros = 5

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    glLineWidth(1.0)

def init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: ejes 3D")
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-450,450,-300,300)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0,0,0,0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    
def InitRobots():
    for i in range(ncarros):
        carros.append(Carro(opera,[1.0,1.0,1.0], 5, screen_width, screen_height))

def display():
    for car in carros:
        car.render()
    
# main program
init()
InitRobots()
opera.loadId()

done = False
while not done:
    keys = pygame.key.get_pressed()
    '''if keys[pygame.K_LEFT]:
        r1.setTurnLR('L')
    if keys[pygame.K_RIGHT]:
        r1.setTurnLR('R')
    if keys[pygame.K_UP]:
        r1.up()
    if keys[pygame.K_DOWN]:
        r1.down()'''
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    glClear(GL_COLOR_BUFFER_BIT)
    Axis()
    display()
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()