import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.OPENGL)

vertices = [
    (0.66, 0, -0.66),
    (-0.66, 0, -0.66),
    (0, 0, 0.66),
    (0, 1, 0),
    (0, -1, 0)
]

edges = [
    (0, 1),
    (1, 2),
    (2, 0),
    (0, 3),
    (1, 3),
    (2, 3),
    (0, 4),
    (1, 4),
    (2, 4)
]

def Triangle():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def Main():
    gluPerspective(45, infoObject.current_w / infoObject.current_h, 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)
    glRotatef(0, 0, 0, 0)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Triangle()
        glRotatef(1, 3, 1, 1)
        pygame.display.flip()
        pygame.time.wait(10)

Main()