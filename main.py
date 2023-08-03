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
pygame.display.set_caption('Python Chess')
time = pygame.time.Clock()

# load in images for each piece
# en:User:Cburnett, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons
white_pawn = pygame.image.load('./images/white_pawn.png')
black_pawn = pygame.image.load('./images/black_pawn.png')
white_rook = pygame.image.load('./images/white_rook.png')
black_rook = pygame.image.load('./images/black_rook.png')
white_knight = pygame.image.load('./images/white_knight.png')
black_knight = pygame.image.load('./images/black_knight.png')
white_bishop = pygame.image.load('./images/white_bishop.png')
black_bishop = pygame.image.load('./images/black_bishop.png')
white_queen = pygame.image.load('./images/white_queen.png')
black_queen = pygame.image.load('./images/black_queen.png')
white_king = pygame.image.load('./images/white_king.png')
black_king = pygame.image.load('./images/black_king.png')

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
selected_x = +inf
selected_y = +inf
# valid_moves represents all valid playable moves of the selected piece as an array of x y tuples
valid_moves = []
# all_valid_moves represents all possible moves as an array of x y tuples, used when checking for check
all_valid_moves = []
# last_move, the latest played move stored as [piece, (previous_x, previous_y), (new_x, new_y)], used for en passant in pawn moves
last_move = []
# piece that is being promoted stored as [colour, (x, y)]
promoting_piece = []
# if castling is possible for each rook (e.g. 'wl' = left white rook)
castling_possibilities = {'wl': True, 'wr': True, 'bl': True, 'br': True}
# tuple of coordinates of checked king, empty otherwise
checked = ()

# used to draw black and white squares (to create the board)
def draw_board():
    offset_x = 0
    offset_y = 0
    row = 1
    window.fill((50, 50, 50))
    for i in range(8):
        if row % 2 == 0:
            offset_x += WIDTH / 8
        for j in range(4):
            pygame.draw.rect(window, 'white', pygame.Rect(offset_x, offset_y, (WIDTH / 8), (HEIGHT / 8)))
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
        pygame.draw.rect(window, 'yellow', [(selected_x * (WIDTH / 8)), (selected_y * (HEIGHT / 8)), (WIDTH / 8), (HEIGHT / 8)], 3)


# used to draw green outline of valid moves for the selected square
def draw_valid_moves():
    for i in range(len(valid_moves)):
        pygame.draw.rect(window, 'green', [(valid_moves[i][0] * (WIDTH / 8)), (valid_moves[i][1] * (HEIGHT / 8)), (WIDTH / 8), (HEIGHT / 8)], 2)


# used to draw red outline around king if in check
def draw_check():
    if checked:
        x = checked[0]
        y = checked[1]
        pygame.draw.rect(window, 'red', [x * (WIDTH / 8), y * (HEIGHT / 8), (WIDTH / 8), (HEIGHT / 8)], 2)


# used to draw promotion selection
def draw_promotion():
    pygame.draw.rect(window, (220, 220, 220), [WIDTH / 4, HEIGHT / 3, WIDTH / 2, HEIGHT / 8])
    offset = WIDTH / 4 + 10
    if promoting_piece[0] == 'w':
        selection = [white_knight, white_bishop, white_rook, white_queen]
    else:
        selection = [black_knight, black_bishop, black_rook, black_queen]
    for i in range(len(selection)):
        window.blit(selection[i], (offset, HEIGHT / 3 + 10))
        offset += WIDTH / 8
        if i < 3:
            pygame.draw.line(window, 'black', [offset - 11, HEIGHT / 3], [offset - 11, HEIGHT / 3 + HEIGHT / 8], 2)


# used draw winning message when win condition has been met
def draw_winning_message():
    pygame.draw.rect(window, 'black', [WIDTH / 4, HEIGHT / 3, WIDTH / 2, HEIGHT / 6])
    if winner == 'w':
        winning_message = font.render('White Player is the Winner!', False, 'white')
    else:
        winning_message = font.render('Black Player is the Winner!', False, 'white')
    window.blit(winning_message, ((WIDTH / 4) + 40, HEIGHT / 3 + (HEIGHT / 6) / 2))


# used to select the right "check moves" function for the currently selected piece
def check_valid_moves(x, y):
    valid = []
    piece = board_layout[y][x][2:]
    if piece == 'pawn':
        valid = check_pawn_moves(x, y)
    if piece == 'knight':
        valid = check_knight_moves(x, y)
    if piece == 'rook':
        valid = check_rook_moves(x, y)
    if piece == 'bishop':
        valid = check_bishop_moves(x, y)
    if piece == 'queen':
        valid = check_queen_moves(x, y)
    if piece == 'king':
        valid = check_king_moves(x, y)
    return valid


