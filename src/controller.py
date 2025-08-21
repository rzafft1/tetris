import random
import copy
from typing import Dict, List, Literal, Optional
from src.gameboard import GameBoard
from src.shape import Shape
from collections import deque

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
        [2, 2],
        [2, 2]
    ],

    "T" : [
        [0, 3, 0],
        [3, 3, 3],
        [0, 0, 0],
    ],

    "J" : [
        [4, 0, 0],
        [4, 4, 4],
        [0, 0, 0]
    ],

    "L" : [
        [0, 0, 5],
        [5, 5, 5],
        [0, 0, 0]
    ],

    "S" : [
        [0, 6, 6],
        [6, 6, 0],
        [0, 0, 0]
    ],

    "Z" : [
        [7, 7, 0],
        [0, 7, 7],
        [0, 0, 0]
    ]
}


class Controller:
    
    """
    Represents the controller for managing the state of the Tetris game. 
    It creates a new game board (instance of the GameBoard class), and creates
    new shapes (instances of the Shape class) as the game goes on. It manages 
    the moving and rotating of shapes on the board, how the game changes 
    each 'tick' (i.e. when rows are erased, when the piece moves automatically, 
    and when a new piece is created), and the shape queue. It also keeps track 
    of the points in the game, and level / tick speed. 

    Attributes:
    - game_board (GameBoard): 20x10 grid representing the tetris board
    - active_shape (Shape): the number of rows in the grid
    """

    def __init__(self, initial_level: int = 1) -> None:
        """
        Initializes the game board and spawns the first shape.
        """
        self.game_board: GameBoard = GameBoard()
        self.active_shape: Optional[Shape] = None
        self.points: int = 0
        self.level: int = initial_level
        self.initial_level = initial_level
        self.total_rows_cleared = 0

        self.shape_queue: deque[Shape] = deque()
        for _ in range(3):
            self.shape_queue.append(self.generate_new_shape())

        self.spawn_new_shape()


    def update_level(self) -> None:
        """
        Decide when to move to the next levels
        """
        required_lines_cleared_per_level = 10
        self.level = self.total_rows_cleared // required_lines_cleared_per_level + self.initial_level # 10 lines per level
        
    def generate_new_shape(self) -> Shape:
        """
        Returns a single random shape
        """
        shape_matrix = random.choice(list(SHAPES.values()))
        return Shape(shape_matrix)
    
    def spawn_new_shape(self) -> bool:
        """
        Sets the active shape to the next shape in the queue, add a new shape to the queue,
        and place the new active shape on the board

        Returns:
        - bool: True if the shape can be placed, False if game over (collision on spawn).
        """
        self.active_shape = copy.deepcopy(self.shape_queue.popleft())
        self.shape_queue.append(self.generate_new_shape())
        if self.game_board.can_place(self.active_shape):
            self.game_board.place_shape(self.active_shape)
            return True
        else:
            return False
            
    def rotate(self) -> bool:
        """
        Attempts to rotate the active shape 90 degrees clockwise

        Returns:
        - bool: True if rotation is successful, False if blocked.
        """
        if self.active_shape is None:
            return False
        
        self.game_board.remove_shape(self.active_shape)
        original_matrix = copy.deepcopy(self.active_shape.matrix)
        self.active_shape.rotate()

        if self.game_board.can_place(self.active_shape):
            self.game_board.place_shape(self.active_shape)
            return True
        
        self.active_shape.matrix = original_matrix
        self.game_board.place_shape(self.active_shape)
        return False

    def move(self, direction: Literal['left', 'right', 'down']) -> bool:
        """
        Attempts to move the active shape one unit in the specified direction.

        Args:
        - direction (Literal['left', 'right', 'down']): Direction to move the shape.

        Returns:
        - bool: True if movement was successful, False if blocked.
        """
        if not self.active_shape:
            return False
        
        changein_row: int = 0
        changein_col: int = 0
        if direction == "left": changein_col = -1
        elif direction == "right": changein_col = 1
        elif direction == "down": changein_row = 1
        else: return False

        self.game_board.remove_shape(self.active_shape)
        self.active_shape.row_position += changein_row
        self.active_shape.col_position += changein_col

        if self.game_board.can_place(self.active_shape):
            self.game_board.place_shape(self.active_shape)
            return True
        
        self.active_shape.row_position -= changein_row
        self.active_shape.col_position -= changein_col
        self.game_board.place_shape(self.active_shape)
        return False
    
    def update_points(self, num_rows_cleared: int) -> None:
        """
        Given the number of rows cleared, the current level, 
        and the current score, update the score

        Args:
        - int: number of rows that were cleared
        """
        self.total_rows_cleared += num_rows_cleared
        points_table = {1: 40, 2: 100, 3: 300, 4: 1200}
        self.points += points_table.get(num_rows_cleared, 0) * self.level
            
            
    def tick(self) -> bool:
        """
        Advances the game state by one tick:
        - Moves the active shape down if possible
        - Locks shape and spawns a new one if movement is blocked
        - Clears full rows

        Returns:
        - bool: True if the game should continue, False if game over.
        """

        # Try to move the shape
        moved = self.move("down")

        # If the shape cannot be moved one unit down then lock the move
        # 1. Clear any rows
        # 2. Spawn a new shape
        # 3. Check to see if the game is over 
        if not moved:
            num_cleared = self.game_board.clear_rows()
            self.update_points(num_cleared)
            self.update_level()
            spawned = self.spawn_new_shape()
            if not spawned:
                return False
        return True