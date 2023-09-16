import sys
import copy
from math import inf

import pygame
from pygame import *

pygame.init()

# create different sized fonts
extremely_small_font = pygame.font.SysFont('verdana', 12)
very_small_font = pygame.font.SysFont('verdana', 15)
small_font = pygame.font.SysFont('verdana', 20, True)
medium_font = pygame.font.SysFont('verdana', 36, True)
large_font = pygame.font.SysFont('verdana', 48, True)
very_large_font = pygame.font.SysFont('verdana', 64, True)

# initiate width, height and fps constants
# TOTAL_WIDTH is the width of the whole window, WIDTH and HEIGHT are the size of the board and SIDE_WIDTH is width of the sidebar
TOTAL_WIDTH = 800
WIDTH = 600
HEIGHT = 600
SIDE_WIDTH = TOTAL_WIDTH - WIDTH
FPS = 60

# set up window, caption and clock
window = pygame.display.set_mode((TOTAL_WIDTH, HEIGHT))
pygame.display.set_caption('Python Chess')
time = pygame.time.Clock()

# set the display to menu when first opened
current_display = 'menu'

# load in background image for menus
# https://www.freepik.com/free-photo/abstract-textured-backgound_12072945.htm#query=black%20gradient&position=11&from_view=keyword&track=ais Image by benzoix on Freepik
background = pygame.image.load('./images/black_background.jpg')
background = pygame.transform.scale(background, (TOTAL_WIDTH, HEIGHT))

# load in pawn image for menu
# https://www.clipartmax.com/middle/m2H7N4K9A0d3K9d3_chess-piece-pawn-queen-knight-chess-piece-pawn-queen-knight Chess Piece Pawn Queen Knight - Chess Piece @clipartmax.com
menu_pawn = pygame.image.load('./images/menu_pawn.png')
menu_pawn = pygame.transform.scale(menu_pawn, (menu_pawn.get_width() / (TOTAL_WIDTH / 400), menu_pawn.get_height() / (HEIGHT / 300)))

# load in setting gear for menu
# https://www.clipartmax.com/middle/m2H7Z5K9d3G6A0Z5_creative-usage-of-sugarcrm-black-and-white-clipart-of-gear Creative Usage Of Sugarcrm - Black And White Clipart Of Gear @clipartmax.com
menu_gear = pygame.image.load('./images/settings_gear.png')
menu_gear = pygame.transform.scale(menu_gear, (menu_gear.get_width() / (TOTAL_WIDTH / 525), menu_gear.get_height() / (HEIGHT / 393.75)))

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

# dictionary to match pieces in board_layout to piece images
PIECES = {'w_pawn': white_pawn, 'w_rook': white_rook, 'w_knight': white_knight, 'w_bishop': white_bishop, 'w_queen': white_queen, 'w_king': white_king,
          'b_pawn': black_pawn, 'b_rook': black_rook, 'b_knight': black_knight, 'b_bishop': black_bishop, 'b_queen': black_queen, 'b_king': black_king}

# points gained for each captured piece
POINTS = {'pawn': 1, 'knight': 3, 'bishop': 3, 'rook': 5, 'queen': 9, 'king': 0}

# initial board layout as 2d array
# when referring to an individual square board_layout[y][x] is used as when indexing the row (y) is the first then column (x) is second
# this makes it easier to visualise in comparison to arrays of columns
board_layout = [['b_rook', 'b_knight', 'b_bishop', 'b_queen', 'b_king', 'b_bishop', 'b_knight', 'b_rook'],
                ['b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn'],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn'],
                ['w_rook', 'w_knight', 'w_bishop', 'w_queen', 'w_king', 'w_bishop', 'w_knight', 'w_rook']]

# list of captured pieces for each colour
captured_white_pieces = []
captured_black_pieces = []

# selected_x and selected_y used to identify which square is currently selected
selected_x = +inf
selected_y = +inf

# moves_list represents all  playable moves of the selected piece as an array of x y tuples
moves_list = []
# last_move, the latest played move stored as [piece, (previous_x, previous_y), (new_x, new_y)], used for en passant in pawn moves
last_move = []

# piece that is being promoted stored as [colour, (x, y)]
promoting_piece = []
# promoting, if pawn needs promoted set to true, initially set to false
promoting = False

