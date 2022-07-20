from cmath import pi, sqrt
from dataclasses import replace
from time import sleep
from math import cos,sin
from FSAT import dftt
from re import findall
import pygame

pygame.init()
clock=pygame.time.Clock()
#visual constants

baseFont = pygame.font.Font(None, 32)
white=255,255,255
black=0,0,0
green=0,255,0
red=255,0,0

spinnerColor=green
drawingColor=white
connectorColor=green
#screen 
Sdims=Swidth,Shight=1024,1024
screen=pygame.display.set_mode(Sdims)
screenCentre=(Swidth/2,Shight/2)




spinnerObjects=[[],[]]
class spinner():
    def __init__(self,freq,phi,rad,plane,x,y):
        self.x,self.y=x,y
        self.rad=rad
        self.freq=freq
        self.angleOffset=phi
        if plane=="x":
            spinnerObjects[0].append(self)
        elif plane=="y":
            spinnerObjects[1].append(self)

    def drawSpinner(self):
        pygame.draw.circle(screen,spinnerColor,(self.x,self.y),self.rad,1)
       

    def updateSpinner(self):
        endx=self.x+self.rad*cos(self.angleOffset+t*self.freq*2*pi)
        endy=self.y+self.rad*sin(self.angleOffset+t*self.freq*2*pi)
        pygame.draw.line(screen,spinnerColor,(self.x,self.y),(endx,endy))
        

    def stack(self,index):
        targetX=index.x+index.rad*cos(index.angleOffset+t*index.freq*2*pi)
        targetY=index.y+index.rad*sin(index.angleOffset+t*index.freq*2*pi)
        self.x=targetX
        self.y=targetY

    def fetchEnd(self):
        endx=self.x+self.rad*cos(self.angleOffset+t*self.freq*2*pi)
        endy=self.y+self.rad*sin(self.angleOffset+t*self.freq*2*pi)
        return((endx,endy))

    def sortAll():
        global spinnerObjects
        def mergeSort(Clist):
            Llist=[]
            Rlist=[]
            middle=int(len(Clist)/2)
            if len(Clist)>1:
                Llist=Clist[:middle]
                Rlist=Clist[middle:]
                Llist=mergeSort(Llist)
                Rlist=mergeSort(Rlist)
                return merge(Llist,Rlist)
            else:
                return Clist

        def merge(listA,listB):
            output=[]
            while len(listA)>0 or len(listB)>0:
                try:
                    if listA[0].rad>listB[0].rad:
                        output.append(listA[0])
                        listA.pop(0)
                    else:
                        output.append(listB[0])
                        listB.pop(0)
                except IndexError:
                    if len(listA)==0:
                        output+=listB
                        listB=[]
                    if len(listB)==0:
                        output+=listA
                        listA=[]
    
            return output
        
        spinnerObjects=mergeSort(spinnerObjects)
def updateEnds():
    x=spinnerObjects[0][-1].fetchEnd()[0]
    y=spinnerObjects[1][-1].fetchEnd()[1]
    points.append((x,y))

def drawOutput():
    xSpinners=spinnerObjects[0][-1].fetchEnd()
    ySpinners=spinnerObjects[1][-1].fetchEnd()
    drawing=(xSpinners[0],ySpinners[1])
    if len(points)>2:
        pygame.draw.lines(screen,drawingColor,False,points)
    pygame.draw.line(screen,connectorColor,xSpinners,drawing)
    pygame.draw.line(screen,connectorColor,ySpinners,drawing)
def mathsFuntion():
    options=[-100-100j,-100+100j,100+100j,100-100j]
    output=[]
    for i in range(8):
        for n in range(1):
            output.append(options[i%4])
    return output
    
def fetchCoords(path):
    output=[]
    with open(path,'r') as file:
        fileContent=file.read()
    fileContent=findall("\[[0-9].*\]",fileContent)[0].split(",")
    for i in range(0,len(fileContent),2):
        re=float(fileContent[i].replace("[",""))
        im=1j*float(fileContent[i+1].replace("]",""))
        num=re+im
        output.append(num)
        
    return output

def start(signal):
    global dt
    xSignal=[]
    ySignal=[]
    for i in signal:
        xSignal.append(i.real)
        ySignal.append(i.imag)
    xFourierValues=dftt(xSignal)
    yFourierValues=dftt(ySignal)
    dt=1/len(signal)
    scaler=5
    for i in range(len(xFourierValues)):
        rad=xFourierValues[i]["amp"]/scaler
        freq=xFourierValues[i]["freq"]
        offSet=xFourierValues[i]["phase"]
        spinner(freq,offSet,rad,"x",Swidth*0.5,Shight*0.25)

    for i in range(len(yFourierValues)):
        rad=yFourierValues[i]["amp"]/scaler
        freq=yFourierValues[i]["freq"]
        offSet=yFourierValues[i]["phase"]
        spinner(freq,offSet+(pi/2),rad,"y",Swidth*0.15,Shight*0.5)
   
path=r"C:\Users/alexw\OneDrive\Desktop\coding shinanigans\python/fourier transformation/textCoords\heart.txt"
#game loop
t=0
dt=0.001
stop=True
points=[]
start(fetchCoords(path))
while True:
    screen.fill(black)
    for plane in (spinnerObjects):
        for i in range(len(plane)):
            if i >=1:
                plane[i].stack(plane[i-1])
            plane[i].drawSpinner()
            plane[i].updateSpinner()
    if len(spinnerObjects[0])>1 and len(spinnerObjects[1])>1:
        updateEnds()
        drawOutput()
    pygame.display.flip()
    if t==0:
        sleep(2)
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: 
                exit()
    t+=dt
    sleep(dt/2)
    
    
    

    
