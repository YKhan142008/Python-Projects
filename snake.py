import pygame,sys,random,os

WIDTH = 640
HEIGHT = 450

CELL_SIZE = 15

fruit_spawn = True
score = 0
x_dir = 0
y_dir = 0
snake_pos = [1,16]

def show_score(color,size):
    font = os.path.join('Font','kongtext.ttf')
    score_font = pygame.font.Font(font,size)
    score_surface = score_font.render(f'Score:{score}',True,color)
    score_rect = score_surface.get_rect()
    screen.blit(score_surface,score_rect)


clock = pygame.time.Clock()
snake_body = [
    [1,16],
    [2,16]
]
fruit_position = [random.randint(1,40),random.randint(1,28)]
direction = [1,0]
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and direction != [0,1]:
                direction = [0,-1]
            if event.key == pygame.K_a and direction != [1,0]:
                direction = [-1,0]
            if event.key == pygame.K_s and direction != [0,-1]:
                direction = [0,1]
            if event.key == pygame.K_d and direction != [-1,0]:
                direction = [1,0]
                
    snake_pos[0] += direction[0]
    snake_pos[1] += direction[1]      
    snake_body.insert(0,list(snake_pos))
    if snake_pos[0] == fruit_position[0] and snake_pos[1] == fruit_position[1]:
        score += 1
        fruit_spawn = False
    else:
        snake_body.pop()
         
    if not fruit_spawn:
        fruit_position = [random.randint(1, 40),
                          random.randint(1, 28)]
    fruit_spawn = True
    screen.fill('orange')
    for pos in snake_body:
                block_rect = pygame.Rect(pos[0]*CELL_SIZE,pos[1]*CELL_SIZE,CELL_SIZE,CELL_SIZE)
                pygame.draw.rect(screen,'white',block_rect)
    if snake_pos[0]*CELL_SIZE > WIDTH or snake_pos[1]*CELL_SIZE > HEIGHT or snake_pos[0]*CELL_SIZE < 0 or snake_pos[1]*CELL_SIZE < 0:
       sys.exit()
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            sys.exit()
        if block[0] == fruit_position[0] and block[1] == fruit_position[1]:
           fruit_spawn = False
    pygame.draw.rect(screen, 'red', pygame.Rect(
        fruit_position[0]*CELL_SIZE, fruit_position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    show_score('white',15)
    pygame.display.update()
    clock.tick(12)



