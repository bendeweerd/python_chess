"""Python Chess!

TODO:
Fix piece button issue - user should be able to select by clicking the picture
Add a scoreboard - based on moves to kill king, write to external file (display by board too?)
    If the entered name is the same as one that already exists in the scoreboard, update the previous entry rather than creating a new line
Add beginning and ending animations
Add pawn promotion?? - append piece to pieces_dict??
Change the pieces_dict to class instances? This may simplify pawn promotion

"""
import tkinter as tk

# Import the pieces_dict dictionary, which has information about each piece on the board
from pieces_dict import pieces_dict

from piececlass import Piece

from tkinter import simpledialog

import tkinter.font as tkFont
import os            # Needed to access files
import webbrowser    ##Needed for a VERY IMPORTANT task later ;)

# Initialize Tkinter window, name it
window = tk.Tk()
window.title("Python Chess!")

# window.configure(bg='white')

# configure the window sections
window.rowconfigure(0, weight = 1)
window.rowconfigure(1, weight = 1)

for i in range(4):
    window.columnconfigure(i, weight=1)

board = tk.Frame(
    master=window,
)

# Create fonts to be used throughout the program
title_text = tkFont.Font(family="Arial", size=36, weight="bold")
standard_text = tkFont.Font(family="Arial", size=14, weight="bold")

# This dictionary includes the rows of the board as dictionaries, with the columns as entries specifying their color and other values
board_dict = {}

current_turn = "white"

#keep track of moves taken for the scoreboard
num_white_turns = 0
num_black_turns = 0

valid_moves = []

def start_game():
    init_board()
    update_board()
    current_turn = "white"
    update_turn_indicator(current_turn)
    update_dead()

def update_turn_indicator(current_turn):
    """This function updates the turn indicator based on the current turn"""
    turnindicator = tk.Label(
        master = window,
        text = "Turn: {}".format(current_turn.capitalize()),
        font = title_text,
    )
    turnindicator.grid(
        row=0,
        column=1,
        pady=15,
    )

def swap_turn():
    '''This function swaps the current turn and iterates the correct num_?????_turns variable'''
    global current_turn, num_white_turns, num_black_turns
    if current_turn == "black":
        num_black_turns += 1
        print('white turns:', num_white_turns)
        print('black turns:', num_black_turns)
        current_turn = "white"
    elif current_turn == "white":
        num_white_turns += 1
        print('white turns:', num_white_turns)
        print('black turns:', num_black_turns)
        current_turn = "black"

def init_board():
    """This function initializes the chessboard at the beginning of the game, creating tiles and putting their color values in board_dict"""
    for i in range(8):
        board.columnconfigure(i, weight=1)
        board.rowconfigure(i, weight=1)
        if i % 2 == 0:
            board_dict[i] = {}
            for j in range(8):
                board_dict[i][j] = {}
                if j % 2 == 0:
                    board_dict[i][j]["color"] = "black"
                else:
                    board_dict[i][j]["color"] = "white"
        else:
            board_dict[i] = {}
            for j in range(8):
                board_dict[i][j] = {}
                if j % 2 == 1:
                    board_dict[i][j]["color"] = "black"
                else:
                    board_dict[i][j]["color"] = "white"

def update_board():
    """This makes each board square a button with command on_select, then calls place_pieces to update their position on the board"""
    for row in board_dict:
        for column in board_dict[row]:
            # create a container frame to keep button from expanding
            btn_frame = tk.Frame(master=board, width=80, height=80)
            button = tk.Button(
                master = btn_frame,
                # see https://stackoverflow.com/questions/17677649/tkinter-assign-button-command-in-loop-with-lambda?noredirect=1&lq=1
                command = lambda row=row, column=column: on_select(row, column),
                bg = board_dict[row][column]["color"],
                borderwidth = 7,
            )
            button.place(x = 0, y = 0, height = 80, width = 80)
            btn_frame.grid(
                row=row,
                column=column,
            )
    board.grid(
        row = 1,
        column = 1,
        pady  = (0, 20)
    )
    place_pieces()


