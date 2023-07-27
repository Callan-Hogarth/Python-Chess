import sys
from math import inf

import pygame
from pygame import *

pygame.init()

font = pygame.font.SysFont(None, 24)

# initiate width, height and fps constants
WIDTH = 600
HEIGHT = 600
FPS = 60

# set up window, caption and start clock
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Chess")
time = pygame.time.Clock()

# load in images for each piece
# en:User:Cburnett, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons
white_pawn = pygame.image.load("./images/white_pawn.png")
black_pawn = pygame.image.load("./images/black_pawn.png")
white_rook = pygame.image.load("./images/white_rook.png")
black_rook = pygame.image.load("./images/black_rook.png")
white_knight = pygame.image.load("./images/white_knight.png")
black_knight = pygame.image.load("./images/black_knight.png")
white_bishop = pygame.image.load("./images/white_bishop.png")
black_bishop = pygame.image.load("./images/black_bishop.png")
white_queen = pygame.image.load("./images/white_queen.png")
black_queen = pygame.image.load("./images/black_queen.png")
white_king = pygame.image.load("./images/white_king.png")
black_king = pygame.image.load("./images/black_king.png")

# initial board layout as 2d array
board_layout = [['b_rook', 'b_knight', 'b_bishop', 'b_queen', 'b_king', 'b_bishop', 'b_knight', 'b_rook'],
                ['b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn'],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn'],
                ['w_rook', 'w_knight', 'w_bishop', 'w_queen', 'w_king', 'w_bishop', 'w_knight', 'w_rook']]

# dictionary to match pieces in board_layout to piece images
pieces = {'w_pawn': white_pawn, 'w_rook': white_rook, 'w_knight': white_knight, 'w_bishop': white_bishop, 'w_queen': white_queen, 'w_king': white_king,
          'b_pawn': black_pawn, 'b_rook': black_rook, 'b_knight': black_knight, 'b_bishop': black_bishop, 'b_queen': black_queen, 'b_king': black_king}

# selected_x and selected_y used to identify which square is currently selected
# valid_moves represents all valid playable moves of the selected square as an array of x y tuples
# all_valid_moves represents all possible moves as an array of x y tuples
# checked tuple of coordinates of checked king empty otherwise
selected_x = +inf
selected_y = +inf
valid_moves = []
all_valid_moves = []
checked = ()


# used to draw black and white squares to create the board
def draw_board():
    offset_x = 0
    offset_y = 0
    row = 1
    window.fill((50, 50, 50))
    for i in range(8):
        if row % 2 == 0:
            offset_x += WIDTH / 8
        for j in range(4):
            pygame.draw.rect(window, "white", pygame.Rect(offset_x, offset_y, (WIDTH / 8), (HEIGHT / 8)))
            offset_x += WIDTH / 4
        offset_y += HEIGHT / 8
        row += 1
        offset_x = 0


# used to draw pieces onto the board from board_layout
def draw_pieces():
    offset_x = 0
    offset_y = 0
    for i in range(8):
        for j in range(8):
            tile = board_layout[i][j]
            if tile != '':
                window.blit(pieces[tile], (offset_x + 6, offset_y + 6))
            offset_x += WIDTH / 8
        offset_y += HEIGHT / 8
        offset_x = 0

# used to draw yellow outline around currently selected square
def draw_selection():
    if selected_x != +inf and selected_y != +inf:
        pygame.draw.rect(window, "yellow", [(selected_x * (WIDTH / 8)), (selected_y * (HEIGHT / 8)), (WIDTH / 8), (HEIGHT / 8)], 3)


# used to draw green outline of valid moves for the selected square
def draw_valid_moves():
    for i in range(len(valid_moves)):
        pygame.draw.rect(window, "green", [(valid_moves[i][0] * (WIDTH / 8)), (valid_moves[i][1] * (HEIGHT / 8)), (WIDTH / 8), (HEIGHT / 8)], 2)


