from pygame_attributes import *
from constants import *




class Board:
    def __init__(self,):
        self.player = 1
        self.squares = [[0,0,0],
                        [0,0,0],
                        [0,0,0]]
    
    def available_moves(self):
        moves = list(map(lambda i: [(i, j) for j in range(ROWS) if self.squares[i][j] == 0], range(COLS)))
        return [move for sublist in moves for move in sublist]
    
    def mark_sqr(self,row,col):
        self.squares[row][col] = self.player
        
          
    def next_turn(self):
        self.player *= -1 
    
    def is_full(self):
        return len(self.available_moves()) == 0
    
    def final_state(self):
        
        for i in range(3):
            #horizontal win
            if self.squares[i][0] == self.squares[i][1] == self.squares[i][2] != 0:
                return self.squares[i][0]
            
            #vertical win
            if self.squares[0][i] == self.squares[1][i] == self.squares[2][i] != 0:
                return self.squares[0][i]
        
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[1][1]
        
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return self.squares[1][1]
    
    def reset(self):
        self.__init__()
 

def minimax(board,depth,alpha,beta,is_maximizing):

    if board.final_state() == 1:  
        return 1
    if board.final_state() == -1:
        return -1
    if board.is_full():
        return 0
    
    if is_maximizing:
        maxEval = -float('inf')
        for move in board.available_moves():
            board.squares[move[0]][move[1]] = 1
            eval = minimax(board,depth+1,alpha,beta,False)
            maxEval = max(maxEval,eval)
            alpha = max(alpha,eval)
            if beta <= alpha:
                board.squares[move[0]][move[1]] = 0
                break
            board.squares[move[0]][move[1]] = 0
        
        return maxEval

    
    else:   
        minEval = float('inf')
        for move in board.available_moves():
            board.squares[move[0]][move[1]] = -1
            eval = minimax(board,depth+1,alpha,beta,True)
            minEval = min(minEval,eval)
            beta = min(beta,eval)
            if beta <= alpha:
                board.squares[move[0]][move[1]] = 0
                break
            board.squares[move[0]][move[1]] = 0
        
        return minEval
    

def best_move(board):
    bestMove = None
    bestScore = -float('inf') 
    for move in board.available_moves():
        board.squares[move[0]][move[1]] = 1
        score = minimax(board,0,-float('inf'),float('inf'),False)
        board.squares[move[0]][move[1]] = 0
        if score > bestScore:
            bestScore = score
            bestMove = (move[0],move[1])
    return bestMove

   

class Game:
    def __init__(self):
        screen.fill(bg_color)
        self.board = Board()
        self.game_mode = 'pvp'
        self.draw_grid()
       
    
    def draw_grid(self):
        #horizontal lines
        aaline(screen,grid_color,(0,SQSIZE),(width,SQSIZE),grid_width)
        aaline(screen,grid_color,(0,SQSIZE*2),(width,SQSIZE*2),grid_width)

        #vertical lines
        aaline(screen,grid_color,(SQSIZE,0),(SQSIZE,height),grid_width)
        aaline(screen,grid_color,(SQSIZE*2,0),(SQSIZE*2,height),grid_width)
    
    def draw_player(self,row,col):
        shift = [SQSIZE*col,SQSIZE*row]
        if self.board.player == 1:
            aaline(screen,cross_color,(20+shift[0],20+shift[1]),(SQSIZE-20+shift[0],SQSIZE-20+shift[1]),line_width)
            aaline(screen,cross_color,(20+shift[0],SQSIZE-20+shift[1]),(SQSIZE-20+shift[0],20+shift[1]),line_width)
        else:
            pygame.draw.circle(screen,circle_color,(SQSIZE//2+shift[0],SQSIZE//2+shift[1]),radius,circ_width)
    
    def mode(self,mode):
        self.game_mode = mode
    
    def reset(self):
        screen.fill(bg_color)
        self.draw_grid()
        game_update()
        
     

pygame.init()
screen = size(width,height)

def main():
    ai_player = False
    game = Game()
    board = game.board
    game_over = False
    

    while True:
        events = pygame.event.get()
        for event in events:
            close_on_click(event)
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and not board.is_full():
                    move = board.available_moves()
                    pos = event.pos
                    row,col = pos[1] // SQSIZE ,pos[0] // SQSIZE
                    if (row,col) in move:
                        board.mark_sqr(row,col)
                        game.draw_player(row,col)
                        board.next_turn()
            if game.game_mode == 'ai':
                ai_player = True
            try:
                
                if ai_player and not game_over and not board.is_full():
                    move = board.available_moves()
                    row,col = best_move(board)
                    if (row,col) in move and board.player == 1:
                        board.mark_sqr(row,col)
                        game.draw_player(row,col)
                        board.next_turn()
                        ai_player = False
        
            
            except TypeError:
                pass
           
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                board.reset()
                game.reset()
                ai_player = False
                game_over = False
            
            if keys[pygame.K_a]:
                game.mode('ai')
            
            if keys[pygame.K_s]:
                game.mode('pvp')
            
           
            
        if board.final_state():
            game_over = True
        
        game_update()

if __name__ == '__main__':
    main()
