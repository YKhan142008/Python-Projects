import random
from pygame_attributes import * 
from pygame.math import Vector2

width,height = 640,360
FPS = 30

pygame.init()

title('Flocking simulation')
clock = pygame.time.Clock()
screen = size(width,height)

 

class Boid:
    def __init__(self):
        self.pos = Vector2(random.uniform(0,width),random.uniform(0,height))
        self.velocity = random_2d(Vector2())
        length = random.uniform(2, 4)
        self.velocity.scale_to_length(length)
        self.acceleration = Vector2()
        self.max_force = 1
        self.max_speed = 4
    
    def edges(self):
        if self.pos.x > width:
            self.pos.x = 0 
        elif self.pos.x < 0:
            self.pos.x = width
        
        if self.pos.y > height:
            self.pos.y = 0 
        elif self.pos.y < 0:
            self.pos.y = height
    
    def align(self,boids):
        perceptionRadius = 50
        total = 0
        avg = Vector2()
        for boid in boids:
            d = self.pos.distance_to(boid.pos)
            if boid != self and d < perceptionRadius:
                avg += boid.velocity
                total += 1
        
        if total > 0:
            avg /= total
            avg.scale_to_length(self.max_speed)
            avg -= self.velocity
            limit_vector_magnitude(avg,self.max_force)
        return avg
    
    def cohesion(self,boids):
        perceptionRadius = 50
        total = 0
        avg = Vector2()
        for boid in boids:
            d = self.pos.distance_to(boid.pos)
            if boid != self and d < perceptionRadius:
                avg += boid.pos
                total += 1
        
        if total > 0:
            avg /= total
            avg -= self.pos
            avg.scale_to_length(self.max_speed)
            avg -= self.velocity
            limit_vector_magnitude(avg,self.max_force)
        return avg
    
    def separation(self,boids):
        perceptionRadius = 30
        total = 0
        avg = Vector2()
        for boid in boids:
            d = self.pos.distance_to(boid.pos)
            if boid != self and d < perceptionRadius:
                diff = self.pos - boid.pos
                diff /= d 
                avg += diff
                total += 1
        
        if total > 0:
            avg /= total
            avg.scale_to_length(self.max_speed)
            avg -= self.velocity
            limit_vector_magnitude(avg,self.max_force)
        return avg


    
    def flock(self,boids):
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)
        self.acceleration += separation
        self.acceleration += alignment
        self.acceleration += cohesion
     
    
    def update(self):
        self.pos += self.velocity
        self.velocity += self.acceleration
        limit_vector_magnitude(self.velocity,self.max_speed)
        self.acceleration *= 0

    def show(self):
        size = 8
        pygame.draw.ellipse(screen,'white',(self.pos.x,self.pos.y,size,size))

class Flock:
    def __init__(self,num_boids):
        self.flock = [Boid() for _ in range(num_boids)] 
    
    def show_flock(self):
        for boid in self.flock:
            boid.edges()
            boid.update()
            boid.show()
            boid.flock(self.flock)
    
flock = Flock(200)

def setup():
    while True:
        events = pygame.event.get()
        for event in events:
            close_on_click(event)
        screen.fill((51,51,51))
        flock.show_flock()
        game_update()
        clock.tick(FPS)
        
setup()
