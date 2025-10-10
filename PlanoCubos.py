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
wheel_rotate = 0.0

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
    glShadeModel(GL_SMOOTH)
    #objetos.append(OBJ("Chevrolet_Camaro_SS_Low.obj", swapyz=True))
    objetos.append(OBJ("Chasis90.obj", swapyz=True)) #Necesario
    objetos.append(OBJ("Llantas_tr90.obj", swapyz=True)) #Necesario
    #objetos.append(OBJ("Llantas_tr.obj", swapyz=True)) #Antiguas
    objetos.append(OBJ("Llantas_ad90.obj", swapyz=True)) #Test
    objetos.append(OBJ("Llantas_ad_der.obj", swapyz=True))
    objetos.append(OBJ("Llanta_ad_iz.obj", swapyz=True))
    objetos.append(OBJ("Llantas0.obj", swapyz=True)) #Test

    
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
    
# Dibujado de Chasis con una matriz
#def displayChasis():
#    glPushMatrix()
#    glTranslatef(Player_X, Player_Y + 15.0, Player_Z)
#    #glTranslatef(0.0, 15.0, 0.0) #Ajusta la altura del chasis
#    glRotatef(car_angle, 0.0, 1.0, 0.0)
#    #glRotatef(-90.0, 1.0, 0.0, 0.0) #Rotar el chasis para que quede en plano XZ (Solo necesario para el chasis original)
#    glScale(10.0,10.0,10.0)
#    objetos[0].render()
#    glPopMatrix()


def displayChasis():
    glPushMatrix()
    # Conversión de ángulo y pre-cálculo de seno/coseno
    theta_rad = math.radians(car_angle)
    cos_theta = math.cos(theta_rad)
    sin_theta = math.sin(theta_rad)
    # Resultado algebraico de: T · Ry · S
    chasis_matrix = [
        10.0 * cos_theta,          
        0.0,                         
        -10.0 * sin_theta,          
        0.0,                         
        
        0.0,                         
        10.0,                        
        0.0,                         
        0.0,                         
        
        10.0 * sin_theta,           
        0.0,                         
        10.0 * cos_theta,           
        0.0,                        
        
        Player_X,                   
        Player_Y + 15.0,            
        Player_Z,                  
        1.0                          
    ]
    # Aplicar matriz colapsada
    glMultMatrixf(chasis_matrix)
    # Renderizar chasis
    objetos[0].render()
    glPopMatrix() 
    
    
    
# def displayLlantas_tr():
#     glPushMatrix()
#     # Mover y rotar el carrito
#     glTranslatef(Player_X, Player_Y + 15.0, Player_Z)
#     glRotatef(car_angle, 0.0, 1.0, 0.0)
#     # Corrección para dibujar el objeto en plano XZ
#     #glRotatef(-90.0, 1.0, 0.0, 0.0)
#     #glTranslatef(0.0, 0.0, 15.0)
#     glScale(10.0,10.0,10.0)
#     #Ajuste para rotar las llantas traseras sobre su eje
#     glTranslatef(0.0, -0.66, 2.56) #Ajusta al nuevo punto de referencia
#     glRotatef(wheel_angle, 1.0, 0.0, 0.0)
#     glTranslatef(0.0, 0.66, -2.56)# Regresa al origen
#     objetos[1].render()
#     glPopMatrix()


def displayLlantas_tr():
    glPushMatrix()

    # Pre-cálculos de ángulos en radianes
    theta = math.radians(car_angle)      # rotación del carro alrededor de Y
    phi   = math.radians(wheel_angle)    # rotación de la rueda alrededor de X

    c = math.cos(theta)
    s = math.sin(theta)
    C = math.cos(phi)
    S = math.sin(phi)

    # 3x3 = 10 * (R_y(theta) * R_x(phi))
    # R_y * R_x = [[ c,   s*S,   s*C],
    #              [ 0,    C,    -S ],
    #              [-s,  c*S,   c*C ]]
    m00 = 10.0 * c
    m10 = 0.0
    m20 = -10.0 * s
    m30 = 0.0

    m01 = 10.0 * (s * S)
    m11 = 10.0 * C
    m21 = 10.0 * (c * S)
    m31 = 0.0

    m02 = 10.0 * (s * C)
    m12 = -10.0 * S
    m22 = 10.0 * (c * C)
    m32 = 0.0

    # Cálculo de la traslación resultante (columna 3)
    # t_pivot = (0, -0.66, 2.56)
    # t_pivot_inv = (0, 0.66, -2.56)
    # d = 10 * R_y * t_pivot = [25.6*s, -6.6, 25.6*c]
    # adicional = 10 * (R_y*R_x) * t_pivot_inv
    # simplificación realizada en derivación
    tx_offset = s * (25.6 + 6.6 * S - 25.6 * C)
    ty_offset = 6.6 * (C - 1.0) + 25.6 * S
    tz_offset = c * (25.6 + 6.6 * S - 25.6 * C)

    tx = Player_X + tx_offset
    ty = Player_Y + 15.0 + ty_offset
    tz = Player_Z + tz_offset

    # Colocar en orden column-major para glMultMatrixf
    llanta_tr_matrix = [
        m00, m10, m20, m30,   # columna 0
        m01, m11, m21, m31,   # columna 1
        m02, m12, m22, m32,   # columna 2
        tx,  ty,  tz,  1.0    # columna 3 (traslación)
    ]

    # Aplicar matriz colapsada y renderizar
    glMultMatrixf(llanta_tr_matrix)
    objetos[1].render()

    glPopMatrix()


    
    
