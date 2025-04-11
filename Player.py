#Author: Modified from Ivan Olmos Pineda's code

import pygame
from pygame.locals import *

# OpenGL libraries import
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import os
import random
import math
import numpy as np

class Player:
    def __init__(self, transform, player_color, scale_factor, screen_width, screen_height, road_network, start_position):
        # Initialize player shape vertices (unit object)
        self.vertices = np.array([
            [-4.0, -2.0, 1.0], [4.0, -2.0, 1.0], [4.0, 2.0, 1.0], [-4.0, 2.0, 1.0], 
            [-4.0, -4.0, 1.0], [-1.0, -4.0, 1.0], [-1.0, -3.0, 1.0], [-4.0, -3.0, 1.0],
            [0.0, -4.0, 1.0], [3.0, -4.0, 1.0], [3.0, -3.0, 1.0], [0.0, -3.0, 1.0],
            [-4.0, 3.0, 1.0], [-1.0, 3.0, 1.0], [-1.0, 4.0, 1.0], [-4.0, 4.0, 1.0],
            [0.0, 3.0, 1.0], [3.0, 3.0, 1.0], [3.0, 4.0, 1.0], [0.0, 4.0, 1.0]
        ])
        
        # Basic properties
        self.transform = transform
        self.color = player_color
        self.scale = np.array([scale_factor, scale_factor])
        self.position = start_position
        self.direction = np.array([1.0, 0.0])
        self.screen_dimensions = (screen_width, screen_height)
        self.rotation_angle = 0.0
        self.delta_rotation = 0.0
        self.delta_scale = np.array([0.0, 0.0])
        self.rotation_counter = 0
        self.road_network = road_network
        self.possible_directions = []
        
        # Collision detection
        self.radius = math.sqrt((4*scale_factor)**2 + (4*scale_factor)**2)
        self.collision_detected = False
        self.current_move = ''
        self.can_move = False
        
    def update_state(self):
        if not self.collision_detected:
            if self.rotation_counter == 0:
                # Check if at an intersection and determine possible directions
                for node_id, node in self.road_network.nodes.items():
                    if np.array_equal(self.position, node.get_position()):
                        # Set possible directions based on intersection type
                        if node.type == 0:  # North only
                            self.possible_directions = [np.array([0.0, 1.0])]
                        elif node.type == 1:  # East only
                            self.possible_directions = [np.array([1.0, 0.0])]
                        elif node.type == 2:  # South only
                            self.possible_directions = [np.array([0.0, -1.0])]
                        elif node.type == 3:  # West only
                            self.possible_directions = [np.array([-1.0, 0.0])]
                        elif node.type == 4:  # East or South
                            self.possible_directions = [np.array([1.0, 0.0]), np.array([0.0, -1.0])]
                        elif node.type == 5:  # West or South
                            self.possible_directions = [np.array([-1.0, 0.0]), np.array([0.0, -1.0])]
                        elif node.type == 6:  # East or North
                            self.possible_directions = [np.array([1.0, 0.0]), np.array([0.0, 1.0])]
                        elif node.type == 7:  # West or North
                            self.possible_directions = [np.array([-1.0, 0.0]), np.array([0.0, 1.0])]
                        elif node.type == 8:  # All directions
                            self.possible_directions = [
                                np.array([1.0, 0.0]),   # East
                                np.array([-1.0, 0.0]),  # West
                                np.array([0.0, 1.0]),   # North
                                np.array([0.0, -1.0])   # South
                            ]
                        elif node.type == 9:  # North, East, West
                            self.possible_directions = [
                                np.array([1.0, 0.0]),   # East
                                np.array([-1.0, 0.0]),  # West
                                np.array([0.0, 1.0])    # North
                            ]
                            
                        self.current_move = ''
                        if self.can_move:
                            self.current_move = 'FWD'
                            self.can_move = False
                            
                        # Handle keyboard input
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_LEFT]:
                            self.current_move = 'LEFT'
                        elif keys[pygame.K_RIGHT]:
                            self.current_move = 'RIGHT'
                        elif keys[pygame.K_UP]:
                            self.current_move = 'FWD'
                
                # Process player movement based on inputs and possible directions
                for possible_dir in self.possible_directions:
                    left_dir = [np.cos(math.radians(self.rotation_angle+90)), np.sin(math.radians(self.rotation_angle+90))]
                    right_dir = [np.cos(math.radians(self.rotation_angle-90)), np.sin(math.radians(self.rotation_angle-90))]
                    
                    if self.current_move == 'LEFT' and np.allclose(left_dir, possible_dir):
                        self.set_turn_direction('LEFT')
                        self.current_move = 'FWD'
                        self.can_move = True
                    elif self.current_move == 'RIGHT' and np.allclose(right_dir, possible_dir):
                        self.set_turn_direction('RIGHT')
                        self.current_move = 'FWD'
                        self.can_move = True
                    elif self.current_move == 'FWD' and np.allclose(self.direction, possible_dir):
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
    
    def set_position(self, pos):
        self.position[0] = pos[0]
        self.position[1] = pos[1]
    
    def set_direction(self, dir):
        self.direction[0] = dir[0]
        self.direction[1] = dir[1]
    
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
        
        # Draw player vehicle (each quad)
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
        if self.rotation_counter == 0 and not self.collision_detected:
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
    
    def detect_collision(self, vehicle):
        next_position = self.position + self.direction
        distance = self.calculate_distance(next_position, vehicle.position)
        
        if (self.radius + vehicle.radius >= distance):
            self.collision_detected = True
        else:
            self.collision_detected = False