# used to find all playable moves
def check_all_valid_moves():
    valid = []
    for i in range(8):
        for j in range(8):
            valid += check_valid_moves(i, j)
    return valid


def check_pawn_moves(x, y):
    valid = []
    colour = board_layout[y][x][:1]
    if colour == 'w':
        if y != 0 and board_layout[y - 1][x] == '':
            valid.append((x, y - 1))
        if y == 6 and board_layout[y - 1][x] == '' and board_layout[y - 2][x] == '':
            valid.append((x, y - 2))
        if x != 0 and y != 0 and board_layout[y - 1][x - 1][:1] == 'b':
            valid.append((x - 1, y - 1))
        if x != 7 and y != 0 and board_layout[y - 1][x + 1][:1] == 'b':
            valid.append((x + 1, y - 1))
        # En Passant
        if y == 3 and board_layout[y][x + 1] == 'b_pawn' and last_move[1] == (x + 1, 1) and last_move[2] == (x + 1, 3):
            valid.append((x + 1, y - 1))
        if y == 3 and board_layout[y][x - 1] == 'b_pawn' and last_move[1] == (x - 1, 1) and last_move[2] == (x - 1, 3):
            valid.append((x - 1, y - 1))
    else:
        if y != 7 and board_layout[y + 1][x] == '':
            valid.append((x, y + 1))
        if y == 1 and board_layout[y + 1][x] == '' and board_layout[y + 2][x] == '':
            valid.append((x, y + 2))
        if x != 0 and y != 7 and board_layout[y + 1][x - 1][:1] == 'w':
            valid.append((x - 1, y + 1))
        if x != 7 and y != 7 and board_layout[y + 1][x + 1][:1] == 'w':
            valid.append((x + 1, y + 1))
        # En Passant
        if y == 4 and board_layout[y][x + 1] == 'w_pawn' and last_move[1] == (x + 1, 6) and last_move[2] == (x + 1, 4):
            valid.append((x + 1, y + 1))
        if y == 4 and board_layout[y][x - 1] == 'w_pawn' and last_move[1] == (x - 1, 6) and last_move[2] == (x - 1, 4):
            valid.append((x - 1, y + 1))
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
    # castling
    if x == 4:
        if castling_possibilities['wl'] and board_layout[y][x - 1] == '' and board_layout[y][x - 2] == '' and board_layout[y][x - 3] == '':
            valid.append((x - 4, y))
        if castling_possibilities['wr'] and board_layout[y][x + 1] == '' and board_layout[y][x + 2] == '':
            valid.append((x + 3, y))
        if castling_possibilities['bl'] and board_layout[y][x - 1] == '' and board_layout[y][x - 2] == '' and board_layout[y][x - 3] == '':
            valid.append((x - 4, y))
        if castling_possibilities['br'] and board_layout[y][x + 1] == '' and board_layout[y][x + 2] == '':
            valid.append((x + 3, y))
    return valid


# used to check if a piece has been chosen from the promotion selection and then return that piece
def promote_piece(x, y):
    if HEIGHT / 3 < y < HEIGHT / 3 + HEIGHT / 8:
        offset = 0
        selection = ['knight', 'bishop', 'rook', 'queen']
        # for each selection check the area that matches the options that appear on screen from draw_promotion
        for i in range(len(selection)):
            # if x is within boundaries of a piece change pawn at position stored in promoting piece to the piece clicked on and set promoting back to false
            if WIDTH / 4 + offset < x < WIDTH / 4 + WIDTH / 8 + offset:
                return selection[i]
            offset += WIDTH / 8
    return ''

# used to check if a king is currently in check
def check_check():
    for i in range(len(all_valid_moves)):
        x = all_valid_moves[i][0]
        y = all_valid_moves[i][1]
        piece = board_layout[y][x][2:]
        colour = board_layout[y][x][:1]
        if piece == 'king' and colour != turn:
            checked_position = (x, y)
            return checked_position


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


# turn, the current players turn
turn = 'w'
# valid_played, initially set to false as no move has been played yet
valid_played = False
# promoting, if pawn needs promoted set to true, initially set to false
promoting = False
# castled, true if castling has taken place in the current turn
castled = False
# winner, set as empty until a player has won
winner = ''

running = True

