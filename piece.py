"""
Python Chess!

This program contains a piece class, used to construct a dictionary of pieces
and generate their attributes.

Created Fall, 2020
@author: Ben DeWeerd
"""

import tkinter as tk       # Used to make the image attribute for each piece
import os                  # Used to get the filename for the image

class Piece():
    def __init__(self, alive, icon, row, column, color, piecetype, is_pawn=False):
        """Create a piece object with the corresponding attributes"""
        self.alive = alive
        self.icon = icon
        self.row = row
        self.column = column
        self.color = color
        self.piece_type = piecetype
        if is_pawn == True:
            self.is_first_turn = True
        self.image = self.get_image()

    def get_image(self):
        """Get the image for the piece, save it as a class attribute"""
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'chessicons', self.icon + '.gif')
        pic = tk.PhotoImage(file=filename)
        pic = pic.subsample(12, 12)
        return pic
