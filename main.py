import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import sys
import os
import time

# Importación de clases personalizadas
from RoadNetwork import RoadNetwork
from Carro import Carro
from Player import Player

# Configuración de pantalla y sistema
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
GRID_BOUNDS = {
    'X_MIN': -512,
    'X_MAX': 512,
    'Y_MIN': -384,
    'Y_MAX': 384
}

# Controlador de transformaciones
class TransformationMatrix:
    def __init__(self):
        self.matrix_stack = []
        self.loadIdentity()
        
    def loadIdentity(self):
        self.current_matrix = np.identity(4)
        
    def push(self):
        self.matrix_stack.append(self.current_matrix.copy())
        
    def pop(self):
        if len(self.matrix_stack) > 0:
            self.current_matrix = self.matrix_stack.pop()
            
    def translate(self, tx, ty, tz=0):
        translation = np.array([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0, 1]
        ])
        self.current_matrix = np.matmul(translation, self.current_matrix)
        
    def rotate(self, angle, x=0, y=0, z=1):
        angle_rad = np.radians(angle)
        c = np.cos(angle_rad)
        s = np.sin(angle_rad)
        
        rotation = np.array([
            [c, -s, 0, 0],
            [s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        self.current_matrix = np.matmul(rotation, self.current_matrix)
        
    def scale(self, sx, sy, sz=1):
        scaling = np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ])
        self.current_matrix = np.matmul(scaling, self.current_matrix)
        
    def mult_Points(self, points):
        for i in range(len(points)):
            # Convertir a vector homogéneo
            homogeneous = np.array([points[i][0], points[i][1], points[i][2], 1])
            # Multiplicar por matriz de transformación
            transformed = np.matmul(self.current_matrix, homogeneous)
            # Actualizar coordenadas normalizadas
            points[i][0] = transformed[0]
            points[i][1] = transformed[1]
            points[i][2] = transformed[2]

# Funciones de inicialización
def init_opengl():
    """Inicializa OpenGL y configura el entorno de renderizado"""
    pygame.init()
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Simulación de Ciudad - Tráfico Urbano")
    
    # Configurar proyección ortográfica
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(GRID_BOUNDS['X_MIN'], GRID_BOUNDS['X_MAX'], 
               GRID_BOUNDS['Y_MIN'], GRID_BOUNDS['Y_MAX'])
    
    # Configurar modelo de vista
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0.1, 0.1, 0.12, 1.0)  # Color de fondo azul oscuro
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    return screen

def draw_coordinate_system():
    """Dibuja los ejes de coordenadas"""
    glShadeModel(GL_FLAT)
    glLineWidth(2.0)
    
    # Eje X (rojo)
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(GRID_BOUNDS['X_MIN'], 0.0, 0.0)
    glVertex3f(GRID_BOUNDS['X_MAX'], 0.0, 0.0)
    glEnd()
    
    # Eje Y (verde)
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, GRID_BOUNDS['Y_MIN'], 0.0)
    glVertex3f(0.0, GRID_BOUNDS['Y_MAX'], 0.0)
    glEnd()
    glLineWidth(1.0)