def on_select(row, column):
    """This function handles all the stuff that happens when a button is selected"""
    # make these global so the changes made in this function will stick
    global valid_moves, current_turn, pieces_dict, board_dict, piece_color
    # if the square has a piece on it, find its color
    if has_piece(row, column) == True:
        #get the type of piece selected and its color
        for key in pieces_dict:
            if pieces_dict[key]["row"] == row and pieces_dict[key]["column"] == column and pieces_dict[key]["alive"] == True:
                piece_selected = key
                piecetype = pieces_dict[key]["piecetype"]
                piece_color = pieces_dict[key]["color"]
                print('-' * 50)
                print("piece:", piece_selected)

        print("piece type:", piecetype)
        print("piece color:", piece_color)
        print()

        if piece_color == current_turn:
        # calculate valid moves given piece type
            global piece_to_move
            piece_to_move = piece_selected
            valid_moves = []
            clearhighlights()
            if piecetype == "king":
                valid_moves = get_king_moves(row, column, piece_color)
            elif piecetype == "knight":
                valid_moves = get_knight_moves(row, column, piece_color)
            elif piecetype == "queen":
                valid_moves = get_queen_moves(row, column, piece_color)
            elif piecetype == "bishop":
                valid_moves = get_bishop_moves(row, column, piece_color)
            elif piecetype == "castle":
                valid_moves = get_castle_moves(row, column, piece_color)
            elif piecetype == "pawn":
                valid_moves = get_pawn_moves(row, column, piece_color, pieces_dict[piece_to_move]["isfirstturn"])  # last argument is isfirstturn

            board_dict[row][column]["color"] = "#ffa200"

            for item in valid_moves:
                # highlight possible kills in red
                if board_dict[item[0]][item[1]]["piece_on_spot"] != piece_color and board_dict[item[0]][item[1]]["piece_on_spot"] != False:
                    board_dict[item[0]][item[1]]["color"] = "#ff4242"
                else:
                    # highlight possible non-kill moves in blue
                    board_dict[item[0]][item[1]]["color"] = "#2aa9db"

            update_board()
            print("valid moves for selected piece:", valid_moves)
            print()

        elif piece_color != current_turn:
            proposed_move = [row, column]
            if proposed_move in valid_moves:
                piece_to_kill = piece_selected
                print("kill move to:", proposed_move)
                print("piece killed:", piece_to_kill)
                pieces_dict[piece_to_move]["row"] = row
                pieces_dict[piece_to_move]["column"] = column
                pieces_dict[piece_to_kill]["alive"] = False
                valid_moves = []

                if pieces_dict[piece_to_move]["piecetype"] == "pawn":
                    pieces_dict[piece_to_move]["isfirstturn"] = False

                swap_turn()
                clearhighlights()
                update_board()
                update_turn_indicator(current_turn)
                update_dead()

    elif [row, column] in valid_moves:
        print("valid move to", [row, column])
        pieces_dict[piece_to_move]["row"] = row
        pieces_dict[piece_to_move]["column"] = column

        if pieces_dict[piece_to_move]["piecetype"] == "pawn":
            pieces_dict[piece_to_move]["isfirstturn"] = False

        # print(pieces_dict[piece_to_move])
        valid_moves = []

        swap_turn()
        clearhighlights()
        update_board()
        update_turn_indicator(current_turn)



def clearhighlights():
    global board_dict
    for i in range(8):
        if i % 2 == 0:
            for j in range(8):
                if j % 2 == 0:
                    board_dict[i][j]["color"] = "black"
                else:
                    board_dict[i][j]["color"] = "white"
        else:
            for j in range(8):
                if j % 2 == 1:
                    board_dict[i][j]["color"] = "black"
                else:
                    board_dict[i][j]["color"] = "white"


############### Add Icons ###############

def place_pieces():
    # Start out with a clean slate
    for i in range(8):
        for j in range(8):
            board_dict[i][j]["piece_on_spot"] = False

    for key in pieces_dict:
        #get filename of image to grab
        if pieces_dict[key]["alive"] == True:
            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, "chessicons", pieces_dict[key]["icon"]) + ".gif"
            #render the icon and place it on the board
            pic = tk.PhotoImage(file=filename)
            pic = pic.subsample(10,10)  #shrink the image by selecting only 1 in 9 pixels
            piece = tk.Label(master=board, image=pic)
            piece.image = pic   #include this or the image gets garbage collected, only showing the last one
            piece.grid(row = pieces_dict[key]["row"], column = pieces_dict[key]["column"])
            # map the key onto the correct entry in the board_dict
            board_dict[pieces_dict[key]["row"]][pieces_dict[key]["column"]]["piece_on_spot"] = pieces_dict[key]["color"]

def rickroll():
    webbrowser.open('https://youtu.be/dQw4w9WgXcQ')  # Go to example.com

def is_in_board(row, column):
    if row >= 0 and column >= 0 and row <= 7 and column <= 7:
        return True
    else:
        return False