# used to draw red outline around king if in check
def draw_check():
    if checked:
        x = checked[0]
        y = checked[1]
        pygame.draw.rect(window, "red", [x * (WIDTH / 8), y * (HEIGHT / 8), (WIDTH / 8), (HEIGHT / 8)], 2)


# used draw winning message when win condition has been met
def draw_winning_message():
    pygame.draw.rect(window, "black", [WIDTH / 4, HEIGHT / 3, WIDTH / 2, HEIGHT / 6])
    if winner == 'w':
        winning_message = font.render("White Player is the Winner!", False, "white")
    else:
        winning_message = font.render("Black Player is the Winner!", False, "white")
    window.blit(winning_message, ((WIDTH / 4) + 40, HEIGHT / 3 + (HEIGHT / 6) / 2))


# used to select the right check moves function for the currently selected piece
def check_valid_moves(x, y):
    valid = []
    piece = board_layout[y][x][2:]
    if piece == "pawn":
        valid = check_pawn_moves(x, y)
    if piece == "knight":
        valid = check_knight_moves(x, y)
    if piece == "rook":
        valid = check_rook_moves(x, y)
    if piece == "bishop":
        valid = check_bishop_moves(x, y)
    if piece == "queen":
        valid = check_queen_moves(x, y)
    if piece == "king":
        valid = check_king_moves(x, y)
    return valid

# used to find all playable moves
def check_all_valid_moves():
    valid = []
    for i in range(8):
        for j in range(8):
            valid += check_valid_moves(i, j)
    return valid

# used to check if a king is currently in check
def check_check():
    for i in range(len(all_valid_moves)):
        x = all_valid_moves[i][0]
        y = all_valid_moves[i][1]
        piece = board_layout[y][x][2:]
        colour = board_layout[y][x][:1]
        if piece == "king" and colour == turn:
            checked_position = (x, y)
            return checked_position


def check_pawn_moves(x, y):
    valid = []
    colour = board_layout[y][x][:1]
    if colour == 'w':
        if board_layout[y - 1][x] == '':
            valid.append((x, y - 1))
        if y == 6 and board_layout[y - 1][x] == '' and board_layout[y - 2][x] == '':
            valid.append((x, y - 2))
        if x != 0 and board_layout[y - 1][x - 1][:1] == 'b':
            valid.append((x - 1, y - 1))
        if x != 7 and board_layout[y - 1][x + 1][:1] == 'b':
            valid.append((x + 1, y - 1))
    else:
        if board_layout[y + 1][x] == '':
            valid.append((x, y + 1))
        if y == 1 and board_layout[y + 1][x] == '' and board_layout[y + 2][x] == '':
            valid.append((x, y + 2))
        if x != 0 and board_layout[y + 1][x - 1][:1] == 'w':
            valid.append((x - 1, y + 1))
        if x != 7 and board_layout[y + 1][x + 1][:1] == 'w':
            valid.append((x + 1, y + 1))
    return valid


def check_knight_moves(x, y):
    valid = []
    colour = board_layout[y][x][:1]
    if y + 2 <= 7 and x + 1 <= 7 and (board_layout[y + 2][x + 1] == '' or board_layout[y + 2][x + 1][:1] != colour):
        valid.append((x + 1, y + 2))
    if y + 1 <= 7 and x + 2 <= 7 and (board_layout[y + 1][x + 2] == '' or board_layout[y + 1][x + 2][:1] != colour):
        valid.append((x + 2, y + 1))
    if y - 2 >= 0 and x - 1 >= 0 and (board_layout[y - 2][x - 1] == '' or board_layout[y - 2][x - 1][:1] != colour):
        valid.append((x - 1, y - 2))
    if y - 1 >= 0 and x - 2 >= 0 and (board_layout[y - 1][x - 2] == '' or board_layout[y - 1][x - 2][:1] != colour):
        valid.append((x - 2, y - 1))
    if y + 2 <= 7 and x - 1 >= 0 and (board_layout[y + 2][x - 1] == '' or board_layout[y + 2][x - 1][:1] != colour):
        valid.append((x - 1, y + 2))
    if y - 2 >= 0 and x + 1 <= 7 and (board_layout[y - 2][x + 1] == '' or board_layout[y - 2][x + 1][:1] != colour):
        valid.append((x + 1, y - 2))
    if y + 1 <= 7 and x - 2 >= 0 and (board_layout[y + 1][x - 2] == '' or board_layout[y + 1][x - 2][:1] != colour):
        valid.append((x - 2, y + 1))
    if y - 1 >= 0 and x + 2 <= 7 and (board_layout[y - 1][x + 2] == '' or board_layout[y - 1][x + 2][:1] != colour):
        valid.append((x + 2, y - 1))
    return valid


