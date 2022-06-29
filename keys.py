import math
import glm
import time

import matrix

ang = 0     #angulo para indicar a rotação do personagem - direita ou esquerda
speed = 1   #velocidade que o personagem anda

inside = True       #Boolean que indica se estamos do lado de dentro ou de fora do cenário
small = False       #Boolean que indica se o personagem está grande ou pequeno
zooming = False     #Boolean que indica se estamos aplicando o zoom "especial"

zoom_begin = None
zoom_pos = None

#Função colision() define se estamos no limite
#do mapa para impedir o personagem de passar os limites
def colision(direction):
    x = matrix.cameraPos[0] + matrix.cameraFront[0]*direction
    w = matrix.cameraPos[2] + matrix.cameraFront[2]*direction
    if inside:
        return x > 29 or x < -29 or w > 29 or w < -29
    else:
        return x > 4 or x < -4 or w < -70 or w > -31

#Função key_event() vai pegar os comandos do teclado e aplicar as funções esperadas
#W/S - Ir para frente/trás
#A/D - Girar para a direita/esquerda
#Barra de espaço - Interage com a xícara e encolhe o personagem
#Barra de espaço - Interage com a porta para fazer a troca entre os cenários interno e externo
#Z - Vai dar o zoom "especial"
def key_event(window,key,scancode,action,mods):
    global ang,speed,small,inside, zooming, zoom_pos, zoom_begin
    if zooming:
        return
    if key == 65:   #tecla A
        ang -= math.pi/30
    if key == 68:   #tecla D
        ang += math.pi/30
    cos = math.cos(ang)
    sin = math.sin(ang)
    matrix.cameraFront = glm.vec3(sin, 0.0,-cos);
    if key == 87 and not colision(1):   #Tecla W
        matrix.cameraPos += matrix.cameraFront * speed
    if key == 83 and not colision(-1):  #Tecla S
        matrix.cameraPos -= matrix.cameraFront * speed
    if key == 32 and matrix.close(18.5,0):  #Barra de espaço
        matrix.cameraPos[1] = 1
        speed = 0.2
        small = True
    if key == 90 and not colision(5):   #Tecla Z
        zoom_begin = time.time()
        zoom_pos = matrix.cameraPos
        zooming = True
    if action == 1:
        if key == 32 and matrix.close(0,-28) and small and inside:  #Barra de espaço
            matrix.cameraPos[0] = 0
            matrix.cameraPos[2] = -32
            inside = False
            return
        if key == 32 and matrix.close(0,-32) and small and not inside:  #Barra de espaço
            matrix.cameraPos[0] = 0
            matrix.cameraPos[2] = -28
            inside = True
            return
    