def has_piece(row, column):
    # TODO: return a dictionary from this function that tells the type of piece, its color, and other information (hopefully will speed up program)
    # details = {}
    #
    # for key in pieces_dict:
    #     if pieces_dict[key]["row"] == row and pieces_dict[key]["column"] == column and pieces_dict[key]["alive"] == True:
    #         details["piecetype"] = pieces_dict[key]["piecetype"]
    #         details["piece_color"] = pieces_dict[key]["color"]
    #         details["piece_selected"] = key
    #
    # print("piece_on_spot details:", details)

    for key in pieces_dict:
        if pieces_dict[key]["row"] == row and pieces_dict[key]["column"] == column and pieces_dict[key]["alive"] == True:
            return True
    return False

############### Find possible moves for selected piece: ###############

def get_king_moves(row, column, piece_color):
    possible_king_moves = [[row + 1, column], [row - 1, column], [row, column + 1], [row, column - 1], [row+1, column+1], [row+1, column-1], [row-1, column+1], [row-1, column-1] ]
    valid_moves = []
    for move in possible_king_moves:
        #check if the move is in the board and if another piece is there
        if is_in_board(move[0], move[1]) == True and (move[0] != row or move[1] != column):
            #check if a piece of the same color is there - if not, don't include the move
            if board_dict[move[0]][move[1]]["piece_on_spot"] != piece_color:
                valid_moves.append(move)
    return valid_moves


def get_queen_moves(row, column, piece_color):
    possible_queen_moves = []
    valid_moves = []

    # BISHOP STYLE #

    piece_hit = False
    i = 0

    while piece_hit == False and i < 8:
        i += 1
        possible_queen_moves.append([row+i, column+i])
        if has_piece(row + i, column + i) == True:
            piece_hit = True

    piece_hit = False
    i = 0

    while piece_hit == False and i < 8:
        i += 1
        possible_queen_moves.append([row+i, column-i])
        if has_piece(row + i, column - i) == True:
            piece_hit = True

    piece_hit = False
    i = 0

    while piece_hit == False and i < 8:
        i += 1
        possible_queen_moves.append([row-i, column+i])
        if has_piece(row - i, column + i) == True:
            piece_hit +=1

    piece_hit = False
    i = 0

    while piece_hit == False and i < 8:
        i += 1
        possible_queen_moves.append([row-i, column-i])
        if has_piece(row - i, column - i) == True:
            piece_hit = True

    # CASTLE STYLE #

    piece_hit = False
    i = 0

    while piece_hit == False and i < 8:
        i += 1
        possible_queen_moves.append([row+i, column])
        if has_piece(row + i, column) == True:
            piece_hit = True

    piece_hit = False
    i = 0

    while piece_hit == False and i < 8:
        i += 1
        possible_queen_moves.append([row-i, column])
        if has_piece(row - i, column) == True:
            piece_hit = True

    piece_hit = False
    i = 0

    while piece_hit == False and i < 8:
        i += 1
        possible_queen_moves.append([row, column-i])
        if has_piece(row, column-i) == True:
            piece_hit = True

    piece_hit = False
    i = 0

    while piece_hit == False and i < 8:
        i += 1
        possible_queen_moves.append([row, column+i])
        if has_piece(row, column+i) == True:
            piece_hit = True

    piece_hit = False
    i = 0

    for move in possible_queen_moves:
        if is_in_board(move[0], move[1]) == True and (move[0] != row or move[1] != column):
            if board_dict[move[0]][move[1]]["piece_on_spot"] != piece_color:
                valid_moves.append(move)
    return valid_moves



def get_bishop_moves(row, column, piece_color):
    possible_bishop_moves = []
    valid_moves = []

    piece_hit = False
    i = 0

    while piece_hit == False and i < 8:
        i += 1
        possible_bishop_moves.append([row+i, column+i])
        if has_piece(row + i, column + i) == True:
            piece_hit = True

    piece_hit = False
    i = 0

    while piece_hit == False and i < 8:
        i += 1
        possible_bishop_moves.append([row+i, column-i])
        if has_piece(row + i, column - i) == True:
            piece_hit = True

    piece_hit = False
    i = 0

    while piece_hit == False and i < 8:
        i += 1
        possible_bishop_moves.append([row-i, column+i])
        if has_piece(row - i, column + i) == True:
            piece_hit +=1

    piece_hit = False
    i = 0

    while piece_hit == False and i < 8:
        i += 1
        possible_bishop_moves.append([row-i, column-i])
        if has_piece(row - i, column - i) == True:
            piece_hit = True

    piece_hit = False
    i = 0

    for move in possible_bishop_moves:
        if is_in_board(move[0], move[1]) == True and (move[0] != row or move[1] != column):

            # make sure it wouldn't move on top of a piece of the same color
            if board_dict[move[0]][move[1]]["piece_on_spot"] != piece_color:
                valid_moves.append(move)

    return valid_moves




