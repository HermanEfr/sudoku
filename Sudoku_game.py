import tkinter as tk
import sudoku_functions as f

REC_SIDE = 450
PAD = 5
NUMBER_FONT = ('Arial', 20, 'bold')
NAME_FONT = ('Arial', 30, 'bold')


class Sudoku(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title('Sudoku')
        self.master.resizable(False, False)
        self.main_canvas = tk.Canvas(self, bg='white', width=REC_SIDE, height=REC_SIDE, bd=0)
        self.main_canvas.grid(pady=(80, 80), padx=(80, 80))

        self.cells = []
        self.active = (10, 10)
        self.matrix = f.generate_board()
        self.create_gui()

        self.master.bind('<Key>', self.type_number)
        self.main_canvas.bind('<Button-1>', self.mark_square)

        self.mainloop()

    def create_gui(self):
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
                num = self.main_canvas.create_text(x_cord, y_cord, text=text, fill='black', font=NUMBER_FONT)
                cell_data = {'rectangle': rec, 'number': num, 'mutable': mutable}
                cell_row.append(cell_data)
            self.cells.append(cell_row)
        for i in range(1, 9):
            vert = ((REC_SIDE / 9) * i, 0, (REC_SIDE / 9) * i, REC_SIDE)
            hor = (0, (REC_SIDE / 9) * i, REC_SIDE, (REC_SIDE / 9) * i)
            if i % 3 == 0:
                width = 2
            else:
                width = 1
            self.main_canvas.create_line(vert, fill='black', width=width)
            self.main_canvas.create_line(hor, fill='black', width=width)

    def mark_square(self, event):
        x, y = event.x, event.y
        x = int(x // (REC_SIDE / 9))
        y = int(y // (REC_SIDE / 9))
        if self.cells[y][x]['mutable']:
            if self.active == (10, 10):
                old_x, old_y = x, y
            else:
                old_x, old_y = self.active
            self.main_canvas.itemconfigure(self.cells[old_y][old_x]['rectangle'], fill='white')
            self.active = x, y
            self.main_canvas.itemconfigure(self.cells[y][x]['rectangle'], fill='grey')

    def type_number(self, event):
        key = event.char
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        if self.active != (10, 10):
            x, y = self.active
            if key in numbers:
                self.matrix = f.change_number(self.matrix, y, x, int(key))
                self.main_canvas.itemconfigure(self.cells[y][x]['number'], text=str(key), fill='blue')
                self.check_win()
            elif key == 'r':
                self.matrix = f.change_number(self.matrix, y, x, 0)
                self.main_canvas.itemconfigure(self.cells[y][x]['number'], text='')
            elif key == 'c':
                self.main_canvas.itemconfigure(self.cells[y][x]['rectangle'], fill='white')
                self.active = 10, 10

    def check_win(self):
        if f.check_win(self.matrix):
            name_frame = tk.Frame(self)
            name_frame.place(relx=0.5, y=45, anchor='center')
            tk.Label(name_frame, text='Congratulations!', font=NAME_FONT).grid()


if __name__ == "__main__":
    Sudoku()
