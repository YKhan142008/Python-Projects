from game_loop import GameLoop
import pygame
import math
import numpy as np

pygame.init()

MAX_VEL = 7
PADDLE_OFFSET = 10
player1_score = 0
player2_score = 0

class Ball:
      def __init__(self,x,y,color,width,height):
            self.x = x
            self.y = y
            self.color = color
            self.width = width
            self.height = height
            self.angle = np.random.uniform(-math.pi,math.pi)
            self.x_vel = MAX_VEL * math.cos(self.angle)
            self.y_vel = MAX_VEL * math.sin(self.angle)
            self.rect = None

      def draw_ball(self,screen):
            self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
            pygame.draw.rect(screen,self.color,self.rect,0,24)
      
      def update(self,game_loop):
            global player1_score,player2_score
            self.x += self.x_vel
            self.y += self.y_vel

            if self.y + self.height >= game_loop.height - 15 or self.y <= 15:
                  self.y_vel *= -1
            if self.x + self.width  >= game_loop.width:
                 self.reset(game_loop)
                 player2_score += 1
            if self.x <= 0:
                 self.reset(game_loop)
                 player1_score += 1
                 
      
      def reset(self,game_loop):
            self.x = game_loop.width // 2
            self.y = game_loop.height // 2

            angle = np.random.uniform(-math.pi/4,math.pi/4)
            self.x_vel = 5 * math.cos(angle)
            self.y_vel = 5 * math.sin(angle)
            
            
            

class Paddle:
      def __init__(self,x,y,color,width,height):
            self.x = x
            self.y = y
            self.color = color
            self.width = width
            self.height = height
            self.rect = None
            self.vel = 5
      
      def draw_paddle(self,screen):
            self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
            pygame.draw.rect(screen,self.color,self.rect)

      def update(self,game_loop):
            keys = pygame.key.get_pressed()

            if self.x >= game_loop.width - (self.width + PADDLE_OFFSET):
                  if keys[pygame.K_UP]:
                        self.y -= self.vel
                  if keys[pygame.K_DOWN]:
                        self.y += self.vel
            else:
                  if keys[pygame.K_w]:
                        self.y -= self.vel
                  if keys[pygame.K_s]:
                        self.y += self.vel
            
            if self.y <= 0:
                  self.y = 0
            elif self.y + self.height >= game_loop.height:
                  self.y = game_loop.height - self.height
            

def collisions(left_paddle,right_paddle,ball):
       right_paddle_collision = pygame.Rect.colliderect(right_paddle.rect,ball.rect)
       left_paddle_collision = pygame.Rect.colliderect(left_paddle.rect,ball.rect)
       if ball.x_vel < 0:
            if left_paddle_collision:
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                angle = math.radians(0-(difference_in_y))
                ball.x_vel = (MAX_VEL * math.cos(angle))
                ball.y_vel = (MAX_VEL * math.sin(angle))
       else:
            if right_paddle_collision:
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                angle = math.radians(180+(difference_in_y))
                ball.x_vel = (MAX_VEL * math.cos(angle))
                ball.y_vel = (MAX_VEL * math.sin(angle))
                

def draw_score(game_loop,screen,scores):
      font = pygame.font.Font(None,20)
      score1_rect = font.render(str(scores[0]),True,'white')
      score2_rect = font.render(str(scores[1]),True,'white')
      screen.blit(score1_rect,(((game_loop.width / 4)*3,10)))
      screen.blit(score2_rect,((game_loop.width / 4,10)))


def main():
    game_loop = GameLoop(600,400,(0,0,0),'Pong',60)
    screen = game_loop.screen
    width,height = game_loop.width,game_loop.height

    #Game objects
    ball = Ball(x=width//2,y=height//2,color=(255,255,255),width=24,height=24)
    right_paddle = Paddle(x=width-20-PADDLE_OFFSET,y=height//2-30,color=(255,255,255),width=20,height=100)
    left_paddle = Paddle(x=PADDLE_OFFSET,y=height//2-30,color=(255,255,255),width=20,height=100)

    while True:
            # game_loop functions
            game_loop.close_game()
            game_loop.fill()
            
            #updates
            ball.update(game_loop)
            right_paddle.update(game_loop)
            left_paddle.update(game_loop)

            #Drawing
            ball.draw_ball(screen)
            right_paddle.draw_paddle(screen)
            left_paddle.draw_paddle(screen)
            draw_score(game_loop,screen,[player1_score,player2_score])

            #collisons
            collisions(left_paddle,right_paddle,ball)
        
            pygame.display.update()
            game_loop.tick()

main()
