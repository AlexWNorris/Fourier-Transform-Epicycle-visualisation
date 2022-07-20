from cmath import pi,exp
from math import atan2,sin,cos,sqrt
from time import sleep


from numpy import real

class creatFourierObject():
    num=0+0j
    frequency=0
    radius=0
    angleOffSet=0
    




def dftt(x):
    X=[]
    N=len(x)
    for i in range(N):
        X.append("")
    
    for k in range(N):
        re=0
        im=0
        for n in range(N):
            phi=(2*pi*k*n)/N
            re+=x[n]*cos(phi)
            im-=x[n]*sin(phi)
        re=re/N
        im=im/N

        freq=k
        amp=sqrt(re*re+im*im)
        phase=atan2(im,re)
        
        X[k]={"re":re,"im":im,"freq":freq,"amp":amp,"phase":phase}
    return X

def dfte(x):
    X=[]
    N=len(x)
    for i in range(N):
        X.append("")
    
    for k in range(N):
        num=0+0j
        for n in range(N):
            phi=(-1j*2*pi*k*n)/N
            num+=x[n]*exp(phi)
        num=num/N
        

        freq=k+1
        amp=sqrt(num.real*num.real+num.imag*num.imag)
        phase=atan2(num.imag,num.real)
        
        X[k]={"re":num.real,"im":num.imag,"freq":freq,"amp":amp,"phase":phase}
    return X

    
        
    




        


    