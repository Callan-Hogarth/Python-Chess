import sys
import copy
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
# moves_list represents all  playable moves of the selected piece as an array of x y tuples
moves_list = []
# last_move, the latest played move stored as [piece, (previous_x, previous_y), (new_x, new_y)], used for en passant in pawn moves
last_move = []
# piece that is being promoted stored as [colour, (x, y)]
promoting_piece = []
# if castling is possible for each rook (e.g. 'wl' = left white rook)
castling_possibilities = {'wl': True, 'wr': True, 'bl': True, 'br': True}
# tuple of coordinates of checked king, empty otherwise
checked = ()
# if checkmate has occurred
checkmate = False


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
def draw_moves():
    for i in range(len(moves_list)):
        pygame.draw.rect(window, 'green', [(moves_list[i][0] * (WIDTH / 8)), (moves_list[i][1] * (HEIGHT / 8)), (WIDTH / 8), (HEIGHT / 8)], 2)


# used to draw red outline around king if in check
def draw_check():
    if checked:
        check_x = checked[0]
        check_y = checked[1]
        pygame.draw.rect(window, 'red', [check_x * (WIDTH / 8), check_y * (HEIGHT / 8), (WIDTH / 8), (HEIGHT / 8)], 2)


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
    elif winner == 'b':
        winning_message = font.render('Black Player is the Winner!', False, 'white')
    else:
        winning_message = font.render('Draw', False, 'white')
    window.blit(winning_message, ((WIDTH / 4) + 40, HEIGHT / 3 + (HEIGHT / 6) / 2))


# used to switch turn
def switch_turn(t):
    if t == 'w':
        return 'b'
    else:
        return 'w'


# used to select the right "get moves" function for the currently selected piece
def get_moves(x, y, board):
    moves = []
    piece = board[y][x][2:]
    if piece == 'pawn':
        moves = get_pawn_moves(x, y, board)
    if piece == 'knight':
        moves = get_knight_moves(x, y, board)
    if piece == 'rook':
        moves = get_rook_moves(x, y, board)
    if piece == 'bishop':
        moves = get_bishop_moves(x, y, board)
    if piece == 'queen':
        moves = get_queen_moves(x, y, board)
    if piece == 'king':
        moves = get_king_moves(x, y, board)
    return moves


# used to get all possible moves for the current players turn (t)
def get_all_moves(board, t):
    all_moves = []
    for i_y in range(8):
        for i_x in range(8):
            if board[i_y][i_x][:1] == t:
                current_moves = get_moves(i_x, i_y, board)
                for m in range(len(current_moves)):
                    all_moves.append([board[i_y][i_x], (i_x, i_y), current_moves[m]])
    return all_moves


# used to get all valid moves, where not in check after turn
def get_all_valid_moves(board, t):
    board_copy = copy.deepcopy(board)
    all_moves = get_all_moves(board, t)
    valid = []
    for i in range(len(all_moves)):
        board = copy.deepcopy(board_copy)
        board = make_move(board, all_moves[i][1][0], all_moves[i][1][1], all_moves[i][2][0], all_moves[i][2][1])
        t = switch_turn(t)
        new_moves = get_all_moves(board, t)
        check = check_check(board, new_moves, t)
        t = switch_turn(t)
        if not check:
            valid.append(all_moves[i])
    return valid


# used to get moves for the  selected piece from a list of moves
def get_selected_moves(all_moves, sel_x, sel_y):
    selected_moves = []
    for i in range(len(all_moves)):
        if all_moves[i][1] == (sel_x, sel_y):
            selected_moves.append(all_moves[i][2])
    return selected_moves


