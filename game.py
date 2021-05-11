"""
Python Chess!

This program implements the move and game logic for the chess program.

Created Fall, 2020
@author: Ben DeWeerd
"""

from piece import Piece     # Import the piece class, used to construct new pieces

class Game:
    """This class handles the game and move logic"""
    def __init__(self):
        """Initialize the game class, which keeps track of the pieces and handles move logic"""
        
        # White always starts the game
        self.current_turn = 'white'
        self.num_white_turns = 0
        self.num_black_turns = 0

        self.valid_moves = []

        self.pieces_dict = {}
        # Initialize the set of pieces using the Piece class (see below)
        self.init_pieces_dict()

    def swap_turn(self):
        """Change the current turn and keep track of how many moves each player has completed"""
        if self.current_turn == 'black':
            self.num_black_turns += 1
            self.current_turn = 'white'
        elif self.current_turn == 'white':
            self.num_white_turns += 1
            self.current_turn = 'black'

    def init_pieces_dict(self):
        """Use the Piece class to construct a dictionary of the pieces"""
        self.pieces_dict['white_rook_1'] = Piece(True, 'whiterook', 7, 0, 'white', 'rook')
        self.pieces_dict['white_knight_1'] = Piece(True, 'whiteknight', 7, 1, 'white', 'knight')
        self.pieces_dict['white_bishop_1'] = Piece(True, 'whitebishop', 7, 2, 'white', 'bishop')
        self.pieces_dict['white_king'] = Piece(True, 'whiteking', 7, 3, 'white', 'king')
        self.pieces_dict['white_queen'] = Piece(True, 'whitequeen', 7, 4, 'white', 'queen')
        self.pieces_dict['white_bishop_2'] = Piece(True, 'whitebishop', 7, 5, 'white', 'bishop')
        self.pieces_dict['white_knight_2'] = Piece(True, 'whiteknight', 7, 6, 'white', 'knight')
        self.pieces_dict['white_rook_2'] = Piece(True, 'whiterook', 7, 7, 'white', 'rook')

        self.pieces_dict['white_pawn_1'] = Piece(True, 'whitepawn', 6, 0, 'white', 'pawn', True)
        self.pieces_dict['white_pawn_2'] = Piece(True, 'whitepawn', 6, 1, 'white', 'pawn', True)
        self.pieces_dict['white_pawn_3'] = Piece(True, 'whitepawn', 6, 2, 'white', 'pawn', True)
        self.pieces_dict['white_pawn_4'] = Piece(True, 'whitepawn', 6, 3, 'white', 'pawn', True)
        self.pieces_dict['white_pawn_5'] = Piece(True, 'whitepawn', 6, 4, 'white', 'pawn', True)
        self.pieces_dict['white_pawn_6'] = Piece(True, 'whitepawn', 6, 5, 'white', 'pawn', True)
        self.pieces_dict['white_pawn_7'] = Piece(True, 'whitepawn', 6, 6, 'white', 'pawn', True)
        self.pieces_dict['white_pawn_8'] = Piece(True, 'whitepawn', 6, 7, 'white', 'pawn', True)

        self.pieces_dict['black_rook_1'] = Piece(True, 'blackrook', 0, 0, 'black', 'rook')
        self.pieces_dict['black_knight_1'] = Piece(True, 'blackknight', 0, 1, 'black', 'knight')
        self.pieces_dict['black_bishop_1'] = Piece(True, 'blackbishop', 0, 2, 'black', 'bishop')
        self.pieces_dict['black_king'] = Piece(True, 'blackking', 0, 3, 'black', 'king')
        self.pieces_dict['black_queen'] = Piece(True, 'blackqueen', 0, 4, 'black', 'queen')
        self.pieces_dict['black_bishop_2'] = Piece(True, 'blackbishop', 0, 5, 'black', 'bishop')
        self.pieces_dict['black_knight_2'] = Piece(True, 'blackknight', 0, 6, 'black', 'knight')
        self.pieces_dict['black_rook_2'] = Piece(True, 'blackrook', 0, 7, 'black', 'rook')

        self.pieces_dict['black_pawn_1'] = Piece(True, 'blackpawn', 1, 0, 'black', 'pawn', True)
        self.pieces_dict['black_pawn_2'] = Piece(True, 'blackpawn', 1, 1, 'black', 'pawn', True)
        self.pieces_dict['black_pawn_3'] = Piece(True, 'blackpawn', 1, 2, 'black', 'pawn', True)
        self.pieces_dict['black_pawn_4'] = Piece(True, 'blackpawn', 1, 3, 'black', 'pawn', True)
        self.pieces_dict['black_pawn_5'] = Piece(True, 'blackpawn', 1, 4, 'black', 'pawn', True)
        self.pieces_dict['black_pawn_6'] = Piece(True, 'blackpawn', 1, 5, 'black', 'pawn', True)
        self.pieces_dict['black_pawn_7'] = Piece(True, 'blackpawn', 1, 6, 'black', 'pawn', True)
        self.pieces_dict['black_pawn_8'] = Piece(True, 'blackpawn', 1, 7, 'black', 'pawn', True)

    def is_in_board(self, row, column):
        """Check if a square is inside the board"""
        if row >= 0 and column >= 0 and row <= 7 and column <= 7:
            return True
        else:
            return False

    def has_piece(self, row, column):
        """Check if a selected square has a piece on it"""
        for key in self.pieces_dict:
            if self.pieces_dict[key].row == row and self.pieces_dict[key].column == column and self.pieces_dict[key].alive == True:
                return True
        return False

    def get_king_moves(self, row, column, piece_color, board_dict):
        """Return valid moves for a king"""
        possible_king_moves = [[row + 1, column], [row - 1, column], [row, column + 1], [row, column - 1], [row+1, column+1], [row+1, column-1], [row-1, column+1], [row-1, column-1] ]
        valid_moves = []
        for move in possible_king_moves:
            # check if the move is in the board and if another piece is there
            if self.is_in_board(move[0], move[1]) == True and (move[0] != row or move[1] != column):
                # check if a piece of the same color is there - if not, don't include the move
                if board_dict[move[0]][move[1]].has_piece != piece_color:
                    valid_moves.append(move)
        return valid_moves

    def get_queen_moves(self, row, column, piece_color, board_dict):
        """Return valid moves for a queen"""
        possible_queen_moves = []
        valid_moves = []

        ##### BISHOP STYLE #####

        piece_hit = False
        i = 0

        while piece_hit == False and i < 8:
            i += 1
            possible_queen_moves.append([row+i, column+i])
            if self.has_piece(row + i, column + i) == True:
                piece_hit = True

        piece_hit = False
        i = 0

        while piece_hit == False and i < 8:
            i += 1
            possible_queen_moves.append([row+i, column-i])
            if self.has_piece(row + i, column - i) == True:
                piece_hit = True

        piece_hit = False
        i = 0

        while piece_hit == False and i < 8:
            i += 1
            possible_queen_moves.append([row-i, column+i])
            if self.has_piece(row - i, column + i) == True:
                piece_hit +=1

        piece_hit = False
        i = 0

        while piece_hit == False and i < 8:
            i += 1
            possible_queen_moves.append([row-i, column-i])
            if self.has_piece(row - i, column - i) == True:
                piece_hit = True

        ##### ROOK STYLE #####

        piece_hit = False
        i = 0

        while piece_hit == False and i < 8:
            i += 1
            possible_queen_moves.append([row+i, column])
            if self.has_piece(row + i, column) == True:
                piece_hit = True

        piece_hit = False
        i = 0

        while piece_hit == False and i < 8:
            i += 1
            possible_queen_moves.append([row-i, column])
            if self.has_piece(row - i, column) == True:
                piece_hit = True

        piece_hit = False
        i = 0

        while piece_hit == False and i < 8:
            i += 1
            possible_queen_moves.append([row, column-i])
            if self.has_piece(row, column-i) == True:
                piece_hit = True

        piece_hit = False
        i = 0

        while piece_hit == False and i < 8:
            i += 1
            possible_queen_moves.append([row, column+i])
            if self.has_piece(row, column+i) == True:
                piece_hit = True

        piece_hit = False
        i = 0

        for move in possible_queen_moves:
            # Validate these moves, return the valid options
            if self.is_in_board(move[0], move[1]) == True and (move[0] != row or move[1] != column):
                if board_dict[move[0]][move[1]].has_piece != piece_color:
                    valid_moves.append(move)
        return valid_moves

    
    def get_bishop_moves(self, row, column, piece_color, board_dict):
        """Return valid moves for a bishop"""
        possible_bishop_moves = []
        valid_moves = []

        piece_hit = False
        i = 0

        while piece_hit == False and i < 8:
            i += 1
            possible_bishop_moves.append([row+i, column+i])
            if self.has_piece(row + i, column + i) == True:
                piece_hit = True

        piece_hit = False
        i = 0

        while piece_hit == False and i < 8:
            i += 1
            possible_bishop_moves.append([row+i, column-i])
            if self.has_piece(row + i, column - i) == True:
                piece_hit = True

        piece_hit = False
        i = 0

        while piece_hit == False and i < 8:
            i += 1
            possible_bishop_moves.append([row-i, column+i])
            if self.has_piece(row - i, column + i) == True:
                piece_hit +=1

        piece_hit = False
        i = 0

        while piece_hit == False and i < 8:
            i += 1
            possible_bishop_moves.append([row-i, column-i])
            if self.has_piece(row - i, column - i) == True:
                piece_hit = True

        piece_hit = False
        i = 0

        for move in possible_bishop_moves:
            if self.is_in_board(move[0], move[1]) == True and (move[0] != row or move[1] != column):

                # make sure it wouldn't move on top of a piece of the same color
                if board_dict[move[0]][move[1]].has_piece != piece_color:
                    valid_moves.append(move)
        return valid_moves
    

    def get_knight_moves(self, row, column, piece_color, board_dict):
        """Return valid moves for a knight"""
        possible_knight_moves = [[row+2, column-1], [row+2, column+1], [row+1, column+2], [row-1, column+2], [row-2, column+1], [row-2, column-1], [row-1, column-2], [row+1, column-2]]
        valid_moves = []
        for move in possible_knight_moves:
            if self.is_in_board(move[0], move[1]) == True and (move[0] != row or move[1] != column):
                if board_dict[move[0]][move[1]].has_piece != piece_color:
                    valid_moves.append(move)
        return valid_moves
    

    def get_rook_moves(self, row, column, piece_color, board_dict):
        """Return valid moves for a rook"""
        possible_rook_moves = []
        valid_moves = []

        piece_hit = False
        i = 0

        while piece_hit == False and i < 8:
            i += 1
            possible_rook_moves.append([row-i, column])
            if self.has_piece(row - i, column) == True:
                piece_hit = True

        piece_hit = False
        i = 0

        while piece_hit == False and i < 8:
            i += 1
            possible_rook_moves.append([row+i, column])
            if self.has_piece(row + i, column) == True:
                piece_hit = True

        piece_hit = False
        i = 0

        while piece_hit == False and i < 8:
            i += 1
            possible_rook_moves.append([row, column-i])
            if self.has_piece(row, column-i) == True:
                piece_hit = True

        piece_hit = False
        i = 0

        while piece_hit == False and i < 8:
            i += 1
            possible_rook_moves.append([row, column+i])
            if self.has_piece(row, column+i) == True:
                piece_hit = True

        piece_hit = False
        i = 0

        for move in possible_rook_moves:
            if self.is_in_board(move[0], move[1]) == True and (move[0] != row or move[1] != column):
                if board_dict[move[0]][move[1]].has_piece != piece_color:
                    valid_moves.append(move)
        return valid_moves  

    def get_pawn_moves(self, row, column, piece_color, board_dict, is_first_turn):
        """Return valid moves for a pawn"""
        possible_pawn_moves = []
        valid_moves = []

        # add vertical moves, 2 options if it's the first move
        if piece_color == 'white' and self.has_piece(row-1, column) == False:
            possible_pawn_moves.append([row - 1, column])

            if is_first_turn == True and self.has_piece(row-2, column) == False:
                possible_pawn_moves.append([row - 2, column])

        elif piece_color == 'black' and self.has_piece(row+1, column) == False:
            possible_pawn_moves.append([row + 1, column])

            if is_first_turn == True and self.has_piece(row+2, column) == False:
                possible_pawn_moves.append([row + 2, column])

        # Add sideways motion if another piece is adjacent
        if piece_color == 'white' and self.is_in_board(row - 1, column - 1):
            if board_dict[row - 1][column - 1].has_piece == 'black':
                valid_moves.append([row-1, column-1])

        if piece_color == 'white' and self.is_in_board(row - 1, column + 1):
            if board_dict[row - 1][column + 1].has_piece == 'black':
                valid_moves.append([row-1, column+1])

        if piece_color == 'black' and self.is_in_board(row + 1, column - 1):
            if board_dict[row + 1][column - 1].has_piece == 'white':
                valid_moves.append([row+1, column-1])

        if piece_color == 'black' and self.is_in_board(row + 1, column + 1):
            if board_dict[row + 1][column + 1].has_piece == 'white':
                valid_moves.append([row+1, column+1])


        for move in possible_pawn_moves:
            if self.is_in_board(move[0], move[1]) == True and (move[0] != row or move[1] != column):
                if board_dict[move[0]][move[1]].has_piece != piece_color:
                    valid_moves.append(move)
        return valid_moves



