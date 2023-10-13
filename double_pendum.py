from pygame_attributes import *
import numpy as np
import math
from math import cos,sin

#costants and variables
width,height = 600,400
bg_color = (255,255,255)
line_color = (0,0,0)

v1 = np.array([133,30])
v2 = np.array([133,30])


a1 = math.pi/4 
a2 = math.pi/4

a1_v = 0
a2_v = 0
g = 1
cx = width/2 
cy = 33

FPS = 60

max_trail_points = 1e12
trail_points1 = []
trail_points2 = []


#pygame attributes
pygame.init()

screen = size(width,height)

origin = (cx,cy)

clock = pygame.time.Clock()

def draw():
    global a1,a2,max_trail_points,a1_v,a2_v

    num1 = -g * (2*v1[1] + v2[1]) * sin(a1)
    num2 = -v2[1] * g * sin(a1 - 2 * a2) 
    num3 = -2*sin(a1-a2)*v2[1]
    num4 = a2_v**2 *v2[0] + a1_v**2*v1[0]*cos(a1-a2)
    den = v1[0] * (2*v1[1]+v2[1]-v2[1]*cos(2*a1-2*a2))
    
    a1_a = (num1 + num2 + num3*num4) / den
    Num1 = 2 * sin(a1 - a2)
    Num2 = (a1_v**2*v1[0]*(v1[1]+v2[1]))
    Num3 = g * (v1[1]+v2[1]) * cos(a1)
    Num4 = a2_v**2*v2[0]*v2[1]*cos(a1-a2)
    Den = v2[0] * (2*v1[1]+v2[1]-v2[1]*cos(2*a1-2*a2))
    
    a2_a = (Num1 * (Num2 + Num3 + Num4)) / Den
    
 


    x1 = (v1[0] * sin(a1))
    y1 = (v1[0] * cos(a1))

    x2 = x1 + v2[0] * sin(a2)
    y2 = y1 + v2[0] * cos(a2)

    start = np.array([0,0]) + origin
    end = np.array([x1,y1]) + origin

    start2 = np.array([x1,y1]) + origin
    end2 = np.array([x2,y2]) + origin 
    
    trail_points1.append(end)
    trail_points2.append(end2)


    if len(trail_points1) > max_trail_points:
        trail_points1.pop()
    elif len(trail_points2) > max_trail_points:
        print(True)
        trail_points2.pop()
    
    
    
    if len(trail_points1) == 0:
        trail_points1.append(end)
        trail_points2.append(end2)
    


    
   
    aaline(screen,line_color,start,end)
    aaline(screen,line_color,start2,end2)
    
    circ_center = (end[0],end[1])
    circ_center2 = (end2[0],end2[1])

    pygame.draw.circle(screen,line_color,circ_center,v1[1])
    pygame.draw.circle(screen,line_color,circ_center2,v1[1])
    for i in range(len(trail_points1) - 1):
        #aaline(screen,line_color,trail_points1[i],trail_points1[i+1])
        if (trail_points2[i] != trail_points2[i+1]).all():
            #pygame.draw.line(screen,line_color,trail_points2[i],trail_points2[i],10)
            aaline(screen,(255,0,0),trail_points2[i],trail_points2[i+1])
    #print(len(trail_points1))
   
    a1_v += a1_a 
    a2_v += a2_a
    a1 += a1_v 
    a2 += a2_v

    a1_v *= 0.9999
    a2_v *= 0.9999
    
   
def main():
    while True:
        for event in pygame.event.get():
            close_on_click(event)
        screen.fill(bg_color)
        draw()
        game_update()
        
        clock.tick(FPS)

main()
