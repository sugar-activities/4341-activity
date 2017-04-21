# globals
import pygame,utils

app='Turtle Machine'; ver='1.0'
ver='1.1'
# 2 new patterns - 31 & 32
ver='1.2'
# circles added
# angle must be zero if repeat 1 used for basic shapes to be correct
#  - see convert(list1)
ver='1.3'
# my_turtle() only uses aaline if ok
ver='1.4'
# accept visually correct answers - see convert()
# removed g.clock.tick() in main loop when turtle running
ver='1.5'
# only draw last bit each time when zero delay - fast_start() & fast_do()
# turtle must be home to be correct - see convert()
# added frame rate to version display
# angler turtle rotated
ver='1.6'
# fixed for widescreen display
ver='1.7'
# show turtle when pattern ok but turtle not
# changed animation nos from 10/10 to 70/40
ver='1.8'
# changed animation nos back
# target pattern clickable when basic shapes all found
# left click-increases; right click-decreases
# sound removed

XO=True # affects the pygame.display.set_mode() call only
screen=None
pointer=None
w=800; h=600 # screen width & height - set dynamically on XO box
font1,font2=None,None
clock=None
factor=0.0 # measurement scaling factor (32x24 = design units)
offset=0 # we assume 4:3 - centre on widescreen
imgf=0.0 # image scaling factor - all images built for 1200x900
message=''
frame_rate=0; version_display=False

# this activity only
aim_n=0
slider=None
angles=[0,12,30,45,60,72,90,120,144]
repeats=[1,2,3,4,5,6,8,12,30]
repeat=1
repeat_cx,repeat_cy=0,0; text_rect=None
basic_shapes=[1,4,3,5,6,8,12,30] # of sides in polygon
basic_imgs=[]; basic_x,basic_y,basic_w,basic_h=0,0,0,0
shapes=[1] # added to as basic shapes found
shape=0 # shapes index
angle=90
level=4 # speed level on slider
utils.load()
checked=False

# images
bgd,magician,sparkle,glow=None,None,None,None

def init(): # called by main()
    global screen,w,h,pointer,font1,font2,clock,slider,bgd
    global magician,sparkle,glow
    global factor,offset,imgf,basic_x,basic_y,basic_w,basic_h
    global repeat_cx,repeat_cy
    pygame.init() # set up pygame
    pygame.display.set_caption(app+' Version '+ver)
    if XO:
        screen=pygame.display.set_mode(); w,h=screen.get_size()
    else:
        screen=pygame.display.set_mode((w,h))
    pygame.mouse.set_visible(False)
    if pygame.font:
        font1=pygame.font.Font(None,26)
        font2=pygame.font.Font(None,128)
    clock=pygame.time.Clock()
    factor=float(h)/24 # measurement scaling factor (32x24 = design units)
    offset=(w-4*h/3)/2 # we assume 4:3 - centre on widescreen
    imgf=float(h)/900 # image scaling factor - all images built for 1200x900
    pointer=utils.load_image('pointer.png',True)
    basic_x=sx(1.3); basic_y=sy(15)
    repeat_cx=sx(3.7); repeat_cy=sy(12.5)
    
    # this activity only
    global basic_imgs
    for n in basic_shapes:
        basic_imgs.append(utils.load_image(str(n)+'.png'))
    basic_w=basic_imgs[0].get_width(); basic_h=basic_imgs[0].get_height()
    slider=utils.Slider(sx(23),sy(20.8),6,utils.BLUE)
    bgd=utils.load_image('bgd.png',True)
    magician=utils.load_image('magician.png',True)
    sparkle=utils.load_image('sparkle.png',True)
    glow=utils.load_image('glow.png',True)

def sx(f): # scale x function
    return f*factor+offset

def sy(f): # scale y function
    return f*factor
