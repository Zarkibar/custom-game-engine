import pygame
import sys
import math
from utility import ZEngine

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Window")
clock = pygame.time.Clock()

screen_center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

CAM_MOVE_SPEED = 0.2
CAM_ROT_SPEED = 0.1
DOT_COLOR = (150, 150, 150)
DOT_RADIUS = 2

camera_pos = [0,0,-3]
camera_rot = [0,0]

move_vertical = 0
move_horizontal = 0
rot_vertical = 0
rot_horizontal = 0

k1 = 600
k2 = 1

theta = math.pi / 180

def project_point(point):
    x = k1 * point[0] / (point[2] + k2) 
    y = k1 * point[1] / (point[2] + k2)
    
    screen_x = int(x + screen_center[0])
    screen_y = int(y + screen_center[1])
    return (screen_x, screen_y)

def rotate_point_y(point, angle):
    x, y, z = point
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return [x * cos_a - z * sin_a, y, x * sin_a + z * cos_a]

def rotate_point_x(point, angle):
    x, y, z = point
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return [x, y * cos_a - z * sin_a, y * sin_a + z * cos_a]

def transform_point(point, cam_pos, cam_rot):
    # Move point relative to camera
    x = point[0] - cam_pos[0]
    y = point[1] - cam_pos[1]
    z = point[2] - cam_pos[2]

    # Rotate around camera
    point = rotate_point_y([x, y, z], -cam_rot[1])  # yaw (left-right)
    point = rotate_point_x(point, -cam_rot[0])      # pitch (up-down)

    return point

def update_point_rotation(point, theta):
    x = point[0]
    z = point[2]
    point[2] = z * math.cos(theta) - x * math.sin(theta)
    point[0] = x * math.cos(theta) + z * math.sin(theta)

def update_all_points_rotation(p, t):
    for point in p:
        update_point_rotation(point, t)

def show_point(point, cam_pos, cam_rot, color=DOT_COLOR, radius=DOT_RADIUS):
    transformed = transform_point(point, cam_pos, cam_rot)
    if transformed[2] > 0.01:
        pygame.draw.circle(screen, color, project_point(transformed), radius)

def show_all_points(p, cam_pos, cam_rot, color=DOT_COLOR, radius=DOT_RADIUS):
    for point in p:
        show_point(point, cam_pos, cam_rot, color=color, radius=radius)


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

def load_vertices_from_obj(path):
    vertices = []

    with open("obj/"+path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                parts = line.strip().split()
                x, y, z = map(float, parts[1:4])
                vertices.append([x, y, z])

    return vertices

# Points
points = load_vertices_from_obj("monkey.obj")

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                move_vertical = 1
            elif event.key == pygame.K_s:
                move_vertical = -1
            if event.key == pygame.K_d:
                move_horizontal = 1
            elif event.key == pygame.K_a:
                move_horizontal = -1

            # if event.key == pygame.K_UP:
            #     rot_vertical = 1
            # elif event.key == pygame.K_DOWN:
            #     rot_vertical = -1
            # if event.key == pygame.K_RIGHT:
            #     rot_horizontal = 1
            # elif event.key == pygame.K_LEFT:
            #     rot_horizontal = -1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                move_vertical = 0
            elif event.key == pygame.K_s:
                move_vertical = 0
            if event.key == pygame.K_d:
                move_horizontal = 0
            elif event.key == pygame.K_a:
                move_horizontal = 0

            # if event.key == pygame.K_UP:
            #     rot_vertical = 0
            # elif event.key == pygame.K_DOWN:
            #     rot_vertical = 0
            # if event.key == pygame.K_RIGHT:
            #     rot_horizontal = 0
            # elif event.key == pygame.K_LEFT:
            #     rot_horizontal = 0

    screen.fill((30, 30, 30))

    if move_vertical == 1:
        camera_pos[2] += CAM_MOVE_SPEED
    elif move_vertical == -1:
        camera_pos[2] -= CAM_MOVE_SPEED

    if move_horizontal == 1:
        camera_pos[0] += CAM_MOVE_SPEED
    elif move_horizontal == -1:
        camera_pos[0] -= CAM_MOVE_SPEED

    # if rot_horizontal == 1:
    #     camera_rot[1] += CAM_ROT_SPEED
    # elif rot_horizontal == -1:
    #     camera_rot[1] -= CAM_ROT_SPEED
    # if rot_vertical == 1:
    #     camera_rot[0] += CAM_ROT_SPEED
    # elif rot_vertical == -1:
    #     camera_rot[1] -= CAM_ROT_SPEED

    update_all_points_rotation(points, theta)
    show_all_points(points, camera_pos, camera_rot)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
