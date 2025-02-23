from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import os
import map_gen

# Texture IDs
wall_texture = None
floor_texture = None
cloud_texture = None
laser_blaster_texture = None
font = None  # Initialized in setup()
display = (800, 600)
time_limit = 60
start_time = None  # Set in setup()

# Cloud scrolling
cloud_offset = 0.0
cloud_speed = 0.002

# Minimap settings
minimap_size = 100
minimap_scale = None  # Set in setup()

def setup():
    global font, minimap_scale, start_time
    font = pygame.font.SysFont("Arial", 36)
    minimap_scale = minimap_size / len(map_gen.maze)
    start_time = pygame.time.get_ticks() / 1000
    load_textures()

def load_textures():
    global wall_texture, floor_texture, cloud_texture, laser_blaster_texture
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
    blaster_path = os.path.join("assets", "laser_blaster.png")
    if os.path.exists(blaster_path):
        blaster_image = pygame.image.load(blaster_path).convert_alpha()
        blaster_data = pygame.image.tostring(blaster_image, "RGBA", 1)
        laser_blaster_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, laser_blaster_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, blaster_image.get_width(), blaster_image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, blaster_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

def render_scene(player_pos, player_angle_x, player_angle_y):
    draw_floor()
    draw_ceiling()
    for z in range(len(map_gen.maze)):
        for x in range(len(map_gen.maze[z])):
            if map_gen.maze[z][x] == 1:
                draw_wall(x, 0, z)
    draw_goal(map_gen.goal[0], map_gen.goal[1], map_gen.goal[2])

def draw_wall(x, y, z, height=2):
    glPushMatrix()
    glTranslatef(x + 0.5, y + height / 2, z + 0.5)
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

def draw_ceiling():
    global cloud_offset
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
    cloud_offset = (cloud_offset + cloud_speed) % 5

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

def render_overlays():
    draw_minimap()
    draw_timer()
    draw_crosshair()
    draw_laser_blaster()

def draw_minimap():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, display[0], display[1], 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    for z in range(len(map_gen.maze)):
        for x in range(len(map_gen.maze[z])):
            if map_gen.maze[z][x] == 1:
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

def draw_timer():
    time_remaining = max(0, time_limit - (pygame.time.get_ticks() / 1000 - start_time))
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
    glOrtho(0, display[0], display[1], 0, -1, 1)
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

def draw_laser_blaster():
    if not laser_blaster_texture:
        return
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, display[0], display[1], 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glEnable(GL_BLEND)
    glBindTexture(GL_TEXTURE_2D, laser_blaster_texture)
    width, height = 375, 250  # Size
    x = 0  # Far left edge of the screen
    y = display[1] - height  # Bottom edge of the screen
    glBegin(GL_QUADS)
    # Rotated 180 degrees
    glTexCoord2f(1, 1); glVertex3f(x, y, 0)
    glTexCoord2f(0, 1); glVertex3f(x + width, y, 0)
    glTexCoord2f(0, 0); glVertex3f(x + width, y + height, 0)
    glTexCoord2f(1, 0); glVertex3f(x, y + height, 0)
    glEnd()
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)