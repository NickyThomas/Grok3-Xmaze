from OpenGL.GL import *
import pygame
import math
import os
import map_gen

# Laser variables
laser_active = False
laser_start_time = 0
laser_duration = 0.2  # Seconds
burn_marks = []  # List to store burn mark positions (x, y, z, is_floor)
burn_mark_texture = None

def setup():
    """Initialize weapon-related resources after display setup."""
    load_burn_mark_texture()

def load_burn_mark_texture():
    """Load the burn mark texture for the laser."""
    global burn_mark_texture
    burn_mark_path = os.path.join("assets", "burn_mark.png")
    if os.path.exists(burn_mark_path):
        burn_mark_image = pygame.image.load(burn_mark_path).convert_alpha()
        burn_mark_data = pygame.image.tostring(burn_mark_image, "RGBA", 1)
        burn_mark_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, burn_mark_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, burn_mark_image.get_width(), burn_mark_image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, burn_mark_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    else:
        print("Warning: burn_mark.png not found in assets folder")

def handle_input(event):
    global laser_active, laser_start_time
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
        laser_active = True
        laser_start_time = pygame.time.get_ticks() / 1000

def update_and_render_laser(player_pos, player_angle_x, player_angle_y):
    global laser_active, laser_start_time
    if laser_active and (pygame.time.get_ticks() / 1000 - laser_start_time) > laser_duration:
        laser_active = False

    if laser_active:
        dir_x = -math.sin(math.radians(player_angle_x)) * math.cos(math.radians(player_angle_y))
        dir_y = math.sin(math.radians(player_angle_y))
        dir_z = math.cos(math.radians(player_angle_x)) * math.cos(math.radians(player_angle_y))
        start_x = player_pos[0]
        start_y = player_pos[1]
        start_z = player_pos[2]
        hit_x, hit_y, hit_z, is_floor = raycast_laser(start_x, start_y, start_z, dir_x, dir_y, dir_z)
        burn_marks.append((hit_x, hit_y, hit_z, is_floor))
        draw_laser(start_x, start_y, start_z, hit_x, hit_y, hit_z)

    draw_burn_marks()

def raycast_laser(start_x, start_y, start_z, dir_x, dir_y, dir_z):
    max_distance = 50
    step_size = 0.05
    steps = int(max_distance / step_size)
    
    for i in range(steps):
        x = start_x + dir_x * i * step_size
        y = start_y + dir_y * i * step_size
        z = start_z + dir_z * i * step_size
        
        grid_x = int(math.floor(x))
        grid_z = int(math.floor(z))
        
        if grid_x < 0 or grid_x >= len(map_gen.maze[0]) or grid_z < 0 or grid_z >= len(map_gen.maze):
            return (x, y, z, False)
        
        if map_gen.maze[grid_z][grid_x] == 1:
            hit_x = x - dir_x * step_size / 2
            hit_y = y - dir_y * step_size / 2
            hit_z = z - dir_z * step_size / 2
            return (hit_x, hit_y, hit_z, False)
        
        if y <= 0.5:
            return (x, 0.5, z, True)
    
    end_x = start_x + dir_x * max_distance
    end_y = start_y + dir_y * max_distance
    end_z = start_z + dir_z * max_distance
    return (end_x, end_y, end_z, False)

def draw_laser(start_x, start_y, start_z, hit_x, hit_y, hit_z):
    glPushMatrix()
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_TEXTURE_2D)
    glColor3f(1, 0, 0)  # Red laser
    glLineWidth(5)  # Thicker line
    glBegin(GL_LINES)
    glVertex3f(start_x, start_y, start_z)
    glVertex3f(hit_x, hit_y, hit_z)
    glEnd()
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    glColor3f(1, 1, 1)
    glPopMatrix()

def draw_burn_marks():
    if not burn_marks:
        return
    
    glPushMatrix()
    glDisable(GL_TEXTURE_2D)
    glColor3f(0, 1, 0)  # Green for visibility
    size = 0.5
    
    for x, y, z, is_floor in burn_marks:
        glPushMatrix()
        glTranslatef(x, y + 0.01, z)  # Slight offset to avoid z-fighting
        if is_floor:
            glRotatef(90, 1, 0, 0)  # Flat on floor
        glBegin(GL_QUADS)
        glVertex3f(-size / 2, -size / 2, 0)
        glVertex3f(size / 2, -size / 2, 0)
        glVertex3f(size / 2, size / 2, 0)
        glVertex3f(-size / 2, size / 2, 0)
        glEnd()
        glPopMatrix()
    
    glEnable(GL_TEXTURE_2D)
    glColor3f(1, 1, 1)
    glPopMatrix()

# ... (previous function definitions)

def setup():
    load_burn_mark_texture()

# No more top-level calls here

#load_burn_mark_texture()