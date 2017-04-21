# animate.py
import pygame,math

def sign(n):
    if n<0: return -1
    else: return 1

class Animation:
    def __init__(self,x1,y1,x2,y2,delay=10):
        dx=x2-x1; dy=y2-y1
        n=math.sqrt(dx*dx+dy*dy)/10 # no of steps
        if abs(dx)>abs(dy):
            f=abs(dx)/n; dy=dy/n; dx=sign(dx)*f
        else:
            f=abs(dy)/n; dx=dx/n; dy=sign(dy)*f
        self.x1=x1; self.x2=x2; self.y1=y1; self.y2=y2
        self.dx=dx; self.dy=dy; self.steps=int(n); self.delay=delay
        self.running=False; self.just_finished=False

    def start(self):
        self.x=self.x1; self.y=self.y1; self.ms=pygame.time.get_ticks()
        self.n=0; self.running=True; self.just_finished=False

    def do(self):
        d=pygame.time.get_ticks()-self.ms
        if d<0 or d>=self.delay:
            self.ms=pygame.time.get_ticks()
            self.n+=1
            if self.n>self.steps:
                self.x=self.x2; self.y=self.y2; self.running=False
                self.just_finished=True
            else:
                self.x+=self.dx; self.y+=self.dy
    
    
