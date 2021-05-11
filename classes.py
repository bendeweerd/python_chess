class Piece():
    def __init__(self, color, piecetype, alive, row, column):
        self.color = color
        self.piecetype = piecetype
        self.alive = alive
        self.row = row
        self.column = column

    def __str__(self):
        return 'color: ' + str(self.color) + '\n' + 'type: ' + str(self.piecetype) + '\n' + 'alive: ' + str(self.alive) + '\n' + 'position: (' + str(self.column) + ',' + str(self.row) + ')'

    




white_castle_1 = Piece('white', 'castle', True, 7, 0)
print(white_castle_1)
print()

white_king = Piece('white', 'king', True, 7, 3)
print(white_king)
