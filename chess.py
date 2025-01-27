import pygame
import sys

# Import classes from local files.
from ChessBoard import ChessBoard
from ChessPieces import ChessPieces
from ChessGame import ChessGame

# Declare constants for screen dimensions.
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Define the size of the chessboard and its tiles.
BOARD_ROWS = 8
BOARD_COLUMNS = 8
SQUARE_SIZE = SCREEN_WIDTH // BOARD_COLUMNS



def main():
    '''This function executes the chess game GUI. '''
    
    # Set up pygame window and clock.
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Chess Game")
    clock = pygame.time.Clock()

    # Create instance of ChessGame class.
    game = ChessGame(screen)
    running = True

    # Start the game loop
    while running:
        for event in pygame.event.get():
            # Check quit event and stop loop.
            if event.type == pygame.QUIT:
                running = False
            # Check mouse button event and pass position to game.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game.handle_mouse_click(pos)

        # Clear screen with black before drawing.
        screen.fill((0,0,0))

        # Draw the board, maintaing 60 frames per second.  
        game.board.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

