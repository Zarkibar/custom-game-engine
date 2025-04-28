import pygame
import sys
import math

class GameManager:
    screen_height = 600
    screen_width = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    screen_center = (screen_width/2, screen_height/2)

    k1 = 600
    k2 = 1

    def __init__(self, window_name: str, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(window_name)

        self.screen_center = (screen_width/2, screen_height/2)

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

    def update_points_rotation(self, p, t):
        for point in p:
            x = point[0]
            z = point[2]
            point[2] = z * math.cos(theta) - x * math.sin(theta)
            point[0] = x * math.cos(theta) + z * math.sin(theta)

    def show_points(self, p, cam_pos, cam_rot, color=dot_color, radius=dot_radius):
        for point in p:
            transformed = self.transform_point(point, cam_pos, cam_rot)
            if transformed[2] > 0.01:
                pygame.draw.circle(self.screen, color, self.project_point(transformed), radius)


    def generate_cube(self, step=0.33):
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

    def generate_torus(self, R=1.0, r=0.4, num_major=30, num_minor=15):
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

    def load_vertices_from_obj(self, filename):
        vertices = []

        with open("obj/" + filename, 'r') as file:
            for line in file:
                if line.startswith('v '):
                    parts = line.strip().split()
                    x, y, z = map(float, parts[1:4])
                    vertices.append([x, y, z])

        return vertices
    
    def exit_program(self):
        pygame.quit()
        sys.exit()