import random
import copy
from typing import Dict, List, Literal, Optional
from src.gameboard import GameBoard
from src.shape import Shape

# Type Aliases
Matrix = List[List[int]]

# Shape Definitions for Tetris Pieces
SHAPES: Dict[str, Matrix] = {
    "I" : [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],

    "O" : [
        [0, 0, 0, 0],
        [0, 2, 2, 0],
        [0, 2, 2, 0],
        [0, 0, 0, 0]
    ],

    "T" : [
        [0, 3, 0, 0],
        [3, 3, 3, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],

    "J" : [
        [4, 0, 0, 0],
        [4, 4, 4, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],

    "L" : [
        [0, 0, 5, 0],
        [5, 5, 5, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],

    "S" : [
        [0, 6, 6, 0],
        [6, 6, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],

    "Z" : [
        [7, 7, 0, 0],
        [0, 7, 7, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
}


class Controller:
    
    """
    Manages the overall Tetris game state, including:
    - The board
    - The next active shape that will fall from the board and its behavior
    - When rows are erased
    """

    # Local Variables
    game_board: GameBoard
    active_shape: Optional[Shape]

    def __init__(self) -> None:
        self.game_board = GameBoard()
        self.active_shape: Optional[Shape] = None
        self.spawn_new_shape()

    def spawn_new_shape(self) -> None:
        """
        Creates a new random shape and positions it at the top-center of the board.
        """
        shape_matrix: Matrix = random.choice(list(SHAPES.values()))
        self.active_shape = Shape(shape_matrix)
        self.game_board.place_shape(self.active_shape)

    def move(self, direction: Literal['left', 'right', 'down']) -> bool:
        """
        Attempts to move the active shape 1 unit in the desired direction

        1. Get the change in direction 
        2. Calculate the new coordinates of the shape
        3. Remove the shape from the board
        4. If the shape can be placed with the new coordinates, place it, return true
        5. Otherwise, place the original shape back on the board

        Args:
        - direction (Literal['left', 'right', 'down'])

        Returns:
        - bool: True if the shape was moved, false if blocked
        """
        if not self.active_shape:
            return False
        
        changein_row: int = 0
        changein_col: int = 0
        if direction == "left": changein_col = -1
        elif direction == "right": changein_col = 1
        elif direction == "down": changein_row = 1
        else: return False
        
        new_row: int = self.active_shape.row_position + changein_row
        new_col: int = self.active_shape.col_position + changein_col
        self.game_board.remove_shape(self.active_shape)
        if self.game_board.can_place(self.active_shape, new_row, new_col):
            self.active_shape.row_position = new_row
            self.active_shape.col_position = new_col
            self.game_board.place_shape(self.active_shape)
            return True
        else:
            self.game_board.place_shape(self.active_shape)
            return False
        
    def rotate(self) -> bool:
        """
        Attempts to rotate the active shape 90 degrees clockwise

        1. Make a copy of the current shape matrix
        2. Remove the shape from the board
        3. Rotate the shape
        4. If the shape can be placed after the new rotation, place it, return true
        5. Otherwise, place the shape with its original matrix back on the board

        Returns:
        - bool: True if the shape was moved, false if blocked
        """
        if self.active_shape is None:
            return False

        original_matrix: Matrix = copy.deepcopy(self.active_shape.matrix)
        self.game_board.remove_shape(self.active_shape)
        self.active_shape.rotate()

        if self.game_board.can_place(self.active_shape, self.active_shape.row_position, self.active_shape.col_position):
            self.game_board.place_shape(self.active_shape)
            return True
        else:
            self.active_shape.matrix = original_matrix
            self.game_board.place_shape(self.active_shape)
            return False
    
    def tick(self) -> None:
        """
        Advances the game state by one tick:
        - Attempts to move the active shape down.
        - If movement is not possible, locks the shape and spawns a new one.
        """
        if self.active_shape is None:
            return

        if self.game_board.can_place(
            self.active_shape,
            self.active_shape.row_position + 1,
            self.active_shape.col_position
        ):
            self.active_shape.row_position += 1
        else:
            self.game_board.place_shape(self.active_shape)
            new_shape_matrix: Matrix = random.choice(list(SHAPES.values()))
            self.active_shape = Shape(new_shape_matrix)