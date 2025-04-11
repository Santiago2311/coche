#Author: Modified from Ivan Olmos Pineda's code

import pygame
from pygame.locals import *

# OpenGL libraries
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import os
import random
import math
import numpy as np

class Carro:
    def __init__(self, transform, vehicle_color, scale_factor, screen_width, screen_height, road_network, initial_position):
        # Initialize vertices for the vehicle shape (unit object)
        self.vertices = np.array([
            [-4.0, -2.0, 1.0], [4.0, -2.0, 1.0], [4.0, 2.0, 1.0], [-4.0, 2.0, 1.0], 
            [-4.0, -4.0, 1.0], [-1.0, -4.0, 1.0], [-1.0, -3.0, 1.0], [-4.0, -3.0, 1.0],
            [0.0, -4.0, 1.0], [3.0, -4.0, 1.0], [3.0, -3.0, 1.0], [0.0, -3.0, 1.0],
            [-4.0, 3.0, 1.0], [-1.0, 3.0, 1.0], [-1.0, 4.0, 1.0], [-4.0, 4.0, 1.0],
            [0.0, 3.0, 1.0], [3.0, 3.0, 1.0], [3.0, 4.0, 1.0], [0.0, 4.0, 1.0]
        ])
        
        # Basic properties
        self.transform = transform
        self.color = vehicle_color
        self.scale = np.array([scale_factor, scale_factor])
        self.position = initial_position
        self.direction = np.array([1.0, 0.0])
        self.screen_dimensions = (screen_width, screen_height)
        self.rotation_angle = 0.0
        self.delta_rotation = 0.0
        self.delta_scale = np.array([0.0, 0.0])
        self.rotation_counter = 0
        self.road_network = road_network
        self.turning = True
        self.target_direction = np.array([1.0, 0.0])
        
        # Collision detection
        self.radius = math.sqrt((4*scale_factor)**2 + (4*scale_factor)**2)
        self.collision_detected = False
        
    def update_state(self):
        if not self.collision_detected:
            if self.rotation_counter == 0:
                if not np.allclose(self.target_direction, self.direction):
                    # Determine turn direction based on current and target directions
                    if ((np.allclose(self.direction, [1.0, 0.0]) and np.array_equal(self.target_direction, [0.0, 1.0])) or 
                        (np.allclose(self.direction, [-1.0, 0.0]) and np.array_equal(self.target_direction, [0.0, -1.0])) or 
                        (np.allclose(self.direction, [0.0, 1.0]) and np.array_equal(self.target_direction, [-1.0, 0.0])) or 
                        (np.allclose(self.direction, [0.0, -1.0]) and np.array_equal(self.target_direction, [1.0, 0.0]))):
                        self.set_turn_direction('LEFT')
                    else: 
                        self.set_turn_direction('RIGHT')
                else:
                    # At intersections, choose a new direction based on node type
                    for node_id, node in self.road_network.nodes.items():
                        if np.array_equal(self.position, node.get_position()):                        
                            random.seed(os.urandom(128))
                            
                            # Direction based on node type
                            if node.type == 0:  # North only
                                self.target_direction = np.array([0.0, 1.0])
                            elif node.type == 1:  # East only
                                self.target_direction = np.array([1.0, 0.0])
                            elif node.type == 2:  # South only
                                self.target_direction = np.array([0.0, -1.0])
                            elif node.type == 3:  # West only
                                self.target_direction = np.array([-1.0, 0.0])
                            elif node.type == 4 and self.turning:  # East or South
                                value = random.randint(1, 2)
                                self.turning = False
                                if value == 1:
                                    self.target_direction = np.array([0.0, -1.0])
                                else:
                                    self.target_direction = np.array([1.0, 0.0])
                            elif node.type == 5 and self.turning:  # West or South
                                value = random.randint(1, 2)
                                self.turning = False
                                if value == 1:
                                    self.target_direction = np.array([0.0, -1.0])
                                else:
                                    self.target_direction = np.array([-1.0, 0.0])
                            elif node.type == 6 and self.turning:  # East or North
                                value = random.randint(1, 2)
                                self.turning = False
                                if value == 1:
                                    self.target_direction = np.array([0.0, 1.0])
                                else:
                                    self.target_direction = np.array([1.0, 0.0])
                            elif node.type == 7 and self.turning:  # West or North
                                value = random.randint(1, 2)
                                self.turning = False
                                if value == 1:
                                    self.target_direction = np.array([0.0, 1.0])
                                else:
                                    self.target_direction = np.array([-1.0, 0.0])
                            elif node.type == 8 and self.turning:  # All directions
                                value = random.randint(1, 4)
                                self.turning = False
                                if value == 1:
                                    self.target_direction = np.array([0.0, 1.0])  # North
                                elif value == 2:
                                    self.target_direction = np.array([1.0, 0.0])  # East
                                elif value == 3:
                                    self.target_direction = np.array([0.0, -1.0])  # South
                                else:
                                    self.target_direction = np.array([-1.0, 0.0])  # West
                            elif node.type == 9 and self.turning:  # North or East or West
                                value = random.randint(1, 3)
                                self.turning = False
                                if value == 1:
                                    self.target_direction = np.array([0.0, 1.0])  # North
                                elif value == 2:
                                    self.target_direction = np.array([1.0, 0.0])  # East
                                else:
                                    self.target_direction = np.array([-1.0, 0.0])  # West
                        elif node_id == 22 and np.allclose(self.target_direction, self.direction):
                            self.turning = True
                            self.move_forward()
            elif self.rotation_counter > 0:  # Turning left
                self.rotation_angle += 1
                self.direction[0] = np.cos(math.radians(self.rotation_angle))
                self.direction[1] = np.sin(math.radians(self.rotation_angle))
                self.rotation_counter -= 1
            elif self.rotation_counter < 0:  # Turning right
                self.rotation_angle -= 1
                self.rotation_counter += 1
                self.direction[0] = np.cos(math.radians(self.rotation_angle))
                self.direction[1] = np.sin(math.radians(self.rotation_angle))
    
    def set_color(self, r, g, b):
        self.color[0] = r
        self.color[1] = g
        self.color[2] = b
    
    def set_position(self, new_position):
        self.position[0] = new_position[0]
        self.position[1] = new_position[1]
    
    def set_direction(self, new_direction):
        self.direction[0] = new_direction[0]
        self.direction[1] = new_direction[1]
    
    def set_rotation(self, angle):
        self.rotation_angle = angle
    
    def set_delta_rotation(self, delta):
        self.delta_rotation = delta
    
    def set_scale(self, new_scale):
        self.scale[0] = new_scale[0]
        self.scale[1] = new_scale[1]
        
    def set_delta_scale(self, delta):
        self.delta_scale[0] = delta[0]
        self.delta_scale[1] = delta[1]
    
    def set_turn_direction(self, direction):
        if self.rotation_counter == 0:
            if direction == 'LEFT':
                self.rotation_counter = 90
            else:
                self.rotation_counter = -90
            
    def render(self):
        self.transform.push()  # Save current state
        self.transform.translate(self.position[0], self.position[1])
        if self.rotation_angle != 0:
            self.transform.rotate(self.rotation_angle)
        self.transform.scale(self.scale[0], self.scale[1])
        
        transformed_vertices = self.vertices.copy()
        self.transform.mult_Points(transformed_vertices)
        
        glColor3fv(self.color)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        # Draw the vehicle body (each quad)
        for i in range(0, 20, 4):
            glBegin(GL_QUADS)
            glVertex2f(transformed_vertices[i][0], transformed_vertices[i][1])
            glVertex2f(transformed_vertices[i+1][0], transformed_vertices[i+1][1])
            glVertex2f(transformed_vertices[i+2][0], transformed_vertices[i+2][1])
            glVertex2f(transformed_vertices[i+3][0], transformed_vertices[i+3][1])
            glEnd()
            
        self.transform.pop()  # Restore state
        self.update_state()
    
    def move_forward(self):
        if self.rotation_counter == 0:
            self.position[0] += self.direction[0]
            self.position[1] += self.direction[1]
    
    def move_backward(self):
        if self.rotation_counter == 0:
            self.position[0] -= self.direction[0]
            self.position[1] -= self.direction[1]
    
    def calculate_distance(self, pos1, pos2):
        x_diff = pos2[0] - pos1[0]
        y_diff = pos2[1] - pos1[1] 
        return math.sqrt((x_diff**2) + (y_diff**2))
    
    def detect_collision(self, other_vehicle):
        next_position = self.position + self.direction
        distance = self.calculate_distance(next_position, other_vehicle.position)
        
        if (self.radius + other_vehicle.radius >= distance):
            self.collision_detected = True
        else:
            self.collision_detected = False