# if castling is possible for each rook (e.g. 'wl' = left white rook)
castling_possibilities = {'wl': True, 'wr': True, 'bl': True, 'br': True}

# tuple of coordinates of checked king, empty otherwise
checked = ()
# if checkmate has occurred
checkmate = False

# valid_played, initially set to false as no move has been played yet
valid_played = False

# turn, the current players turn
turn = 'w'
# winner, set as empty until a player has won
winner = ''

# the current point totals for each player
white_points = 0
black_points = 0

# the time setting selected per player initially set to no time can be changed from settings before starting a game
time_setting = 'No time'
# set each timer initially to 0
white_timer = 0
black_timer = 0
# if time has started yet
time_started = False


# game code -------------------------------------------------------------------------------------------------------------------

# used to draw black and white squares (to create the board)
def draw_board():
    offset_x = 0
    offset_y = 0
    row = 1
    window.fill((50, 50, 50))
    for i_x in range(8):
        if row % 2 == 0:
            offset_x += WIDTH / 8
        for i_y in range(4):
            pygame.draw.rect(window, 'white', [offset_x, offset_y, (WIDTH / 8), (HEIGHT / 8)])
            offset_x += WIDTH / 4
        offset_y += HEIGHT / 8
        row += 1
        offset_x = 0


# used to draw A to H and 1 to 8 coordinates along the edges of the board
def draw_coords():
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
    offset = 0
    for i in range(len(letters)):
        letter = very_small_font.render(letters[i], True, (120, 120, 120))
        window.blit(letter, ((WIDTH / 8 - letter.get_width()) / 2 + offset, HEIGHT - letter.get_height()))
        number = very_small_font.render(numbers[i], True, (120, 120, 120))
        window.blit(number, (WIDTH / 256, HEIGHT * 7 / 8 + ((HEIGHT / 8 - letter.get_height()) / 2) - offset))
        offset += WIDTH / 8


# used to draw pieces onto the board from board_layout
def draw_pieces(board):
    offset_x = 0
    offset_y = 0
    for i_y in range(8):
        for i_x in range(8):
            square = board[i_y][i_x]
            if square != '':
                window.blit(PIECES[square], (offset_x + 6, offset_y + 6))
            offset_x += WIDTH / 8
        offset_y += HEIGHT / 8
        offset_x = 0


# used to draw yellow outline around currently selected square
def draw_selection(sel_x, sel_y):
    if sel_x != +inf and sel_y != +inf:
        pygame.draw.rect(window, 'yellow', [(sel_x * (WIDTH / 8)), (sel_y * (HEIGHT / 8)), (WIDTH / 8), (HEIGHT / 8)], 3)


# used to draw green circles in the centre of squares for each valid move for the selected piece
def draw_moves(moves):
    for i in range(len(moves)):
        pygame.draw.circle(window, 'green', [moves[i][0] * (WIDTH / 8) + (WIDTH / 16), moves[i][1] * (HEIGHT / 8) + (WIDTH / 16)], 5)


# used to draw red outline around king if in check
def draw_check(check):
    if check:
        check_x = check[0]
        check_y = check[1]
        pygame.draw.rect(window, 'red', [check_x * (WIDTH / 8), check_y * (HEIGHT / 8), (WIDTH / 8), (HEIGHT / 8)], 2)


# used to draw all regular board parts
def draw_all_board(board, sel_x, sel_y, moves, check):
    draw_board()
    draw_coords()
    draw_pieces(board)
    draw_selection(sel_x, sel_y)
    draw_moves(moves)
    draw_check(check)


