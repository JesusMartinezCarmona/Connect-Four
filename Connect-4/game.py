import numpy as np

ROWS = 6
COLS = 7
EMPTY = 0

class Connect4:
    def __init__(self):
        self.board = np.zeros((ROWS, COLS), dtype=int)

    def drop_piece(self, col, piece):
        for r in range(ROWS-1, -1, -1):
            if self.board[r][col] == EMPTY:
                self.board[r][col] = piece
                return r
        return None

    def is_valid_location(self, col):
        return self.board[0][col] == EMPTY

    def get_valid_locations(self):
        return [c for c in range(COLS) if self.is_valid_location(c)]

    def get_state(self):
        # Convierte la matriz en una tupla para usarla como "llave" en el diccionario Q-Table
        return tuple(self.board.flatten())

    def check_win(self, piece):
        for c in range(COLS-3):
            for r in range(ROWS):
                if all(self.board[r][c+i] == piece for i in range(4)): return True
        for c in range(COLS):
            for r in range(ROWS-3):
                if all(self.board[r+i][c] == piece for i in range(4)): return True
        for c in range(COLS-3):
            for r in range(ROWS-3):
                if all(self.board[r+i][c+i] == piece for i in range(4)): return True
        for c in range(COLS-3):
            for r in range(3, ROWS):
                if all(self.board[r-i][c+i] == piece for i in range(4)): return True
        return False