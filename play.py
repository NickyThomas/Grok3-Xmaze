import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import os

# Initialize Pygame and OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Set up perspective and depth testing
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_POSITION, (5, 5, 5, 1))
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_TEXTURE_2D)

# Player position and angles
player_pos = [1.5, 0.5, 1.5]  # Starting position (x, y, z)
player_angle_x = 0  # Yaw (left-right)
player_angle_y = 0  # Pitch (up-down)
step_size = 1.0  # One grid square per move
turn_angle = 90  # Turn 90 degrees with A/D

# Define a 10x10 maze (1 = wall, 0 = path)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
goal = [4.5, 0, 4.5]  # Center of the maze

# Texture IDs
wall_texture = None
floor_texture = None

# Load textures from /assets/
def load_textures():
    global wall_texture, floor_texture
    wall_path = os.path.join("assets", "brick_texture.jpeg")
    if not os.path.exists(wall_path):
        print(f"Error: {wall_path} not found!")
        return
    wall_image = pygame.image.load(wall_path).convert()
    wall_data = pygame.image.tostring(wall_image, "RGBA", 1)
    wall_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, wall_texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, wall_image.get_width(), wall_image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, wall_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    floor_path = os.path.join("assets", "floor_texture.jpeg")
    if not os.path.exists(floor_path):
        print(f"Error: {floor_path} not found!")
        return
    floor_image = pygame.image.load(floor_path).convert()
    floor_data = pygame.image.tostring(floor_image, "RGBA", 1)
    floor_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, floor_texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, floor_image.get_width(), floor_image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, floor_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

# Draw a wall cube with texture
def draw_wall(x, y, z, height=2):
    glPushMatrix()
    glTranslatef(x, y + height / 2, z)
    glScalef(1, height, 1)
    glBindTexture(GL_TEXTURE_2D, wall_texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, -0.5)
    glTexCoord2f(1, 0); glVertex3f(0.5, -0.5, -0.5)
    glTexCoord2f(1, 1); glVertex3f(0.5, 0.5, -0.5)
    glTexCoord2f(0, 1); glVertex3f(-0.5, 0.5, -0.5)
    glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, 0.5)
    glTexCoord2f(1, 0); glVertex3f(0.5, -0.5, 0.5)
    glTexCoord2f(1, 1); glVertex3f(0.5, 0.5, 0.5)
    glTexCoord2f(0, 1); glVertex3f(-0.5, 0.5, 0.5)
    glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, -0.5)
    glTexCoord2f(1, 0); glVertex3f(-0.5, -0.5, 0.5)
    glTexCoord2f(1, 1); glVertex3f(-0.5, 0.5, 0.5)
    glTexCoord2f(0, 1); glVertex3f(-0.5, 0.5, -0.5)
    glTexCoord2f(0, 0); glVertex3f(0.5, -0.5, -0.5)
    glTexCoord2f(1, 0); glVertex3f(0.5, -0.5, 0.5)
    glTexCoord2f(1, 1); glVertex3f(0.5, 0.5, 0.5)
    glTexCoord2f(0, 1); glVertex3f(0.5, 0.5, -0.5)
    glEnd()
    glPopMatrix()

# Draw floor with texture
def draw_floor():
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, floor_texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
    glTexCoord2f(10, 0); glVertex3f(10, 0, 0)
    glTexCoord2f(10, 10); glVertex3f(10, 0, 10)
    glTexCoord2f(0, 10); glVertex3f(0, 0, 10)
    glEnd()
    glPopMatrix()

# Draw goal
def draw_goal(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glDisable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    glColor3f(0, 1, 0)
    vertices = [
        (-0.2, -0.2, -0.2), (0.2, -0.2, -0.2), (0.2, 0.2, -0.2), (-0.2, 0.2, -0.2),
        (-0.2, -0.2, 0.2), (0.2, -0.2, 0.2), (0.2, 0.2, 0.2), (-0.2, 0.2, 0.2),
        (-0.2, -0.2, -0.2), (-0.2, 0.2, -0.2), (-0.2, 0.2, 0.2), (-0.2, -0.2, 0.2),
        (0.2, -0.2, -0.2), (0.2, 0.2, -0.2), (0.2, 0.2, 0.2), (0.2, -0.2, 0.2),
    ]
    for i in range(0, 16, 4):
        for vertex in vertices[i:i+4]:
            glVertex3fv(vertex)
    glEnd()
    glEnable(GL_TEXTURE_2D)
    glPopMatrix()

# Check collision with walls
def check_collision(x, z):
    grid_x = int(round(x))  # Round to nearest grid square
    grid_z = int(round(z))
    if grid_x < 0 or grid_x >= len(maze) or grid_z < 0 or grid_z >= len(maze[0]):
        return True
    return maze[grid_z][grid_x] == 1

# Load textures
load_textures()

# Main game loop
running = True
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
move_cooldown = 0  # To prevent rapid movement

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Mouse look (pitch only)
    mouse_dx, mouse_dy = pygame.mouse.get_rel()
    player_angle_y -= mouse_dy * 0.1
    player_angle_y = max(-90, min(90, player_angle_y))

    # Handle movement and turning (one step at a time)
    keys = pygame.key.get_pressed()
    if move_cooldown <= 0:
        if keys[pygame.K_w]:
            direction_x = math.cos(math.radians(player_angle_x))
            direction_z = math.sin(math.radians(player_angle_x))
            new_x = player_pos[0] + direction_x * step_size
            new_z = player_pos[2] + direction_z * step_size
            if not check_collision(new_x, new_z):
                player_pos[0] = new_x
                player_pos[2] = new_z
            move_cooldown = 10  # Cooldown frames
        elif keys[pygame.K_s]:
            direction_x = math.cos(math.radians(player_angle_x))
            direction_z = math.sin(math.radians(player_angle_x))
            new_x = player_pos[0] - direction_x * step_size
            new_z = player_pos[2] - direction_z * step_size
            if not check_collision(new_x, new_z):
                player_pos[0] = new_x
                player_pos[2] = new_z
            move_cooldown = 10
        elif keys[pygame.K_a]:
            player_angle_x += turn_angle  # Turn left
            move_cooldown = 10
        elif keys[pygame.K_d]:
            player_angle_x -= turn_angle  # Turn right
            move_cooldown = 10

    # Decrease cooldown
    if move_cooldown > 0:
        move_cooldown -= 1

    # Clear screen and set up camera
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glRotatef(player_angle_y, 1, 0, 0)  # Pitch
    glRotatef(player_angle_x, 0, 1, 0)  # Yaw
    glTranslatef(-player_pos[0], -player_pos[1], -player_pos[2])

    # Draw floor and maze
    draw_floor()
    for z in range(len(maze)):
        for x in range(len(maze[z])):
            if maze[z][x] == 1:
                draw_wall(x, 0, z)
    draw_goal(goal[0], goal[1], goal[2])

    # Check if player reached the goal
    if abs(player_pos[0] - goal[0]) < 0.5 and abs(player_pos[2] - goal[2]) < 0.5:
        print("You reached the center!")
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()