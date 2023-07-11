import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from board import Board


# GUI
class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Two")
        self.root.configure(bg='white')

        line1 = tk.Frame(root, width=300, height=2, bg="black")
        line1.grid(row=0, column=0, columnspan=3,sticky="swse")
        line2 = tk.Frame(root, width=300, height=2, bg="black")
        line2.grid(row=1, column=0, columnspan=3,sticky="swse")
        line3 = tk.Frame(self.root, width=2, height=300, bg="black")
        line3.grid(row=0, column=0, rowspan=3, sticky="nese")
        line4 = tk.Frame(self.root, width=2, height=300, bg="black")
        line4.grid(row=0, column=1, rowspan=3, sticky="nese")

        self.prepare_board()



    def prepare_board(self):
        self.game = Board()

        self.buttons = []
        for row in range(3):
            row_buttons = []

            for col in range(3):
                button = tk.Button(self.root, text="", font=("Arial", 50), width=5, height=2,relief='flat',overrelief='solid',
                                   command=lambda r=row, c=col: self.make_move(r,c))
                button.grid(row=row, column=col, padx=5, pady=5)
                button.configure(bg="white")
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def make_move(self, row, col):
        cell_index = row*3+col
        if self.game.apply_move(cell_index):
            self.buttons[row][col].configure(text=self.game._value_to_char(self.game.board[cell_index]))
            result = self.game.check_win()
            if result:
                self.show_result(result)
            self.game.current_player = not self.game.current_player
            self.update_buttons()

    def update_buttons(self):
        valid_moves = self.game.available_moves()
        for row in range(3):
            for col in range(3):
                if row*3+col not in valid_moves:
                    self.buttons[row][col].configure(overrelief='flat')
                else:
                    self.buttons[row][col].configure(overrelief='solid')


    def show_result(self, result):
        if result == "draw":
            messagebox.showinfo("Game Over", "It's a draw!")
        else:
            messagebox.showinfo("Game Over", f'{"player 1" if self.game.current_player else "player 2"} wins!')
        self.prepare_board()


