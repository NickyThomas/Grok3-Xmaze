import pygame
from pygame.locals import *
import math
import map_gen

base_move_speed = 0.05  # Base walking speed
sprint_multiplier = 2.0  # Sprinting doubles speed
player_y_velocity = 0.0  # Vertical velocity for jumping
gravity = 0.005  # Gravity strength
jump_strength = 0.08  # Jump height
ground_level = 0.5  # Ground height
player_radius = 0.4  # Player collision radius

def handle_input(event, player_pos):
    global player_y_velocity
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player_pos[1] <= ground_level:
        player_y_velocity = jump_strength

def update_player_position(player_pos, player_angle_x):
    global player_y_velocity
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

    new_x = player_pos[0] + dx
    new_z = player_pos[2] + dz
    if not check_collision(new_x, player_pos[2]):
        player_pos[0] = new_x
    if not check_collision(player_pos[0], new_z):
        player_pos[2] = new_z

    # Gravity and jumping
    player_y_velocity -= gravity
    player_pos[1] = max(ground_level, player_pos[1] + player_y_velocity)

def check_collision(x, z):
    min_x = int(math.floor(x - player_radius))
    max_x = int(math.ceil(x + player_radius))
    min_z = int(math.floor(z - player_radius))
    max_z = int(math.ceil(z + player_radius))
    
    for grid_z in range(max(0, min_z), min(len(map_gen.maze), max_z)):
        for grid_x in range(max(0, min_x), min(len(map_gen.maze[0]), max_x)):
            if map_gen.maze[grid_z][grid_x] == 1:
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

def check_goal(player_pos):
    return abs(player_pos[0] - map_gen.goal[0]) < 0.5 and abs(player_pos[2] - map_gen.goal[2]) < 0.5