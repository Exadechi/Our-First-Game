import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import random

vertices = [
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, 1, 1),
    (-1, -1, 1)
]

edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4)
]

#ORDERING MATTERS FOR THESE A LOT
faces = [
    (0, 1, 2, 3),
    (0, 4, 5, 1),
    (2, 1, 5, 6),
    (3, 7, 6, 2),
    (3, 0, 4, 7),
    (7, 6, 5, 4)
]

colors = [
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 0, 0),
    (1, 1, 1),
    (0, 1, 1),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 0, 0),
    (1, 1, 1),
    (0, 1, 1),
]

def Cube():

    glBegin(GL_QUADS)
    for face in faces:
        x = 0
        glColor3fv(colors[x])
        for vertex in face:
            glColor3fv(colors[x])
            x += 1
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_LINES)
    glColor3fv(colors[4])
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def Main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

    gluPerspective(45, display[0] / display[1], 0.1, 50)

    glTranslatef(random.randrange(-5, 5), random.randrange(-5, 5), -40)
    # glRotatef(25, 2, 1, 0)
    x_move = 0
    y_move = 0

    object_passed = False

    # glEnable(GL_DEPTH_TEST)
    while not object_passed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_move = 0.3
                if event.key == pygame.K_RIGHT:
                    x_move = -0.3

                if event.key == pygame.K_DOWN:
                    y_move = 0.3

                if event.key == pygame.K_UP:
                    y_move = -0.3

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_move = 0

                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    y_move = 0

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if event.button == 4:
            #         glTranslatef(0, 0, 1)
            #     if event.button == 5:
            #         glTranslatef(0, 0, -1)

        #glRotatef(1, 3, 1, 1)

        x = glGetDoublev(GL_MODELVIEW_MATRIX)

        camera_x = x[3][0]
        camera_y = x[3][1]
        camera_z = x[3][2]
        print(camera_z)

        if camera_z < -1:
            object_passed = True

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glTranslatef(x_move, y_move, 0.5)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)

for x in range(10):
    Main()
pygame.quit()
quit()