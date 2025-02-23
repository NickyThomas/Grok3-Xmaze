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
glEnable(GL_TEXTURE_2D)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# Player variables
player_pos = [1.5, 0.5, 1.5]  # Starting position (x, y, z)
player_angle_x = 0  # Yaw (left-right)
player_angle_y = 0  # Pitch (up-down)
base_move_speed = 0.05  # Base walking speed
sprint_multiplier = 2.0  # Sprinting doubles speed
player_y_velocity = 0.0  # Vertical velocity for jumping
gravity = 0.005  # Gravity strength
jump_strength = 0.08  # Jump height
ground_level = 0.5  # Ground height
player_radius = 0.4  # Player collision radius

# Define a 20x20 maze (1 = wall, 0 = path)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
goal = [18.5, 0, 18.5]  # Goal position (x, y, z)

# Timer setup
time_limit = 60
start_time = pygame.time.get_ticks() / 1000
font = pygame.font.SysFont("Arial", 36)

# Texture IDs
wall_texture = None
floor_texture = None
cloud_texture = None

# Cloud scrolling
cloud_offset = 0.0
cloud_speed = 0.002

# Minimap settings
minimap_size = 100
minimap_scale = minimap_size / len(maze)

# Load textures
def load_textures():
    global wall_texture, floor_texture, cloud_texture
    wall_path = os.path.join("assets", "brick_texture.jpeg")
    if os.path.exists(wall_path):
        wall_image = pygame.image.load(wall_path).convert()
        wall_data = pygame.image.tostring(wall_image, "RGBA", 1)
        wall_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, wall_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, wall_image.get_width(), wall_image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, wall_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    floor_path = os.path.join("assets", "floor_texture.jpeg")
    if os.path.exists(floor_path):
        floor_image = pygame.image.load(floor_path).convert()
        floor_data = pygame.image.tostring(floor_image, "RGBA", 1)
        floor_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, floor_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, floor_image.get_width(), floor_image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, floor_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    cloud_path = os.path.join("assets", "clouds.png")
    if os.path.exists(cloud_path):
        cloud_image = pygame.image.load(cloud_path).convert_alpha()
        cloud_data = pygame.image.tostring(cloud_image, "RGBA", 1)
        cloud_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, cloud_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, cloud_image.get_width(), cloud_image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, cloud_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

# Check collision with AABB
def check_collision(x, z):
    # Calculate the grid cells the player overlaps including radius
    min_x = int(math.floor(x - player_radius))
    max_x = int(math.ceil(x + player_radius))
    min_z = int(math.floor(z - player_radius))
    max_z = int(math.ceil(z + player_radius))
    
    # Ensure the check stays within maze bounds
    for grid_z in range(max(0, min_z), min(len(maze), max_z)):
        for grid_x in range(max(0, min_x), min(len(maze[0]), max_x)):
            if maze[grid_z][grid_x] == 1:
                # Check intersection with wall cell bounds
                wall_left = grid_x
                wall_right = grid_x + 1
                wall_bottom = grid_z
                wall_top = grid_z + 1
                player_left = x - player_radius
                player_right = x + player_radius
                player_bottom = z - player_radius
                player_top = z + player_radius
                if (player_right > wall_left and player_left < wall_right and
                    player_top > wall_bottom and player_bottom < wall_top):
                    return True
    return False

# Draw a wall cube
def draw_wall(x, y, z, height=2):
    glPushMatrix()
    glTranslatef(x + 0.5, y + height / 2, z + 0.5)  # Center the wall in the grid cell
    glScalef(1, height, 1)
    glBindTexture(GL_TEXTURE_2D, wall_texture)
    glColor3f(1, 1, 1)
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

# Draw floor
def draw_floor():
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, floor_texture)
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
    glTexCoord2f(20, 0); glVertex3f(20, 0, 0)
    glTexCoord2f(20, 20); glVertex3f(20, 0, 20)
    glTexCoord2f(0, 20); glVertex3f(0, 0, 20)
    glEnd()
    glPopMatrix()

# Draw ceiling
def draw_ceiling():
    glPushMatrix()
    glTranslatef(0, 2, 0)
    glDisable(GL_TEXTURE_2D)
    glColor3f(0.53, 0.81, 0.98)
    glBegin(GL_QUADS)
    glVertex3f(0, 0, 0)
    glVertex3f(20, 0, 0)
    glVertex3f(20, 0, 20)
    glVertex3f(0, 0, 20)
    glEnd()
    if cloud_texture:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, cloud_texture)
        glColor3f(1, 1, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0 + cloud_offset, 0); glVertex3f(0, 0, 0)
        glTexCoord2f(5 + cloud_offset, 0); glVertex3f(20, 0, 0)
        glTexCoord2f(5 + cloud_offset, 5); glVertex3f(20, 0, 20)
        glTexCoord2f(0 + cloud_offset, 5); glVertex3f(0, 0, 20)
        glEnd()
    glPopMatrix()

