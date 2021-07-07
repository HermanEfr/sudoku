# Change numbers, check if win,
import numpy as np


def generate_board():
    board = np.array([[8, 1, 0, 0, 3, 0, 0, 2, 7],
                    [0, 6, 2, 0, 5, 0, 0, 9, 0],
                    [0, 7, 0, 0, 0, 0, 0, 0, 0],
                    [0, 9, 0, 6, 0, 0, 1, 0, 0],
                    [1, 0, 0, 0, 2, 0, 0, 0, 4],
                    [0, 0, 8, 0, 0, 5, 0, 7, 0],
                    [0, 0, 0, 0, 0, 0, 0, 8, 0],
                    [0, 2, 0, 0, 1, 0, 7, 5, 0],
                    [3, 8, 0, 0, 7, 0, 0, 4, 2]])
    return board


def change_number(board, row, col, new):
    board[row][col] = new
    return board


def number(board, row, col):
    return board[row][col]


def check_win(board):
    template = np.arange(1, 10)
    errors = 0
    for i in range(9):
        row, col = np.sort(board[i, :]), np.sort(board[:, i])
        if not np.array_equal(row, template):
            errors += 1
        if not np.array_equal(col, template):
            errors += 1
    if errors == 0:
        return True
    else:
        return False
