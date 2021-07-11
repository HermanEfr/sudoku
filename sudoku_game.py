import tkinter as tk
import sudoku_functions as f
from time import time

REC_SIDE = 450
PAD = 10
FONT = {'Number': ('Arial', 20, 'bold'),
        'Display': ('Arial', 20, 'bold'),
        'Time': ('Arial', 15, 'bold'),
        'Menu': ('Arial', 10, 'bold')}

NUMBER_FONT = ('Arial', 20, 'bold')
NAME_FONT = ('Arial', 20, 'bold')

COLOUR = {'Active': 'peach puff',
          'Number': 'maroon',
          'Robot': 'RoyalBlue2'}
# Små saker att lägga till:
# 1. Knapp till algorithm
# Stora saker:
# 1. Linear annealing algorithm
# 2. OpenCV bildläsare för att skanna in sudokun
# 3. Algorithm X https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X


class Sudoku(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title('Sudoku')
        self.master.resizable(False, False)
        self.main_canvas = tk.Canvas(self, width=REC_SIDE, height=REC_SIDE, bd=0)
        self.main_canvas.grid(row=1, pady=(0, PAD), padx=(PAD, PAD))
        self.panel_frame = tk.Frame(self, width=REC_SIDE, height=35, bd=0)
        self.panel_frame.grid(row=0, pady=(0, 0), padx=(PAD, PAD), sticky='news')
        self.time_frame = tk.Frame(self.panel_frame, bd=0)
        self.time_label = tk.Label(self.time_frame, text='', width=7, font=FONT['Time'])
        self.display_frame = tk.Frame(self.panel_frame, bd=0)
        self.display_label = tk.Label(self.display_frame, text='', font=FONT['Display'])

        self.cells = []
        self.active = (10, 10)
        self.difficulty = tk.StringVar(self)
        self.difficulty.set('Medium')
        self.matrix = f.generate_board(self.difficulty.get())
        self.start_time = time()
        self.after_id = None
        self.run_stopwatch()
        self.create_gui()

        self.master.bind('<Key>', self.type_number)
        self.main_canvas.bind('<Button-1>', self.mark_square)

        self.mainloop()

    def create_gui(self):
        self.create_panel()
        for row in range(9):
            cell_row = []
            for col in range(9):
                x_cord = (REC_SIDE / 9) / 2 + (REC_SIDE / 9) * col
                y_cord = (REC_SIDE / 9) / 2 + (REC_SIDE / 9) * row
                rec_cord = (
                    (REC_SIDE / 9) * col, (REC_SIDE / 9) * row, (REC_SIDE / 9) * (col + 1), (REC_SIDE / 9) * (row + 1))
                if f.number(self.matrix, row, col) == 0:
                    text = ''
                    mutable = True
                else:
                    text = f.number(self.matrix, row, col)
                    mutable = False
                rec = self.main_canvas.create_rectangle(rec_cord, fill='white', width=0)
                num = self.main_canvas.create_text(x_cord, y_cord, text=text, fill='black', font=FONT['Number'])
                cell_data = {'rectangle': rec, 'number': num, 'mutable': mutable}
                cell_row.append(cell_data)
            self.cells.append(cell_row)
        # Creating stripes
        for i in range(1, 9):
            vert = ((REC_SIDE / 9) * i, 0, (REC_SIDE / 9) * i, REC_SIDE)
            hor = (0, (REC_SIDE / 9) * i, REC_SIDE, (REC_SIDE / 9) * i)
            if i % 3 == 0:
                width = 2
            else:
                width = 1
            self.main_canvas.create_line(vert, fill='black', width=width)
            self.main_canvas.create_line(hor, fill='black', width=width)

    def create_panel(self):
        self.panel_frame.grid_columnconfigure((0, 2), weight=1)
        self.panel_frame.grid_columnconfigure(1, weight=4)
        # Creating difficulty menu
        options_list = ['Easy', 'Medium', 'Hard', 'Expert']
        dif_menu = tk.OptionMenu(self.panel_frame, self.difficulty, *options_list, command=self.set_difficulty)
        dif_menu.config(width=7, relief='raised', bd=1, font=FONT['Menu'])
        dif_menu.grid(column=0, row=0, sticky='w')
        # Creating stopwatch and display labels
        self.time_frame.grid(column=2, row=0, sticky='e')
        self.time_label.pack()
        self.display_frame.grid(column=1, row=0)
        self.display_label.configure(text='Sudoku')
        self.display_label.pack()

    def run_stopwatch(self):
        now = time()
        elapsed = int(now - self.start_time)
        second = elapsed % 60
        minute = elapsed // 60
        self.time_label.configure(text=f'{minute:02d}:{second:02d}')
        self.after_id = self.master.after(500, self.run_stopwatch)

    def stop_stopwatch(self):
        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None

    def set_difficulty(self, *args):
        self.matrix = f.generate_board(self.difficulty.get())
        self.cells = []
        self.start_time = time()
        self.stop_stopwatch()
        self.run_stopwatch()
        self.create_gui()
        self.update_idletasks()

    def update_gui(self, colour):
        for row in range(9):
            for col in range(9):
                if self.cells[row][col]['mutable']:
                    if self.matrix[row][col] != 0:
                        num = self.matrix[row][col]
                        self.main_canvas.itemconfigure(self.cells[row][col]['number'], text=str(num),
                                                       fill=colour)
                    else:
                        self.main_canvas.itemconfigure(self.cells[row][col]['number'], text='',
                                                       fill=colour)
        self.update_idletasks()

    def mark_square(self, event):
        x, y = int(event.x // (REC_SIDE / 9)), int(event.y // (REC_SIDE / 9))
        if self.cells[y][x]['mutable']:
            if self.active == (10, 10):
                old_x, old_y = x, y
            else:
                old_x, old_y = self.active
            self.main_canvas.itemconfigure(self.cells[old_y][old_x]['rectangle'], fill='white')
            self.active = x, y
            self.main_canvas.itemconfigure(self.cells[y][x]['rectangle'], fill=COLOUR['Active'])

    def type_number(self, event):
        key = event.char
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        if key == 'b':
            self.brute_force()
        elif self.active != (10, 10):
            x, y = self.active
            if key in numbers:
                self.matrix = f.change_number(self.matrix, y, x, int(key))
                self.main_canvas.itemconfigure(self.cells[y][x]['number'], text=str(key), fill=COLOUR['Number'])
                self.check_win()
            elif key == 'r':
                self.matrix = f.change_number(self.matrix, y, x, 0)
                self.main_canvas.itemconfigure(self.cells[y][x]['number'], text='')
            elif key == 'c':
                self.main_canvas.itemconfigure(self.cells[y][x]['rectangle'], fill='white')
                self.active = 10, 10

    def check_win(self):
        if f.check_win(self.matrix):
            self.display_label.configure(text='Congratulations!')
            self.stop_stopwatch()

    def brute_force(self):
        self.stop_stopwatch()
        self.matrix = f.generate_board(self.difficulty.get())
        brute = f.BruteForceSearch(self.matrix)
        self.matrix = brute.brute_force_search()
        self.update_gui(COLOUR['Robot'])
        self.check_win()


if __name__ == "__main__":
    Sudoku()
