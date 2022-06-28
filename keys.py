import math
import glm

import matrix

ang = 0
speed = 1

inside = True
small = False

def colision(direction):
    x = matrix.cameraPos[0] + matrix.cameraFront[0]*direction
    w = matrix.cameraPos[2] + matrix.cameraFront[2]*direction
    if inside:
        return x > 29 or x < -29 or w > 29 or w < -29
    else:
        return x > 4 or x < -4 or w < -70 or w > -31

def key_event(window,key,scancode,action,mods):
    global ang,speed,small,inside
    if key == 65:
        ang -= math.pi/30
    if key == 68:
        ang += math.pi/30
    cos = math.cos(ang)
    sin = math.sin(ang)
    matrix.cameraFront = glm.vec3(sin, 0.0,-cos);
    if key == 87 and not colision(1):
        matrix.cameraPos += matrix.cameraFront * speed
    if key == 83 and not colision(-1):
        matrix.cameraPos -= matrix.cameraFront * speed
    if key == 32 and matrix.close(18.5,0):
        matrix.cameraPos[1] = 1
        speed = 0.2
        small = True
    if action == 1:
        if key == 32 and matrix.close(0,-28) and small and inside:
            matrix.cameraPos[0] = 0
            matrix.cameraPos[2] = -32
            inside = False
            return
        if key == 32 and matrix.close(0,-32) and small and not inside:
            matrix.cameraPos[0] = 0
            matrix.cameraPos[2] = -28
            inside = True
            return
    