def check_rook_moves(x, y):
    valid = []
    colour = board_layout[y][x][:1]

    i = 1
    while y + i <= 7 and board_layout[y + i][x] == '':
        valid.append((x, y + i))
        i += 1
    if y + i <= 7 and board_layout[y + i][x][:1] != colour:
        valid.append((x, y + i))

    i = 1
    while y - i >= 0 and board_layout[y - i][x] == '':
        valid.append((x, y - i))
        i += 1
    if y - i >= 0 and board_layout[y - i][x][:1] != colour:
        valid.append((x, y - i))

    i = 1
    while x + i <= 7 and board_layout[y][x + i] == '':
        valid.append((x + i, y))
        i += 1
    if x + i <= 7 and board_layout[y][x + i][:1] != colour:
        valid.append((x + i, y))

    i = 1
    while x - i >= 0 and board_layout[y][x - i] == '':
        valid.append((x - i, y))
        i += 1
    if x - i >= 0 and board_layout[y][x - i][:1] != colour:
        valid.append((x - i, y))
    return valid


def check_bishop_moves(x, y):
    valid = []
    colour = board_layout[y][x][:1]

    i = 1
    while y + i <= 7 and x + i <= 7 and board_layout[y + i][x + i] == '':
        valid.append((x + i, y + i))
        i += 1
    if y + i <= 7 and x + i <= 7 and board_layout[y + i][x + i][:1] != colour:
        valid.append((x + i, y + i))

    i = 1
    while y - i >= 0 and x - i >= 0 and board_layout[y - i][x - i] == '':
        valid.append((x - i, y - i))
        i += 1
    if y - i >= 0 and x - i >= 0 and board_layout[y - i][x - i][:1] != colour:
        valid.append((x - i, y - i))

    i = 1
    while y - i >= 0 and x + i <= 7 and board_layout[y - i][x + i] == '':
        valid.append((x + i, y - i))
        i += 1
    if y - i >= 0 and x + i <= 7 and board_layout[y - i][x + i][:1] != colour:
        valid.append((x + i, y - i))

    i = 1
    while y + i <= 7 and x - i >= 0 and board_layout[y + i][x - i] == '':
        valid.append((x - i, y + i))
        i += 1
    if y + i <= 7 and x - i >= 0 and board_layout[y + i][x - i][:1] != colour:
        valid.append((x - i, y + i))
    return valid


def check_queen_moves(x, y):
    rook_moves = check_rook_moves(x, y)
    bishop_moves = check_bishop_moves(x, y)
    valid = rook_moves + bishop_moves
    return valid


