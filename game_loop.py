# The Game Loop is used for the pong game

import pygame,sys

pygame.init()

class GameLoop:
    def __init__(self,width,height,color,caption,FPS=0):
        self.width = width
        self.height = height
        self.caption = pygame.display.set_caption(caption)
        self.color = color
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.FPS = FPS
     
        
    
    def close_game(self):
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 pygame.quit()
                 sys.exit()
    
    def fill(self):
        self.screen.fill(self.color)
    
    def tick(self):
        clock = pygame.time.Clock()
        clock.tick(self.FPS)
    
