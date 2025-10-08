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
FOVY=60.0
ZNEAR=0.01
ZFAR=900.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X = 300.0
EYE_Y = 200.0
EYE_Z = 300.0
Player_X = 0.0
Player_Y = 0.0
Player_Z = 0.0
# Ángulo de rotación del carrito
car_angle = 0.0
CENTER_X = 0
CENTER_Y = 0
CENTER_Z = 0
UP_X=0
UP_Y=1
UP_Z=0
# Variable para el ángulo de las ruedas
wheel_angle = 0.0

#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500
#Dimension del plano
DimBoard = 200

objetos = []

#Variables para el control del observador
theta = 0.0
radius = 300


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
    pygame.display.set_caption("OpenGL: Carro")

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
    #objetos.append(OBJ("Chevrolet_Camaro_SS_Low.obj", swapyz=True))
    objetos.append(OBJ("Chasis.obj", swapyz=True))
    objetos.append(OBJ("Llantas_tr.obj", swapyz=True))
    objetos.append(OBJ("Llantas_ad.obj", swapyz=True))
    
    

    for i in range(len(objetos)): 
        objetos[i].generate()

#Se mueve al observador circularmente al rededor del plano XZ a una altura fija (EYE_Y)
def lookat():
    global EYE_X
    global EYE_Z
    global radius
    EYE_X = radius * (math.cos(math.radians(theta)) + math.sin(math.radians(theta)))
    EYE_Z = radius * (-math.sin(math.radians(theta)) + math.cos(math.radians(theta)))
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    
#Maquinas de dibujar
def displayChasis():
    glPushMatrix()
    # Mover y rotar el carrito según controles
    glTranslatef(Player_X, Player_Y, Player_Z)
    glRotatef(car_angle, 0.0, 1.0, 0.0)
    # Corrección para dibujar el objeto en plano XZ
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(0.0, 0.0, 15.0)
    glScale(10.0,10.0,10.0)
    objetos[0].render()
    glPopMatrix()
    
def displayLlantas_tr():
    glPushMatrix()
    # Mover y rotar el carrito
    glTranslatef(Player_X, Player_Y, Player_Z)
    glRotatef(car_angle, 0.0, 1.0, 0.0)
    # Corrección para dibujar el objeto en plano XZ
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(0.0, 0.0, 15.0)
    
    # Llantas traseras: giran sobre su propio eje X (no afectan el eje del carro)
    glPushMatrix()
    # Ajusta la posición local de las llantas traseras si es necesario
    glRotatef(wheel_angle, 1.0, 0.0, 0.0)
    
    glScale(10.0,10.0,10.0)
    objetos[1].render()
    glPopMatrix()
    glPopMatrix()
    
def displayLlantas_ad():
    glPushMatrix()
    # Mover y rotar las llantas según controles
    glTranslatef(Player_X, Player_Y, Player_Z)
    glRotatef(car_angle, 0.0, 1.0, 0.0)
    # Corrección para dibujar el objeto en plano XZ
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(0.0, 0.0, 15.0)
    glScale(10.0,10.0,10.0)
    objetos[2].render()
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
    
    #Se dibuja el Chasis
    displayChasis()
    
    #Se dibujan las llantas
    displayLlantas_tr()
    displayLlantas_ad()
    
done = False
Init()
move_speed = 1.0
turn_speed = 1.0
while not done:
    keys = pygame.key.get_pressed()
    # Controles observador (flechas)
    if keys[pygame.K_RIGHT]:
        if theta > 359.0:
            theta = 0
        else:
            theta += 1.0
        lookat()
    if keys[pygame.K_LEFT]:
        if theta < 1.0:
            theta = 360.0
        else:
            theta += -1.0
        lookat()
        
    if keys[pygame.K_UP]:
        if radius > 1.0:
            radius += -1.0
        lookat()
        
    if keys[pygame.K_DOWN]:
        if radius < 900.0:
            radius += 1.0
        lookat()

    # Controles Carro (WASD)
    # Calcular dirección actual del carrito
    rad = math.radians(car_angle)
    dir_x = math.sin(rad)
    dir_z = math.cos(rad)
    if keys[pygame.K_s]:
        Player_X += dir_x * move_speed
        Player_Z += dir_z * move_speed
        wheel_angle -= 5.0  # Incrementa el ángulo de las ruedas al retroceder
        if wheel_angle <= -360.0:
            wheel_angle += 360.0
    if keys[pygame.K_w]:
        Player_X -= dir_x * move_speed
        Player_Z -= dir_z * move_speed
        wheel_angle += 5.0  # Incrementa el ángulo de las ruedas al avanzar
        if wheel_angle >= 360.0:
            wheel_angle -= 360.0
    if keys[pygame.K_a]:
        car_angle += turn_speed
    if keys[pygame.K_d]:
        car_angle -= turn_speed

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

    display()
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()