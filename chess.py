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
    color = Color.NONE
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

    def valid_moves(self, start):
        piece = self.state[start[0]][start[1]]
        possible_moves = [ [ False for i in range(8) ] for i in range(8) ]

        if piece.piece == ChessPiece.PAWN:
            # TODO: En passant

            if start[0] == (7 if piece.color == Color.WHITE else 0):
                 # TODO: Chess Special Move Called Promotion
                print("Chess Promotion Case Reached!")
            else:
                self.relativePossibleMove(possible_moves, start, piece, 1, 0) # Forward 1
                if not piece.hasMoved:
                    self.relativePossibleMove(possible_moves, start, piece, 2, 0) # Forward 2 on first move
                self.relativePossibleMove(possible_moves, start, piece, 1, -1, True)  # Front Top
                self.relativePossibleMove(possible_moves, start, piece, 1, 1, True)   # Front Bottom

        if piece.piece == ChessPiece.KNIGHT:
            self.relativePossibleMove(possible_moves, start, piece, 2, -1) # Top L
            self.relativePossibleMove(possible_moves, start, piece, 2, 1) # Bottom L
        
        if piece.piece == ChessPiece.KING:
            # TODO: King can't get itself in check. Remove moves that would result in Check.
            # TODO: Castling -> At most once per game
            self.relativePossibleMove(possible_moves, start, piece, 0, -1)  # Above
            self.relativePossibleMove(possible_moves, start, piece, 0, 1)   # Below
            self.relativePossibleMove(possible_moves, start, piece, 1, 0)   # Front
            self.relativePossibleMove(possible_moves, start, piece, 1, -1)  # Front Top
            self.relativePossibleMove(possible_moves, start, piece, 1, 1)   # Front Bottom
            self.relativePossibleMove(possible_moves, start, piece, -1, 0)  # Behind
            self.relativePossibleMove(possible_moves, start, piece, -1, 1)  # Behind Bottom
            self.relativePossibleMove(possible_moves, start, piece, -1, -1) # Behind Top

        if piece.piece == ChessPiece.ROOK or piece.piece == ChessPiece.QUEEN:
            self.relativePossibleMoveScanning(possible_moves, start, piece, 1, 0)  # Scan forward
            self.relativePossibleMoveScanning(possible_moves, start, piece, -1, 0) # Scan backwards
            self.relativePossibleMoveScanning(possible_moves, start, piece, 0, -1) # Scan up
            self.relativePossibleMoveScanning(possible_moves, start, piece, 0, 1)  # Scan down
        
        if piece.piece == ChessPiece.BISHOP or piece.piece == ChessPiece.QUEEN:
            self.relativePossibleMoveScanning(possible_moves, start, piece, 1, -1)  # Scan up forwards
            self.relativePossibleMoveScanning(possible_moves, start, piece, 1, 1)   # Scan down forwards
            self.relativePossibleMoveScanning(possible_moves, start, piece, -1, 1)  # Scan down backwards
            self.relativePossibleMoveScanning(possible_moves, start, piece, -1, -1) # Scan up backwards
        
        return possible_moves

    def print(self):
        for y in self.state:
            for x in y:
                print(x.color.name[0] + " " +x.piece.name.ljust(6), end=', ')
            print()
        print()

    def relativePossibleMove(self, possible_moves, start, piece, translateX, translateY, ignoreIfIntoEmpty=False):
        endX = (start[0]+translateX) if piece.color == Color.WHITE else (start[0]-translateX)
        endY = start[1]+translateY

        if self.state[endX][endY].color != piece.color and (endX >= 0 and endX <= 7) and (endY >= 0 and endY <= 7):
            if ignoreIfIntoEmpty and self.state[endX][endY].piece == ChessPiece.EMPTY:
                return
            possible_moves[endX][endY] = True

    def relativePossibleMoveScanning(self, possible_moves, start, piece, changeTranslateX, changeTranslateY):
        for i in range(0, 7):
            x = start[0] + ((i + 1) * changeTranslateX)
            y = start[1] + ((i + 1) * changeTranslateY)

            if  (x >= 0 and x <= 7) and (y >= 0 and y <= 7):
                if self.state[x][y].color == piece.color:
                    break
                
                possible_moves[x][y] = True

                if self.state[x][y].piece != ChessPiece.EMPTY:
                    break
