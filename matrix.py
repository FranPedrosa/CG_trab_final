#Arquivo com as definições das matrizes model, view e projection que são usadas no programa
import glm
import math
import numpy as np

cameraPos   = glm.vec3(0.0,  8.0,  0.0);
cameraFront = glm.vec3(0.0,  0.0,  -1.0);
cameraUp    = glm.vec3(0.0,  1.0,  0.0);

camera_ang = 45.0

#Função que retorna um bool sobre a posição da câmera num certo alcance
def close(x,z):
    return (abs(cameraPos[0] - x) < 3) and (abs(cameraPos[2] - z) < 3)

#Definição da matrix model que aplica todas as tranformações geométricas aos objetos
def model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z):

    angle = math.radians(angle)
    
    matrix_transform = glm.mat4(1.0) # instanciando uma matriz identidade
       
    # aplicando rotacao
    matrix_transform = glm.rotate(matrix_transform, angle, glm.vec3(r_x, r_y, r_z))
        
  
    # aplicando translacao
    matrix_transform = glm.translate(matrix_transform, glm.vec3(t_x, t_y, t_z))    
    
    # aplicando escala
    matrix_transform = glm.scale(matrix_transform, glm.vec3(s_x, s_y, s_z))
    
    matrix_transform = np.array(matrix_transform)
    
    return matrix_transform

#Definição da matrix view
def view():
    mat_view = glm.lookAt(cameraPos, cameraPos + cameraFront, cameraUp);
    mat_view = np.array(mat_view)
    return mat_view

#Definição da Matrix projection
def projection():
    # perspective parameters: fovy, aspect, near, far
    rad = math.radians(camera_ang)
    mat_projection = glm.perspective(rad, 1, 0.1, 1000.0)
    mat_projection = np.array(mat_projection)    
    return mat_projection
