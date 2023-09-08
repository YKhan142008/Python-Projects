import pygame
import random
import time

pygame.init()
w,h = 640,480
screen = pygame.display.set_mode((w,h))

x = w / 2
y = h / 2

index = random.randrange(0,3)

rand_color_index = random.randrange(0,2)
rand_outline_index = random.randrange(0,2)



color_value = [100,255]

SNAKE_COLOR = [0,0,0]
SNAKE_OUTLINE = [0,0,0]

SNAKE_COLOR[random.randrange(0,3)] = color_value[rand_color_index]
SNAKE_OUTLINE[random.randrange(0,3)] = color_value[rand_outline_index]
BG_COLOR = (0,0,0)

class Snake:
    def __init__(self,x,y,color,outline):
        self.size = 20
        self.color = color
        self.x = x
        self.y = y
        self.outline = outline
       
  
        
        self.head = [x,y]
        self.body = [self.head,[self.x-self.size,self.y],[self.x-self.size*2,self.y]]
        self.direction = 'right'
        self.score = 0
        self.scores = []
        
        self.fruit = [random.randrange(0,w//self.size)*self.size,random.randrange(0,h//self.size)*self.size]
        
    def high_score(self):
        self.scores.append(self.score)
        record = max(self.scores)
        return record

    
    def reset(self,x,y,color,outline):

        SNAKE_COLOR[random.randrange(0,3)] = color_value[rand_color_index]
        SNAKE_OUTLINE[random.randrange(0,3)] = color_value[rand_outline_index]

        self.size = 20
        self.color = color
        self.x = x
        self.y = y
        self.outline = outline
  
        
        self.head = [x,y]
        self.body = [self.head,[self.x-self.size,self.y],[self.x-self.size*2,self.y]]
        self.direction = 'right'
        self.score = 0

        self.fruit = [random.randrange(0,w//self.size)*self.size,random.randrange(0,h//self.size)*self.size]
        

        
    
    
    
    def draw_snake(self):
        
        for block in self.body:
            x = block[0]
            y = block[1]
            pygame.draw.rect(screen,self.color,pygame.Rect(x,y,self.size,self.size))
            pygame.draw.rect(screen,self.outline,pygame.Rect(x,y,self.size,self.size),4)
    
    def move_snake(self):
        x = self.head[0]
        y = self.head[1]
        
        if self.direction == 'right':
            x += self.size
        if self.direction == 'left':
            x -= self.size
        if self.direction == 'down':
            y += self.size
        if self.direction == 'up':
            y -= self.size
        
        self.head = [x,y]
    
    def draw_fruit(self):
        if self.fruit in self.body:
            x = random.randrange(0,w//self.size)*self.size
            y = random.randrange(0,h//self.size)*self.size

            self.fruit = [x,y]

        pygame.draw.rect(screen,'red',pygame.Rect(self.fruit[0],self.fruit[1],self.size,self.size))
    
    def blit_score(self,s):
        scores = []
        scores.append(s)
        font = pygame.font.Font('Arimo-Regular.ttf',25)
        score = font.render(f'Score: {s} High Score: {self.high_score()}',True,'white')
        screen.blit(score,[0,0])
    
    
    
    def game_over(self):
        x = self.head[0]
        y = self.head[1]
        
        if x > w - self.size or x < 0 or y > h - self.size or y < 0:
            return True
        
        if self.head in self.body[1:]:
            return True




def play():
    x = w / 2
    y = h / 2
    snake = Snake(x,y,SNAKE_COLOR,SNAKE_OUTLINE)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and snake.direction != 'left':
                    snake.direction = 'right'
                if event.key == pygame.K_LEFT and snake.direction != 'right':
                    snake.direction = 'left'
                if event.key == pygame.K_DOWN and snake.direction != 'up':
                    snake.direction = 'down'
                if event.key == pygame.K_UP and snake.direction != 'down':
                    snake.direction = 'up'
        
        
        
        if snake.game_over():
            time.sleep(0.5)
            snake.reset(x,y,SNAKE_COLOR,SNAKE_OUTLINE)
    
        screen.fill(BG_COLOR)
        snake.draw_snake()
        snake.draw_fruit()
        snake.move_snake()
        

        snake.body.insert(0,snake.head)

        if snake.head == snake.fruit:
            snake.draw_fruit()
            snake.score += 1
        else:
            snake.body.pop()
      
        snake.blit_score(snake.score)
        pygame.display.update()
        clock.tick(10)

play()




        