def displayLlantas_ad():
    glPushMatrix()
    # Mover y rotar las llantas según controles
    glRotatef(1.0, 1.0, wheel_rotate , 0.0)  #Giro de direccion 
    glTranslatef(Player_X, Player_Y + 15.0, Player_Z)
    glRotatef(car_angle, 0.0, 1.0, 0.0)
    # Corrección para dibujar el objeto en plano XZ
    #glRotatef(-90.0, 1.0, 0.0, 0.0)
 # Trasladar al eje de las llantas traseras (ajusta Z si es necesario)
    glTranslatef(0.0, -7.2, -32.2)  # Ajuste al nuevo origen
    glRotatef(wheel_angle, 1.0, 0.0, 0.0)
    glTranslatef(0.0, 7.2, 32.2)  # Ajuste al nuevo origen
    glScale(10.0,10.0,10.0)
    objetos[2].render()
    glPopMatrix()

#Maquinas de llantas delanteras
# def displayADder():
#     glPushMatrix()
#     glTranslatef(Player_X, Player_Y + 15.0, Player_Z) #15 es la altura del chasis
#     glRotatef(car_angle, 0.0, 1.0, 0.0)
#     # Aplicar rotación de dirección ANTES de mover al eje de la llanta
#     glTranslatef(0.0, 0.0, -15.0)  # Ajuste al nuevo origen
#     glRotatef(wheel_rotate, 0.0, 1.0, 0.0)  # Giro de dirección en eje Y
#     glTranslatef(0.0, 0.0, 15.0)  # Ajuste al nuevo origen
#  #Ajuste para rotar las llantas delanteras sobre su eje
#     glTranslatef(0.0, -7.2, -32.2)  # Ajuste al nuevo origen
#     glRotatef(wheel_angle, 1.0, 0.0, 0.0)  # Rotación de la llanta sobre su eje
#     glTranslatef(0.0, 7.2, 32.2)   # Regresa al origen
#     glScale(10.0,10.0,10.0)
#     objetos[3].render()
#     glPopMatrix()

