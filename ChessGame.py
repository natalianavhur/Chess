import pygame
from ChessBoard import ChessBoard

# Define constantsfor screen and board.
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BOARD_ROWS = 8
BOARD_COLUMNS = 8
SQUARE_SIZE = SCREEN_WIDTH // BOARD_COLUMNS


class ChessGame:
    def __init__(self, screen):
        """The function initializes the chess game with a given screen.
        Inputs:
                - screen: pygame surface display.       """
        self.board = ChessBoard()
        self.current_turn = "white"
        self.selected_piece = None
        self.screen = screen

    def move_piece(self, start_pos, end_pos):
        """The function tries to move a piece from their start position to end position.
        Inputs:
                - start_pos: tuple (row, col)
                - end_pos: tuple (row, col) 
        Output:
                - condition: boolean"""
        
        piece = self.board.get_piece(start_pos)
        
        # Check if the piece belongs to the player's turn.
        if piece and piece.color == self.current_turn:
            success = self.board.move_piece(start_pos, end_pos, self.screen)
            
            if success:
                # Change players turn.
                self.current_turn = "black" if self.current_turn == "white" else "white"
                return True
            
        return False

    def handle_mouse_click(self, pos):
        """The function handles mouse click events to select and move chess pieces.
        Inputs:
                - pos: tuple (row, col)"""
        # Convert position to board coordinates
        column = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE
        position = (row, column)

        if self.selected_piece:

            if self.move_piece(self.selected_piece, position):
                # Deselect the chess piece after moving it.
                self.selected_piece = None  
            else:
                # Deselect the chess piece if move is invalid.
                self.selected_piece = None  
        else:
            # Select piece at clicked position with current player's turn color.
            piece = self.board.get_piece(position)
            if piece and piece.color == self.current_turn:
                self.selected_piece = position