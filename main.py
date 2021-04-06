import pygame
import chess

board = chess.Board()

# Setup Pygame Window
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

# Color for UI
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
GREEN = (0, 255, 0)

# UI State
highlightedPiece = None
CELL_SIZE = screen.get_width() / len(board.state)
CELL_PADDING = 3

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pos = pygame.mouse.get_pos()
    leftClickActive, _, rightClickActive = pygame.mouse.get_pressed()

    if board.game_over:
        highlightedPiece = None
        pygame.draw.rect(screen, GREEN, (0, 0, screen.get_width(), 20))
    else:
        for i, y in enumerate(board.state):
            for ii, x in enumerate(y):
                # Board Background
                color = WHITE
                if ((i + ii) % 2) == 1:
                    color = GREY
                
                # Actively selected piece has blue background
                if highlightedPiece != None and i == highlightedPiece[0] and ii == highlightedPiece[1]:
                    color = BLUE

                # If Actively selected piece can move to square set yellow
                isValidMove = highlightedPiece != None and board.is_valid_move(highlightedPiece, [i, ii])
                if isValidMove:
                    color = YELLOW
                
                squareRect = pygame.draw.rect(screen, color, (i * CELL_SIZE, ii * CELL_SIZE, CELL_SIZE - CELL_PADDING, CELL_SIZE - CELL_PADDING))

                # Move if left click valid move
                if leftClickActive and squareRect.collidepoint(pos) and isValidMove:
                    board.move_piece(highlightedPiece, [i, ii])
                    highlightedPiece = None

                if x.piece != chess.ChessPiece.EMPTY:
                    pieceRect = screen.blit(pygame.image.load("./assets/" + x.piece.name + "_" + x.color.name + ".png"), (i * CELL_SIZE, ii * CELL_SIZE))
                    
                    if leftClickActive and pieceRect.collidepoint(pos):
                        highlightedPiece = [i, ii]
                    elif rightClickActive:
                        highlightedPiece = None

    pygame.display.update()
    clock.tick(60)

pygame.quit()