# Draw goal
def draw_goal(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glDisable(GL_TEXTURE_2D)
    glColor3f(1, 1, 0)
    glBegin(GL_QUADS)
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

# Draw minimap correctly at top-left
def draw_minimap():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, display[0], display[1], 0, -1, 1)  # Top-left is (0, 0), bottom-right is (display[0], display[1])
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    for z in range(len(maze)):
        for x in range(len(maze[z])):
            if maze[z][x] == 1:
                glColor3f(0.5, 0.5, 0.5)  # Gray walls
            else:
                glColor3f(0, 0, 0)  # Black floor
            minimap_x = x * minimap_scale
            minimap_y = z * minimap_scale
            glVertex2f(minimap_x, minimap_y)
            glVertex2f(minimap_x + minimap_scale, minimap_y)
            glVertex2f(minimap_x + minimap_scale, minimap_y + minimap_scale)
            glVertex2f(minimap_x, minimap_y + minimap_scale)
    glColor3f(1, 0, 0)  # Red player
    player_minimap_x = player_pos[0] * minimap_scale
    player_minimap_z = player_pos[2] * minimap_scale
    glVertex2f(player_minimap_x - 2, player_minimap_z - 2)
    glVertex2f(player_minimap_x + 2, player_minimap_z - 2)
    glVertex2f(player_minimap_x + 2, player_minimap_z + 2)
    glVertex2f(player_minimap_x - 2, player_minimap_z + 2)
    glEnd()
    glEnable(GL_TEXTURE_2D)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

# Draw timer
def draw_timer(time_remaining):
    text_surface = font.render(f"Time: {int(time_remaining)}", True, (255, 255, 255), (0, 0, 0, 0))
    text_width, text_height = text_surface.get_size()
    timer_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, timer_texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_width, text_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(text_surface, "RGBA", False))
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, display[0], display[1], 0, -1, 1)  # Correct orientation
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glEnable(GL_BLEND)
    glBindTexture(GL_TEXTURE_2D, timer_texture)
    x = (display[0] - text_width) / 2
    y = 0  # Top of the screen
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x, y)
    glTexCoord2f(1, 0); glVertex2f(x + text_width, y)
    glTexCoord2f(1, 1); glVertex2f(x + text_width, y + text_height)
    glTexCoord2f(0, 1); glVertex2f(x, y + text_height)
    glEnd()
    glDeleteTextures([timer_texture])
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

# Draw crosshair
def draw_crosshair():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, display[0], display[1], 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_TEXTURE_2D)
    glColor3f(1, 1, 1)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(display[0]/2 - 10, display[1]/2)
    glVertex2f(display[0]/2 + 10, display[1]/2)
    glVertex2f(display[0]/2, display[1]/2 - 10)
    glVertex2f(display[0]/2, display[1]/2 + 10)
    glEnd()
    glEnable(GL_TEXTURE_2D)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

# Load textures
load_textures()

# Main game loop
running = True
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player_pos[1] <= ground_level:
            player_y_velocity = jump_strength

    # Mouse rotation
    mouse_dx, mouse_dy = pygame.mouse.get_rel()
    player_angle_x += mouse_dx * 0.1
    player_angle_y = max(-90, min(90, player_angle_y - mouse_dy * 0.1))

    # Movement with sprinting
    keys = pygame.key.get_pressed()
    move_speed = base_move_speed * (sprint_multiplier if keys[pygame.K_LSHIFT] else 1.0)
    forward_x = math.sin(math.radians(player_angle_x))
    forward_z = -math.cos(math.radians(player_angle_x))
    strafe_x = math.cos(math.radians(player_angle_x))
    strafe_z = math.sin(math.radians(player_angle_x))

    dx = dz = 0
    if keys[pygame.K_w]:
        dx += forward_x * move_speed
        dz += forward_z * move_speed
    if keys[pygame.K_s]:
        dx -= forward_x * move_speed
        dz -= forward_z * move_speed
    if keys[pygame.K_a]:
        dx -= strafe_x * move_speed
        dz -= strafe_z * move_speed
    if keys[pygame.K_d]:
        dx += strafe_x * move_speed
        dz += strafe_z * move_speed

    # Apply movement with collision
    new_x = player_pos[0] + dx
    new_z = player_pos[2] + dz
    temp_x = player_pos[0]
    temp_z = player_pos[2]
    
    # Check x movement
    if not check_collision(new_x, player_pos[2]):
        temp_x = new_x
    
    # Check z movement
    if not check_collision(player_pos[0], new_z):
        temp_z = new_z
    
    # Update position
    player_pos[0] = temp_x
    player_pos[2] = temp_z

    # Gravity and jumping
    player_y_velocity -= gravity
    player_pos[1] = max(ground_level, player_pos[1] + player_y_velocity)

    # Update clouds
    cloud_offset = (cloud_offset + cloud_speed) % 5

    # Timer
    time_remaining = max(0, time_limit - (pygame.time.get_ticks() / 1000 - start_time))
    if time_remaining <= 0:
        print("Game Over - Time's up!")
        running = False

    # Check goal
    if abs(player_pos[0] - goal[0]) < 0.5 and abs(player_pos[2] - goal[2]) < 0.5:
        print("You win!")
        running = False

    # Render 3D scene
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluPerspective(45, display[0] / display[1], 0.1, 50.0)
    glRotatef(player_angle_y, 1, 0, 0)
    glRotatef(player_angle_x, 0, 1, 0)
    glTranslatef(-player_pos[0], -player_pos[1], -player_pos[2])
    draw_floor()
    draw_ceiling()
    for z in range(len(maze)):
        for x in range(len(maze[z])):
            if maze[z][x] == 1:
                draw_wall(x, 0, z)
    draw_goal(goal[0], goal[1], goal[2])

    # Render 2D overlays
    draw_minimap()
    draw_timer(time_remaining)
    draw_crosshair()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()