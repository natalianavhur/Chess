import pygame
import math

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Chessboard Example"

# Define the size of the chessboard and its tiles.
BOARD_ROWS = 8
BOARD_COLUMNS = 8
SQUARE_SIZE = SCREEN_WIDTH // BOARD_COLUMNS

# Define constants for RGB colors.
black = (0, 0, 0)
white = (255, 255, 255)


class ChessPieces:

    def __init__(self, piece_type, color, pos):
        """The function initializes a chess piece with specific type, color and board position.
        Inputs:
                - piece_type: string
                - color: string
                - pos: tuple (row, col)"""
        self.piece_type = piece_type
        self.color = color
        self.pos = pos

    def draw(self, screen):
        """The function draws the chess pieces on the board using geometric shapes based on piece type and position."""

        # Calculate the center coordinate of the square tile.
        center_x = self.pos[1] * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = self.pos[0] * SQUARE_SIZE + SQUARE_SIZE // 2

        # Set the colors of the piece.
        color = (
            pygame.Color("black") if self.color == "black" else pygame.Color("white")
        )
        highlight = pygame.Color("gold")

        draw_methods = {
            "pawn": self.draw_pawn,
            "rook": self.draw_rook,
            "knight": self.draw_knight,
            "bishop": self.draw_bishop,
            "queen": self.draw_queen,
            "king": self.draw_king,
        }

        # Call the drawing methods.
        draw_method = draw_methods.get(self.piece_type)
        if draw_method:
            draw_method(screen, center_x, center_y, color)

    def draw_pawn(self, screen, center_x, center_y, color):
        """The function draws a pawn with basic geometric shapes.
        Inputs:
                - screen
                - center_x: integer
                - center_y: integer
                - color: RGB tuple"""

        # Constants for size of shapes.
        radius = SQUARE_SIZE // 7
        circle_diameter = 2 * radius
        rect_width = circle_diameter + 4
        rect_height = 8

        pygame.draw.circle(screen, color, (center_x, center_y - 20), radius)

        rect_top = center_y - 20 + radius

        rounded_rect = pygame.Rect(
            center_x - rect_width // 2, rect_top, rect_width, rect_height
        )
        pygame.draw.rect(screen, color, rounded_rect, border_radius=5)

        trapezoid_height = 20
        trapezoid_top_width = rect_width - 6
        trapezoid_bottom_width = rect_width + 6
        trapezoid_top = rect_top + rect_height

        pygame.draw.polygon(
            screen,
            color,
            [
                (center_x - trapezoid_top_width // 2, trapezoid_top),  # Top left
                (center_x + trapezoid_top_width // 2, trapezoid_top),  # Top right
                (
                    center_x + trapezoid_bottom_width // 2,
                    trapezoid_top + trapezoid_height,
                ),  
                (
                    center_x - trapezoid_bottom_width // 2,
                    trapezoid_top + trapezoid_height,
                ),
            ],
        )

        lower_rect_height = 8
        lower_rect_width = trapezoid_bottom_width + 10
        lower_rect_top = trapezoid_top + trapezoid_height

        first_lower_rect = pygame.Rect(
            center_x - lower_rect_width // 2,
            lower_rect_top,
            lower_rect_width,
            lower_rect_height,
        )
        pygame.draw.rect(screen, color, first_lower_rect, border_radius=5)

        second_lower_rect_height = 8

        # Adjust the centering of the second rounded rectangle.
        second_lower_rect_x_center = center_x - (lower_rect_width + 5) // 2

        second_lower_rect = pygame.Rect(
            second_lower_rect_x_center,
            lower_rect_top + lower_rect_height,
            lower_rect_width + 5,
            second_lower_rect_height,
        )
        pygame.draw.rect(screen, color, second_lower_rect, border_radius=5)

    def draw_rook(self, screen, center_x, center_y, color):
        """The function draws a pawn with basic geometric shapes.
        Inputs:
                - screen
                - center_x: integer
                - center_y: integer
                - color: RGB tuple"""

        # Constants for size
        rect_height = 10
        rect_width = 10
        space_between = 5

        # Calculate positions of the three rectangles and center them as a group.
        first_rect_x = (
            center_x - 1.5 * rect_width - space_between
        )  
        second_rect_x = (
            center_x - rect_width / 2
        )  
        third_rect_x = center_x + 0.5 * rect_width + space_between
        

        # Top three separate rectangles
        top_rects = [
            pygame.Rect(first_rect_x, center_y - 25, rect_width, rect_height),
            pygame.Rect(second_rect_x, center_y - 25, rect_width, rect_height),
            pygame.Rect(third_rect_x, center_y - 25, rect_width, rect_height),
        ]
        for rect in top_rects:
            pygame.draw.rect(screen, color, rect)

        large_rect_width = 3 * rect_width + 2 * space_between
        large_rect_top = center_y - 25 + rect_height
        large_rect = pygame.Rect(
            first_rect_x, large_rect_top, large_rect_width, rect_height
        )
        pygame.draw.rect(screen, color, large_rect)

        body_rect_top = large_rect_top + rect_height
        body_rect_width = large_rect_width - 10
        body_rect_height = rect_height + 10
        body_rect = pygame.Rect(
            first_rect_x + 5, body_rect_top, body_rect_width, body_rect_height
        )
        pygame.draw.rect(screen, color, body_rect)

        toop_x = body_rect_top + body_rect_height
        rook_lower_rectangle_height = rect_height - 3
        rook_lower_rectangle = pygame.Rect(
            first_rect_x,
            toop_x,
            large_rect_width,
            rook_lower_rectangle_height,
        )
        pygame.draw.rect(screen, color, rook_lower_rectangle)

        rect2_top = toop_x + rook_lower_rectangle_height
        rook_second_lower_rectangle = pygame.Rect(
            first_rect_x - 5,
            rect2_top,
            large_rect_width + 10,
            rect_height - 3,
        )
        pygame.draw.rect(screen, color, rook_second_lower_rectangle)

    def draw_knight(self, screen, center_x, center_y, color):
        """The function draws a pawn with basic geometric shapes.
        Inputs:
                - screen
                - center_x: integer
                - center_y: integer
                - color: RGB tuple"""
        # Calculate top and bottom half widths and shift.
        shift = 10
        top_width = 15
        bottom_width = 15
        height = 20
        top_half_width = top_width // 2
        bottom_half_width = bottom_width // 2

        # Adjust center_x to move the trapezoid to the left.
        adjusted_center_x = center_x - 20

        # Coordinates of the trapezoid.
        top_left = (
            adjusted_center_x - top_half_width + shift,
            center_y - height // 2,
        )
        top_right = (
            adjusted_center_x + top_half_width + shift,
            center_y - height // 2,
        )
        bottom_right = (
            adjusted_center_x + bottom_half_width,
            center_y + height // 2,
        )
        bottom_left = (
            adjusted_center_x - bottom_half_width,
            center_y + height // 2,
        )

        # Draw the trapezoid
        pygame.draw.polygon(
            screen, color, [top_left, top_right, bottom_right, bottom_left]
        )

        top_y = center_y - height + 10
        top_x = center_x - top_half_width + shift - 5

        ellipse_height = 25
        ellipse_width = 35
        ellipse_top = center_y - height - 5
        pygame.draw.ellipse(
            screen,
            color,
            (
                center_x - ellipse_width // 2,
                ellipse_top,
                ellipse_width,
                ellipse_height,
            ),
        )

        # Triangle properties (to the left-top of the circle)
        triangle_height = 5
        triangle_base = 25
        triangle_top_point = (top_x - 5, top_y - 25)
        triangle_left_point = (
            top_x - triangle_base // 2,
            top_y + triangle_height - 5,
        )
        triangle_right_point = (
            top_x + triangle_base // 2,
            top_y + triangle_height - 5,
        )

        # Draw the triangle.
        pygame.draw.polygon(
            screen,
            color,
            [triangle_top_point, triangle_left_point, triangle_right_point],
        )

        # Rectangle properties (right side below the circle).
        rect_width = 20
        rect_height = 30
        rect_top_left = (top_x, top_y)

        # Draw the rectangle
        pygame.draw.rect(
            screen,
            color,
            (rect_top_left[0], rect_top_left[1], rect_width, rect_height),
        )

        new_trap_top_width = 5
        new_trap_bottom_width = 13
        new_trap_height = 30
        new_trap_x_start = (
            rect_top_left[0] + rect_width - 5
        )
        new_trap_y_start = rect_top_left[1]

        # Calculate the coordinates for the new trapezoid
        new_trap_top_left = (new_trap_x_start, new_trap_y_start)
        new_trap_top_right = (
            new_trap_x_start + new_trap_top_width,
            new_trap_y_start,
        )
        new_trap_bottom_right = (
            new_trap_x_start + new_trap_bottom_width,
            new_trap_y_start + new_trap_height,
        )
        new_trap_bottom_left = (
            new_trap_x_start,
            new_trap_y_start + new_trap_height,
        )

        # Draw the new trapezoid
        pygame.draw.polygon(
            screen,
            color,
            [
                new_trap_top_left,
                new_trap_top_right,
                new_trap_bottom_right,
                new_trap_bottom_left,
            ],
        )

        rect2_top_x = top_x - 5
        rect2_width = rect_width + 17
        rect2_top = top_y + rect_height
        rect2_height = 7
        rook_second_lower_rectangle = pygame.Rect(
            rect2_top_x,
            rect2_top,
            rect2_width,
            rect2_height,
        )
        pygame.draw.rect(
            screen,
            color,
            rook_second_lower_rectangle,
            border_radius=5,
        )

        rect3_top_x = rect2_top_x - 5
        rect3_top = rect2_top + rect2_height
        rect3_width = rect2_width + 10
        rect3_height = 7
        rook_third_lower_rectangle = pygame.Rect(
            rect3_top_x,
            rect3_top,
            rect3_width,
            rect3_height,
        )
        pygame.draw.rect(
            screen,
            color,
            rook_third_lower_rectangle,
            border_radius=5,
        )

    def draw_bishop(self, screen, center_x, center_y, color):
        """The function draws a pawn with basic geometric shapes.
        Inputs:
                - screen
                - center_x: integer
                - center_y: integer
                - color: RGB tuple"""

        # Start drawing the bishop components from the top down
        radius = SQUARE_SIZE // 14
        circle_diameter = 2 * radius
        top_y = center_y - 27

        pygame.draw.circle(screen, color, (center_x, top_y), radius)

        # Ellipse touching the circle
        ellipse_height = 25
        ellipse_width = 18
        ellipse_top = top_y + radius - 2
        pygame.draw.ellipse(
            screen,
            color,
            (
                center_x - ellipse_width // 2,
                ellipse_top,
                ellipse_width,
                ellipse_height,
            ),
        )

        # Curved rectangle wider than the ellipse
        rect1_width = 27
        rect1_height = 4
        rect1_top = ellipse_top + ellipse_height - 3
        pygame.draw.rect(
            screen,
            color,
            (center_x - rect1_width // 2, rect1_top, rect1_width, rect1_height),
            border_radius=5,
        )

        # Smaller rectangle below the first curved rectangle
        rect2_width = 20
        rect2_height = 2
        rect2_top = rect1_top + rect1_height
        pygame.draw.rect(
            screen,
            color,
            (center_x - rect2_width // 2, rect2_top, rect2_width, rect2_height),
        )

        rect1_width = 27
        rect1_height = 4
        rect1_top = rect2_top + rect2_height
        pygame.draw.rect(
            screen,
            color,
            (center_x - rect1_width // 2, rect1_top, rect1_width, rect1_height),
            border_radius=5,
        )

        # Trapezoid below the larger curved rectangle
        trapezoid_top_width = 15
        trapezoid_bottom_width = 30
        trapezoid_height = 17
        trapezoid_top = (
            rect1_top + rect1_height
        )
        trapezoid_top_left = center_x - trapezoid_top_width // 2
        trapezoid_bottom_left = center_x - trapezoid_bottom_width // 2
        pygame.draw.polygon(
            screen,
            color,
            [
                (trapezoid_top_left, trapezoid_top),
                (trapezoid_top_left + trapezoid_top_width, trapezoid_top),
                (
                    trapezoid_bottom_left + trapezoid_bottom_width,
                    trapezoid_top + trapezoid_height,
                ),
                (trapezoid_bottom_left, trapezoid_top + trapezoid_height),
            ],
        )

        # Final curved rectangle below the trapezoid
        rect4_width = 40
        rect4_height = 5
        rect4_top = trapezoid_top + trapezoid_height
        pygame.draw.rect(
            screen,
            color,
            (center_x - rect4_width // 2, rect4_top, rect4_width, rect4_height),
            border_radius=5,
        )
        rect5_width = 45
        rect5_height = 5
        rect5_top = rect4_top + rect4_height
        pygame.draw.rect(
            screen,
            color,
            (center_x - rect5_width // 2, rect5_top, rect5_width, rect5_height),
            border_radius=5,
        )

    def draw_queen(self, screen, center_x, center_y, color):
        """The function draws a pawn with basic geometric shapes.
        Inputs:
                - screen
                - center_x: integer
                - center_y: integer
                - color: RGB tuple"""
        # Define the top of the queen.
        top_y = center_y - 25

        # Semi-circle at the top
        queen_circle_radius = SQUARE_SIZE // 8
        circle_diameter = 2 * queen_circle_radius

        pygame.draw.circle(screen, color, (center_x, top_y), queen_circle_radius)

        rect_width = queen_circle_radius + 4
        rect_height = 8

        # Curved rectangle below the semi-circle
        rect1_width = 30
        rect1_height = 7
        rect1_top = top_y + queen_circle_radius / 2
        pygame.draw.rect(
            screen,
            color,
            (center_x - rect1_width // 2, rect1_top, rect1_width, rect1_height),
            border_radius=5,
        )

        # Trapezoid below the first curved rectangle
        trapezoid1_top_width = 30
        trapezoid1_bottom_width = 15
        trapezoid1_height = 7
        trapezoid1_top = rect1_top + rect1_height - 3
        pygame.draw.polygon(
            screen,
            color,
            [
                (center_x - trapezoid1_top_width // 2, trapezoid1_top),
                (center_x + trapezoid1_top_width // 2, trapezoid1_top),
                (
                    center_x + trapezoid1_bottom_width // 2,
                    trapezoid1_top + trapezoid1_height,
                ),
                (
                    center_x - trapezoid1_bottom_width // 2,
                    trapezoid1_top + trapezoid1_height,
                ),
            ],
        )

        # Second curved rectangle below the first trapezoid
        rect2_width = 25
        rect2_height = 7
        rect2_top = trapezoid1_top + trapezoid1_height
        pygame.draw.rect(
            screen,
            color,
            (center_x - rect2_width // 2, rect2_top, rect2_width, rect2_height),
            border_radius=5,
        )

        # Second trapezoid below the second curved rectangle
        trapezoid2_top_width = 15
        trapezoid2_bottom_width = 30
        trapezoid2_height = 27
        trapezoid2_top = rect2_top + rect2_height
        pygame.draw.polygon(
            screen,
            color,
            [
                (center_x - trapezoid2_top_width // 2, trapezoid2_top),
                (center_x + trapezoid2_top_width // 2, trapezoid2_top),
                (
                    center_x + trapezoid2_bottom_width // 2,
                    trapezoid2_top + trapezoid2_height,
                ),
                (
                    center_x - trapezoid2_bottom_width // 2,
                    trapezoid2_top + trapezoid2_height,
                ),
            ],
        )

        # Third curved rectangle below the second trapezoid
        rect1_width = 40
        rect1_height = 7
        rect1_top = trapezoid2_top + trapezoid2_height
        pygame.draw.rect(
            screen,
            color,
            (center_x - rect1_width // 2, rect1_top, rect1_width, rect1_height),
            border_radius=5,
        )

        # Fourth curved rectangle below the third one
        rect4_width = 50
        rect4_height = 7
        rect4_top = rect1_top + rect1_height
        pygame.draw.rect(
            screen,
            color,
            (center_x - rect4_width // 2, rect4_top, rect4_width, rect4_height),
            border_radius=5,
        )

    def draw_king(self, screen, center_x, center_y, color):
        """The function draws a pawn with basic geometric shapes.
        Inputs:
                - screen
                - center_x: integer
                - center_y: integer
                - color: RGB tuple"""

        top_y = center_y - 33

        cross_height = 15
        cross_width = 6
        cross_arm_length = 20

        # Vertical part of cross.
        pygame.draw.rect(
            screen,
            color,
            (center_x - cross_width // 2, top_y, cross_width, cross_height),
        )
        # Horizontal part of cross.
        pygame.draw.rect(
            screen,
            color,
            (
                center_x - cross_arm_length // 2,
                top_y + cross_height // 2 - cross_width // 2,
                cross_arm_length,
                cross_width,
            ),
        )

        # Trapezoid below the cross
        trapezoid1_top = top_y + cross_height
        trapezoid1_height = 10
        trapezoid1_top_width = 20
        trapezoid1_bottom_width = 15
        pygame.draw.polygon(
            screen,
            color,
            [
                (center_x - trapezoid1_top_width // 2, trapezoid1_top),
                (center_x + trapezoid1_top_width // 2, trapezoid1_top),
                (
                    center_x + trapezoid1_bottom_width // 2,
                    trapezoid1_top + trapezoid1_height,
                ),
                (
                    center_x - trapezoid1_bottom_width // 2,
                    trapezoid1_top + trapezoid1_height,
                ),
            ],
        )

        # First curved rectangle below the second trapezoid
        rect1_width = 30
        rect1_height = 7
        rect1_top = trapezoid1_top + trapezoid1_height
        pygame.draw.rect(
            screen,
            color,
            (center_x - rect1_width // 2, rect1_top, rect1_width, rect1_height),
            border_radius=5,
        )

        # Another trapezoid below the first curved rectangle
        trapezoid2_top = rect1_top + rect1_height
        trapezoid2_height = 25
        trapezoid2_top_width = 15
        trapezoid2_bottom_width = 30
        pygame.draw.polygon(
            screen,
            color,
            [
                (center_x - trapezoid2_top_width // 2, trapezoid2_top),
                (center_x + trapezoid2_top_width // 2, trapezoid2_top),
                (
                    center_x + trapezoid2_bottom_width // 2,
                    trapezoid2_top + trapezoid2_height,
                ),
                (
                    center_x - trapezoid2_bottom_width // 2,
                    trapezoid2_top + trapezoid2_height,
                ),
            ],
        )

        # First curved rectangle below the second trapezoid
        rect2_width = 40
        rect2_height = 7
        rect2_top = trapezoid2_top + trapezoid2_height
        pygame.draw.rect(
            screen,
            color,
            (center_x - rect2_width // 2, rect2_top, rect2_width, rect2_height),
            border_radius=5,
        )

        # First curved rectangle below the second trapezoid
        rect3_width = 45
        rect3_height = 7
        rect3_top = rect2_top + rect2_height
        pygame.draw.rect(
            screen,
            color,
            (center_x - rect3_width // 2, rect3_top, rect3_width, rect3_height),
            border_radius=5,
        )