def get_knight_moves(row, column, piece_color):
    possible_knight_moves = [[row+2, column-1], [row+2, column+1], [row+1, column+2], [row-1, column+2], [row-2, column+1], [row-2, column-1], [row-1, column-2], [row+1, column-2]]
    valid_moves = []
    for move in possible_knight_moves:
        if is_in_board(move[0], move[1]) == True and (move[0] != row or move[1] != column):
            if board_dict[move[0]][move[1]]["piece_on_spot"] != piece_color:
                valid_moves.append(move)
    return valid_moves




def get_castle_moves(row, column, piece_color):
    possible_castle_moves = []
    valid_moves = []

    piece_hit = False
    i = 0

    while piece_hit == False and i < 8:
        i += 1
        possible_castle_moves.append([row-i, column])
        if has_piece(row - i, column) == True:
            piece_hit = True

    piece_hit = False
    i = 0

    while piece_hit == False and i < 8:
        i += 1
        possible_castle_moves.append([row+i, column])
        if has_piece(row + i, column) == True:
            piece_hit = True

    piece_hit = False
    i = 0

    while piece_hit == False and i < 8:
        i += 1
        possible_castle_moves.append([row, column-i])
        if has_piece(row, column-i) == True:
            piece_hit = True

    piece_hit = False
    i = 0

    while piece_hit == False and i < 8:
        i += 1
        possible_castle_moves.append([row, column+i])
        if has_piece(row, column+i) == True:
            piece_hit = True

    piece_hit = False
    i = 0

    for move in possible_castle_moves:
        if is_in_board(move[0], move[1]) == True and (move[0] != row or move[1] != column):
            if board_dict[move[0]][move[1]]["piece_on_spot"] != piece_color:
                valid_moves.append(move)
    return valid_moves




def get_pawn_moves(row, column, piece_color, isfirstturn):
    possible_pawn_moves = []
    valid_moves = []


    # add vertical moves, 2 options if it's the first move
    if piece_color == "white" and has_piece(row-1, column) == False:
        possible_pawn_moves.append([row - 1, column])

        if isfirstturn == True and has_piece(row-2, column) == False:
            possible_pawn_moves.append([row - 2, column])

    elif piece_color == "black" and has_piece(row+1, column) == False:
        possible_pawn_moves.append([row + 1, column])

        if isfirstturn == True and has_piece(row+2, column) == False:
            possible_pawn_moves.append([row + 2, column])



    # Add sideways motion if another piece is adjacent
    if piece_color == "white" and is_in_board(row - 1, column - 1):
        if board_dict[row - 1][column - 1]["piece_on_spot"] == "black":
            valid_moves.append([row-1, column-1])

    if piece_color == "white" and is_in_board(row - 1, column + 1):
        if board_dict[row - 1][column + 1]["piece_on_spot"] == "black":
            valid_moves.append([row-1, column+1])

    if piece_color == "black" and is_in_board(row + 1, column - 1):
        if board_dict[row + 1][column - 1]["piece_on_spot"] == "white":
            valid_moves.append([row+1, column-1])

    if piece_color == "black" and is_in_board(row + 1, column + 1):
        if board_dict[row + 1][column + 1]["piece_on_spot"] == "white":
            valid_moves.append([row+1, column+1])


    for move in possible_pawn_moves:
        if is_in_board(move[0], move[1]) == True and (move[0] != row or move[1] != column):
            if board_dict[move[0]][move[1]]["piece_on_spot"] != piece_color:
                valid_moves.append(move)



    return valid_moves


deadwhites = tk.Frame(
    master=window,
)

deadblacks = tk.Frame(
    master=window,
)

deadwhites.columnconfigure(0, weight=1)
for i in range(16):
    deadwhites.rowconfigure(i, weight=1)

deadblacks.columnconfigure(0, weight=1)
for i in range(16):
    deadblacks.rowconfigure(i, weight=1)