# used to draw promotion selection
def draw_promotion(x, y):
    offset = WIDTH / 4
    if promoting_piece[0] == 'w':
        selection = [white_knight, white_bishop, white_rook, white_queen]
    else:
        selection = [black_knight, black_bishop, black_rook, black_queen]
    for i in range(len(selection)):
        if offset < x < offset + WIDTH / 8 and HEIGHT / 2 - HEIGHT / 16 < y < HEIGHT / 2 - HEIGHT / 16 + HEIGHT / 8:
            pygame.draw.rect(window, 'white', [offset, HEIGHT / 2 - HEIGHT / 16, WIDTH / 8, HEIGHT / 8])
        else:
            pygame.draw.rect(window, (200, 200, 200), [offset, HEIGHT / 2 - HEIGHT / 16, WIDTH / 8, HEIGHT / 8])
        pygame.draw.rect(window, 'black', [offset, HEIGHT / 2 - HEIGHT / 16, WIDTH / 8, HEIGHT / 8], 2)
        window.blit(selection[i], (offset + WIDTH / 64, HEIGHT / 2 - HEIGHT / 16 + WIDTH / 64))
        offset += WIDTH / 8


# used draw winning message when win condition has been met
def draw_winning_message(w):
    pygame.draw.rect(window, 'black', [WIDTH / 4, HEIGHT / 2 - HEIGHT / 12, WIDTH / 2, HEIGHT / 6])
    pygame.draw.rect(window, 'white', [WIDTH / 4, HEIGHT / 2 - HEIGHT / 12, WIDTH / 2, HEIGHT / 6], 2)
    if w == 'w':
        winning_message = very_small_font.render('White Player is the Winner!', True, 'white')
    elif w == 'b':
        winning_message = very_small_font.render('Black Player is the Winner!', True, 'white')
    else:
        winning_message = very_small_font.render('Draw', True, 'white')
    window.blit(winning_message, (WIDTH / 4 + (WIDTH / 2 - winning_message.get_width()) / 2, HEIGHT / 2 - HEIGHT / 16))
    restart_message = very_small_font.render('Press [R] to restart', True, 'white')
    window.blit(restart_message, (WIDTH / 4 + (WIDTH / 2 - restart_message.get_width()) / 2, HEIGHT / 2 - HEIGHT / 16 + winning_message.get_height()))
    menu_message = very_small_font.render('Press [M] to return to the menu', True, 'white')
    window.blit(menu_message, (WIDTH / 4 + (WIDTH / 2 - menu_message.get_width()) / 2, HEIGHT / 2 - HEIGHT / 16 + winning_message.get_height() * 2))


# used to draw the sidebar displaying turn, captured pieces and score (time also on sidebar but drawn separately)
# wp = white points, cwp = captured white pieces (same for black), t = turn
def draw_side_bar(wp, bp, cwp, cbp, t):
    pygame.draw.line(window, 'black', (WIDTH, 0), (WIDTH, HEIGHT), 5)
    pygame.draw.rect(window, (230, 230, 230), [WIDTH, 0, SIDE_WIDTH, HEIGHT])
    restart_prompt = extremely_small_font.render('Press R to restart game', True, 'black')
    window.blit(restart_prompt, (WIDTH + ((SIDE_WIDTH - restart_prompt.get_width()) / 2), HEIGHT / 2 - restart_prompt.get_height()))
    menu_prompt = extremely_small_font.render('Press M to return to menu', True, 'black')
    window.blit(menu_prompt, (WIDTH + ((SIDE_WIDTH - menu_prompt.get_width()) / 2), HEIGHT / 2))
    pygame.draw.line(window, 'black', (WIDTH, HEIGHT / 2 - restart_prompt.get_height() - HEIGHT / 64), (TOTAL_WIDTH, HEIGHT / 2 - restart_prompt.get_height() - HEIGHT / 64), 2)
    pygame.draw.line(window, 'black', (WIDTH, HEIGHT / 2 + menu_prompt.get_height() + HEIGHT / 64), (TOTAL_WIDTH, HEIGHT / 2 + menu_prompt.get_height() + HEIGHT / 64), 2)
    if t == 'w':
        pygame.draw.rect(window, (10, 100, 10), [WIDTH, HEIGHT * 7 / 8, SIDE_WIDTH, HEIGHT / 8])
    else:
        pygame.draw.rect(window, (10, 100, 10), [WIDTH, 0, SIDE_WIDTH, HEIGHT / 8])
    pygame.draw.line(window, 'black', (WIDTH, HEIGHT / 8), (TOTAL_WIDTH, HEIGHT / 8), 2)
    pygame.draw.line(window, 'black', (WIDTH, HEIGHT * 7 / 8), (TOTAL_WIDTH, HEIGHT * 7 / 8), 2)
    draw_score(wp, bp)
    draw_captured(cwp, cbp)


