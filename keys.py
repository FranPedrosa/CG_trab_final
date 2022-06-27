import math
import glm

import matrix

ang = 0

def key_event(window,key,scancode,action,mods):
    global ang
    if key == 65:
        ang -= math.pi/30
    if key == 68:
        ang += math.pi/30
    cos = math.cos(ang)
    sin = math.sin(ang)
    matrix.cameraFront = glm.vec3(sin, 0.0,-cos);
    if key == 87:
        matrix.cameraPos += matrix.cameraFront
    if key == 83:
        matrix.cameraPos -= matrix.cameraFront
    