def displayADder():
    glPushMatrix()

    # --- Parámetros (de tu código) ---
    # Traslación del jugador / chasis
    tx_player = Player_X
    ty_player = Player_Y + 15.0
    tz_player = Player_Z

    # Desplazamientos intermedios (según tu secuencia)
    # T_a = (0,0,-15)
    # después R_wheel_rotate (Y) y luego combinamos:
    # T_comb1 = T_b + T_c  con T_b=(0,0,15) y T_c=(0,-7.2,-32.2)
    # T_b + T_c = (0, -7.2, 15 - 32.2) = (0, -7.2, -17.2)
    t_comb1 = (0.0, -7.2, -17.2)
    # T_d = (0, 7.2, 32.2)
    t_d = (0.0, 7.2, 32.2)

    # Escala uniforme
    s = 10.0

    # Ángulos (convertir a radianes)
    theta = math.radians(car_angle)      # rotación del carro alrededor de Y
    phi   = math.radians(wheel_rotate)   # giro de dirección (Y)
    psi   = math.radians(wheel_angle)    # rotación de la llanta sobre X

    # Precomputados trigonométricos
    c_th = math.cos(theta);  s_th = math.sin(theta)
    c_ph = math.cos(phi);    s_ph = math.sin(phi)
    c_ps = math.cos(psi);    s_ps = math.sin(psi)

    # --- Construir matrices 4x4 (row-major) ---
    def mat_identity():
        return [[1.0,0.0,0.0,0.0],
                [0.0,1.0,0.0,0.0],
                [0.0,0.0,1.0,0.0],
                [0.0,0.0,0.0,1.0]]

    def mat_translate(t):
        tx,ty,tz = t
        M = mat_identity()
        M[0][3] = tx
        M[1][3] = ty
        M[2][3] = tz
        return M

    def mat_scale(k):
        return [[k,0.0,0.0,0.0],
                [0.0,k,0.0,0.0],
                [0.0,0.0,k,0.0],
                [0.0,0.0,0.0,1.0]]

    def mat_rotate_y(c,s):
        return [[ c, 0.0,  s, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [-s, 0.0,  c, 0.0],
                [0.0, 0.0, 0.0, 1.0]]

    def mat_rotate_x(c,s):
        return [[1.0, 0.0, 0.0, 0.0],
                [0.0,   c,  -s, 0.0],
                [0.0,   s,   c, 0.0],
                [0.0, 0.0, 0.0, 1.0]]

    def mat_mult(A,B):
        # A and B are 4x4 row-major lists -> return C = A * B (row-major)
        C = [[0.0]*4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                ssum = 0.0
                for k in range(4):
                    ssum += A[i][k] * B[k][j]
                C[i][j] = ssum
        return C

    # Matrices según la secuencia original:
    # M = T_player * R_y(theta) * T_a * R_y(phi) * T_comb1 * R_x(psi) * T_d * S
    T_player = mat_translate((tx_player, ty_player, tz_player))
    R_y_theta = mat_rotate_y(c_th, s_th)
    T_a = mat_translate((0.0, 0.0, -15.0))
    R_y_phi = mat_rotate_y(c_ph, s_ph)
    T_comb1 = mat_translate(t_comb1)   # (0, -7.2, -17.2)
    R_x_psi = mat_rotate_x(c_ps, s_ps)
    T_d = mat_translate(t_d)           # (0, 7.2, 32.2)
    S = mat_scale(s)

    # Multiplicaciones (en el orden indicado)
    M = mat_mult(T_player, mat_mult(R_y_theta,
            mat_mult(T_a, mat_mult(R_y_phi,
            mat_mult(T_comb1, mat_mult(R_x_psi,
            mat_mult(T_d, S)))))))

    # Convertir M (row-major) a lista column-major para glMultMatrixf
    mm = [
        M[0][0], M[1][0], M[2][0], M[3][0],
        M[0][1], M[1][1], M[2][1], M[3][1],
        M[0][2], M[1][2], M[2][2], M[3][2],
        M[0][3], M[1][3], M[2][3], M[3][3]
    ]

    # Aplicar la matriz colapsada y renderizar la llanta
    glMultMatrixf(mm)
    objetos[3].render()

    glPopMatrix()


def displayADizq():
    glPushMatrix()
    glTranslatef(Player_X, Player_Y + 15.0, Player_Z) #15 es la altura del chasis
    glRotatef(car_angle, 0.0, 1.0, 0.0)
    # Aplicar rotación de dirección ANTES de mover al eje de la llanta
    glTranslatef(0.0, 0.0, -15.0)  # Ajuste al nuevo origen
    glRotatef(wheel_rotate, 0.0, 1.0, 0.0)  # Giro de dirección en eje Y
    glTranslatef(0.0, 0.0, 15.0)  # Ajuste al nuevo origen
 #Ajuste para rotar las llantas delanteras sobre su eje
    glTranslatef(0.0, -7.2, -32.2)  # Ajuste al nuevo origen
    glRotatef(wheel_angle, 1.0, 0.0, 0.0)  # Rotación de la llanta sobre su eje
    glTranslatef(0.0, 7.2, 32.2)   # Regresa al origen
    glScale(10.0,10.0,10.0)
    objetos[4].render()
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
    #displayLlantas_ad()

   #Llantas delateras individuales
    displayADder()
    displayADizq()
    
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
        wheel_angle += 10.0  # Incrementa el ángulo de las ruedas al retroceder
        if wheel_angle <= -360.0:
            wheel_angle += 360.0
    if keys[pygame.K_w]:
        Player_X -= dir_x * move_speed
        Player_Z -= dir_z * move_speed
        wheel_angle -= 10.0  # Incrementa el ángulo de las ruedas al avanzar
        if wheel_angle >= 360.0:
            wheel_angle -= 360.0
    if keys[pygame.K_a]:
        car_angle += turn_speed
        wheel_rotate = 5.0  # Ajusta este valor para el ángulo de giro de las ruedas delanteras
    if keys[pygame.K_d]:
        car_angle -= turn_speed
        wheel_rotate = -5.0  # Ajusta este valor para el ángulo de giro de las ruedas delanteras
    if not (keys[pygame.K_a] or keys[pygame.K_d]):
        wheel_rotate = 0.0  # Vuelve las ruedas delanteras a la posición recta si no se gira

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

    display()
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()