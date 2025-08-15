from typing import Dict, List
import random 


# --------------------------------------------------------------------------------
# Type Aliases
# --------------------------------------------------------------------------------
# Represents a 4x4 matrix of integers where:
#   1 → occupied cell (block present)
#   0 → empty cell
Matrix = List[List[int]]

# --------------------------------------------------------------------------------
# Shape Definitions for Tetris Pieces
# --------------------------------------------------------------------------------
# Each piece is defined as a 4x4 matrix (Matrix) in its default orientation.
# The shapes follow the standard Tetris pieces (I, O, T, L, J, S, Z variants).
SHAPES: Dict[str, Matrix] = {
    "I" : [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],

    "O" : [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ],

    "T" : [
        [0, 1, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],

    "J" : [
        [1, 0, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],

    "L" : [
        [0, 0, 1, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],

    "S" : [
        [0, 1, 1, 0],
        [1, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],

    "Z" : [
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
}


class Piece:
    """
    Represents a Tetris piece, including:
    - The shape matrix (4x4)
    - Current rotation state
    - Current position on the board
    """

    def __init__(self, shape: Matrix):
        self.shape: Matrix = shape
        self.rotation_state: int = 0  # Tracks rotation count (0–3)
        self.row_position: int = 0    # Top-left row position on the board
        self.col_position: int = 2    # Top-left column position on the board

    def rotate(self) -> Matrix:
        """
        Rotates the shape 90° clockwise in place.
        Steps:
        1. Transpose the matrix.
        2. Reverse each row.

        Returns:
            Matrix: The rotated shape.
        """
        for i in range(len(self.shape)): # Transpose the matrix
            for j in range(i, len(self.shape)):
                self.shape[i][j], self.shape[j][i] = self.shape[j][i], self.shape[i][j]
        for i in range(len(self.shape)): # Reverse each row
            self.shape[i].reverse()
        self.rotation_state = (self.rotation_state + 1) % 4
        return self.shape
    
class Board: 
    """
    Represents the Tetris board grid and handles:
    - Piece placement
    - Collision checks
    """

    def __init__(self, num_rows: int = 20, num_cols: int = 10):
        self.num_rows: int = num_rows
        self.num_cols: int = num_cols
        # Initialize empty grid
        self.grid: Matrix = [[0] * num_cols for _ in range(num_rows)]

    def can_place(self, piece: Piece, target_row: int, target_col: int) -> bool:
        """
        Checks whether the given piece can be placed at the specified position
        without colliding with existing blocks or going out of bounds.

        Args:
        - piece (Piece): The piece to check.
        - target_row (int): The target top-left row position.
        - target_col (int): The target top-left column position.

        Returns:
        - bool: True if placement is possible, False otherwise.
        """
        for row_idx in range(len(piece.shape)):
            for col_idx in range(len(piece.shape[0])):
                if piece.shape[row_idx][col_idx] == 1:
                    board_row = target_row + row_idx
                    board_col = target_col + col_idx
                    # Out-of-bounds check
                    if (board_row < 0 or board_row >= self.num_rows or
                        board_col < 0 or board_col >= self.num_cols):
                        return False
                    # Collision check
                    if self.grid[board_row][board_col] == 1:
                        return False
        return True
    
    def place_piece(self, piece: Piece) -> None:
        """
        Places a piece on the board by marking its occupied cells as 1.
        ARGS:
        - piece (Piece): The piece to place.
        """
        for row_idx in range(len(piece.shape)):
            for col_idx in range(len(piece.shape[0])):
                if piece.shape[row_idx][col_idx] == 1:
                    self.grid[piece.row_position + row_idx][piece.col_position + col_idx] = 1

class Game:
    """
    Manages the overall Tetris game state, including:
    - The board
    - The current falling piece
    """

    def __init__(self):
        self.board: Board = Board()
        self.current_piece: Piece = Piece(random.choice(list(SHAPES.values())))

    def tick(self) -> None:
        """
        Advances the game state by one tick:
        - Attempts to move the current piece down.
        - If movement is not possible, locks the piece and spawns a new one.
        """
        if self.board.can_place(
            self.current_piece,
            self.current_piece.row_position + 1,
            self.current_piece.col_position
        ):
            self.current_piece.row_position += 1
        else:
            self.board.place_piece(self.current_piece)
            self.current_piece = Piece(random.choice(list(SHAPES.values())))