def create_road_network():
    """Crea y configura la red de carreteras con nodos e intersecciones"""
    city = RoadNetwork(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Añadir intersecciones (nodo_id = city.add_intersection(x, y, tipo))
    # Tipos de intersección:
    # 0: Norte, 1: Este, 2: Sur, 3: Oeste
    # 4: Este o Sur, 5: Oeste o Sur, 6: Este o Norte, 7: Oeste o Norte
    # 8: Todas direcciones, 9: Norte, Este y Oeste
    
    # Centro de la ciudad
    city.add_intersection(0, 0, 8)  # Nodo 0: Intersección central
    
    # Avenida Principal (Este-Oeste)
    city.add_intersection(-400, 0, 7)  # Nodo 1
    city.add_intersection(-200, 0, 8)  # Nodo 2
    city.add_intersection(200, 0, 8)   # Nodo 3
    city.add_intersection(400, 0, 6)   # Nodo 4
    
    # Avenida Norte-Sur
    city.add_intersection(0, 300, 5)   # Nodo 5
    city.add_intersection(0, 150, 8)   # Nodo 6
    city.add_intersection(0, -150, 8)  # Nodo 7
    city.add_intersection(0, -300, 4)  # Nodo 8
    
    # Distrito Norte
    city.add_intersection(-250, 200, 7)  # Nodo 9
    city.add_intersection(250, 200, 6)   # Nodo 10
    
    # Distrito Sur
    city.add_intersection(-250, -200, 7)  # Nodo 11
    city.add_intersection(250, -200, 6)   # Nodo 12
    
    # Calles adicionales
    city.add_intersection(-350, 300, 5)   # Nodo 13
    city.add_intersection(350, 300, 5)    # Nodo 14
    city.add_intersection(-350, -300, 4)  # Nodo 15
    city.add_intersection(350, -300, 4)   # Nodo 16
    
    # Nodos nuevos (5 adicionales)
    city.add_intersection(150, 100, 6)    # Nodo 17: Conexión diagonal NO
    city.add_intersection(-150, 100, 7)   # Nodo 18: Conexión diagonal NE
    city.add_intersection(150, -100, 6)   # Nodo 19: Conexión diagonal SO
    city.add_intersection(-150, -100, 7)  # Nodo 20: Conexión diagonal SE
    city.add_intersection(-400, -150, 3)  # Nodo 21: Calle sin salida Oeste
    
    # Conexiones entre nodos
    # Avenida Principal
    city.connect_intersections(1, 2)
    city.connect_intersections(2, 0)
    city.connect_intersections(0, 3)
    city.connect_intersections(3, 4)
    
    # Avenida Norte-Sur
    city.connect_intersections(5, 6)
    city.connect_intersections(6, 0)
    city.connect_intersections(0, 7)
    city.connect_intersections(7, 8)
    
    # Conectar distritos norte y sur
    city.connect_intersections(9, 2)
    city.connect_intersections(10, 3)
    city.connect_intersections(11, 2)
    city.connect_intersections(12, 3)
    
    # Conectar calles adicionales
    city.connect_intersections(13, 5)
    city.connect_intersections(5, 14)
    city.connect_intersections(15, 8)
    city.connect_intersections(8, 16)
    
    # Conectar a nodos nuevos
    city.connect_intersections(0, 17)
    city.connect_intersections(17, 10)
    city.connect_intersections(0, 18)
    city.connect_intersections(18, 9)
    city.connect_intersections(0, 19)
    city.connect_intersections(19, 12)
    city.connect_intersections(0, 20)
    city.connect_intersections(20, 11)
    city.connect_intersections(1, 21)
    
    # Conexiones bidireccionales para algunos casos
    city.connect_intersections(6, 9)
    city.connect_intersections(9, 6)
    city.connect_intersections(6, 10)
    city.connect_intersections(10, 6)
    city.connect_intersections(7, 11)
    city.connect_intersections(11, 7)
    city.connect_intersections(7, 12)
    city.connect_intersections(12, 7)
    
    return city

def create_vehicles(transform_manager, road_network):
    """Crea y configura los vehículos en la simulación"""
    vehicles = []
    
    # Añadir vehículos controlados por IA a la ciudad
    starting_positions = [1, 5, 8, 4, 10, 12, 14, 16, 19, 20]
    colors = [
        [1.0, 0.0, 0.0],  # Rojo
        [0.0, 0.0, 1.0],  # Azul
        [0.0, 1.0, 0.0],  # Verde
        [1.0, 0.5, 0.0],  # Naranja
        [1.0, 0.0, 1.0],  # Magenta
        [0.0, 1.0, 1.0],  # Cian
        [0.5, 0.5, 0.5],  # Gris
        [0.7, 0.3, 0.3],  # Marrón
        [0.5, 0.0, 0.5],  # Púrpura
        [0.3, 0.7, 0.3]   # Verde oliva
    ]
    
    for i in range(10):
        vehicles.append(
            Carro(transform_manager, 
                  colors[i], 
                  4.5, 
                  SCREEN_WIDTH, 
                  SCREEN_HEIGHT, 
                  road_network, 
                  road_network.get_position(starting_positions[i]))
        )
    
    # Añadir vehículo controlado por el jugador
    player_car = Player(
        transform_manager,
        [1.0, 1.0, 0.0],  # Color amarillo
        5.0,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        road_network,
        road_network.get_position(0)  # Iniciar en el centro
    )
    vehicles.append(player_car)
    
    return vehicles

def check_collisions(vehicles):
    """Verifica colisiones entre todos los vehículos"""
    for i, vehicle1 in enumerate(vehicles):
        for j, vehicle2 in enumerate(vehicles):
            if i != j:
                vehicle1.detect_collision(vehicle2)
                if vehicle1.collision_detected:
                    break

def main():
    """Función principal del programa"""
    # Inicializar OpenGL y configurar pantalla
    screen = init_opengl()
    
    # Crear administrador de transformaciones
    transform_manager = TransformationMatrix()
    transform_manager.loadIdentity()
    
    # Configurar la ciudad y los vehículos
    city_network = create_road_network()
    vehicles = create_vehicles(transform_manager, city_network)
    
    # Variables para controlar el tiempo y framerate
    clock = pygame.time.Clock()
    fps = 60
    running = True
    
    # Bucle principal
    while running:
        # Procesamiento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Limpiar buffer
        glClear(GL_COLOR_BUFFER_BIT)
        
        # Dibujar elementos
        draw_coordinate_system()
        city_network.render()
        
        # Verificar colisiones
        check_collisions(vehicles)
        
        # Renderizar vehículos
        for vehicle in vehicles:
            vehicle.render()
        
        # Actualizar pantalla
        pygame.display.flip()
        
        # Control de framerate
        clock.tick(fps)
    
    # Terminar Pygame
    pygame.quit()

if __name__ == "__main__":
    main()