import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import glm
import math

import codes
import load
import matrix
import keys

objs = ['parede.obj','chao.obj','mesa.obj','frasco.obj','key.obj','bau.obj']
texts = ['parede.jpg','chao.png','mesa.png','frasco.png','key.jpg','bau.jpg']
pos = []
params = [[0,0,0,30],[0,0,0,30],[0,0,0,4],[4,5.8,0,5],[0,5.8,4,0.1],[20,0,2,0.1]]



vertices_list = []    
normals_list = []    
textures_coord_list = []

buffs = None
program = None

def init_window(width,height,name):
    global buffs, program
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
    window = glfw.create_window(width,height,name, None, None)
    glfw.make_context_current(window)

    program  = glCreateProgram()
    vertex   = glCreateShader(GL_VERTEX_SHADER)
    fragment = glCreateShader(GL_FRAGMENT_SHADER)

    glShaderSource(vertex, codes.vertex)
    glShaderSource(fragment, codes.fragment)

    for c in [vertex,fragment]:
        glCompileShader(c)
        if not glGetShaderiv(c, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(c).decode()
            print(error)
            raise RuntimeError("Erro de compilacao")

    glAttachShader(program, vertex)
    glAttachShader(program, fragment)

    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        print(glGetProgramInfoLog(program))
        raise RuntimeError('Linking error')
    
    glUseProgram(program)
    buffs = glGenBuffers(3)

    return window

def add_model(modelo):
    start = len(vertices_list)
    for face in modelo['faces']:
        for vertice_id in face[0]:
            vertices_list.append( modelo['vertices'][vertice_id-1] )
        for texture_id in face[1]:
            textures_coord_list.append( modelo['texture'][texture_id-1] )
        for normal_id in face[2]:
            normals_list.append( modelo['normals'][normal_id-1] )
    end = len(vertices_list)
    return start,end


def send_gpu(l, coords, num_buff, var_name):
    array = np.zeros(len(l), [("position", np.float32, coords)])
    array['position'] = l

    glBindBuffer(GL_ARRAY_BUFFER, buffs[num_buff])
    glBufferData(GL_ARRAY_BUFFER, array.nbytes, array, GL_STATIC_DRAW)
    stride = array.strides[0]
    offset = ctypes.c_void_p(0)
    loc = glGetAttribLocation(program, var_name)
    glEnableVertexAttribArray(loc)
    glVertexAttribPointer(loc, coords, GL_FLOAT, False, stride, offset)

def all_gpu():
    send_gpu(vertices_list,3,0,'position')
    send_gpu(textures_coord_list,2,1,'texture_coord')
    send_gpu(normals_list,3,2,'normals')
    glEnable(GL_DEPTH_TEST)

def desenha_obj(mat_model,ks,tex,pos):
    begin, end = pos
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
    
    loc_ka = glGetUniformLocation(program, "ka") # recuperando localizacao da variavel ka na GPU
    glUniform1f(loc_ka, ks[0]) ### envia ka pra gpu
    
    loc_kd = glGetUniformLocation(program, "kd") # recuperando localizacao da variavel kd na GPU
    glUniform1f(loc_kd, ks[1]) ### envia kd pra gpu    
    
    loc_ks = glGetUniformLocation(program, "ks") # recuperando localizacao da variavel ks na GPU
    glUniform1f(loc_ks, ks[2]) ### envia ks pra gpu        
    
    loc_ns = glGetUniformLocation(program, "ns") # recuperando localizacao da variavel ns na GPU
    glUniform1f(loc_ns, ks[3]) ### envia ns pra gpu        

    glBindTexture(GL_TEXTURE_2D, tex)
    glDrawArrays(GL_TRIANGLES, begin,end-begin)


def main_loop():
    glfw.poll_events() 

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.2, 0.2, 0.2, 1.0)

    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)


    for i in range(len(objs)):
        x,y,z,s = params[i]
        kss = [0.5,0.5,0.5,32]
        mat_model = matrix.model(0, 0,1,0, x,y,z, s,s,s)
        desenha_obj(mat_model,kss,i,pos[i])

    mat_view = matrix.view()
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)

    mat_projection = matrix.projection()
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)    

    cpos = matrix.cameraPos
    loc_view_pos = glGetUniformLocation(program, "viewPos")
    glUniform3f(loc_view_pos, cpos[0], cpos[1], cpos[2])
    
    glfw.swap_buffers(window)


if __name__ == '__main__':

    window = init_window(900,900,'Doginho')
    for obj in objs:
        m = load.load_model(obj)
        pos.append( add_model(m))

    i = 0
    for t in texts:
        load.load_texture(i,t)
        i+=1

    all_gpu()

    glfw.show_window(window)
    glfw.set_key_callback(window,keys.key_event)

    while not glfw.window_should_close(window):
        main_loop()

    glfw.terminate()

        
        
