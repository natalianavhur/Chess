import pygame
import copy
from ChessPieces import ChessPieces

# Declare constants for screen dimensions.
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Define the size of the chessboard and its tiles.
BOARD_ROWS = 8
BOARD_COLUMNS = 8
SQUARE_SIZE = SCREEN_WIDTH // BOARD_COLUMNS

# Define constants for RGB colors.
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
brown = (139, 69, 19)


class ChessBoard:

    def __init__(self):
        """The function initializes a 8x8 board array with chess pieces."""
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.create_pieces()

    def create_pieces(self):
        """The function places the pieces for both players on the board."""

        # Place pawns on the board.
        for column in range(BOARD_COLUMNS):
            self.board[1][column] = ChessPieces("pawn", "black", (1, column))
            self.board[6][column] = ChessPieces("pawn", "white", (6, column))

        # Place pieces except pawns on the board.
        pieces = [
            "rook",
            "knight",
            "bishop",
            "queen",
            "king",
            "bishop",
            "knight",
            "rook",
        ]
        for i, piece in enumerate(pieces):
            self.board[0][i] = ChessPieces(piece, "black", (0, i))
            self.board[7][i] = ChessPieces(piece, "white", (7, i))

    def draw(self, screen):
        """The function draws the chessboard and pieces on the screen."""
        # Draw board tiles.
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if (row + column) % 2 == 0:
                    color = gray
                else:
                    color = brown
                pygame.draw.rect(
                    screen,
                    color,
                    (column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                )
        # Draw chess pieces.
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                piece = self.board[row][column]
                if piece is not None:
                    piece.draw(screen)

    def get_piece(self, position):
        """The function returns the piece given the position coordinates.
        Inputs: position as a tuple (row, col)
        Outputs:chess piece"""
        return self.board[position[0]][position[1]]

    def move_piece(self, start_position, end_position, screen):
        """The function moves a chess piece.
        Inputs:
                - start_position: (row, col)
                - end_position: (row, col)
                - screen
        Output:
                - condition: boolean"""

        # Get the piece.
        start_row, start_col = start_position
        end_row, end_col = end_position
        moving_piece = self.get_piece(start_position)

        # Check if the move is valid and if it is update the piece position.
        if self.validate_move(moving_piece, start_position, end_position):
            self.board[end_row][end_col] = moving_piece
            self.board[start_row][start_col] = None
            moving_piece.pos = end_position

            # Update the game state, including checking for checks
            _, threats = self.is_king_in_check(moving_piece.color)
            if threats:
                # Move results in a check against the moving player; undo the move
                self.board[end_row][end_col] = None
                self.board[start_row][start_col] = moving_piece
                moving_piece.pos = start_position
                return False

            self.draw(screen)
            return True

        else:
            return False

    def validate_move(self, piece, start, end):
        """The function validates moves based on the type of piece.
        Inputs:
                - piece: ChessPieces class attribute
                - start: (row, col)
                - end: (row, col)
        Output:
                - valid_move: boolean"""
        # Get chess piece name attribute.
        piece_type = piece.piece_type

        # Validate move based on the type of piece.
        if piece_type == "pawn":
            # Check pawn diagonal move to capture.
            if abs(start[1] - end[1]) == 1:
                valid_move = self.validate_pawn_capture(start, end, piece.color)
            # Check pawn straight move.
            else:
                valid_move = self.validate_pawn_move(start, end, piece.color)
        elif piece_type == "knight":
            valid_move = self.validate_knight_move(start, end)
        elif piece_type == "rook":
            valid_move = self.validate_rook_move(start, end)
        elif piece_type == "bishop":
            valid_move = self.validate_bishop_move(start, end)
        elif piece_type == "queen":
            valid_move = self.validate_queen_move(start, end)
        elif piece_type == "king":
            valid_move = self.validate_king_move(start, end)
        else:
            valid_move = False  # If piece type is unknown or not handled
        return valid_move

    def validate_pawn_capture(self, start, end, color):
        """The function validates the capture movement of pawn.
        Inputs:
                - start: (row, col)
                - end: (row, col)
                - color: RGB touple
        Output:
                - condition: boolean
        """
        start_row, start_col = start
        end_row, end_col = end

        # Adjust the pawn direction movement.
        direction = -1 if color == "white" else 1
        piece_at_destination = self.get_piece(end)

        # Check for pawn diagonal capture movement.
        if abs(start_col - end_col) == 1 and (end_row - start_row == direction):
            if piece_at_destination and piece_at_destination.color != color:
                return True
            else:
                return False
        return False

    def validate_pawn_move(self, start, end, color):
        """The function validates the pawn movement.
        Inputs:
                - start: (row, col)
                - end: (row, col)
                - color: RGB touple
        Output:
                - condition: boolean"""

        start_row, start_col = start
        end_row, end_col = end
        direction = -1 if color == "white" else 1  # Adjust the direction based on color
        piece_at_destination = self.get_piece(end)

        # Check for normal straight move forward.
        if start_col == end_col:
            # Check single step from initial position.
            if (end_row - start_row == direction) and not piece_at_destination:
                return True
            # Check double step from initial position.
            if (
                (start_row == 6 and color == "white")
                or (start_row == 1 and color == "black")
            ) and (end_row - start_row == 2 * direction):
                mid_square = (start_row + direction, start_col)
                if not self.get_piece(mid_square) and not piece_at_destination:
                    return True

        return False

    def validate_rook_move(self, start, end):
        """The function validates the rook movement to capture pieces and move across the board.
        Inputs:
                - start: (row, col)
                - end: (row, col)
        Output:
                - condition: boolean"""
        start_row, start_col = start
        end_row, end_col = end
        if start_row != end_row and start_col != end_col:
            return False  # Rooks must move in a straight line

        step_row = 0 if start_row == end_row else (1 if end_row > start_row else -1)
        step_col = 0 if start_col == end_col else (1 if end_col > start_col else -1)

        cur_row, cur_col = start_row + step_row, start_col + step_col
        while (cur_row, cur_col) != (end_row, end_col):
            current_piece = self.get_piece((cur_row, cur_col))
            if current_piece:
                return False  # There is a piece in the way, cannot move through
            cur_row += step_row
            cur_col += step_col

        # Check the final position, if there is a piece, it must be capturable (different color)
        destination_piece = self.get_piece((end_row, end_col))
        if destination_piece:
            if destination_piece.color == self.get_piece(start).color:
                return False

        return True

    def validate_knight_move(self, start, end):
        """The function validates the knight movement to capture pieces and move across the board.
        Inputs:
                - start: (row, col)
                - end: (row, col)
        Output:
                - condition: boolean"""
        start_row, start_col = start
        end_row, end_col = end
        row_diff = abs(end_row - start_row)
        col_diff = abs(end_col - start_col)
        piece_at_destination = self.get_piece((end_row, end_col))

        # Check the "L-shaped" movement
        valid_move = (row_diff == 2 and col_diff == 1) or (
            row_diff == 1 and col_diff == 2
        )

        if valid_move:
            # Ensure that the destination is empty or contains an opponent's piece
            if piece_at_destination is None:
                return True
            elif piece_at_destination.color != self.get_piece(start).color:
                return True
            else:
                return False
        else:
            return False

    def validate_bishop_move(self, start, end):
        """The function validates the bishop movement to capture pieces and move across the board.
        Inputs:
                - start: (row, col)
                - end: (row, col)
        Output:
                - condition: boolean"""
        start_row, start_col = start
        end_row, end_col = end

        if abs(start_row - end_row) != abs(start_col - end_col):
            return False  # Bishop must move diagonally

        step_row = 1 if end_row > start_row else -1
        step_col = 1 if end_col > start_col else -1

        cur_row, cur_col = start_row + step_row, start_col + step_col
        while (cur_row, cur_col) != (end_row, end_col):
            # Ensure you call get_piece on self, not self.board
            if self.get_piece((cur_row, cur_col)):
                return False  # Path must be clear
            cur_row += step_row
            cur_col += step_col

        return True

    def validate_queen_move(self, start, end):
        """The function validates the queen movement to capture pieces and move across the board.
        Inputs:
                - start: (row, col)
                - end: (row, col)
        Output:
                - condition: boolean"""
        # Combine the logic for rooks and bishops.
        return self.validate_rook_move(start, end) or self.validate_bishop_move(
            start, end
        )

    def validate_king_move(self, start, end):
        """The function validates the king movement to capture pieces and move across the board.
        Inputs:
                - start: (row, col)
                - end: (row, col)
        Output:
                - condition: boolean"""
        start_row, start_col = start
        end_row, end_col = end
        row_diff = abs(end_row - start_row)
        col_diff = abs(end_col - start_col)

        # Ensure the king moves only one square in any direction
        if row_diff > 1 or col_diff > 1:
            return False

        moving_piece = self.get_piece(start)
        destination_piece = self.get_piece(end)

        # Prevent the king from capturing a piece of the same color
        if destination_piece and destination_piece.color == moving_piece.color:
            return False

        # Temporarily make the move on the actual board to check for threats
        original_piece = self.board[end_row][end_col]
        self.board[end_row][end_col] = moving_piece
        self.board[start_row][start_col] = None
        moving_piece.pos = (end_row, end_col)

        # Check if this move puts the king in check using is_king_in_check
        _, threats = self.is_king_in_check(moving_piece.color)
        if threats:
            # Undo the move because it results in check
            self.board[end_row][end_col] = original_piece
            self.board[start_row][start_col] = moving_piece
            moving_piece.pos = start
            return False

        # Restore the board to its original state if no check is detected
        self.board[end_row][end_col] = original_piece
        self.board[start_row][start_col] = moving_piece
        moving_piece.pos = start

        return True

    def is_king_in_check(self, color):
        """The function checks if the king is in check in a position.
        Inputs:
                - color: RGB touple
        Output:
                - condition: boolean
                - threats: list"""
        king_position = None
        threats = []  # List to store threats for more advanced handling like blocking
        for row in range(8):
            for col in range(8):
                piece = self.get_piece((row, col))
                if piece and piece.piece_type == "king" and piece.color == color:
                    king_position = (row, col)

        if not king_position:
            return False, []  # If no king is found, return False and an empty list

        for row in range(8):
            for col in range(8):
                attacker = self.get_piece((row, col))
                if attacker and attacker.color != color:
                    if self.validate_move(attacker, (row, col), king_position):
                        threats.append(
                            (attacker, (row, col))
                        )  # Include the attacker and its position
        return (
            bool(threats),
            threats,
        )  # Return both the check status and details of the threats

    def resolve_check(self, color):
        """The function checks if there ia a valid movement by a piece to stop a check.
        Inputs:
                - color: RGB touple
        Output:
                - condition: boolean"""
        in_check, threats = self.is_king_in_check(color)
        if not in_check:
            return False  # No need to resolve check if not in check

        valid_responses = []
        for threat in threats:
            threat_piece, threat_pos = threat
            # Check every piece of the current player to see if they can capture the threatening piece
            for row in range(8):
                for col in range(8):
                    defender = self.get_piece((row, col))
                    if defender and defender.color == color:
                        if self.validate_move(defender, (row, col), threat_pos):
                            # Simulate the capture
                            simulated_board = copy.deepcopy(self.board)
                            simulated_board[threat_pos[0]][threat_pos[1]] = defender
                            simulated_board[row][col] = None
                            # Check if the move resolves the check
                            _, new_threats = simulated_board.is_king_in_check(color)
                            if not new_threats:
                                valid_responses.append(
                                    (defender, (row, col), threat_pos)
                                )

        if valid_responses:
            return True  # There are valid moves to capture the threatening piece
        return False

    def check_game_status(self, color):
        """The function checks if the king is in check in a position.
        Inputs:
                - color: RGB touple
        Output:
                - condition: boolean"""
        if self.is_king_in_check(color):
            if not self.resolve_check(color):
                return "Checkmate"
        else:
            if not self.has_legal_moves(color):
                return "Stalemate"
        return "Continue playing"
