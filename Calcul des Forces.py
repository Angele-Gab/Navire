import numpy as np

def ProdVect(u,v):

    wx=u[1]*v[2]-u[2]*v[1]
    wy=u[2]*v[0]-u[0]*v[2]
    wz=u[0]*v[1]-u[1]*v[0]
    w=np.array([wx,wy,wz])
    return(w)

A = np.array([0,0,0])
B = np.array([1,0,0])
C = np.array([0,0,1])
normale = np.array([0,1,0])

print("normale : ",normale)
constante = 1000 *9.81

ZA = A[2:]
ZB = B[2:]
ZC = C[2:]
Zfk = (ZA + ZB + ZC)/3

print("z : ",Zfk)

AB = np.array([(B[:1]-A[:1]),(B[1::2]-A[1::2]), ZB - ZA])
AC = np.array([(C[:1]-A[:1]),(C[1::2]-A[1::2]), ZC - ZA])

k=ProdVect(AB,AC)


surface2 = (((k[0])**2 +(k[1])**2 + (k[2])**2  ))**(1/2)

surface1 = surface2 /2


print("surface:",surface1)





Force1 = constante * Zfk
#print(Force1)
Force2 = Force1 * surface1
#print(Force2)
Force = Force2 * normale

print(Force)
