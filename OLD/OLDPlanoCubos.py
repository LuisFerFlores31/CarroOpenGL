import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math

# Se carga el archivo de la clase Cubo
import sys
sys.path.append('..')

# Import obj loader
from objloader import *

screen_width = 1200
screen_height = 800
#vc para el obser.
FOVY=90.0
ZNEAR=1.0
ZFAR=900.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X = 0.0 
EYE_Y = 0.0 #Variable para ajuste de camara
EYE_Z = 0.0
CENTER_X=1.0
CENTER_Y=5.0
CENTER_Z=0.0
UP_X=0
UP_Y=1
UP_Z=0
#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500
#Dimension del plano
DimBoard = 200

#Jugador/Camara
PLAYER_X = 0 
PLAYER_Y = 47  # Ground level 35 Llantas 47
#PLAYER_Y = 35  # Ground level 35
PLAYER_Z = 0

#Variables del jugador
EYE_X = PLAYER_X
EYE_Y = PLAYER_Y
EYE_Z = PLAYER_Z
CENTER_X = EYE_X + 1.0
CENTER_Y = EYE_Y - 0.6
CENTER_Z = EYE_Z

objetos = []

#Variables para el control del observador
#Vector de direcc. del observador
dir = [1.0, 0.0, 0.0]
theta = 0.0


pygame.init()

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    #Z axis in blue
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    glLineWidth(1.0)


def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: cubos")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
        
    #glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_POSITION,  (0, 200, 0, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded    
    objetos.append(OBJ("Chevrolet_Camaro_SS_Low.obj", swapyz=True))
    #objetos.append(OBJ("Llantas_ad.obj", swapyz=True))
    #objetos.append(OBJ("Llantas_tr.obj", swapyz=True))
    #objetos.append(OBJ("Chasis.obj", swapyz=True))


    

    for i in range(len(objetos)): 
        objetos[i].generate()

def lookat():
    global EYE_X
    global EYE_Z
    global CENTER_X
    global CENTER_Z
    global dir
    global theta
    dir_x = 0.0
    dir_z = 0.0
    rads = math.radians(theta)
    dir_x = math.cos(rads)*dir[0] + math.sin(rads)*dir[2]
    dir_z = -math.sin(rads)*dir[0] + math.cos(rads)*dir[2]
    dir[0] = dir_x
    dir[2] = dir_z
    CENTER_X = EYE_X + dir[0]
    CENTER_Z = EYE_Z + dir[2]
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    
def displayobj():
    global theta
    glPushMatrix()
    # Posiciona el carro debajo de la cámara
    glTranslatef(EYE_X, EYE_Y - 35.0, EYE_Z)
    # Rota el auto para que mire hacia adelante según la cámara
    glRotatef(-theta - 90, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glScale(10.0, 10.0, 10.0)
    objetos[0].render()
    glPopMatrix()
    
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    #Se dibuja el plano gris
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()

        
    displayobj()
    
done = False
Init()
while not done:
    keys = pygame.key.get_pressed()
    # Movimiento y giro de cámara sincronizado con el auto
    move_speed = 2.0
    turn_speed = 2.0
    if keys[pygame.K_RIGHT]:
        theta += turn_speed
    if keys[pygame.K_LEFT]:
        theta -= turn_speed

    # Actualiza el vector de dirección según theta
    rads = math.radians(theta)
    dir[0] = math.cos(rads)
    dir[2] = math.sin(rads)

    if keys[pygame.K_UP]:
        EYE_X += dir[0] * move_speed
        EYE_Z += dir[2] * move_speed
    if keys[pygame.K_DOWN]:
        EYE_X -= dir[0] * move_speed
        EYE_Z -= dir[2] * move_speed

    CENTER_X = EYE_X + dir[0]
    CENTER_Z = EYE_Z + dir[2]
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

    display()

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()