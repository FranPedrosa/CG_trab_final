'''
Nomes:                          Nusp:
Bruno Fernandes Moreira         11218712
Francisco de Freitas Pedrosa    11215699
Savio Duarte Fontes             10737251
Thales Willian Dalvi da Silva   11219196
'''
#Importação dos pacotes
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import glm
import math
import time

#importação dos outros arquivos que tem as demais funções
import codes
import load
import matrix
import keys

#definição dos parâmetros dos objetos
inds = []
objs = ['parede.obj'  ,'chao.obj','mesa.obj','xicara.obj' ,'porta.obj'     ,'grama.obj','estrada.obj','carta.obj','cogumelo.obj','lagarta.obj','ceu.obj' ]
texs = ['parede_3.jpg','chao.png','mesa.png','xicara.jpg' ,'porta.jpg'     ,'grama.jpg','estrada.jpg','carta.jpg','cogumelo.jpg','lagarta.jpg','ceu.jpg' ]
poss = [(0,0,0       ),(0,0,0   ),(15,0,0  ),(18.5,6.3,0 ),(0,30,0        ),(-30,30,0 ),(0,0,-90    ),(-5,0,-70 ),(10,40,1)     ,(-15,35,1   ),(0,0,-45 )]
scas = [(30,30,30    ),(30,30,30),(4,4,4   ),(0.5,0.5,0.5),(0.01,0.01,0.01),(2,2,2    ),(5,5,5      ),(5,5,5    ),(1,1,1)       ,(3,3,3      ),(30,30,30)]
rots = [(0,1,0       ),(0,1,0   ),(0,1,0   ),(0,1,0      ),(-1,0,0        ),(-1,0,0   ),(0,1,0      ),(0,1,0    ),(-1,0,0)      ,(-1,0,0     ),(0,1,0   )]
angs = [ 0            , 0        , 0        , 0           ,90              , 90        ,0           , 0         , 90           , 90          , 1         ]

#Váriaveis Globais que guardam todas as informações dos objetos
vertices_list = []    
normals_list = []    
textures_coord_list = []
begin = 0

buffs = None
program = None

#Função que vai inicializar a janela e já cria os Buffers do progrma
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

#Função que vai pegar os modelos dos arquivos .obj e adicionar seus parâmetros aos seus devidos arrays
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

#Função que manda os arrays para a gpu
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

#Função que manda todos os arrays de parâmetros para gpu
def all_gpu():
    send_gpu(vertices_list,3,0,'position')
    send_gpu(textures_coord_list,2,1,'texture_coord')
    send_gpu(normals_list,3,2,'normals')
    glEnable(GL_DEPTH_TEST)

#Função que renderiza o objeto de acordo com sua matriz modelo
def desenha_obj(mat_model,tex,indexes):
    begin, end = indexes
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
    glBindTexture(GL_TEXTURE_2D, tex)
    glDrawArrays(GL_TRIANGLES, begin,end-begin)

#Função que faz a animação do cenário, tanto a função do cogumelo crescendo e diminuindo e a função do zoom "especial"
def animation():
    t = time.time() - begin
    ft = 1+0.3*math.cos(t) 
    scas[8] = (1,ft,ft)

    if keys.zooming:
        print('a')
        t = 2*(time.time() - keys.zoom_begin)
        ft = math.sin(t) 
        matrix.camera_ang = 45 + ft*10
        matrix.cameraPos = keys.zoom_pos + ft*5*matrix.cameraFront
        if t >= (math.pi):
            keys.zooming = False
            matrix.camera_ang = 45
            matrix.camera_pos = keys.zoom_pos

#função que faz o loop enquanto a janela está aberta
def main_loop():

    glfw.poll_events() 

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.2, 0.2, 0.2, 1.0)

    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)

    animation()

    #renderiza os objetos nas posições deles
    for i in range(len(objs)):
        px,py,pz = poss[i]
        rx,ry,rz = rots[i]
        sx,sy,sz = scas[i]
        ang      = angs[i]
        mat_model = matrix.model(ang,rx,ry,rz,px,py,pz,sx,sy,sz)
        desenha_obj(mat_model,i,inds[i])

    #renderiza a matriz view
    mat_view = matrix.view()
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)

    #renderiza a matriz projection 
    mat_projection = matrix.projection()
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)    

    cpos = matrix.cameraPos
    loc_view_pos = glGetUniformLocation(program, "viewPos")
    glUniform3f(loc_view_pos, cpos[0], cpos[1], cpos[2])

    loc_view_pos = glGetUniformLocation(program, "lightPos")
    glUniform3f(loc_view_pos, cpos[0], cpos[1], cpos[2])
    
    glfw.swap_buffers(window)


#Função principal que chama todos os outros comandos do progrma
if __name__ == '__main__':

    begin = time.time()
    window = init_window(900,900,'Alice')

    #carregamento dos objetos
    for obj in objs:
        m = load.load_model(obj)
        inds.append( add_model(m))

    #carregamento das texturas
    i = 0
    for t in texs:
        load.load_texture(i,t)
        i+=1

    #criação dos buffers
    all_gpu()

    glfw.show_window(window)
    glfw.set_key_callback(window,keys.key_event)

    #loop da janela aberta
    while not glfw.window_should_close(window):
        main_loop()

    glfw.terminate()
