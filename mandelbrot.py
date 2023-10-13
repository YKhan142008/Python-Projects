from pygame_attributes import *
import math 

width,height = 360,360

pygame.init()

screen = size(width,height)
surface = pygame.Surface((width,height),pygame.SRCALPHA)

def remap(value, old_min, old_max, new_min, new_max):
    return (value - old_min) * (new_max - new_min) / (old_max - old_min) + new_min

minval = -2.5
maxval = 2.5



def pixels():
    max_iterations = 50
    for i in range(width):
        for j in range(height):
            A = remap(i,0,width,minval,maxval)
            B = remap(j,0,height,minval,maxval)
            CA = A 
            CB = B
            z = 0
            for n in range(max_iterations):
                AA = A**2 - B**2 
                BB = 2*A*B 
                

                A = AA + CA
                B = BB + CB
                if abs(A**2 + B**2) > 16:
                    break
               
            
            bright = remap(n,0,max_iterations,0,1)
            bright = remap(math.sqrt(bright),0,1,0,255)
            if n == max_iterations - 1:
                bright = 0
          


            r,g,b,a = bright,bright,bright,255
            pygame.draw.rect(surface,(r,g,b,a),(i,j,1,1))
    screen.blit(surface,(0,0))

          
def setup():
    global minval,maxval
    while True:
        events = pygame.event.get()
        for event in events:
            close_on_click(event)
        
        screen.fill((0,0,0))
        pixels()
        pygame.display.flip()

setup()
