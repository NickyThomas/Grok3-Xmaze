import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Initialize Pygame and set up the display BEFORE importing modules that use display-dependent functions
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glEnable(GL_DEPTH_TEST)
glEnable(GL_TEXTURE_2D)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# Now import modules
import map_gen
import movement
import graphics
import weapons

# Setup graphics and weapons after display initialization
graphics.setup()  # Assuming this exists in your graphics.py
weapons.setup()   # Call this to load the burn mark texture

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        movement.handle_input(event, player_pos)  # Handle jumping
        weapons.handle_input(event)  # Handle laser firing

    # Mouse rotation
    mouse_dx, mouse_dy = pygame.mouse.get_rel()
    player_angle_x += mouse_dx * 0.1
    player_angle_y = max(-90, min(90, player_angle_y - mouse_dy * 0.1))

    # Movement with sprinting
    movement.update_player_position(player_pos, player_angle_x)

    # Render 3D scene
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glRotatef(player_angle_y, 1, 0, 0)
    glRotatef(player_angle_x, 0, 1, 0)
    glTranslatef(-player_pos[0], -player_pos[1], -player_pos[2])
    graphics.render_scene(player_pos, player_angle_x, player_angle_y)
    weapons.update_and_render_laser(player_pos, player_angle_x, player_angle_y)

    # Render 2D overlays
    graphics.render_overlays()

    pygame.display.flip()
    clock.tick(60)

    # Check win condition
    if movement.check_goal(player_pos):
        print("You win!")
        running = False

pygame.quit()