# used draw the current points for each player
def draw_score(wp, bp):
    wp_text = medium_font.render(str(wp), True, 'black')
    window.blit(wp_text, (WIDTH + (SIDE_WIDTH - wp_text.get_width()) / 2, HEIGHT * 4 / 7))
    bp_text = medium_font.render(str(bp), True, 'black')
    window.blit(bp_text, (WIDTH + (SIDE_WIDTH - bp_text.get_width()) / 2, HEIGHT * 3 / 7 - bp_text.get_height()))


# used to draw the all captured pieces
def draw_captured(cwp, cbp):
    x_offset = 0
    y_offset = 0
    scaled = white_pawn.get_width() / 2
    for i in range(len(cwp)):
        captured_piece = pygame.transform.scale(PIECES[cwp[i]], (scaled, scaled))
        window.blit(captured_piece, (WIDTH + scaled / 3 + x_offset, HEIGHT / 8 + y_offset))
        x_offset += scaled
        if (i + 1) % 6 == 0:
            x_offset = 0
            y_offset += scaled
    x_offset = 0
    y_offset = 0
    for i in range(len(cbp)):
        captured_piece = pygame.transform.scale(PIECES[cbp[i]], (scaled, scaled))
        window.blit(captured_piece, (WIDTH + scaled / 3 + x_offset, HEIGHT * 7 / 8 - scaled - y_offset))
        x_offset += scaled
        if (i + 1) % 6 == 0:
            x_offset = 0
            y_offset += scaled


# draws turn where timer would be if playing with time (only when playing without time)
def draw_turn(t):
    if t == 'w':
        turn_text = small_font.render('White Turn', True, 'black')
        window.blit(turn_text, (WIDTH + (SIDE_WIDTH - turn_text.get_width()) / 2, HEIGHT * 7 / 8 + (HEIGHT / 8 - turn_text.get_height()) / 2))
    else:
        turn_text = small_font.render('Black Turn', True, 'black')
        window.blit(turn_text, (WIDTH + (SIDE_WIDTH - turn_text.get_width()) / 2, (HEIGHT / 8 - turn_text.get_height()) / 2))