def get_pawn_moves(x, y, board):
    valid = []
    colour = board[y][x][:1]
    if colour == 'w':
        if y != 0 and board[y - 1][x] == '':
            valid.append((x, y - 1))
        if y == 6 and board[y - 1][x] == '' and board[y - 2][x] == '':
            valid.append((x, y - 2))
        if x != 0 and y != 0 and board[y - 1][x - 1][:1] == 'b':
            valid.append((x - 1, y - 1))
        if x != 7 and y != 0 and board[y - 1][x + 1][:1] == 'b':
            valid.append((x + 1, y - 1))
        # En Passant
        if y == 3 and board[y][x + 1] == 'b_pawn' and last_move[1] == (x + 1, 1) and last_move[2] == (x + 1, 3):
            valid.append((x + 1, y - 1))
        if y == 3 and board[y][x - 1] == 'b_pawn' and last_move[1] == (x - 1, 1) and last_move[2] == (x - 1, 3):
            valid.append((x - 1, y - 1))
    else:
        if y != 7 and board[y + 1][x] == '':
            valid.append((x, y + 1))
        if y == 1 and board[y + 1][x] == '' and board[y + 2][x] == '':
            valid.append((x, y + 2))
        if x != 0 and y != 7 and board[y + 1][x - 1][:1] == 'w':
            valid.append((x - 1, y + 1))
        if x != 7 and y != 7 and board[y + 1][x + 1][:1] == 'w':
            valid.append((x + 1, y + 1))
        # En Passant
        if y == 4 and board[y][x + 1] == 'w_pawn' and last_move[1] == (x + 1, 6) and last_move[2] == (x + 1, 4):
            valid.append((x + 1, y + 1))
        if y == 4 and board[y][x - 1] == 'w_pawn' and last_move[1] == (x - 1, 6) and last_move[2] == (x - 1, 4):
            valid.append((x - 1, y + 1))
    return valid


def get_knight_moves(x, y, board):
    valid = []
    colour = board[y][x][:1]
    if y + 2 <= 7 and x + 1 <= 7 and (board[y + 2][x + 1] == '' or board[y + 2][x + 1][:1] != colour):
        valid.append((x + 1, y + 2))
    if y + 1 <= 7 and x + 2 <= 7 and (board[y + 1][x + 2] == '' or board[y + 1][x + 2][:1] != colour):
        valid.append((x + 2, y + 1))
    if y - 2 >= 0 and x - 1 >= 0 and (board[y - 2][x - 1] == '' or board[y - 2][x - 1][:1] != colour):
        valid.append((x - 1, y - 2))
    if y - 1 >= 0 and x - 2 >= 0 and (board[y - 1][x - 2] == '' or board[y - 1][x - 2][:1] != colour):
        valid.append((x - 2, y - 1))
    if y + 2 <= 7 and x - 1 >= 0 and (board[y + 2][x - 1] == '' or board[y + 2][x - 1][:1] != colour):
        valid.append((x - 1, y + 2))
    if y - 2 >= 0 and x + 1 <= 7 and (board[y - 2][x + 1] == '' or board[y - 2][x + 1][:1] != colour):
        valid.append((x + 1, y - 2))
    if y + 1 <= 7 and x - 2 >= 0 and (board[y + 1][x - 2] == '' or board[y + 1][x - 2][:1] != colour):
        valid.append((x - 2, y + 1))
    if y - 1 >= 0 and x + 2 <= 7 and (board[y - 1][x + 2] == '' or board[y - 1][x + 2][:1] != colour):
        valid.append((x + 2, y - 1))
    return valid


def get_rook_moves(x, y, board):
    valid = []
    colour = board[y][x][:1]
    i = 1
    while y + i <= 7 and board[y + i][x] == '':
        valid.append((x, y + i))
        i += 1
    if y + i <= 7 and board[y + i][x][:1] != colour:
        valid.append((x, y + i))
    i = 1
    while y - i >= 0 and board[y - i][x] == '':
        valid.append((x, y - i))
        i += 1
    if y - i >= 0 and board[y - i][x][:1] != colour:
        valid.append((x, y - i))
    i = 1
    while x + i <= 7 and board[y][x + i] == '':
        valid.append((x + i, y))
        i += 1
    if x + i <= 7 and board[y][x + i][:1] != colour:
        valid.append((x + i, y))
    i = 1
    while x - i >= 0 and board[y][x - i] == '':
        valid.append((x - i, y))
        i += 1
    if x - i >= 0 and board[y][x - i][:1] != colour:
        valid.append((x - i, y))
    return valid


