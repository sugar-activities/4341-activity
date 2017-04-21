# TurtleMachine.py
import g
g.init()
import my_turtle,angler,utils,pygame,buttons,animate
from pygame.locals import *

def display():
    aim.do()
    aim.draw()
    if not aim.running: aim.draw_turtle_abs()
    player.delay=100*(6-g.level)
    player.do()
    player.draw()
    g.screen.blit(g.basic_imgs[g.shape],(g.basic_x,g.basic_y))
    g.screen.blit(g.bgd,(g.sx(0),0))
    if buttons.active('cyan'):
        g.screen.blit(g.magician,(g.sx(1),g.sy(1.5)))
        utils.centre_blit(g.screen,g.sparkle,(g.sx(4.5),g.sy(3.1)))
    angler.draw()
    s=str(g.repeats[g.repeat]); c=(g.repeat_cx,g.repeat_cy)
    g.text_rect=utils.text_blit(g.screen,s,g.font2,c,(0,0,200))
    s=str(g.aim_n+1)+' / '+str(len(my_turtle.aims))
    utils.text_blit1(g.screen,s,g.font1,(g.sx(6.3),g.sy(8.3)),(0,0,255))
    buttons.draw()
    g.slider.draw()

def aim_setup():
    aim.set_program(my_turtle.aims[g.aim_n]); aim.ht()
    aim.set_delay(0); aim.start()

def player_start():
    if player.steps==0:
        n=g.shapes[g.shape]
        side=my_turtle.aims[g.aim_n][3]
        program=[g.repeats[g.repeat],n,g.angle,side]
        player.set_program(program)
        player.cg(); player.start()
    else:
        player.running=True

def next1():
    n=len(g.shapes)
    if n==len(g.basic_shapes): n=len(my_turtle.aims)
    g.aim_n+=1
    if g.aim_n==n: g.aim_n=0
    aim_setup()

def check():
    if player.complete:
        if convert(player.get_program())==aim.get_program():
            buttons.on('cyan')
            p=aim.get_program()
            if p[1]==1: # have basic shape
                n=p[0]
                if n not in g.shapes: g.shapes.append(n); anim.start()
        else:
            g.checked=True

def animation():
    if anim.running:
        anim.do(); anim_draw()
    elif anim.just_finished:
        anim.just_finished=False; anim_draw()
        pygame.display.flip()
        pygame.time.wait(300)

def anim_draw():
    last=len(g.shapes)-1
    dx=g.sx(.8);dy=g.sy(.8)
    g.screen.blit(g.glow,(anim.x-dx,anim.y-dy))
    g.screen.blit(g.basic_imgs[last],(anim.x,anim.y))

def convert(list1):
    aim1=aim.get_program()
    if list1[1]==aim1[1] and list1[2]==aim1[2] and list1[0]>aim1[0]:
        if abs(player.x)<1 and abs(player.y)<1 and abs(player.h)<1:
            return [aim1[0],list1[1],list1[2],list1[3]] # allow overdrawing
        else: # have overdrawing but turtle not ok
            player.st() # so player can see problem
            player.draw_turtle()
    elif list1[0]==1 and list1[2]==0:
        return [list1[1],1,360/list1[1],list1[3]]
    else:
        return list1

def shape_click(mouse_button):
    if utils.mouse_in(g.basic_x,g.basic_y,g.basic_w,g.basic_h):
        if mouse_button==2: return True # ignore middle button
        if mouse_button==1:
            g.shape+=1
            if g.shape==len(g.shapes): g.shape=0
        if mouse_button==3:
            g.shape-=1
            if g.shape<0: g.shape=len(g.shapes)-1 
        player.reset(); return True
    else: return False

def target_click(mouse_button):
    if utils.mouse_in(aim.top_left[0],aim.top_left[1],aim.side,aim.side):
        if len(g.shapes)>7:
            if mouse_button==2: return True # ignore middle button
            aim.clear()
            if mouse_button==1:
                g.aim_n+=1
                if g.aim_n==len(my_turtle.aims): g.aim_n=0
            if mouse_button==3:
                g.aim_n-=1
                if g.aim_n<0: g.aim_n=len(my_turtle.aims)-1
            aim_setup(); player.reset()
        return True
    else: return False

def repeat_click(mouse_button):
    if utils.mouse_in_rect(g.text_rect):
        if mouse_button==2: return True # ignore middle button
        if mouse_button==1:
            g.repeat+=1
            if g.repeat==len(g.repeats): g.repeat=0
        if mouse_button==3:
            g.repeat-=1
            if g.repeat<0: g.repeat=len(g.repeats)-1
        player.reset(); return True
    else: return False
        
def do_button(bu):
    if bu=='green': player_start(); g.checked=False
    elif bu=='red': player.stop()
    elif bu=='cyan': next1(); buttons.off('cyan')
    elif bu=='white': player.clear()
    elif bu=='turtle': player.toggle_turtle()

# initialisation
aim=my_turtle.Turtle(.014,8,(6,1))
aim_setup()
player=my_turtle.Turtle(.028,15,(15.5,1))
player.draw_turtle()
angler=angler.Angler(8,16.5,5)
# buttons
x=g.sx(4); y=g.sy(7.5)
buttons.Button("cyan",(x,y))
x=g.sx(18.6); y=g.sy(17.8); dx=(g.sx(27.6)-x)/3.0
buttons.Button("green",(x,y)); x+=dx
buttons.Button("red",(x,y)); x+=dx
buttons.Button("white",(x,y)); x+=dx
buttons.Button("turtle",(x,y))
buttons.off('cyan')
anim=animate.Animation(aim.top_left[0],aim.top_left[1],g.basic_x,g.basic_y)

def main():
    while True:
        ms=pygame.time.get_ticks()
        for event in pygame.event.get(): # check for app close
            if event.type==QUIT:
                utils.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN: # allow any button - left, right or middle
                button=event.button
                display(); pygame.display.flip() # no pointer in case button pressed
                anim.running=False
                if angler.click(): player.reset(); break
                if shape_click(button): break
                if target_click(button): break
                if repeat_click(button): break
                if g.slider.mouse():
                    if g.level==6: player.fast_start()
                    break
                bu=buttons.check()
                if bu<>'':do_button(bu)
            elif event.type==KEYDOWN:
                anim.running=False
                if event.key==K_ESCAPE: utils.exit()
                if event.key==K_x: g.version_display=not g.version_display
        display()
        if not g.checked: check()
        animation()
        if g.version_display:
            g.message=g.app+' Version '+g.ver
            g.message+='  '+str(g.w)+' x '+str(g.h)
            g.message+='  '+str(g.frame_rate)+'fps'
            utils.message(g.screen,g.font1,g.message)
        mx,my=pygame.mouse.get_pos()
        if my>g.pointer.get_height(): g.screen.blit(g.pointer,(mx,my))
        pygame.display.flip()
        if not player.running and not aim.running:
            g.clock.tick(40) # 40 frames per second
        d=pygame.time.get_ticks()-ms; g.frame_rate=int(1000/d)

if __name__=="__main__":
    main()
