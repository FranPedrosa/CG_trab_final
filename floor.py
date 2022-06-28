import random
import numpy as np

w = 10
h = 10

zs = np.zeros((w,h))

for x in range(w):
    for y in range(h):
        z = -2 if x == 6 else random.random()*2 
        z = -7 if x == 3 else random.random()*2
        print('v',x*3,y*3,z)
        zs[x,y] = z


for x in range(w):
    for y in range(h):
        if x < w-1 and y < h-1:
            v = [1, 0,zs[x+1,y] - zs[x,y]]
            u = [0 ,1,zs[x,y+1] - zs[x,y]]
            vu = np.cross(v,u)
            print('vn',vu[0],vu[1],vu[2])
        if x > 0 and y > 0:
            v = [-1, 0,zs[x-1,y] - zs[x,y]]
            u = [0 ,-1,zs[x,y-1] - zs[x,y]]
            vu = np.cross(v,u)
            print('vn',vu[0],vu[1],vu[2])

print('vt',0,0)
print('vt',0,1)
print('vt',1,1)


def pos(x,y):
    return str(x*w + y+1)


i = 1
for x in range(w):
    for y in range(h):
        if x < w-1 and y < h-1:
            a = pos(x,y)+'/1/'+str(i)
            b = pos(x+1,y)+'/2/'+str(i)
            c = pos(x,y+1)+'/3/'+str(i)
            print('f',a,b,c)
            i += 1
        if x > 0 and y > 0:
            a = pos(x,y)+'/1/'+str(i)
            b = pos(x-1,y)+'/2/'+str(i)
            c = pos(x,y-1)+'/3/'+str(i)
            print('f',a,b,c)
            i += 1



