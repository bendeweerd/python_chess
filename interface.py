"""
Python Chess!

This GUI view for the chess game shows the users a chessboard
with pieces.  The user can select the pieces by clicking the
square they are on and move them to another square if the move is valid.

Created Fall, 2020
@author: Ben DeWeerd
"""

import tkinter as tk
from tkinter import simpledialog    # Used for dialog box to input winner name

import tkinter.font as tkFont       # Used to create fonts used in the GUI
import webbrowser                   # Used for 'Cheat Codes' button
import sys

# Import classes from other files
from game import Game
from board_square import BoardSquare

class Interface:
    """The Interface Class shows the GUI - chessboard, pieces, scoreboard, and button"""
    def __init__(self, window):
        """Initialize interface class instance"""
        self.window = window
        self.board = tk.Frame(master=self.window)
        # Start an instance of the game class
        self.game = Game()
        # The board_dict will help keep track of the board pieces
        self.board_dict = {}

        self.create_fonts()

        # Set up an indicator at the top of the window to show the current turn
        self.turn_indicator = tk.Label(
            master = self.window,
            text = "{}'s Turn".format(self.game.current_turn.capitalize()),
            font = self.title_text,
        )
        
        # Create frames on either side of the board to show pieces taken
        self.dead_white = tk.Frame(master=window)
        self.dead_black = tk.Frame(master=window)

        self.scoreview = tk.Frame(master=window)

        # Never gonna give you up
        self.rickroll = tk.Button(
            master=self.scoreview,
            command=self.rickroll,
            text='Cheat Codes',
            font=self.subtitle_text,
        )

        # Initialize the GUI with class methods (see below)
        self.init_board()
        self.update_board()
        self.init_scoreboard()

        # Place the components of the GUI
        self.rickroll.grid(row=1, column=0, pady=(50,0))
        self.scoreview.grid(row=1, column=3, padx=20)

        self.dead_white.grid(row=1, column=0, padx=20)
        self.dead_black.grid(row=1, column=2, padx=20)
        self.turn_indicator.grid(row=0, column=1, pady=15)
        
    def rickroll(self):
        """Never gonna give you up"""
        webbrowser.open('https://youtu.be/dQw4w9WgXcQ')

    def create_fonts(self):
        """Create a set of fonts to be used in the GUI"""
        self.title_text = tkFont.Font(family='Arial', size=36, weight='bold')
        self.subtitle_text = tkFont.Font(family='Arial', size=14, weight='bold')
        self.description_text = tkFont.Font(family='Arial', size=11)

    def init_board(self):
        """Initialize the checkered board pattern, add the pieces to board_dict"""
        for i in range(8):
            if i % 2 == 0:
                self.board_dict[i] = {}
                for j in range(8):
                    if j % 2 == 0:
                        self.board_dict[i][j] = BoardSquare(i, j, 'black')
                    else:
                        self.board_dict[i][j] = BoardSquare(i, j, 'white')
            else:
                self.board_dict[i] = {}
                for j in range(8):
                    if j % 2 == 1:
                        self.board_dict[i][j] = BoardSquare(i, j, 'black')
                    else:
                        self.board_dict[i][j] = BoardSquare(i, j, 'white')

    def update_board(self):
        """Update the board, showing any highlights"""
        for row in self.board_dict:
            for column in self.board_dict[row]:
                btn_frame = tk.Frame(master=self.board, width=80, height=80)
                button = tk.Button(
                    master = btn_frame,
                    # When a square is selected, execute the on_select method with the selected row and column
                    # See https://stackoverflow.com/questions/17677649/tkinter-assign-button-command-in-loop-with-lambda?noredirect=1&lq=1
                    command = lambda row=row, column=column: self.on_select(row, column),
                    # access the correct color for this board square from the class instance
                    bg = self.board_dict[row][column].color,
                    borderwidth = 7,
                )
                button.place(x=0, y=0, height=80, width=80)
                btn_frame.grid(
                    row=row,
                    column=column,
                )
        # Place the board in the window grid
        self.board.grid(
            row = 1,
            column = 1,
            pady = (0, 20)
        )
        # Call the place_pieces method to show all pieces in their current locations
        self.place_pieces()

    def place_pieces(self):
        """Place each piece still alive on the board"""
        for i in range(8):
            for j in range(8):
                # Start with a blank slate
                self.board_dict[i][j].has_piece = False
        # Check if each piece is alive, if so place it on the board
        for key in self.game.pieces_dict:
            if self.game.pieces_dict[key].alive == True:
                piece = tk.Label(master=self.board, image=self.game.pieces_dict[key].image)
                piece.grid(
                    row=self.game.pieces_dict[key].row, 
                    column=self.game.pieces_dict[key].column,
                )
                # Update the board_dict to show that the square has a piece on it
                self.board_dict[self.game.pieces_dict[key].row][self.game.pieces_dict[key].column].has_piece = self.game.pieces_dict[key].color

    def clear_highlights(self):
        """Resets all the squares on the board to their original color"""
        for i in range(8):
            if i % 2 == 0:
                for j in range(8):
                    if j % 2 == 0:
                        self.board_dict[i][j].color = 'black'
                    else:
                        self.board_dict[i][j].color = 'white'
            else:
                for j in range(8):
                    if j % 2 == 1:
                        self.board_dict[i][j].color = 'black'
                    else:
                        self.board_dict[i][j].color = 'white'

    def on_select(self, row, column):
        """This function handles the selection of any square on the board"""
        if self.game.has_piece(row, column) == True:
            # If the square has a piece on it, determine which piece that is
            for key in self.game.pieces_dict:
                # Find which piece has been selected
                if self.game.pieces_dict[key].row == row and self.game.pieces_dict[key].column == column and self.game.pieces_dict[key].alive == True:
                    piece_selected = key
                    piece_type = self.game.pieces_dict[key].piece_type
                    piece_color = self.game.pieces_dict[key].color

            # If the color of the piece selected is the same as the current turn, show possible moves for that piece
            if piece_color == self.game.current_turn:
                # Create a clean slate, remove any past highlights and clear the valid moves list
                self.piece_to_move = piece_selected
                self.game.valid_moves = []
                self.clear_highlights()

                # Get the valid moves for the piece selected, using methods from the game class
                if piece_type == "king":
                    self.game.valid_moves = self.game.get_king_moves(row, column, piece_color, self.board_dict)
                elif piece_type == "knight":
                    self.game.valid_moves = self.game.get_knight_moves(row, column, piece_color, self.board_dict)
                elif piece_type == "queen":
                    self.game.valid_moves = self.game.get_queen_moves(row, column, piece_color, self.board_dict)
                elif piece_type == "bishop":
                    self.game.valid_moves = self.game.get_bishop_moves(row, column, piece_color, self.board_dict)
                elif piece_type == "rook":
                    self.game.valid_moves = self.game.get_rook_moves(row, column, piece_color, self.board_dict)
                elif piece_type == "pawn":
                    # Pawns have to know some additional information about themselves (their first move is different)
                    self.game.valid_moves = self.game.get_pawn_moves(row, column, piece_color, self.board_dict, self.game.pieces_dict[self.piece_to_move].is_first_turn)

                # Highlight selected piece in blue
                self.board_dict[row][column].color = '#120078'

                # Highlight valid moves in purple, kill moves in yellow
                for item in self.game.valid_moves:
                    if self.board_dict[item[0]][item[1]].has_piece != piece_color and self.board_dict[item[0]][item[1]].has_piece != False:
                        # highlight possible kill moves in yellow
                        self.board_dict[item[0]][item[1]].color = '#fecd1a'
                    else:
                        # highlight possible non-kill moves in purple
                        self.board_dict[item[0]][item[1]].color = '#9d0191'

                self.update_board()

            elif piece_color != self.game.current_turn:
                # If a piece selected is of the opposite color, check if it's a valid kill move.  If so, execute it.
                proposed_move = [row, column]
                if proposed_move in self.game.valid_moves:
                    self.piece_to_kill = piece_selected
                    
                    # Move the piece to the new location
                    self.game.pieces_dict[self.piece_to_move].row = row
                    self.game.pieces_dict[self.piece_to_move].column = column
                    
                    # Remove the piece killed from the game
                    self.game.pieces_dict[self.piece_to_kill].alive = False
                    self.game.valid_moves = []

                    # Pawns have different rules for their first turn - if a pawn moves, indicate that it's no longer their first turn
                    if self.game.pieces_dict[self.piece_to_move].piece_type == "pawn":
                        self.game.pieces_dict[self.piece_to_move].is_first_turn = False
                        
                    # Change turn to other player, get board ready for their turn
                    self.game.swap_turn()
                    self.clear_highlights()
                    self.update_board()
                    self.update_turn_indicator()
                    self.update_dead()

        elif [row, column] in self.game.valid_moves:
            # If the selected move is valid but not a kill move, simply move the piece to that location and change turn
            self.game.pieces_dict[self.piece_to_move].row = row
            self.game.pieces_dict[self.piece_to_move].column = column

            # Pawns have different rules for their first turn - if a pawn moves, indicate that it's no longer their first turn
            if self.game.pieces_dict[self.piece_to_move].piece_type == "pawn":
                self.game.pieces_dict[self.piece_to_move].is_first_turn = False

            self.game.valid_moves = []

            # Change turn to other player, get board ready for their turn
            self.game.swap_turn()
            self.clear_highlights()
            self.update_board()
            self.update_turn_indicator()

    def update_turn_indicator(self):
        """Update turn indicator to show the current turn"""
        self.turn_indicator = tk.Label(
            master = self.window,
            text = "{}'s Turn".format(self.game.current_turn.capitalize()),
            font = self.title_text,
        )
        self.turn_indicator.grid(
            row=0,
            column=1,
            pady=15,
        )

    def update_dead(self):
        """Update the display of pieces taken"""
        
        # Get list of dead white pieces
        dead_white_pieces = []
        for key in self.game.pieces_dict:
            if self.game.pieces_dict[key].color == "white" and self.game.pieces_dict[key].alive == False:
                dead_white_pieces.append(key)

        # Get list of dead black pieces
        dead_black_pieces = []
        for key in self.game.pieces_dict:
            if self.game.pieces_dict[key].color == "black" and self.game.pieces_dict[key].alive == False:
                dead_black_pieces.append(key)

        for item in dead_white_pieces:
            # Get the icon for the dead piece, just a miniature version of the one shown on the board
            pic = self.game.pieces_dict[item].image.subsample(2,2)
            # Create a small frame to show each piece, grid it
            deadpieceframe = tk.Frame(master=self.dead_white)
            deadpiecelabel = tk.Label(master=deadpieceframe, image=pic)
            deadpiecelabel.image = pic
            deadpiecelabel.grid(column=0, row=0)
            deadpieceframe.grid(column=0, row=dead_white_pieces.index(item))

        for item in dead_black_pieces:
            # Get the icon for the dead piece, just a miniature version of the one shown on the board
            pic = self.game.pieces_dict[item].image.subsample(2,2)
            # Create a small frame to show each piece, grid it
            deadpieceframe = tk.Frame(master=self.dead_black)
            deadpiecelabel = tk.Label(master=deadpieceframe, image = pic)
            deadpiecelabel.image = pic
            deadpiecelabel.grid(column=0, row=0)
            deadpieceframe.grid(column=0, row=dead_black_pieces.index(item))

        # If a king is dead, update the scoreboard file and end the game
        if self.game.pieces_dict['white_king'].alive == False:
            self.update_scoreboard('black')
            self.end_game()
        if self.game.pieces_dict['black_king'].alive == False:
            self.update_scoreboard('white')
            self.end_game()

        self.dead_white.grid(row=1, column=0, padx=20)
        self.dead_black.grid(row=1, column=2, padx=20)

    def init_scoreboard(self):
        """Initialize the scoreboard, reading the data from the leaderboard.txt file"""
        with open('leaderboard.txt', 'r+') as leaderboard:
            self.score_dict = {}
            leaders = leaderboard.read().splitlines()
            for item in leaders:
                # Create an entry on the scoreboard for each line in the leaderboard.txt file
                entry = item.split()
                self.score_dict[entry[0]] = int(entry[1])

            # Get a dictionary of values sorted by the score
            # See https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
            self.sorted_dict = {k: v for k, v in sorted(self.score_dict.items(), key=lambda item: item[1])}

            self.scoreboard = tk.Frame(master=self.scoreview)

            self.names = list(self.sorted_dict.keys())

            leaderboard_title = tk.Label(master=self.scoreboard, text='Leaderboard', font=self.subtitle_text)
            leaderboard_title.grid(row=0, column=0, columnspan=2)

            leaderboard_description = tk.Label(master=self.scoreboard, text='(Turns to kill King):', font=self.description_text)
            leaderboard_description.grid(row=1, column=0, columnspan=2, pady=(0,5))

            for i in range(len(self.sorted_dict)):
                # Get name for each label
                name = self.names[i]
                name_label = tk.Label(master=self.scoreboard, text=name)
                name_label.grid(row=i+2, column=0)

                # Get the corresponding score
                name_score = self.sorted_dict[name]
                name_score_label = tk.Label(master=self.scoreboard, text=name_score)
                name_score_label.grid(row=i+2, column=1)

        self.scoreboard.grid(row=0, column=0)

    def update_scoreboard(self, winner):
        """Prompt for the winner's name to add to the scoreboard using a dialog box"""
        winner_name = simpledialog.askstring('Input', "Enter the winner's first name:", parent=self.window)

        if winner_name == None:
            # If the user hits the cancel button, re-raise the prompt
            print('winner name: {}'.format(winner_name))
            # This actually uses recursion, something I didn't foresee needing...
            self.update_scoreboard(winner)    
            return

        # Update the leaderboard.txt file with the given name and their respective score (moves to kill the king)
        with open('leaderboard.txt', 'a+') as leaderboard:
            if winner == 'white':
                winner_score = self.game.num_white_turns
            elif winner == 'black':
                winner_score = self.game.num_black_turns
            
            print("winner name: {}".format(winner_name))
            print("winner score: {}".format(winner_score))
            
            entry = winner_name + ' ' + str(winner_score)
            print("entry:", entry)
            leaderboard.write(entry + '\n')

    def end_game(self):
        """End the game"""
        sys.exit()

# Create the interface
if __name__ == '__main__':
    window = tk.Tk()
    window.title('Python Chess!')
    app = Interface(window)
    window.mainloop()
