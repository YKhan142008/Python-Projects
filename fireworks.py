from pygame_attributes import *
from pygame.math import Vector2
import random

width,height = 600,450
bg_color = (51,51,51)

class Particle:
    def __init__(self,x,y,hu,size,firework=False):
        self.size = size
        self.hu = hu
        self.firework = firework
        self.pos = Vector2(x,y)
        self.vel = Vector2()
        self.lifespan = 255

        if self.firework:
            self.vel = Vector2(0,random.randrange(-12,-8))
           
        else:
            self.vel = random_2d(self.vel)
            self.vel *= random.randint(2,10)
        self.acc = Vector2()


    
    def apply_force(self,force):
        self.acc += force
    
    def update(self):
        if not self.firework:
            self.vel *= 0.9
            self.lifespan -= 4
        self.vel += self.acc 
        self.pos += self.vel 
        self.acc *= 0 
    
    def done(self):
        if self.lifespan < 0:
            return True 
        return False
    
    def show(self):
        if not self.firework:
            alpha = max(0,min(255,self.lifespan))
            color = (self.hu[0],self.hu[1],self.hu[2],alpha)
            self.size = 2
        else:
           color = self.hu
           
        pygame.draw.circle(surface,color,(int(self.pos.x),int(self.pos.y)),self.size)
    

class Firework:
    def __init__(self):
        self.hu = hsl_to_rgb((random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)))
        self.firework = Particle(random.uniform(8,width),height,self.hu,4,True)
        self.exploded = False
        self.particles = []
    
    def done(self):
        if self.exploded and len(self.particles) == 0:
            return True 
        return False

    def update(self,force):
        if not self.exploded:
            self.firework.apply_force(force)
            self.firework.update()
            if self.firework.vel.y >= 0:
                self.exploded = True
                self.explode()
        
        for i in range(len(self.particles)):
            if not self.done():
                try:
                    self.particles[i].apply_force(force)
                    self.particles[i].update()
                except IndexError:
                    break
            if self.particles[i].done() and len(self.particles) > 1:
                self.particles = self.particles[i:1]
                
                
   
    def explode(self):
        self.particles = [Particle(self.firework.pos.x,self.firework.pos.y,self.hu,4) for _ in range(100)]
      

    
    def show(self):
        if not self.exploded:
            self.firework.show()
        
    
        for i in range(len(self.particles)):
            self.particles[i].show()

pygame.init()

title('Fireworks!')

screen = size(width,height)
surface = pygame.Surface((width,height),pygame.SRCALPHA)
FPS = 60
clock = pygame.time.Clock()

fireworks = []
gravity = Vector2(0,0.2)

def update():
    if random.random() < 0.05:
        fireworks.append(Firework())
    for i in range(len(fireworks)):
        fireworks[i].update(gravity)
        fireworks[i].show()
        if fireworks[i].done():
           fireworks[i:1]
       # print(len(fireworks))


def setup():
    screen.fill((0,0,0))
    while True:
        for event in pygame.event.get():
            close_on_click(event)
        
        #screen.fill((51,51,51))
        surface.fill((0,0,0,25))
        update()
        screen.blit(surface,(0,0))
        clock.tick(FPS)
        game_update()
setup()
