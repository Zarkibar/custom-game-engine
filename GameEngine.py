import pygame
import sys
import math
import numpy as np

def generate_cube(step=0.33):
    coords = []
    val = -1
    while val <= 1:
        coords.append(round(val, 2))
        val += step
    coords[-1] = 1.0  # ensure exact endpoint

    points = []
    for x in coords:
        for y in coords:
            for z in coords:
                # Only add if point is on the surface (at least one coordinate at boundary)
                if abs(x) == 1 or abs(y) == 1 or abs(z) == 1:
                    points.append([x, y, z])
    return points

def generate_torus(R=1.0, r=0.4, num_major=30, num_minor=15):
    points = []

    for i in range(num_major):
        theta = (2 * math.pi * i) / num_major
        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)

        for j in range(num_minor):
            phi = (2 * math.pi * j) / num_minor
            cos_phi = math.cos(phi)
            sin_phi = math.sin(phi)

            x = (R + r * cos_phi) * cos_theta
            y = (R + r * cos_phi) * sin_theta
            z = r * sin_phi

            points.append([round(x, 4), round(y, 4), round(z, 4)])

    return points

def load_vertices_from_obj(filename):
        vertices = []

        with open("models/" + filename, 'r') as file:
            for line in file:
                if line.startswith('v '):
                    parts = line.strip().split()
                    x, y, z = map(float, parts[1:4])
                    vertices.append([x, y, z])

        return vertices

class GameObject:
    def __init__(self, model: str, dot_color: tuple, dot_radius: int):
        if model == "torus":
            self.points = np.array(generate_torus())
        elif model == "cube":
            self.points = np.array(generate_cube())
        else:
            self.points = np.array(load_vertices_from_obj(model))

        self.dot_color = dot_color
        self.dot_radius = dot_radius

        self.position = pygame.math.Vector3(0, 0, 0)

    def translate(self, vector):
        self.position += vector


class Camera:
    def __init__(self, position: list, rotation: list, move_speed=0.2, rotation_speed=0.06):
        self.move_speed = move_speed
        self.rotation_speed = rotation_speed

        self.position = position
        self.rotation = rotation

        self.move_vertical = 0
        self.move_horizontal = 0
        self.rot_vertical = 0
        self.rot_horizontal = 0

    def move_forward(self):
        x_rot = math.cos(self.rotation[1])
        y_rot = math.sin(self.rotation[1])

        self.position[2] += self.move_speed * x_rot
        self.position[0] -= self.move_speed * y_rot
    def move_backward(self):
        x_rot = math.cos(self.rotation[1])
        y_rot = math.sin(self.rotation[1])

        self.position[2] -= self.move_speed * x_rot
        self.position[0] += self.move_speed * y_rot
    def move_right(self):
        x_rot = math.cos(self.rotation[1] + math.pi/2)
        y_rot = math.sin(self.rotation[1] + math.pi/2)

        self.position[2] -= self.move_speed * x_rot
        self.position[0] += self.move_speed * y_rot
    def move_left(self):
        x_rot = math.cos(self.rotation[1] + math.pi/2)
        y_rot = math.sin(self.rotation[1] + math.pi/2)

        self.position[2] += self.move_speed * x_rot
        self.position[0] -= self.move_speed * y_rot

    def rotate_right(self):
        self.rotation[1] -= self.rotation_speed
    def rotate_left(self):
        self.rotation[1] += self.rotation_speed
    def rotate_up(self):
        self.rotation[0] += self.rotation_speed
    def rotate_down(self):
        self.rotation[0] -= self.rotation_speed

class GameWindow:
    def __init__(self, window_name: str, screen_width: int, screen_height: int, k1=600, k2=2):
        self.screen_width = screen_width
        self.screen_height = screen_height

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(window_name)
        self.screen_center = (screen_width/2, screen_height/2)

        self.k1 = k1
        self.k2 = k2

    def project_point(self, point):
        x = self.k1 * point[0] / (point[2] + self.k2) 
        y = self.k1 * point[1] / (point[2] + self.k2)
        
        screen_x = int(x + self.screen_center[0])
        screen_y = int(y + self.screen_center[1])
        return (screen_x, screen_y)

    def rotate_point_y(self, point, angle):
        x, y, z = point
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return [x * cos_a - z * sin_a, y, x * sin_a + z * cos_a]

    def rotate_point_x(self, point, angle):
        x, y, z = point
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return [x, y * cos_a - z * sin_a, y * sin_a + z * cos_a]

    def transform_point(self, point, cam_pos, cam_rot):
        # Move point relative to camera
        x = point[0] - cam_pos[0]
        y = point[1] - cam_pos[1]
        z = point[2] - cam_pos[2]

        # Rotate around camera
        point = self.rotate_point_y([x, y, z], -cam_rot[1])  # yaw (left-right)
        point = self.rotate_point_x(point, -cam_rot[0])      # pitch (up-down)

        return point
    
    def rotate_object(object: GameObject, t):
        for point in object.points:
            x = point[0]
            z = point[2]
            point[2] = z * math.cos(t) - x * math.sin(t)
            point[0] = x * math.cos(t) + z * math.sin(t)

    def show_object(self, object: GameObject, camera: Camera):
        for point in object.points:
            transformed_point = point + object.position
            cam_transformed = self.transform_point(transformed_point, camera.position, camera.rotation)
            if cam_transformed[2] > 0.01:
                pygame.draw.circle(self.screen, object.dot_color, self.project_point(cam_transformed), object.dot_radius)

    def set_background(self, color: tuple):
        self.screen.fill(color)

    def exit_program(self):
        pygame.quit()
        sys.exit()