########### Testing ##########

if __name__ == '__main__':
    # Just import these here for testing; don't typically need it as part of this module
    from board_square import BoardSquare
    import tkinter as tk

    # This is needed to use the image attributes used to create piece objects
    test_window = tk.Tk()
    test_game = Game()

    board_dict = {}

    # Create a board_dict for testing purposes
    for i in range(8):
            if i % 2 == 0:
                board_dict[i] = {}
                for j in range(8):
                    if j % 2 == 0:
                        board_dict[i][j] = BoardSquare(i, j, 'black')
                    else:
                        board_dict[i][j] = BoardSquare(i, j, 'white')
            else:
                board_dict[i] = {}
                for j in range(8):
                    if j % 2 == 1:
                        board_dict[i][j] = BoardSquare(i, j, 'black')
                    else:
                        board_dict[i][j] = BoardSquare(i, j, 'white')

    # Test is_in_board method
    assert test_game.is_in_board(0, 0) == True
    assert test_game.is_in_board(3, 3) == True
    assert test_game.is_in_board(8, 8) == False

    board_dict[6][7].has_piece = 'white'

    # Test has_piece method
    assert test_game.has_piece(6, 7) == True
    
    # Test rook
    assert [6, 7] not in test_game.get_rook_moves(7, 7, 'white', board_dict)
    assert [6, 7] in test_game.get_rook_moves(7, 7, 'black', board_dict) 
    assert [9, 9] not in test_game.get_rook_moves(7, 7, 'white', board_dict)

    # Test king
    assert [6, 7] in test_game.get_king_moves(7, 7, 'black', board_dict)
    assert [6, 7] not in test_game.get_king_moves(7, 7, 'white', board_dict)
    assert [7, 6] in test_game.get_king_moves(7, 7, 'white', board_dict)

    # Test queen
    assert [6, 7] in test_game.get_queen_moves(5, 6, 'black', board_dict)
    assert [6, 7] in test_game.get_queen_moves(1, 2, 'black', board_dict)
    assert [0, 0] in test_game.get_queen_moves(1, 1, 'white', board_dict)

    # Test bishop
    assert [6, 7] in test_game.get_bishop_moves(5, 6, 'black', board_dict)
    assert [6, 7] not in test_game.get_bishop_moves(6, 0, 'black', board_dict)
    assert [6, 7] not in test_game.get_bishop_moves(5, 6, 'white', board_dict)

    # Test pawn
    assert [6, 7] in test_game.get_pawn_moves(5, 6, 'black', board_dict, True)
    assert [6, 7] not in test_game.get_pawn_moves(5, 7, 'black', board_dict, True)
    assert [4, 3] in test_game.get_pawn_moves(6, 3, 'white', board_dict, True)
    assert [4, 3] not in test_game.get_pawn_moves(6, 3, 'white', board_dict, False)

    print('Yay! All tests passed!')
    

