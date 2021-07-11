import numpy as np
import stored_games as sg


# Creating the sudoku matrix
def generate_board(difficulty):
    if difficulty == 'Easy':
        return np.array(sg.Easy[1])
    elif difficulty == 'Medium':
        return np.array(sg.Medium[1])
    elif difficulty == 'Hard':
        return np.array(sg.Hard[1])
    elif difficulty == 'Expert':
        return np.array(sg.Expert[1])


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
        self.board = np.reshape(self.vector, self.shape)
        num = self.vector[self.pointer]
        row = self.pointer // 9
        col = self.pointer % 9
        num_row = self.board[row]
        num_col = self.board.T[col]
        if np.count_nonzero(num_row == num) != 1 or np.count_nonzero(num_col == num) != 1:
            return True
        else:
            cell_row = (row // 3) * 3
            cell_col = (col // 3) * 3
            cell = self.board[cell_row:cell_row+3, cell_col:cell_col+3]
            if np.count_nonzero(cell == num) != 1:
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
                if self.vector[self.pointer] > 9:
                    self.vector[self.pointer] = 0
                    self.board = np.reshape(self.vector, self.shape)
                    self.move_back()
                elif self.check_errors():
                    continue
                else:
                    if self.pointer == self.vector.size - 1:
                        self.solution = True
                        return self.board, self.solution
                    else:
                        self.pointer += 1
            else:
                if self.pointer == self.vector.size - 1:
                    self.solution = True
                    return self.board, self.solution
                else:
                    self.pointer += 1
