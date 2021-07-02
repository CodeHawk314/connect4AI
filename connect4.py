import numpy as np
# import sys
# import math
# import pygame


class Connect4:

    def __init__(self, ROW_COUNT=6, COLUMN_COUNT=7):
        self.ROW_COUNT = ROW_COUNT
        self.COLUMN_COUNT = COLUMN_COUNT

        self.board = self.create_board()
        self.curr_player = 1

    def create_board(self):
        return np.zeros((self.ROW_COUNT, self.COLUMN_COUNT))

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[self.ROW_COUNT-1][col] == 0

    def get_next_open_row(self, col):
        for r in range(self.ROW_COUNT):
            if self.board[r][col] == 0:
                return r

    def print_board(self, board=None):
        if board:
            print(np.flip(board, 0))
        else:
            print(np.flip(self.board))

    def is_winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(self.COLUMN_COUNT-3):
            for r in range(3, self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True

    def switch_player(self):
        self.curr_player = (self.curr_player % 2) + 1

    def play_move(self, col):
        if self.is_valid_location(col):
            row = self.get_next_open_row(col)

            self.drop_piece(row, col, self.curr_player)

            if self.is_winning_move(self.curr_player):
                return self.curr_player

            # flip the player
            self.switch_player()

        # self.print_board()
        return None

    def neural_net_board_encoding(self):
        new_encoding = np.zeros((3, self.ROW_COUNT, self.COLUMN_COUNT))

        for i in range(3):
            new_encoding[i, :, :] = (self.board == (i + 1) % 3)

        # for r in range(self.ROW_COUNT):
        #     for c in range(self.COLUMN_COUNT):
        #         if self.board[r][c] == 1:
        #             new_encoding[r][c][0] = 1
        #         elif self.board[r][c] == 2:
        #             new_encoding[r][c][1] = 1
        #         else:
        #             new_encoding[r][c][2] = 1

        return new_encoding


game = Connect4()

game.play_move(0)
game.play_move(0)
game.play_move(0)

game.print_board()

print(game.neural_net_board_encoding())


"""
# colors for pygame
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
"""

"""
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r *
                            SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(
                c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(
                    c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(
                    c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()
"""

# board = create_board()
# print_board(board)
# game_over = False
# turn = 0


"""
# initalize pygame
# pygame.init()

# define our screen size
SQUARESIZE = 100

# define width and height of board
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

# screen = pygame.display.set_mode(size)
# Calling function draw_board again
# draw_board(board)
# pygame.display.update()

# myfont = pygame.font.SysFont("monospace", 75)

"""

"""
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(
                    screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(
                    screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # print(event.pos)
            # Ask for Player 1 Input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

            # # Ask for Player 2 Input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render("Player 2 wins!!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)
"""
