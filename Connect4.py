import random
from turtle import screensize
import numpy as np              #used to rotate board orientation
import pygame
import sys
import math

# --------------------------------- GLOBAL VARIABLES --------------------------------- #

# colors
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

# size of screen and circles
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)

# rows and columns
ROW_COUNT = 6
COLUMN_COUNT = 7

# player and AI ints
PLAYER = 0
AI = 1

# player and AI piece ints
PLAYER_PIECE = 1
AI_PIECE = 2

# search window size and number of empty spaces in search window
WINDOW_LENGTH = 4
EMPTY = 0

# --------------------------------- DEFINITIONS --------------------------------- #

# creates board
def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

# places piece in board
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# checks whether location already has a piece in it
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

# finds the next open row
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# prints the board image
def print_board(board):
    # alters board orientation so coordinates 
    # start with (0,0) at the bottom left
    print(np.flip(board, 0))

# checks if the placement of a piece results in a win
def winning_move(board, piece):
    # check horizontal
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # check vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    
    # check rising diagonal
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    
    # check falling diagonal
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

# returns a score for evaluated window
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

# returns score for each evaluated column
# based on evaluated windows
def score_position(board, piece):
    score = 0

    #center column score
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3
    
    # horizontal score
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # vertical score
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # rising diagonal score
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)


    # falling fiagonal score
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

# returns true if the player can win, if the AI can win,
# or if there are no more valid locations
def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

# implementation of the minimax algorithm 
# to determine the best move for the AI
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -100000)
            else:   # game is over, no valid moves
                return (None, 0)
        else:       # depth == 0
            return (None, score_position(board, AI_PIECE))
    
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            # alpha beta pruning
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:   # minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            # alpha beta pruning
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

# returns remaining valid locations
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

# returns the column with the highest score for the AI to play
def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -1000
    best_col = random.choice(valid_locations)

    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    
    return best_col

# draws the board including the frame, wholes, and pieces already placed
def draw_board(board):
    # draws the board
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    # draws the pieces
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

# --------------------------------- GAME INITIATED --------------------------------- #

board = create_board()
print_board(board)
game_over = False

# initiates the connect 4 game
pygame.init()

# used for the screen orientation
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)

# "Go First" button placement
FIRST_BUTTON_TOP = height/2-50
FIRST_BUTTON_BOTTOM = height/2-10

# "Go Second" button placement
SECOND_BUTTON_TOP = height/2+50
SECOND_BUTTON_BOTTOM = height/2+90

# Dimensions of both buttons
BUTTON_LEFT_SIDE = width/2-75
BUTTON_RIGHT_SIDE = width/2+75
BUTTON_WIDTH = 150
BUTTON_LENGTH = 40

# sets the screen size and presents the board to the user
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

# font for text appearing after the game is won
winningFont = pygame.font.SysFont("monospace", 75)
# font appearing on the buttons
buttonFont = pygame.font.SysFont("monospace", int(SQUARESIZE/4))

# "Go First" button text
firstText = buttonFont.render('Go First', True, BLACK)
# "Go Second" button text
secondText = buttonFont.render('Go Second', True, BLACK)

# turn set to 2 until user decides whether 
# they would like to go first or second
turn = 2

# --------------------------------- TURN SELECTION --------------------------------- #

# loop terminates after user selects whether
# they would like to go first or second
while turn == 2:
    for event in pygame.event.get():
        # quit if user selects exit
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # user goes first if they click the "Go First" button
            if BUTTON_LEFT_SIDE <= mouse[0] <= BUTTON_RIGHT_SIDE and FIRST_BUTTON_TOP <= mouse[1] <= FIRST_BUTTON_BOTTOM:       
                turn = 0
            # user goes second if they click the "Go Second" button
            elif BUTTON_LEFT_SIDE <= mouse[0] <= BUTTON_RIGHT_SIDE and SECOND_BUTTON_TOP <= mouse[1] <= SECOND_BUTTON_BOTTOM:   
                turn = 1

    mouse = pygame.mouse.get_pos()

    # Start first button hover
    if BUTTON_LEFT_SIDE <= mouse[0] <= BUTTON_RIGHT_SIDE and FIRST_BUTTON_TOP <= mouse[1] <= FIRST_BUTTON_BOTTOM:
        pygame.draw.rect(screen, RED, [BUTTON_LEFT_SIDE, FIRST_BUTTON_TOP, BUTTON_WIDTH, BUTTON_LENGTH])
    else:
        pygame.draw.rect(screen, YELLOW, [BUTTON_LEFT_SIDE, FIRST_BUTTON_TOP, BUTTON_WIDTH, BUTTON_LENGTH])

    # Start second button hover
    if BUTTON_LEFT_SIDE <= mouse[0] <= BUTTON_RIGHT_SIDE and SECOND_BUTTON_TOP <= mouse[1] <= SECOND_BUTTON_BOTTOM:
        pygame.draw.rect(screen, RED, [BUTTON_LEFT_SIDE, SECOND_BUTTON_TOP, BUTTON_WIDTH, BUTTON_LENGTH])
    else:
        pygame.draw.rect(screen, YELLOW, [BUTTON_LEFT_SIDE, SECOND_BUTTON_TOP, BUTTON_WIDTH, BUTTON_LENGTH])
    
    # button text
    screen.blit(firstText, (BUTTON_LEFT_SIDE+10, FIRST_BUTTON_TOP+5))
    screen.blit(secondText, (BUTTON_LEFT_SIDE+5, SECOND_BUTTON_TOP+5))
    
    # updates the frames of the game
    pygame.display.update()

# --------------------------------- GAME BEGINS --------------------------------- #

while not game_over:
    for event in pygame.event.get():
        # quit if user selects exit
        if event.type == pygame.QUIT:
            sys.exit()

        # player piece appearance at top of board when it is the players turn
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

        pygame.display.update()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))

            #player 1 input
            if turn == PLAYER:
                posx = event.pos[0]
                # sets column to the column the player clicks over
                col = int(math.floor(posx/SQUARESIZE))

                # if column is valid, drops piece in next available row
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)
                    
                    # end game if move has won the game
                    if winning_move(board, PLAYER_PIECE):
                        label = winningFont.render("Player 1 Wins!!", 1, RED)
                        screen.blit(label, (10, 10))
                        game_over = True

                    turn += 1
                    turn = turn % 2

                    print_board(board)
                    draw_board(board)

    #AI input
    if turn == AI and not game_over:

        # sets column and minimax score to the minimax output
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

        # if column is valid, drops piece in next available row
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            # end game if move has won the game
            if winning_move(board, AI_PIECE):
                label = winningFont.render("Player 2 Wins!!", 1, YELLOW)
                screen.blit(label, (10, 10))
                game_over = True
            
            turn += 1
            turn = turn % 2
            
            print_board(board)
            draw_board(board)

            
    # pause after the game ends
    if game_over:
        pygame.time.wait(3000)