def update_dead():
    dead_white_pieces = []
    for key in pieces_dict:
        if pieces_dict[key]["color"] == "white" and pieces_dict[key]["alive"] == False:
            dead_white_pieces.append(key)

    dead_black_pieces = []
    for key in pieces_dict:
        if pieces_dict[key]["color"] == "black" and pieces_dict[key]["alive"] == False:
            dead_black_pieces.append(key)

    # print("white pieces dead:", dead_white_pieces)
    # print("black pieces dead:", dead_black_pieces)

    for item in dead_white_pieces:
        #get filename of image to grab
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "chessicons", pieces_dict[item]["icon"]) + ".gif"

        #render the icon and place it on the board

        pic = tk.PhotoImage(file=filename)
        pic = pic.subsample(18, 18)  #shrink the image by selecting only 1 in 18 pixels

        deadpieceframe = tk.Frame(master=deadwhites)
        deadpieceframe.rowconfigure(0, weight=1)
        deadpieceframe.columnconfigure(0, weight=1)

        deadpiecelabel = tk.Label(master=deadpieceframe, image=pic)
        deadpiecelabel.image = pic
        deadpiecelabel.grid(column=0, row=0)
        deadpieceframe.grid(column=0, row=dead_white_pieces.index(item))
        # print("piece row:", dead_white_pieces.index(item))


    for item in dead_black_pieces:
        #get filename of image to grab
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "chessicons", pieces_dict[item]["icon"]) + ".gif"

        #render the icon and place it on the board

        pic = tk.PhotoImage(file=filename)
        pic = pic.subsample(18, 18)  #shrink the image by selecting only 1 in 18 pixels

        deadpieceframe = tk.Frame(master=deadblacks)
        deadpieceframe.rowconfigure(0, weight=1)
        deadpieceframe.columnconfigure(0, weight=1)

        deadpiecelabel = tk.Label(master=deadpieceframe, image = pic)
        deadpiecelabel.image = pic
        deadpiecelabel.grid(column=0, row=0)
        deadpieceframe.grid(column=0, row=dead_black_pieces.index(item))
        # print("piece row:", dead_black_pieces.index(item))

    # if a king is dead, end the game
    if pieces_dict['white_king']['alive'] == False:
        end_game()
        update_scoreboard('black')
    if pieces_dict['black_king']['alive'] == False:
        end_game()
        update_scoreboard('white')

    deadwhites.grid(row=1, column=0, padx=20)
    deadblacks.grid(row=1, column=2, padx=20)

############### Create Score View and Info to right of baord ###############



def update_scoreboard(winner):
    print('updating scoreboard...')
    #prompt the user for the winner's name to add to the scoreboard
    winner_name = simpledialog.askstring('Input', "Enter the winner's name:", parent=window)
    print(winner_name)

    with open('leaderboard.txt', 'a+') as leaderboard:


        if winner == 'white':
            winner_score = num_white_turns
        elif winner == 'black':
            winner_score = num_black_turns
        entry = winner_name + ' ' + str(winner_score)
        print("entry:", entry)
        leaderboard.write(entry + '\n')


def end_game():
    print('ending game...')



scoreview = tk.Frame(
    master=window,
)

scoreview.rowconfigure(0, weight=1)
scoreview.rowconfigure(1, weight=1)
scoreview.rowconfigure(2, weight=1)
scoreview.columnconfigure(0, weight=1)

rickroll = tk.Button(
    master=scoreview,
    command=rickroll,
    text="Developer\nOptions",
    font = standard_text,
)

rickroll.grid(
    row=0,
    column=0
)

#Implement scoreboard
with open('leaderboard.txt', 'r+') as leaderboard:
    score_dict = {}
    leaders = leaderboard.read().splitlines()
    for item in leaders:
        entry = item.split()
        score_dict[entry[0]] = int(entry[1])
    print('score_dict:', score_dict)

    #https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    sorted_dict = {k: v for k, v in sorted(score_dict.items(), key=lambda item: item[1])}
    print('sorted_dict:', sorted_dict)

    scoreboard = tk.Frame(master=scoreview)

    scoreboard.columnconfigure(0, weight=1)
    scoreboard.columnconfigure(1, weight=1)

    names = list(sorted_dict.keys())
    print('names:', names)

    for i in range(len(sorted_dict)):
        scoreboard.rowconfigure(i, weight=1)

        #Get name for each label
        name = names[i]
        name_label = tk.Label(master=scoreboard, text=name)
        name_label.grid(row=i, column=0)

        #Get the corresponding score
        name_score = sorted_dict[name]
        name_score_label = tk.Label(master=scoreboard, text=name_score)
        name_score_label.grid(row=i, column=1)

    scoreboard.grid(row=2, column=0)

scoreview.grid(row = 1, column = 3, padx=20)

############### Function Calls ###############

start_game()

window.mainloop()
