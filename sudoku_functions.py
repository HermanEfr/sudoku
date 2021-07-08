import numpy as np
from time import sleep

# Creating the sudoku matrix
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


# Functions for changing and checking board
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


# Solver using Brute-force search

class BruteForceSearch:
    def __init__(self, board):
        self.board = board
        self.shape = np.shape(self.board)
        self.vector = np.reshape(self.board, -1)
        self.template = self.vector == 0
        self.solution = False
        self.pointer = 0

    def check_errors(self):
        for i in self.board:
            i = i[i != 0]
            if len(np.unique(i)) != len(i):
                return True
        else:
            for i in self.board.T:
                i = i[i != 0]
                if len(np.unique(i)) != len(i):
                    return True
            else:
                for i in [0, 3, 6]:
                    for j in [0, 3, 6]:
                        cell = self.board[i:i+3, j:j+3]
                        cell = cell[cell != 0]
                        if len(np.unique(cell)) != len(cell):
                            return True
                else:
                    return False

    def move_back(self):
        for i in reversed(range(self.pointer)):
            if self.template[i]:
                self.pointer = i
                break

    def brute_force_search(self):
        while not self.solution:
            if self.template[self.pointer]:
                self.vector[self.pointer] += 1
                self.board = np.reshape(self.vector, self.shape)
                if self.vector[self.pointer] > 9:
                    self.vector[self.pointer] = 0
                    self.move_back()
                elif self.check_errors():
                    continue
                else:
                    if self.pointer == self.vector.size - 1:
                        self.solution = True
                    else:
                        self.pointer += 1
            else:
                if self.pointer == self.vector.size - 1:
                    self.solution = True
                else:
                    self.pointer += 1
            return self.board, self.solution