# draws timers for each player in minutes:seconds format
def draw_timers(wt, bt):
    if wt >= 60:
        wt_text = str(wt // 60) + ':'
        if len(str(wt % 60)) == 1:
            wt_text = wt_text + '0' + str(wt % 60)
        else:
            wt_text = wt_text + str(wt % 60)
    else:
        wt_text = str(wt)
    if bt >= 60:
        bt_text = str(bt // 60) + ':'
        if len(str(bt % 60)) == 1:
            bt_text = bt_text + '0' + str(bt % 60)
        else:
            bt_text = bt_text + str(bt % 60)
    else:
        bt_text = str(bt)
    time_text = medium_font.render(wt_text, True, 'black')
    window.blit(time_text, (WIDTH + (SIDE_WIDTH - time_text.get_width()) / 2, HEIGHT * 7 / 8 + (HEIGHT / 8 - time_text.get_height()) / 2))
    time_text = medium_font.render(bt_text, True, 'black')
    window.blit(time_text, (WIDTH + (SIDE_WIDTH - time_text.get_width()) / 2, (HEIGHT / 8 - time_text.get_height()) / 2))


# used to convert time setting to number of frames
def convert_time(ts):
    converted_t = 60 * 60
    if ts == '5 Min':
        converted_t *= 5
    if ts == '10 Min':
        converted_t *= 10
    if ts == '20 Min':
        converted_t *= 20
    return converted_t


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


# used to get moves for the selected piece from a list of moves
def get_selected_moves(all_moves, sel_x, sel_y):
    selected_moves = []
    for i in range(len(all_moves)):
        if all_moves[i][1] == (sel_x, sel_y):
            selected_moves.append(all_moves[i][2])
    return selected_moves


# get moves functions for each piece

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


# takes current board selected piece (where piece is moving from) and the new destination and returns board after move has been made
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


# used to check if a piece has been chosen from the promotion selection and then return that piece empty otherwise
def promote_select(x, y):
    if HEIGHT / 2 - HEIGHT / 16 < y < HEIGHT / 2 - HEIGHT / 16 + HEIGHT / 8:
        offset = WIDTH / 4
        selection = ['knight', 'bishop', 'rook', 'queen']
        # for each selection check the area that matches the options that appear on screen from draw_promotion
        for i in range(len(selection)):
            # if x is within boundaries of a piece change pawn at position stored in promoting piece to the piece clicked on and set promoting back to false
            if offset < x < offset + WIDTH / 8:
                return selection[i]
            offset += WIDTH / 8
    return ''


# used to check if a king is currently in check by checking all pieces under threat
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


# used to see if current player is in checkmate (or stalemate) by checking if there are any valid playable moves
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


# menu code -------------------------------------------------------------------------------------------------------------------

# used to draw the main menu including title and buttons to play and change settings
def draw_main_menu(x, y):
    window.blit(background, (0, 0))
    title = very_large_font.render('Python Chess', True, 'white')
    window.blit(title, ((TOTAL_WIDTH - title.get_width()) / 2, HEIGHT / 16))
    window.blit(menu_pawn, (TOTAL_WIDTH * 2 / 9, HEIGHT / 3.5))
    window.blit(menu_gear, (TOTAL_WIDTH * 5 / 9, HEIGHT / 3.5))
    if TOTAL_WIDTH * 2 / 9 < x < TOTAL_WIDTH * 4 / 9 and HEIGHT / 3.5 < y < HEIGHT * 3 / 4:
        play_text = large_font.render('Play', True, 'yellow')
    else:
        play_text = large_font.render('Play', True, 'white')
    if TOTAL_WIDTH * 5 / 9 < x < TOTAL_WIDTH * 8 / 9 and HEIGHT / 3.5 < y < HEIGHT * 3 / 4:
        settings_text = large_font.render('Settings', True, 'yellow')
    else:
        settings_text = large_font.render('Settings', True, 'white')
    window.blit(play_text, (TOTAL_WIDTH * 2 / 9, HEIGHT * 2 / 3))
    window.blit(settings_text, (TOTAL_WIDTH * 5 / 9, HEIGHT * 2 / 3))


# settings code -------------------------------------------------------------------------------------------------------------------

# used to draw a button using a list of parameters
def draw_button(x, y, text, text_colour, font_type, colour_one, colour_two, offset_x, offset_y, width, height):
    if offset_x < x < offset_x + width and offset_y < y < offset_y + height:
        pygame.draw.rect(window, colour_two, [offset_x, offset_y, width, height])
    else:
        pygame.draw.rect(window, colour_one, [offset_x, offset_y, width, height])
    button_text = font_type.render(text, True, text_colour)
    window.blit(button_text, (offset_x + (width - button_text.get_width()) / 2, offset_y + (height - button_text.get_height()) / 2))


# used to draw the settings menu, buttons to change the time per player and apply
def draw_settings_menu(x, y, ts):
    window.blit(background, (0, 0))
    title = large_font.render('Settings', True, 'white')
    window.blit(title, ((TOTAL_WIDTH - title.get_width()) / 2, HEIGHT / 16))
    time_title = small_font.render('Time: ' + ts, True, 'white')
    window.blit(time_title, (TOTAL_WIDTH / 10, HEIGHT / 8 + title.get_height()))
    offset = TOTAL_WIDTH / 10
    time_selection = ['No time', '1 Min', '5 Min', '10 Min', '20 Min']
    for i in range(len(time_selection)):
        draw_button(x, y, time_selection[i], 'black', very_small_font, 'white', (220, 220, 220), offset, (HEIGHT * 2/7), TOTAL_WIDTH / 6, HEIGHT / 16)
        offset += TOTAL_WIDTH / 6 - 1
    draw.rect(window, 'black', [TOTAL_WIDTH / 10, HEIGHT * 2/7, TOTAL_WIDTH * 5/6 - 4, HEIGHT / 16], 2)
    draw_button(x, y, 'Apply', 'black', very_small_font, 'white', (220, 220, 220), (TOTAL_WIDTH * 3/4) / 2, HEIGHT * 7/8, TOTAL_WIDTH / 4, HEIGHT / 12)
    draw.rect(window, 'black', [(TOTAL_WIDTH * 3/4) / 2, HEIGHT * 7/8, TOTAL_WIDTH / 4, HEIGHT / 12], 3)


# used to check if a time button has been clicked on the menu
def get_time_button(x, y):
    if HEIGHT * 2 / 7 < y < (HEIGHT * 2 / 7) + HEIGHT / 16:
        offset = TOTAL_WIDTH / 10
        time_selection = ['No time', '1 Min', '5 Min', '10 Min', '20 Min']
        for i in range(len(time_selection)):
            if offset < x < HEIGHT / 6 + offset:
                return time_selection[i]
            offset += TOTAL_WIDTH / 6
    return ''


# loop for whole game -------------------------------------------------------------------------------------------------------------------

# set initial all valid moves to all the valid moves for white
all_valid_moves = get_all_valid_moves(board_layout, turn)
running = True

while running:
    time.tick(FPS)
    # get mouse position
    mouse = pygame.mouse.get_pos()
    mouse_x = mouse[0]
    mouse_y = mouse[1]

    # main menu loop
    if current_display == 'menu':
        draw_main_menu(mouse_x, mouse_y)
        for event in pygame.event.get():
            # if option is clicked set the current display to match the option
            if event.type == pygame.MOUSEBUTTONDOWN:
                if TOTAL_WIDTH * 2 / 9 < mouse_x < TOTAL_WIDTH * 4 / 9 and HEIGHT / 3.5 < mouse_y < HEIGHT * 3 / 4:
                    current_display = 'game'
                if TOTAL_WIDTH * 5 / 9 < mouse_x < TOTAL_WIDTH * 8 / 9 and HEIGHT / 3.5 < mouse_y < HEIGHT * 3 / 4:
                    current_display = 'settings'
            # stop running if window is quit
            if event.type == pygame.QUIT:
                running = False

    # settings loop
    if current_display == 'settings':
        draw_settings_menu(mouse_x, mouse_y, time_setting)
        for event in pygame.event.get():
            # check if a button has been clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if get_time_button(mouse_x, mouse_y):
                    time_setting = get_time_button(mouse_x, mouse_y)
                # apply button position
                if (TOTAL_WIDTH * 3 / 4) / 2 < mouse_x < (TOTAL_WIDTH * 3 / 4) / 2 + TOTAL_WIDTH / 4 and \
                        HEIGHT * 7 / 8 < mouse_y < HEIGHT * 7 / 8 + HEIGHT / 12:
                    current_display = 'menu'
            # stop running if window is quit
            if event.type == pygame.QUIT:
                running = False

    # game loop
    if current_display == 'game':
        # draw everything onto window
        draw_all_board(board_layout, selected_x, selected_y, moves_list, checked)
        draw_side_bar(white_points, black_points, captured_white_pieces, captured_black_pieces, turn)
        # if pawn needs promotion draw promotion selection
        if promoting:
            draw_promotion(mouse_x, mouse_y)
        # if there is a winner draw the winning message
        if winner:
            draw_winning_message(winner)
        # if a time is set and there is not currently a winner start timer code otherwise just draw turn instead
        if time_setting != 'No time' and not winner:
            # if time is not started set timers equal to the time setting selected
            if not time_started:
                white_timer = convert_time(time_setting)
                black_timer = convert_time(time_setting)
                time_started = True
            # depending on the turn decrement the timer
            if turn == 'w':
                white_timer -= 1
            else:
                black_timer -= 1
            # if the timer reaches 0 set the winner equal to the opposite players turn
            if white_timer == 0:
                winner = 'b'
            if black_timer == 0:
                winner = 'w'
            # draw timers, pass in rounded down to the nearest second
            draw_timers(white_timer // 60, black_timer // 60)
        else:
            draw_turn(turn)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and not winner:
                # if promoting a pawn check if within promotion selection window
                if promoting:
                    promotion_selection = promote_select(mouse_x, mouse_y)
                    # if piece is selected set pawn stored at the location in promoting_piece equal to the chosen piece and set promoting back to false
                    if promotion_selection:
                        board_layout[promoting_piece[1][1]][promoting_piece[1][0]] = promoting_piece[0] + '_' + promotion_selection
                        promoting = False
                # if not promoting a pawn continue with normal play
                else:
                    # change mouse click position to coordinates on the board
                    m_x = int(mouse_x // (WIDTH / 8))
                    m_y = int(mouse_y // (HEIGHT / 8))
                    # save colour of piece before move
                    piece_colour = board_layout[m_y][m_x][:1]
                    # set valid_played back to false
                    valid_played = False
                    # if a piece is already selected store selected piece details and check the coordinates are a valid move
                    if 0 <= selected_x <= 7 and 0 <= selected_y <= 7:
                        for index in range(len(moves_list)):
                            valid_x = moves_list[index][0]
                            valid_y = moves_list[index][1]
                            if m_x == valid_x and m_y == valid_y:
                                # if valid update points and add taken pieces to respective captured list
                                if turn == 'w' and piece_colour == 'b':
                                    white_points += POINTS[board_layout[m_y][m_x][2:]]
                                    captured_black_pieces.append(board_layout[m_y][m_x])
                                if turn == 'b' and piece_colour == 'w':
                                    black_points += POINTS[board_layout[m_y][m_x][2:]]
                                    captured_white_pieces.append(board_layout[m_y][m_x])
                                # store move in last_move and make move
                                last_move = [board_layout[selected_y][selected_x], (selected_x, selected_y), (m_x, m_y)]
                                board_layout = make_move(board_layout, selected_x, selected_y, m_x, m_y)
                                # if pawn reaches other side set promoting to true and store information about the promoting piece
                                if (m_y == 7 or m_y == 0) and board_layout[m_y][m_x][2:] == 'pawn':
                                    promoting_piece = [turn, (m_x, m_y)]
                                    promoting = True
                                # update castling possibilities
                                if board_layout[m_y][m_x][2:] == 'king' or board_layout[m_y][m_x][2:] == 'rook':
                                    if board_layout[m_y][m_x] == 'w_king' or (selected_x == 0 and selected_y == 7):
                                        castling_possibilities['wl'] = False
                                    if board_layout[m_y][m_x] == 'w_king' or (selected_x == 7 and selected_y == 7):
                                        castling_possibilities['wr'] = False
                                    if board_layout[m_y][m_x] == 'b_king' or (selected_x == 0 and selected_y == 0):
                                        castling_possibilities['bl'] = False
                                    if board_layout[m_y][m_x] == 'b_king' or (selected_x == 7 and selected_y == 0):
                                        castling_possibilities['br'] = False
                                # set valid played to true as move has been made
                                valid_played = True
                        # set selected back to infinite and moves list to empty
                        selected_x = +inf
                        selected_y = +inf
                        moves_list = []
                    # if the colour of the piece is the same as turn and a valid move has not been chosen, set selected to coordinates and get valid moves at that position
                    if turn == piece_colour and not valid_played:
                        selected_x = m_x
                        selected_y = m_y
                        moves_list = get_selected_moves(all_valid_moves, selected_x, selected_y)
                # if a valid move has been played and not promoting check if other player is in check and swap turns
                # if promoting, promotion will take place first which will set promoting to false
                if valid_played and not promoting:
                    all_next_moves = get_all_moves(board_layout, turn)
                    checked = check_check(board_layout, all_next_moves, turn)
                    turn = switch_turn(turn)
                # generate all valid moves for the current players turn
                all_valid_moves = get_all_valid_moves(board_layout, turn)
                # check for checkmate, if checked winner is set to the other player
                # if not it is stalemate and the game ends in a draw
                checkmate = check_checkmate(all_valid_moves)
                if checkmate:
                    if checked:
                        winner = switch_turn(turn)
                    else:
                        winner = 'draw'
            if event.type == KEYDOWN:
                # if r or m is pressed reset board to starting position
                if event.key == pygame.K_r or event.key == pygame.K_m:
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
                    white_points = 0
                    black_points = 0
                    captured_white_pieces = []
                    captured_black_pieces = []
                    time_started = False
                # if m is pressed return to the menu
                if event.key == pygame.K_m:
                    current_display = 'menu'
            # stop running if window is quit
            if event.type == pygame.QUIT:
                running = False

    pygame.display.flip()
sys.exit()
