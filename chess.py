from enum import Enum

class Color(Enum):
    NONE = 0
    WHITE = 1
    BLACK = 2

class ChessPiece(Enum):
    EMPTY = 0
    KING = 1
    QUEEN = 2
    BISHOP = 3
    KNIGHT = 4
    ROOK = 5
    PAWN = 6

class Piece:
    piece = ChessPiece.EMPTY
    faction = Color.WHITE
    hasMoved = False

    def __init__(self, piece, color):
        self.piece = piece
        self.color = color

class Board:
    state = [
        [ Piece(ChessPiece.ROOK, Color.WHITE), Piece(ChessPiece.KNIGHT, Color.WHITE), Piece(ChessPiece.BISHOP, Color.WHITE), Piece(ChessPiece.KING, Color.WHITE), Piece(ChessPiece.QUEEN, Color.WHITE), Piece(ChessPiece.BISHOP, Color.WHITE), Piece(ChessPiece.KNIGHT, Color.WHITE), Piece(ChessPiece.ROOK, Color.WHITE) ],
        [ Piece(ChessPiece.PAWN, Color.WHITE) for i in range(8) ],
        [ Piece(ChessPiece.EMPTY, Color.NONE) for i in range(8) ],
        [ Piece(ChessPiece.EMPTY, Color.NONE) for i in range(8) ],
        [ Piece(ChessPiece.EMPTY, Color.NONE) for i in range(8) ],
        [ Piece(ChessPiece.EMPTY, Color.NONE) for i in range(8) ],
        [ Piece(ChessPiece.PAWN, Color.BLACK) for i in range(8) ],
        [ Piece(ChessPiece.ROOK, Color.BLACK), Piece(ChessPiece.KNIGHT, Color.BLACK), Piece(ChessPiece.BISHOP, Color.BLACK), Piece(ChessPiece.KING, Color.BLACK), Piece(ChessPiece.QUEEN, Color.BLACK), Piece(ChessPiece.BISHOP, Color.BLACK), Piece(ChessPiece.KNIGHT, Color.BLACK), Piece(ChessPiece.ROOK, Color.BLACK) ]
    ]
    game_over = False

    def move_piece(self, start, end):
        if (isinstance(start, list) and len(start) != 2) or (isinstance(end, list) and len(end) != 2):
            raise Exception("Invalid arguments to move_piece")

        if self.state[end[0]][end[1]].piece == ChessPiece.KING:
            self.game_over = True
        
        start_piece = self.state[start[0]][start[1]]
        start_piece.hasMoved = True
        self.state[end[0]][end[1]] = start_piece
        self.state[start[0]][start[1]] = Piece(ChessPiece.EMPTY, Color.NONE)

    def is_valid_move(self, start, end):
        piece = self.state[start[0]][start[1]]

        # TODO: Account for checkmate, check, stalemate when working out if you can move

        if piece.color == Color.WHITE:
            yMoveDifference = end[0] - start[0]
            xMoveDifference = end[1] - start[1]
        elif piece.color == Color.BLACK:
            yMoveDifference = start[0] - end[0]
            xMoveDifference = start[1] - end[1]

        if piece.piece == ChessPiece.PAWN:
            # Pawn can move forward one space (or two on first move)
            if xMoveDifference == 0 and yMoveDifference > 0 and yMoveDifference <= (1 if piece.hasMoved else 2):
                return True

            # If a piece is diagonally in front by one space can take it
            if yMoveDifference == 1 and (xMoveDifference == 1 or xMoveDifference == -1):
                if self.state[end[0]][end[1]].piece != ChessPiece.EMPTY:
                    return True

        return False

    def print(self):
        for y in self.state:
            for x in y:
                print(x.color.name[0] + " " +x.piece.name.ljust(6), end=', ')
            print()
        print()
    
    def print_possible_moves(self, start):
        if isinstance(start, list) and len(start) != 2:
            raise Exception("Invalid arguments to print_possible_moves")
        
        for y in range(8):
            for x in range(8):
                print(str(self.is_valid_move(start, [y, x])).ljust(5), end=', ')
            print()
        print()