while running:
    time.tick(FPS)
    # draw everything onto window
    draw_board()
    draw_pieces()
    draw_selection()
    draw_valid_moves()
    draw_check()
    # if pawn needs promotion draw promotion selection window
    if promoting:
        draw_promotion()
    # if there is a winner draw the winning message
    if winner:
        draw_winning_message()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and not winner:
            # get mouse click position
            x = event.pos[0]
            y = event.pos[1]
            # if promoting a pawn check if within promotion selection window
            if promoting:
                promotion_selection = promote_piece(x, y)
                # if piece is selected set pawn stored at the location in promoting_piece equal to the chosen piece and set promoting back to false
                if promotion_selection:
                    board_layout[promoting_piece[1][1]][promoting_piece[1][0]] = promoting_piece[0] + '_' + promotion_selection
                    promoting = False
            # if not promoting a pawn continue with normal play
            else:
                # change mouse click position to coordinates on the board
                x = int(x // (WIDTH / 8))
                y = int(y // (HEIGHT / 8))
                piece_colour = board_layout[y][x][:1]
                # set valid_played and castled back to false
                valid_played = False
                castled = False
                # if a piece is already selected store selected piece details and check the coordinates are a valid move
                if 0 <= selected_x <= 7 and 0 <= selected_y <= 7:
                    for index in range(len(valid_moves)):
                        valid_x = valid_moves[index][0]
                        valid_y = valid_moves[index][1]
                        if x == valid_x and y == valid_y:
                            # if piece at coordinates is a king of the opposite colour set winner equal to turn
                            if board_layout[y][x][2:] == 'king' and board_layout[y][x][:1] != turn:
                                winner = turn
                            # if en passant opportunity taken set piece captured by en_passant to empty
                            if board_layout[selected_y][selected_x][2:] == 'pawn' and board_layout[y][x] == '' and selected_x != x:
                                if x > selected_x:
                                    board_layout[selected_y][selected_x + 1] = ''
                                else:
                                    board_layout[selected_y][selected_x - 1] = ''
                            # store move in last_move
                            last_move = [board_layout[selected_y][selected_x], (selected_x, selected_y), (x, y)]
                            # if castling move king 2 spaces towards rook and then place rook on the other side
                            if board_layout[selected_y][selected_x][2:] == 'king' and board_layout[y][x][2:] == 'rook':
                                if x == 0:
                                    board_layout[selected_y][selected_x - 2] = board_layout[selected_y][selected_x]
                                    board_layout[selected_y][selected_x - 1] = board_layout[y][x]
                                else:
                                    board_layout[selected_y][selected_x + 2] = board_layout[selected_y][selected_x]
                                    board_layout[selected_y][selected_x + 1] = board_layout[y][x]
                                board_layout[selected_y][selected_x] = ''
                                castled = True
                            # otherwise play normal move, set board_layout at coordinates to the selected piece and set the selected piece to an empty square
                            else:
                                board_layout[y][x] = board_layout[selected_y][selected_x]
                                board_layout[selected_y][selected_x] = ''
                            # if pawn reaches other side set promoting to true and store information about the promoting piece
                            if (y == 7 or y == 0) and board_layout[y][x][2:] == 'pawn':
                                promoting = True
                                promoting_piece = [turn, (x, y)]
                            # update castling possibilities
                            if board_layout[y][x][2:] == 'king' or board_layout[y][x][2:] == 'rook':
                                if board_layout[y][x] == 'w_king' or (selected_x == 0 and selected_y == 7):
                                    castling_possibilities['wl'] = False
                                if board_layout[y][x] == 'w_king' or (selected_x == 7 and selected_y == 7):
                                    castling_possibilities['wr'] = False
                                if board_layout[y][x] == 'b_king' or (selected_x == 0 and selected_y == 0):
                                    castling_possibilities['bl'] = False
                                if board_layout[y][x] == 'b_king' or (selected_x == 7 and selected_y == 0):
                                    castling_possibilities['br'] = False
                            # find all playable moves
                            all_valid_moves = check_all_valid_moves()
                            # check if king is in check after move has been played
                            checked = check_check()
                            # set valid played as move has been made
                            valid_played = True
                    # set selected back to infinite and valid moves to empty
                    selected_x = +inf
                    selected_y = +inf
                    valid_moves = []
                # if the colour of the piece selected equals the turn, set selected to coordinates and check valid moves at that position
                # will not be called when making valid move as cannot move to space where the colour of the piece is the same as the selected piece except for castling
                if turn == piece_colour and not castled:
                    selected_x = x
                    selected_y = y
                    valid_moves = check_valid_moves(selected_x, selected_y)
                # if a valid move has been played swap turns
                if valid_played:
                    if turn == 'w':
                        turn = 'b'
                    else:
                        turn = 'w'
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
                last_move = []
                promoting_piece = []
                castling_possibilities = {'wl': True, 'wr': True, 'bl': True, 'br': True}
                board_layout = reset_board()
        # stop running if window is quit
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
sys.exit()
