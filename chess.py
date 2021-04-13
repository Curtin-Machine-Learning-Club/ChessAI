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

    def _moveX(self, y, x):
        return (y + x) if self.color == Color.WHITE else (y - x)

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

        # TODO: Account for checkmate, check, stalemate when working out if you can move because you MUST get yourself out if in that state.

        if piece.piece == ChessPiece.PAWN:
            # TODO: En passant

            if start[0] == (7 if piece.color == Color.WHITE else 0):
                 # TODO: Chess Special Move Called Promotion
                print("Chess Promotion Case Reached!")
            else:
                # Pawn can move forward one space (or two on first move)
                possible_moves[piece._moveX(start[0], 1)][start[1]] = True
                if not piece.hasMoved:
                    possible_moves[piece._moveX(start[0], 2)][start[1]] = True
                
                # If a piece is diagonally in front by one space can take it
                if start[1]-1 >= 0:
                    if self.state[piece._moveX(start[0], 1)][start[1]-1].piece != ChessPiece.EMPTY:
                        possible_moves[piece._moveX(start[0], 1)][start[1]-1] = True
                
                if start[1]+1 <= 7:
                    if self.state[piece._moveX(start[0], 1)][start[1]+1].piece != ChessPiece.EMPTY:
                        possible_moves[piece._moveX(start[0], 1)][start[1]+1] = True
        elif piece.piece == ChessPiece.KNIGHT:
            # TODO: If possible move location has own piece in it, it's not a possible move!

            if start[1]+1 <= 7:
                # Bottom Right
                if piece._moveX(start[0], 2) >= 0 and piece._moveX(start[0], 2) <= 7:
                    possible_moves[piece._moveX(start[0], 2)][start[1]+1] = True

                # Bottom Left
                if piece._moveX(start[0], -2) >= 0 and piece._moveX(start[0], -2) <= 7:
                    possible_moves[piece._moveX(start[0], -2)][start[1]+1] = True
            
            if start[1]+2 <= 7:
                if start[0]+1 >= 0 and start[0]+1 <= 7:
                    possible_moves[start[0]+1][start[1]+2] = True

                if start[0]-1 >= 0 and start[0]-1 <= 7:
                    possible_moves[start[0]-1][start[1]+2] = True

            if start[1]-1 >= 0:
                # Top Right
                if piece._moveX(start[0], 2) >= 0 and piece._moveX(start[0], 2) <= 7:
                    possible_moves[piece._moveX(start[0], 2)][start[1]-1] = True

                # Top Left
                if piece._moveX(start[0], -2) >= 0 and piece._moveX(start[0], -2) <= 7:
                    possible_moves[piece._moveX(start[0], -2)][start[1]-1] = True

            if start[1]-2 >= 0:
                if start[0]+1 >= 0 and start[0]+1 <= 7:
                    possible_moves[start[0]+1][start[1]-2] = True

                if start[0]-1 >= 0 and start[0]-1 <= 7:
                    possible_moves[start[0]-1][start[1]-2] = True
        elif piece.piece == ChessPiece.KING:
            # TODO: If possible move location has own piece in it, it's not a possible move!
            # TODO: Label each case
            # TODO: King can't get itself in check. Remove moves that would result in Check.
            # TODO: Castling

            if start[1]+1 <= 7:
                possible_moves[start[0]][start[1]+1] = True

                if piece._moveX(start[0], 1) >= 0 and piece._moveX(start[0], 1) <= 7:
                    possible_moves[piece._moveX(start[0], 1)][start[1]+1] = True
                    possible_moves[piece._moveX(start[0], 1)][start[1]] = True

                if piece._moveX(start[0], -1) >= 0 and piece._moveX(start[0], -1) <= 7:
                    possible_moves[piece._moveX(start[0], -1)][start[1]+1] = True
                    possible_moves[piece._moveX(start[0], -1)][start[1]] = True

            if start[1]-1 >= 0:
                possible_moves[start[0]][start[1]-1] = True

                if piece._moveX(start[0], 1) >= 0 and piece._moveX(start[0], 1) <= 7:
                    possible_moves[piece._moveX(start[0], 1)][start[1]-1] = True
                    possible_moves[piece._moveX(start[0], 1)][start[1]] = True

                if piece._moveX(start[0], -1) >= 0 and piece._moveX(start[0], -1) <= 7:
                    possible_moves[piece._moveX(start[0], -1)][start[1]-1] = True
                    possible_moves[piece._moveX(start[0], -1)][start[1]] = True

        # elif piece.piece == ChessPiece.QUEEN:
            # TODO: Scanning diagonally, horizontally, or vertically

        elif piece.piece == ChessPiece.ROOK:
            # Scan left
            for i in range(0, 7):
                x = start[0]-(i+1)

                # Hit edge
                if x < 0:
                    break

                # Hit own piece so stop scanning
                if self.state[x][start[1]].piece != ChessPiece.EMPTY and self.state[x][start[1]].color == piece.color:
                    break

                possible_moves[x][start[1]] = True

                # Hit piece so stop
                if self.state[x][start[1]].piece != ChessPiece.EMPTY:
                    break

            # Scan right
            for i in range(0, 7):
                x = start[0]+(i+1)

                # Hit edge
                if x > 7:
                    break

                # Hit own piece so stop scanning
                if self.state[x][start[1]].piece != ChessPiece.EMPTY and self.state[x][start[1]].color == piece.color:
                    break

                possible_moves[x][start[1]] = True

                # Hit piece so stop scanning
                if self.state[x][start[1]].piece != ChessPiece.EMPTY:
                    break

            # Scan up
            for i in range(0, 7):
                y = start[1]-(i+1)

                # Hit edge
                if y < 0:
                    break

                # Hit own piece so stop scanning
                if self.state[start[0]][y].piece != ChessPiece.EMPTY and self.state[start[0]][y].color == piece.color:
                    break

                possible_moves[start[0]][y] = True

                # Hit piece so stop scanning
                if self.state[start[0]][y].piece != ChessPiece.EMPTY:
                    break
            
            # Scan down
            for i in range(0, 7):
                y = start[1]+(i+1)

                # Hit edge
                if y > 7:
                    break

                # Hit own piece so stop scanning
                if self.state[start[0]][y].piece != ChessPiece.EMPTY and self.state[start[0]][y].color == piece.color:
                    break

                possible_moves[start[0]][y] = True

                # Hit piece so stop scanning
                if self.state[start[0]][y].piece != ChessPiece.EMPTY:
                    break
        elif piece.piece == ChessPiece.BISHOP:
            # Scan down right
            for i in range(0, 7):
                x = start[0]+(i+1)
                y = start[1]+(i+1)

                # Hit edge
                if x < 0 or x > 7 or y > 7:
                    break

                # Hit own piece so stop scanning
                if self.state[x][y].piece != ChessPiece.EMPTY and self.state[x][y].color == piece.color:
                    break

                possible_moves[x][y] = True

                # Hit piece so stop scanning
                if self.state[x][y].piece != ChessPiece.EMPTY:
                    break
            
            # Scan down left
            for i in range(0, 7):
                x = start[0]-(i+1)
                y = start[1]+(i+1)

                # Hit edge
                if x < 0 or y > 7:
                    break

                # Hit own piece so stop scanning
                if self.state[x][y].piece != ChessPiece.EMPTY and self.state[x][y].color == piece.color:
                    break

                possible_moves[x][y] = True

                # Hit piece so stop scanning
                if self.state[x][y].piece != ChessPiece.EMPTY:
                    break
            
            # Scan up right
            for i in range(0, 7):
                x = start[0]+(i+1)
                y = start[1]-(i+1)

                # Hit edges
                if x < 0 or x > 7 or y < 0:
                    break

                # Hit own piece so stop scanning
                if self.state[x][y].piece != ChessPiece.EMPTY and self.state[x][y].color == piece.color:
                    break

                possible_moves[x][y] = True

                # Hit piece so stop scanning
                if self.state[x][y].piece != ChessPiece.EMPTY:
                    break
            
            # Scan up left
            for i in range(0, 7):
                x = start[0]-(i+1)
                y = start[1]-(i+1)

                # Hit edges
                if x < 0 or y < 0:
                    break

                # Hit own piece so stop scanning
                if self.state[x][y].piece != ChessPiece.EMPTY and self.state[x][y].color == piece.color:
                    break

                possible_moves[x][y] = True

                # Hit piece so stop scanning
                if self.state[x][y].piece != ChessPiece.EMPTY:
                    break
        
        return possible_moves

    def isInCheck(self):
        # TODO: When king threatened (but can escape). If in check only valid moves are to prevent check!
        return False
    
    def isInCheckmate(self):
        # TODO: when a king is placed in check and there is no legal move to escape
        return False
    
    def isInStalemate(self):
        # TODO: No possible moves and not in check
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