def check_king_moves(x, y):
    valid = []
    colour = board_layout[y][x][:1]
    if y + 1 <= 7 and (board_layout[y + 1][x] == '' or board_layout[y + 1][x][:1] != colour):
        valid.append((x, y + 1))
    if y - 1 >= 0 and (board_layout[y - 1][x] == '' or board_layout[y - 1][x][:1] != colour):
        valid.append((x, y - 1))
    if x + 1 <= 7 and (board_layout[y][x + 1] == '' or board_layout[y][x + 1][:1] != colour):
        valid.append((x + 1, y))
    if x - 1 >= 0 and (board_layout[y][x - 1] == '' or board_layout[y][x - 1][:1] != colour):
        valid.append((x - 1, y))
    if y + 1 <= 7 and x + 1 <= 7 and (board_layout[y + 1][x + 1] == '' or board_layout[y + 1][x + 1][:1] != colour):
        valid.append((x + 1, y + 1))
    if y - 1 >= 0 and x - 1 >= 0 and (board_layout[y - 1][x - 1] == '' or board_layout[y - 1][x - 1][:1] != colour):
        valid.append((x - 1, y - 1))
    if y - 1 >= 0 and x + 1 <= 7 and (board_layout[y - 1][x + 1] == '' or board_layout[y - 1][x + 1][:1] != colour):
        valid.append((x + 1, y - 1))
    if y + 1 <= 7 and x - 1 >= 0 and (board_layout[y + 1][x - 1] == '' or board_layout[y + 1][x - 1][:1] != colour):
        valid.append((x - 1, y + 1))
    return valid


# used to reset board to starting layout
def reset_board():
    r_board_layout = [['b_rook', 'b_knight', 'b_bishop', 'b_queen', 'b_king', 'b_bishop', 'b_knight', 'b_rook'],
                      ['b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn'],
                      ['', '', '', '', '', '', '', ''],
                      ['', '', '', '', '', '', '', ''],
                      ['', '', '', '', '', '', '', ''],
                      ['', '', '', '', '', '', '', ''],
                      ['w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn'],
                      ['w_rook', 'w_knight', 'w_bishop', 'w_queen', 'w_king', 'w_bishop', 'w_knight', 'w_rook']]
    return r_board_layout


running = True

# turn, the current players turn
# valid_played, initially set to false as no move has been played yet
# winner, set as empty until a player has won
turn = 'w'
valid_played = False
winner = ''

while running:
    time.tick(FPS)
    # draw everything onto window
    draw_board()
    draw_pieces()
    draw_selection()
    draw_valid_moves()
    draw_check()
    # if there is a winner draw the winning message
    if winner:
        draw_winning_message()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and not winner:
            # change mouse click position to coordinates on the board
            x = int(event.pos[0] // (WIDTH / 8))
            y = int(event.pos[1] // (HEIGHT / 8))
            # get piece colour from the first letter of the piece at the coordinates
            piece_colour = board_layout[y][x][:1]
            # set valid_played back to false
            valid_played = False
            # if a piece is already selected check the coordinates are a valid move
            if 0 <= selected_x <= 7 and 0 <= selected_y <= 7:
                for index in range(len(valid_moves)):
                    valid_x = valid_moves[index][0]
                    valid_y = valid_moves[index][1]
                    if x == valid_x and y == valid_y:
                        # if piece at coordinates is a king set winner equal to turn
                        if board_layout[y][x][2:] == 'king':
                            winner = turn
                        # set board_layout at coordinates to the selected piece and set the selected piece to an empty square, set valid_played to true
                        board_layout[y][x] = board_layout[selected_y][selected_x]
                        board_layout[selected_y][selected_x] = ''
                        valid_played = True
                # set selected back to infinite and valid moves to empty
                selected_x = +inf
                selected_y = +inf
                valid_moves = []
            # if the colour of the piece selected equals the turn, set selected to coordinates and check valid moves at that position
            # will not be called when making valid move as cannot move to space where the colour of the piece is the same as the selected
            if turn == piece_colour:
                print('hello')
                selected_x = x
                selected_y = y
                valid_moves = check_valid_moves(selected_x, selected_y)
            # if a valid move has been played swap turns
            if valid_played:
                if turn == 'w':
                    turn = 'b'
                else:
                    turn = 'w'
            # find all playable moves
            all_valid_moves = check_all_valid_moves()
            # check if king is in check
            checked = check_check()
        if event.type == KEYDOWN:
            # if r is pressed reset board to starting position
            if event.key == pygame.K_r:
                winner = ''
                turn = 'w'
                selected_x = +inf
                selected_y = +inf
                valid_moves = []
                all_valid_moves = []
                checked = ()
                board_layout = reset_board()
        # stop running if window is quit
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
sys.exit()
