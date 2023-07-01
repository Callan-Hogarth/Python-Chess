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


turn = 'w'
running = True

while running:
    time.tick(FPS)
    draw_board()
    draw_pieces()
    draw_selection()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            selected_x = event.pos[0]
            selected_y = event.pos[1]
            selected_x //= (WIDTH / 8)
            selected_y //= (HEIGHT / 8)
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.QUIT
sys.exit()
