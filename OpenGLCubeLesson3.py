import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.OPENGL)

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
    gluPerspective(45, infoObject.current_w / infoObject.current_h, 0.1, 50)

    glTranslatef(0, 0, -10)
    glRotatef(25, 2, 1, 0)

    glEnable(GL_DEPTH_TEST)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glTranslatef(-0.5, 0, 0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(0.5, 0, 0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0, -0.5, 0)
                if event.key == pygame.K_UP:
                    glTranslatef(0, 0.5, 0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0, 0, 1)
                if event.button == 5:
                    glTranslatef(0, 0, -1)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        #glRotatef(1, 3, 1, 1)
        pygame.display.flip()
        pygame.time.wait(10)

Main()