def get_bishop_moves(x, y, board):
    valid = []
    colour = board[y][x][:1]
    i = 1
    while y + i <= 7 and x + i <= 7 and board[y + i][x + i] == '':
        valid.append((x + i, y + i))
        i += 1
    if y + i <= 7 and x + i <= 7 and board[y + i][x + i][:1] != colour:
        valid.append((x + i, y + i))
    i = 1
    while y - i >= 0 and x - i >= 0 and board[y - i][x - i] == '':
        valid.append((x - i, y - i))
        i += 1
    if y - i >= 0 and x - i >= 0 and board[y - i][x - i][:1] != colour:
        valid.append((x - i, y - i))
    i = 1
    while y - i >= 0 and x + i <= 7 and board[y - i][x + i] == '':
        valid.append((x + i, y - i))
        i += 1
    if y - i >= 0 and x + i <= 7 and board[y - i][x + i][:1] != colour:
        valid.append((x + i, y - i))
    i = 1
    while y + i <= 7 and x - i >= 0 and board[y + i][x - i] == '':
        valid.append((x - i, y + i))
        i += 1
    if y + i <= 7 and x - i >= 0 and board[y + i][x - i][:1] != colour:
        valid.append((x - i, y + i))
    return valid


def get_queen_moves(x, y, board):
    rook_moves = get_rook_moves(x, y, board)
    bishop_moves = get_bishop_moves(x, y, board)
    valid = rook_moves + bishop_moves
    return valid


def get_king_moves(x, y, board):
    valid = []
    colour = board[y][x][:1]
    if y + 1 <= 7 and (board[y + 1][x] == '' or board[y + 1][x][:1] != colour):
        valid.append((x, y + 1))
    if y - 1 >= 0 and (board[y - 1][x] == '' or board[y - 1][x][:1] != colour):
        valid.append((x, y - 1))
    if x + 1 <= 7 and (board[y][x + 1] == '' or board[y][x + 1][:1] != colour):
        valid.append((x + 1, y))
    if x - 1 >= 0 and (board[y][x - 1] == '' or board[y][x - 1][:1] != colour):
        valid.append((x - 1, y))
    if y + 1 <= 7 and x + 1 <= 7 and (board[y + 1][x + 1] == '' or board[y + 1][x + 1][:1] != colour):
        valid.append((x + 1, y + 1))
    if y - 1 >= 0 and x - 1 >= 0 and (board[y - 1][x - 1] == '' or board[y - 1][x - 1][:1] != colour):
        valid.append((x - 1, y - 1))
    if y - 1 >= 0 and x + 1 <= 7 and (board[y - 1][x + 1] == '' or board[y - 1][x + 1][:1] != colour):
        valid.append((x + 1, y - 1))
    if y + 1 <= 7 and x - 1 >= 0 and (board[y + 1][x - 1] == '' or board[y + 1][x - 1][:1] != colour):
        valid.append((x - 1, y + 1))
    # castling
    if x == 4:
        if castling_possibilities['wl'] and board[y][x - 1] == '' and board[y][x - 2] == '' and board[y][x - 3] == '':
            valid.append((x - 4, y))
        if castling_possibilities['wr'] and board[y][x + 1] == '' and board[y][x + 2] == '':
            valid.append((x + 3, y))
        if castling_possibilities['bl'] and board[y][x - 1] == '' and board[y][x - 2] == '' and board[y][x - 3] == '':
            valid.append((x - 4, y))
        if castling_possibilities['br'] and board[y][x + 1] == '' and board[y][x + 2] == '':
            valid.append((x + 3, y))
    return valid


