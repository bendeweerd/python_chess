"""
Python Chess!

This program implements a simple class for each
square on the chess board.

Created Fall, 2020
@author: Ben DeWeerd
"""

class BoardSquare:
    def __init__(self, row, column, color):
        """This simple class creates class instances for each square"""
        self.row = row
        self.column = column
        self.color = color
        self.has_piece = False
