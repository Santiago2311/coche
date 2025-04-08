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
from Grafo import *

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
#ncarros = 5

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
        
def InitGrafo():
    graph = Grafo(screen_width, screen_height)
    graph.nuevo_nodo(0, 0, 5) #0
    graph.nuevo_nodo(-350, 250, 2) #1
    graph.nuevo_nodo(-150, 250, 3) #2
    graph.nuevo_nodo(0, 250, 5) #3
    graph.nuevo_nodo(150, 250, 3) #4
    graph.nuevo_nodo(350, 250, 3) #5
    graph.nuevo_nodo(-350, 0, 2) #6
    graph.nuevo_nodo(-150, 0, 7) #7
    graph.nuevo_nodo(150, 0, 7) #8
    graph.nuevo_nodo(350, 0, 7) #9
    graph.nuevo_nodo(-350, -250, 1) #10
    graph.nuevo_nodo(-150, -250, 6) #11
    graph.nuevo_nodo(0, -250, 1) #12
    graph.nuevo_nodo(150, -250, 6) #13
    graph.nuevo_nodo(350, -250, 0) #14
    graph.nuevo_nodo(-150, 150, 6) #15
    graph.nuevo_nodo(-350, 150, 4) #16
    graph.nuevo_nodo(0, 150, 2) #17
    graph.nuevo_nodo(250, 250, 5) #18
    graph.nuevo_nodo(250, 0, 3) #19
    graph.nuevo_nodo(0, -100, 2) #20
    graph.nuevo_nodo(150, -100, 7) #21
    graph.nuevo_nodo(400, 400, 0)
    graph.conectar_nodos(1, 16)
    graph.conectar_nodos(16, 6)
    graph.conectar_nodos(6, 10)
    graph.conectar_nodos(10, 11)
    graph.conectar_nodos(11, 12)
    graph.conectar_nodos(12, 13)
    graph.conectar_nodos(13, 14)
    graph.conectar_nodos(14, 9)
    graph.conectar_nodos(9, 5)
    graph.conectar_nodos(5, 18)
    graph.conectar_nodos(18, 4)
    graph.conectar_nodos(4, 3)
    graph.conectar_nodos(3, 2)
    graph.conectar_nodos(2, 1)
    graph.conectar_nodos(16, 15)
    graph.conectar_nodos(15, 17)
    graph.conectar_nodos(9, 19)
    graph.conectar_nodos(19, 8)
    graph.conectar_nodos(8, 0)
    graph.conectar_nodos(0, 7)
    graph.conectar_nodos(7, 6)
    graph.conectar_nodos(21, 20)
    graph.conectar_nodos(11, 7)
    graph.conectar_nodos(7, 15)
    graph.conectar_nodos(15, 2)
    graph.conectar_nodos(3, 17)
    graph.conectar_nodos(17, 0)
    graph.conectar_nodos(0, 20)
    graph.conectar_nodos(20, 12)
    graph.conectar_nodos(13, 21)
    graph.conectar_nodos(21, 8)
    graph.conectar_nodos(8, 4)
    graph.conectar_nodos(18, 19)
    return graph

def InitRobots(graph):
    #for i in range(ncarros):
    carros.append(Carro(opera,[1.0,0.0,0.0], 5, screen_width, screen_height, graph, graph.posicion(14)))
    carros.append(Carro(opera,[1.0,0.0,0.0], 5, screen_width, screen_height, graph, graph.posicion(5)))
    carros.append(Carro(opera,[1.0,0.0,0.0], 5, screen_width, screen_height, graph, graph.posicion(10)))
    carros.append(Carro(opera,[1.0,0.0,0.0], 5, screen_width, screen_height, graph, graph.posicion(8)))
    carros.append(Carro(opera,[1.0,0.0,0.0], 5, screen_width, screen_height, graph, graph.posicion(1)))
    carros.append(Carro(opera,[1.0,0.0,0.0], 5, screen_width, screen_height, graph, graph.posicion(18)))
    carros.append(Carro(opera,[1.0,0.0,0.0], 5, screen_width, screen_height, graph, graph.posicion(20)))
    carros.append(Carro(opera,[1.0,0.0,0.0], 5, screen_width, screen_height, graph, graph.posicion(12)))
    carros.append(Carro(opera,[1.0,0.0,0.0], 5, screen_width, screen_height, graph, graph.posicion(3)))
    carros.append(Carro(opera,[1.0,1.0,0.0], 5, screen_width, screen_height, graph, graph.posicion(0)))
    

def display():
    for c1 in carros:
        for c2 in carros:
            if c1 != c2:
                c1.detCol(c2)
                if c1.col == True:
                    break
    for car in carros:
        car.render()
    
# main program
init()
graph = InitGrafo()
InitRobots(graph)
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
    graph.render()
    display()
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()