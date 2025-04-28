from GameEngine import *

clock = pygame.time.Clock()

# Set up display
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
WINDOW_NAME = "Game Window"

screen_center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

CAM_MOVE_SPEED = 0.2
CAM_ROT_SPEED = 0.1
DOT_COLOR = (150, 150, 150)
DOT_RADIUS = 2

cam_pos = [0,0,-3]
cam_rot = [0,0]

move_vertical = 0
move_horizontal = 0
rot_vertical = 0
rot_horizontal = 0

k1 = 600
k2 = 1

game = GameWindow(WINDOW_NAME, SCREEN_WIDTH, SCREEN_HEIGHT, k1=k1, k2=k2)
camera = Camera(cam_pos, cam_rot, move_speed=CAM_MOVE_SPEED, rotation_speed=CAM_ROT_SPEED)
cube = GameObject("cube", DOT_COLOR, DOT_RADIUS)

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

            if event.key == pygame.K_UP:
                camera.rotate_up()
            elif event.key == pygame.K_DOWN:
                camera.rotate_down()
            if event.key == pygame.K_RIGHT:
                camera.rotate_right()
            elif event.key == pygame.K_LEFT:
                camera.rotate_left()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                move_vertical = 0
            elif event.key == pygame.K_s:
                move_vertical = 0
            if event.key == pygame.K_d:
                move_horizontal = 0
            elif event.key == pygame.K_a:
                move_horizontal = 0

    if move_vertical == 1:
        camera.move_forward()
    elif move_vertical == -1:
        camera.move_backward()
    if move_horizontal == 1:
        camera.move_right()
    elif move_horizontal == -1:
        camera.move_left()

    game.set_background((30, 30, 30))
    game.show_object(cube, camera)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
