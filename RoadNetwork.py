import numpy as np
import random
import math

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Intersection:
    def __init__(self, x_pos, y_pos, intersection_id, intersection_type):
        self.x_coord = x_pos
        self.y_coord = y_pos
        self.id = intersection_id
        self.type = intersection_type
        self.connections = []
    
    def add_connection(self, target_id):
        if target_id not in self.connections:
            self.connections.append(target_id)
    
    def get_position(self):
        return np.array([self.x_coord, self.y_coord])

class RoadNetwork:
    def __init__(self, screen_width, screen_height):
        self.nodes = {}
        self.screen_dimensions = (screen_width, screen_height)
        self.road_width = 28  # Width of roads in pixels
    
    def add_intersection(self, x_pos, y_pos, intersection_type):
        new_id = len(self.nodes)
        self.nodes[new_id] = Intersection(x_pos, y_pos, new_id, intersection_type)
        return new_id
    
    def connect_intersections(self, source_id, target_id):
        if source_id in self.nodes and target_id in self.nodes:
            self.nodes[source_id].add_connection(target_id)
    
    def get_position(self, node_id):
        return self.nodes[node_id].get_position()
    
    def render(self):
        # Render nodes as intersection points
        glPointSize(56.0)
        glColor3f(0.65, 0.65, 0.7)  # Slightly darker gray for intersections
        glBegin(GL_POINTS)
        for node_id, node in self.nodes.items():
            glVertex2f(node.x_coord, node.y_coord)
        glEnd()
        
        # Render roads between intersections
        glColor3f(0.75, 0.75, 0.75)  # Light gray for roads
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glShadeModel(GL_SMOOTH)
        
        for node_id, node in self.nodes.items():
            for connected_id in node.connections:
                connected_node = self.nodes[connected_id]
                
                # Draw road as a quad
                glBegin(GL_QUADS)
                # Check if road is horizontal or vertical
                if node.x_coord - connected_node.x_coord == 0:  # Vertical road
                    # Draw vertical road (left side, right side)
                    glVertex2f(node.x_coord - self.road_width, node.y_coord)
                    glVertex2f(node.x_coord + self.road_width, node.y_coord)
                    glVertex2f(connected_node.x_coord + self.road_width, connected_node.y_coord)
                    glVertex2f(connected_node.x_coord - self.road_width, connected_node.y_coord)
                else:  # Horizontal road
                    # Draw horizontal road (bottom side, top side)
                    glVertex2f(node.x_coord, node.y_coord - self.road_width)
                    glVertex2f(node.x_coord, node.y_coord + self.road_width)
                    glVertex2f(connected_node.x_coord, connected_node.y_coord + self.road_width)
                    glVertex2f(connected_node.x_coord, connected_node.y_coord - self.road_width)
                glEnd()
