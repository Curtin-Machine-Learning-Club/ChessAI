import pygame

pieces = [ "empty", "king", "rook", "bishop", "queen", "knight", "pawn" ]
board = [
    [ 2, 5, 3, 4, 1, 3, 5, 2 ],
    [ 6, 6, 6, 6, 6, 6, 6, 6 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 6, 6, 6, 6, 6, 6, 6, 6 ],
    [ 2, 5, 3, 4, 1, 3, 5, 2 ],
]

activePiece = None

def move_piece(start, end):
    start_piece = board[start[0]][start[1]]
    end_piece = board[end[0]][end[1]]

    if end_piece != 0:
        raise Exception("You can't move where a piece already is")

    board[end[0]][end[1]] = start_piece
    board[start[0]][start[1]] = 0
    
def print_board():
    print("Board State:")
    print(*board, sep='\n')


# print_board()
# move_piece([1, 0], [2, 0])
# print_board()

pygame.init()

gameDisplay = pygame.display.set_mode((800,800))
pygame.display.set_caption('Chess')
clock = pygame.time.Clock()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)

CELL_SIZE = 100 # TODO: Derive from window
CELL_PADDING = 3

crashed = False
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        for i in range(0, 8):
            for ii in range(0, 8):
                color = WHITE
                if ((i + ii) % 2) == 1:
                    color = GREY

                if activePiece != None and i == activePiece[0] and ii == activePiece[1]:
                    color = BLUE

                squareRect = pygame.draw.rect(gameDisplay, color, (i*CELL_SIZE, ii * CELL_SIZE, CELL_SIZE - CELL_PADDING, CELL_SIZE - CELL_PADDING))

                textRect = None
                pieceIndex = board[ii][i]
                if pieceIndex != 0:
                    textsurface = myfont.render(pieces[pieceIndex], False, (0, 0, 0))
                    textRect = gameDisplay.blit(textsurface, (i*CELL_SIZE, ii * CELL_SIZE))

                pos = pygame.mouse.get_pos()
                pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()

                if pressed1 and (squareRect.collidepoint(pos) or (textRect != None and textRect.collidepoint(pos))):
                    if board[ii][i] != 0:
                        activePiece = [i, ii]
    pygame.display.update()
    clock.tick(60)

pygame.quit()