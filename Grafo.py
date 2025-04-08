import numpy as np
import random
import math

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Nodo:
    def __init__(self, x, y, id, tipo):
        self.x = x
        self.y = y
        self.id = id
        self.tipo = tipo
        self.aristas = []
    
    def nueva_arista(self, id):
        if id not in self.aristas:
            self.aristas.append(id)
    
    def posicion(self):
        return np.array([self.x, self.y])

class Grafo:
    def __init__(self, width, height):
        self.nodos = {}
        self.width = width
        self.height = height
    
    def nuevo_nodo(self, x, y, tipo):
        id = len(self.nodos)
        self.nodos[id] = Nodo(x, y, id, tipo)
    
    def conectar_nodos(self, nodo1_id, nodo2_id):
        if nodo1_id in self.nodos and nodo2_id in self.nodos:
            self.nodos[nodo1_id].nueva_arista(nodo2_id)
    
    def posicion(self, id):
        return self.nodos[id].posicion()
    
    def render(self):
        offset = 28
        glPointSize(56.0)
        glColor3f(0.7, 0.7, 0.7)  # Blue for nodes
        glBegin(GL_POINTS)
        for node_id, node in self.nodos.items():
            glVertex2f(node.x, node.y)
        glEnd()
        
        # Render edges
        glColor3f(0.7, 0.7, 0.7)  # Gray for edges
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glShadeModel(GL_SMOOTH)
        for node_id, node in self.nodos.items():
            for connected_id in node.aristas:
                connected_node = self.nodos[connected_id]
                glBegin(GL_QUADS)
                if node.x - connected_node.x == 0:
                    glVertex2f(node.x-offset, node.y)
                    glVertex2f(node.x+offset, node.y)
                    glVertex2f(connected_node.x+offset, connected_node.y)
                    glVertex2f(connected_node.x-offset, connected_node.y)
                else:
                    glVertex2f(node.x, node.y-offset)
                    glVertex2f(node.x, node.y+offset)
                    glVertex2f(connected_node.x, connected_node.y+offset)
                    glVertex2f(connected_node.x, connected_node.y-offset)
                glEnd()