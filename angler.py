#angler.py
import g,pygame,math,utils,my_turtle

class Angler:
    circle=utils.load_image('circle.png',True)

    def __init__(self,cx,cy,r):
        self.cx=g.sx(cx);self.cy=g.sy(cy);self.r=g.sy(r)

    def draw(self):
        k=100; colour=(k,k,k); w=int(g.sy(.16))
        x1=self.cx; y1=self.cy; r=self.r
        pygame.draw.line(g.screen,colour,(int(x1),int(y1-r)),(int(x1),int(y1+r)),w)
        for a in g.angles:
            rad=math.radians(a); x2=x1+r*math.sin(rad); y2=y1-r*math.cos(rad)
            if a==g.angle: colour=(0,255,0)
            pygame.draw.line(g.screen,colour,(int(x1),int(y1)),(int(x2),int(y2)),w)
            utils.centre_blit(g.screen,self.circle,(x2,y2))
            colour=(k,k,k)
            if a==g.angle:
                text=g.font1.render(str(a),True,(0,0,0))
                utils.centre_blit(g.screen,text,(x2,y2+2))
        imgr=pygame.transform.rotate(my_turtle.img,-g.angle)
        utils.centre_blit(g.screen,imgr,(x1,y1))

    def click(self):
        (mx,my)=pygame.mouse.get_pos()
        x1=self.cx; y1=self.cy; r=self.r
        circle_r=self.circle.get_width()/2
        for a in g.angles:
            rad=math.radians(a); x2=x1+r*math.sin(rad); y2=y1-r*math.cos(rad)
            rect=pygame.Rect(x2-circle_r,y2-circle_r,circle_r*2,circle_r*2)
            if rect.collidepoint(mx,my):
                g.angle=a; return True #****
        return False
            