# takes current board and move data and returns new board after move has been made
def make_move(board, sel_x, sel_y, new_x, new_y):
    # if en passant opportunity taken set piece captured by en_passant to empty
    if board[sel_y][sel_x][2:] == 'pawn' and board[new_y][new_x] == '' and sel_x != new_x:
        if new_x > sel_x:
            board[sel_y][sel_x + 1] = ''
        else:
            board[sel_y][sel_x - 1] = ''
        board[new_y][new_x] = board[sel_y][sel_x]
        board[sel_y][sel_x] = ''
    # if castling move king 2 spaces towards rook and then place rook on the other side
    elif board[sel_y][sel_x][2:] == 'king' and board[new_y][new_x][2:] == 'rook' and board[new_y][new_x][:1] == turn:
        if new_x == 0:
            board[sel_y][sel_x - 2] = board[sel_y][sel_x]
            board[sel_y][sel_x - 1] = board[new_y][new_x]
        else:
            board[sel_y][sel_x + 2] = board[sel_y][sel_x]
            board[sel_y][sel_x + 1] = board[new_y][new_x]
        board[sel_y][sel_x] = ''
    # else play normal move
    else:
        board[new_y][new_x] = board[sel_y][sel_x]
        board[sel_y][sel_x] = ''
    return board


# used to check if a piece has been chosen from the promotion selection and then return that piece
def promote_select(x, y):
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
def check_check(board, all_moves, t):
    for i in range(len(all_moves)):
        x = all_moves[i][2][0]
        y = all_moves[i][2][1]
        piece = board[y][x][2:]
        colour = board[y][x][:1]
        if piece == 'king' and t != colour:
            checked_position = (x, y)
            return checked_position
    return ()


# used to check if current player is in checkmate (or stalemate) by checking if there are any valid playable moves
def check_checkmate(all_moves):
    if all_moves:
        return False
    else:
        return True


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
# set initial all valid moves to all the valid moves for white
all_valid_moves = get_all_valid_moves(board_layout, turn)
# winner, set as empty until a player has won
winner = ''

running = True

while running:
    time.tick(FPS)
    # draw everything onto window
    draw_board()
    draw_pieces()
    draw_selection()
    draw_moves()
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
                promotion_selection = promote_select(x, y)
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
                    for index in range(len(moves_list)):
                        valid_x = moves_list[index][0]
                        valid_y = moves_list[index][1]
                        if x == valid_x and y == valid_y:
                            # store move in last_move
                            last_move = [board_layout[selected_y][selected_x], (selected_x, selected_y), (x, y)]
                            board_layout = make_move(board_layout, selected_x, selected_y, x, y)
                            # if pawn reaches other side set promoting to true and store information about the promoting piece
                            if (y == 7 or y == 0) and board_layout[y][x][2:] == 'pawn':
                                promoting_piece = [turn, (x, y)]
                                promoting = True
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
                            # set valid played to true as move has been made
                            valid_played = True
                    # set selected back to infinite and moves list to empty
                    selected_x = +inf
                    selected_y = +inf
                    moves_list = []
                # if the colour of the piece is the same as turn and a valid move has not been chosen, set selected to coordinates and get valid moves at that position
                if turn == piece_colour and not valid_played:
                    selected_x = x
                    selected_y = y
                    moves_list = get_selected_moves(all_valid_moves, selected_x, selected_y)
            # if a valid move has been played and not promoting check if other player is in check and swap turns
            # if promoting, promotion will take place first which will set promoting to false
            if valid_played and not promoting:
                all_next_moves = get_all_moves(board_layout, turn)
                checked = check_check(board_layout, all_next_moves, turn)
                turn = switch_turn(turn)
            # generate all valid moves for the current players turn
            all_valid_moves = get_all_valid_moves(board_layout, turn)
            # check if in checkmate, if checked winner is set to the other player
            # if not it is stalemate and the game ends in a draw
            checkmate = check_checkmate(all_valid_moves)
            if checkmate:
                if checked:
                    winner = switch_turn(turn)
                else:
                    winner = 'draw'
        if event.type == KEYDOWN:
            # if r is pressed reset board to starting position
            if event.key == pygame.K_r:
                board_layout = reset_board()
                all_valid_moves = get_all_valid_moves(board_layout, turn)
                moves_list = []
                last_move = []
                valid_played = False
                selected_x = +inf
                selected_y = +inf
                promoting_piece = []
                promoting = False
                castling_possibilities = {'wl': True, 'wr': True, 'bl': True, 'br': True}
                turn = 'w'
                winner = ''
                checked = ()
                checkmate = False
        # stop running if window is quit
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
sys.exit()

