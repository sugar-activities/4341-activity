# my_turtle.py
import g,pygame,math,utils,copy,buttons

img=utils.load_image("turtle.png",True)

class Turtle:

    def __init__(self,unit,side,(x,y)): #.03,16 for lge screen
         # unit=turtle unit (on 32x24 grid of course)
         # side=width of turtle screen
        self.top_left=(g.sx(x),g.sy(y)) # convert to pixels
        self.unit=g.sy(unit); self.side=g.sy(side); self.offset=self.side/2
         # turtle origin is at screen centre - hence the need fort offset
        self.screen=pygame.Surface((self.side,self.side))
        self.screen.fill((255,255,255))
        self.no_turtle_screen=copy.copy(self.screen)
        self.x=0.0; self.y=0.0; self.h=0.0; self.colour=(0,0,0)
        self.repeat=0; self.poly_n=1; self.angle=0; self.size=0 #program
        self.turtle_showing=True; self.delay=200
        self.ms=0; self.running=False; self.steps=0;
        self.complete=False; self.aaline_state=0# not tested yet, 1=ok -1=not ok

    def set_delay(self,delay):
        self.delay=delay
        
    def home(self):
        self.x=0.0; self.y=0.0; self.h=0.0
        
    def draw(self):
        g.screen.blit(self.screen,self.top_left)

    def cg(self):
        self.screen.fill((255,255,255))
        self.no_turtle_screen.fill((255,255,255))

    def fd(self,d):
        n=self.unit*d
        rad=math.radians(self.h)
        x1=self.x; y1=self.y;
        x2=x1+n*math.sin(rad); y2=y1-n*math.cos(rad)
        self.x=x2; self.y=y2
        x1+=self.offset; y1+=self.offset; x2+=self.offset; y2+=self.offset
        if self.aaline_state==1: # ok
            pygame.draw.aaline(self.screen,self.colour,(x1,y1),(x2,y2))
        elif self.aaline_state==-1: # not ok
            pygame.draw.line(self.screen,self.colour,(x1,y1),(x2,y2))
        else: # must be 1st time
            try:
                pygame.draw.aaline(self.screen,self.colour,(x1,y1),(x2,y2))
                self.aaline_state=1 #ok
            except:
                pygame.draw.line(self.screen,self.colour,(x1,y1),(x2,y2))
                self.aaline_state=-1 #not ok

    def rt(self,a):
        self.h+=a
        if self.h>=360: self.h-=360

    def set_program(self,list1):
        self.repeat,self.poly_n,self.angle,self.size=list1

    def get_program(self):
        return [self.repeat,self.poly_n,self.angle,self.size]

    def do(self):
        if self.running:
            if self.delay==0: self.fast_do(); return #**** 
            self.cg(); self.home()
            d=pygame.time.get_ticks()-self.ms
            if self.delay==0 or d<0 or d>=self.delay: #next step
                self.steps+=1; self.ms=pygame.time.get_ticks()
            n=self.poly_n; a=360/n; k=1
            for i in range(self.repeat):
                for j in range(n):
                    if self.steps==k: self.draw_turtle(); return #****
                    self.fd(self.size)
                    k+=1
                    if self.steps==k: self.draw_turtle(); return #****
                    self.rt(a)
                    k+=1
                    if self.steps==k: self.draw_turtle(); return #****
                self.rt(self.angle)
                k+=1
                if self.steps==k: self.draw_turtle(); return #****
            self.draw_turtle()
            self.running=False; self.steps=0; self.complete=True #finished

    def clear(self):
        self.cg(); self.home(); self.steps=0; self.running=False;
        self.draw_turtle(); buttons.on('turtle')
        
    def reset(self):
        self.steps=0; self.running=False; buttons.on('turtle')
        
    def start(self):
        self.running=True
        if self.steps==0:
            self.complete=False
            if self.delay==0: self.fast_start(); return #****
            self.cg(); self.home() 
            self.ms=pygame.time.get_ticks()-self.delay

    def stop(self):
        self.running=False

    def st(self):
        self.turtle_showing=True
            
    def ht(self):
        self.turtle_showing=False

    def draw_turtle(self):
        if self.turtle_showing:
            self.no_turtle_screen=copy.copy(self.screen)
            x=self.x+self.offset; y=self.y+self.offset
            imgr=pygame.transform.rotate(img,-self.h)
            utils.centre_blit(self.screen,imgr,(x,y))

    def draw_turtle_abs(self): # @ home
        x=self.offset+self.top_left[0]; y=self.offset+self.top_left[1]
        utils.centre_blit(g.screen,img,(x,y))

    def toggle_turtle(self):
        self.turtle_showing=not self.turtle_showing
        if self.turtle_showing:
            self.draw_turtle()
        else:
            self.screen=copy.copy(self.no_turtle_screen)
            
    def fast_do(self):
        if self.running:
            self.steps+=2
            self.fd(self.size)
            self.rt(self.a)
            self.j+=1
            if self.j==self.n:
                self.j=0
                self.rt(self.angle)
                self.i+=1
                if self.i==self.repeat:
                    self.draw_turtle(); buttons.on('turtle')
                    self.running=False; self.steps=0; self.complete=True #finished
                    #print pygame.time.get_ticks()-self.start_ms

    def fast_start(self):
        #self.start_ms=pygame.time.get_ticks()
        self.cg(); self.home()
        self.n=self.poly_n; self.a=360/self.n
        self.i=0; self.j=0
        buttons.off('turtle')
            
aims=[
#[1,1,0,183], #line
[4,1,90,183], #square
[3,1,120,240], #triangle
[5,1,72,155], #pentagon
[6,1,60,125], #hexagon
[8,1,45,100], #octagon
[12,1,30,64], #duodecagon
[30,1,12,27], #circle
[5,1,144,240], #star
[4,4,90,183], #panes
[8,4,45,183], #sq rotate 1

[6,4,60,183], #sq rotate 2
[6,3,60,240], #triangles
[3,3,120,240], #radiation symbol
[5,5,72,155], #pentagons
[4,6,90,125], #hexagons
[6,6,60,125], #hexagons
[8,8,45,100], #octagaons
[12,12,30,64], #duodecagons
[4,8,90,100],
[5,3,72,240],

[6,5,60,155],
[12,6,30,125],
[3,12,120,64],
[4,5,90,155],
[6,8,60,100],
[8,5,45,155],
[12,4,30,183],
[3,8,120,100],
[4,3,90,240],
[5,6,72,125],

[6,12,60,64],
[12,3,30,240],
[12,5,30,155],
[12,8,30,100],
[4,30,90,27],
[30,4,12,183],
[6,30,60,27],
[30,3,12,240],
[12,30,30,27],
[30,30,12,27]
]
                
