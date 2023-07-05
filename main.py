import sys
from math import inf

import pygame

pygame.init()

WIDTH = 600
HEIGHT = 600
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Chess")
time = pygame.time.Clock()

# en:User:Cburnett, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons
white_pawn = pygame.image.load("./images/white_pawn.png")
black_pawn = pygame.image.load("./images/black_pawn.png")
white_rook = pygame.image.load("./images/white_rook.png")
black_rook = pygame.image.load("./images/black_rook.png")
white_knight = pygame.image.load("./images/white_knight.png")
black_knight = pygame.image.load("./images/black_knight.png")
white_bishop = pygame.image.load("./images/white_bishop.png")
black_bishop = pygame.image.load("./images/black_bishop.png")
white_bishop = pygame.image.load("./images/white_bishop.png")
black_bishop = pygame.image.load("./images/black_bishop.png")
white_queen = pygame.image.load("./images/white_queen.png")
black_queen = pygame.image.load("./images/black_queen.png")
white_king = pygame.image.load("./images/white_king.png")
black_king = pygame.image.load("./images/black_king.png")

board_layout = [['b_rook', 'b_knight', 'b_bishop', 'b_queen', 'b_king', 'b_bishop', 'b_knight', 'b_rook'],
                ['b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn'],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn'],
                ['w_rook', 'w_knight', 'w_bishop', 'w_queen', 'w_king', 'w_bishop', 'w_knight', 'w_rook']]

pieces = {'w_pawn': white_pawn, 'w_rook': white_rook, 'w_knight': white_knight, 'w_bishop': white_bishop, 'w_queen': white_queen, 'w_king': white_king,
          'b_pawn': black_pawn, 'b_rook': black_rook, 'b_knight': black_knight, 'b_bishop': black_bishop, 'b_queen': black_queen, 'b_king': black_king}

selected_x = +inf
selected_y = +inf
valid_moves = []

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


def draw_selection():
    if selected_x != +inf and selected_y != +inf:
        pygame.draw.rect(window, "yellow", [(selected_x * (WIDTH / 8)), (selected_y * (HEIGHT / 8)), (WIDTH / 8), (HEIGHT / 8)], 3)


def draw_valid_moves():
    for i in range(len(valid_moves)):
        pygame.draw.rect(window, "green", [(valid_moves[i][0] * (WIDTH / 8)), (valid_moves[i][1] * (HEIGHT / 8)), (WIDTH / 8), (HEIGHT / 8)], 2)


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


turn = 'w'
running = True
valid_played = False

while running:
    time.tick(FPS)
    draw_board()
    draw_pieces()
    draw_selection()
    draw_valid_moves()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            x = int(event.pos[0] // (WIDTH / 8))
            y = int(event.pos[1] // (HEIGHT / 8))
            colour = board_layout[y][x][:1]
            valid_played = False
            if 0 <= selected_x <= 7 and 0 <= selected_y <= 7:
                for i in range(len(valid_moves)):
                    valid_x = valid_moves[i][0]
                    valid_y = valid_moves[i][1]
                    if x == valid_x and y == valid_y:
                        board_layout[y][x] = board_layout[selected_y][selected_x]
                        board_layout[selected_y][selected_x] = ''
                        valid_played = True
                selected_x = +inf
                selected_y = +inf
                valid_moves = []
            if turn == colour:
                selected_x = x
                selected_y = y
                valid_moves = check_valid_moves(selected_x, selected_y)
            if valid_played:
                if turn == 'w':
                    turn = 'b'
                else:
                    turn = 'w'
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.QUIT
sys.exit()
