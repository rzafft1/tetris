from typing import Dict, List, Literal
import random 
import copy
import pygame 

# --------------------------------------------------------------------------------
# Type Aliases
# --------------------------------------------------------------------------------
# Represents a 4x4 matrix of integers where:
#   1 → occupied cell (block present)
#   0 → empty cell
Matrix = List[List[int]]


# --------------------------------------------------------------------------------
# Colors for UI
# --------------------------------------------------------------------------------
COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "YELLOW": (255, 255, 0),
    "BLUE": (0, 0, 255),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "PINK": (255, 192, 203),
    "PURPLE": (128, 0, 128),
    "ORANGE": (255, 165, 0)
}

# --------------------------------------------------------------------------------
# Tetris shape key mapping to color
# --------------------------------------------------------------------------------
COLORS_MAPPING = {
    1: COLORS["BLUE"],
    2: COLORS["YELLOW"],
    3: COLORS["PURPLE"],
    4: COLORS["PINK"],
    5: COLORS["ORANGE"],
    6: COLORS["RED"],
    7: COLORS["GREEN"]
}

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



# --------------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------------
class Shape:
    """
    Represents a Tetris piece, including:
    - The shape matrix (4x4)
    - The top left position of the shape matrix on the board
    - The current rotation state of the matrix
    - the color of the shape
    """

    def __init__(self, matrix: Matrix):
        self.matrix: Matrix = matrix
        self.rotation_state: int = 0  # Tracks rotation count (0–3)
        self.row_position: int = 0    # Top-left row position on the board
        self.col_position: int = 0    # Top-left column position on the board

        # Get the key of the shape (the key is the shape's matrices non-zero values)
        self.key: int | None = None
        for i, row in enumerate(self.matrix):
            for j, val in enumerate(row):
                if val != 0:
                    self.key = val
                    break
            if self.key is not None:
                break

    def show(self) -> None:
        """
        Prints the matrix (4 x 4) to the terminal
        - 1's are converted to '*'s, and represent cells that make up the shape
        - 0's are converted to empty strings, and represent padding
        """
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.matrix[i][j] == 0:
                    print("0", end=' ')
                else:
                    print("*", end=' ')
            print()

    def rotate(self) -> Matrix:
        """
        Rotates the shape 90° clockwise within its matrix.
        Steps:
        1. Transpose the matrix.
        2. Reverse each row.

        Returns:
            Matrix: The rotated shape.
        """
        for i in range(len(self.matrix)): # Transpose the matrix
            for j in range(i, len(self.matrix)):
                self.matrix[i][j], self.matrix[j][i] = self.matrix[j][i], self.matrix[i][j]
        for i in range(len(self.matrix)): # Reverse each row
            self.matrix[i].reverse()
        self.rotation_state = (self.rotation_state + 1) % 4
        return self.matrix
    
class Board: 
    """
    Represents the Tetris board grid and handles:
    - Shape placement
    - Collision checks
    - Clearning rows
    """

    def __init__(self, num_rows: int = 20, num_cols: int = 10):
        self.num_rows: int = num_rows
        self.num_cols: int = num_cols
        self.grid: Matrix = [[0] * num_cols for _ in range(num_rows)]

    def show(self) -> None:
        """
        Prints the grid (num_rows x num_cols Matrix) to the terminal
        - 1's are converted to '*'s, and represent occupied cells
        - 0's are converted to '_'s, and represent unoccupied cells
        """
        print(end='  j ')
        [print(j, end = ' ') for j in range(self.num_cols)]
        print()
        print("i", end = ' ')
        print('-'*(self.num_rows + 3), end = '')
        print()
        for i in range(self.num_rows):
            print(f"{i:<2}|", end = ' ')
            for j in range(self.num_cols):
                if self.grid[i][j] == 0:
                    print("_", end=' ')
                else:
                    print(self.grid[i][j], end=' ')
                if j == self.num_cols - 1:
                    print(f"|")
        print('-'*(self.num_rows + 3))
        print()
        
    def can_place(self, shape: Shape, target_row: int, target_col: int) -> bool:
        """
        Checks whether the given piece can be placed at the specified position
        without colliding with existing blocks or going out of bounds.

        Args:
        - shape (Shape): The shape to check.
        - target_row (int): The target top-left row position.
        - target_col (int): The target top-left column position.

        Returns:
        - bool: True if placement is possible, False otherwise.
        """
        for row_idx in range(len(shape.matrix)):
            for col_idx in range(len(shape.matrix[0])):
                if shape.matrix[row_idx][col_idx] != 0:
                    board_row: int = target_row + row_idx
                    board_col: int = target_col + col_idx
                    # Out-of-bounds check
                    if (board_row < 0 or board_row >= self.num_rows or
                        board_col < 0 or board_col >= self.num_cols):
                        print("OUT OF BOUNDS")
                        return False
                    # Collision check
                    if self.grid[board_row][board_col] != 0:
                        print("COLLISION")
                        return False
        return True
    
    def place_shape(self, shape: Shape) -> None:
        """
        Places a shape on the board by marking its occupied cells as 1.

        Args:
        - shape (Shape): The shape to place.
        """
        for row_idx in range(len(shape.matrix)):
            for col_idx in range(len(shape.matrix[0])):
                if shape.matrix[row_idx][col_idx] != 0:
                    self.grid[shape.row_position + row_idx][shape.col_position + col_idx] = shape.key

    def remove_shape(self, shape: Shape) -> None:
        """
        Removes a shape on the board by marking its occupied cells of 1 as 0.

        Args:
        - shape (Shape): The shape to remove.
        """
        for row_idx in range(len(shape.matrix)):
            for col_idx in range(len(shape.matrix[0])):
                if shape.matrix[row_idx][col_idx] != 0:
                    self.grid[shape.row_position + row_idx][shape.col_position + col_idx] = 0

    def clear_rows(self) -> int:
        """
        Starting from the bottom of the board, for each row that is all non-zero, 
        remove the row, and shift every row above it down 1 unit

        Returns:
        - int: number of rows that were cleared
        """
        cleared = 0
        row_idx = self.num_rows - 1

        while row_idx >= 0:
            if all(self.grid[row_idx][col_idx] != 0 for col_idx in range(self.num_cols)):
                # clear the row
                del self.grid[row_idx]
                # insert empty row at the top
                self.grid.insert(0, [0] * self.num_cols)
                cleared += 1
                # stay on the same row index since we just pulled everything down
            else:
                row_idx -= 1

        return cleared


class Game:
    """
    Manages the overall Tetris game state, including:
    - The board
    - The next active shape that will fall from the board and its behavior
    - When rows are erased
    """

    def __init__(self):
        self.board: Board = Board()
        self.active_shape: Shape | None = None
        self.spawn_new_shape()

    def spawn_new_shape(self) -> None:
        """
        Creates a new random shape and positions it at the top-center of the board.
        """
        shape = random.choice(list(SHAPES.values()))
        self.active_shape = Shape(shape)
        self.board.place_shape(self.active_shape)

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
        self.board.remove_shape(self.active_shape)
        if self.board.can_place(self.active_shape, new_row, new_col):
            self.active_shape.row_position = new_row
            self.active_shape.col_position = new_col
            self.board.place_shape(self.active_shape)
            return True
        else:
            self.board.place_shape(self.active_shape)
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
        if not self.active_shape:
            return False
        
        original_shape = copy.deepcopy(self.active_shape.matrix)
        self.board.remove_shape(self.active_shape)
        self.active_shape.rotate()
        if self.board.can_place(self.active_shape, self.active_shape.row_position, self.active_shape.col_position):
            self.board.place_shape(self.active_shape)
            return True 
        else:
            self.active_shape.matrix = original_shape
            self.board.place_shape(self.active_shape)
            return False
    
    def tick(self) -> None:
        """
        Advances the game state by one tick:
        - Attempts to move the active shape down.
        - If movement is not possible, locks the shape and spawns a new one.
        """
        if self.board.can_place(
            self.active_shape,
            self.active_shape.row_position + 1,
            self.active_shape.col_position
        ):
            self.active_shape.row_position += 1
        else:
            self.board.place_shape(self.active_shape)
            self.active_shape = Shape(random.choice(list(SHAPES.values())))

class GameUI:
    def __init__(self):
        pygame.init()
        self.WINDOW_SCALE = 0.75
        self.WINDOW_HEIGHT = int(pygame.display.Info().current_h * self.WINDOW_SCALE)
        self.WINDOW_WIDTH = int(pygame.display.Info().current_w * self.WINDOW_SCALE)
        self.surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        self.game = Game()

        self.BACKGROUND_COLOR = COLORS["WHITE"]
        self.GRID_CELL_COLOR = COLORS["WHITE"]
        self.GRID_BORDER_COLOR = COLORS["BLACK"]

        self.GRID_SCALE = 0.9
        self.CELL_SIZE = min((self.WINDOW_WIDTH * self.GRID_SCALE) // self.game.board.num_cols, (self.WINDOW_HEIGHT * self.GRID_SCALE) // self.game.board.num_rows)
        self.CELL_WIDTH = self.CELL_HEIGHT = self.CELL_SIZE
        self.GRID_WIDTH = self.game.board.num_cols * self.CELL_WIDTH
        self.GRID_HEIGHT = self.game.board.num_rows * self.CELL_HEIGHT
        self.X_OFFSET = (self.WINDOW_WIDTH - self.GRID_WIDTH) // 2
        self.Y_OFFSET = (self.WINDOW_HEIGHT - self.GRID_HEIGHT) // 2

    def draw_grid(self):
        for row in range(self.game.board.num_rows):
            for col in range(self.game.board.num_cols):
                x = col * self.CELL_WIDTH + self.X_OFFSET
                y = row * self.CELL_HEIGHT + self.Y_OFFSET
                square = pygame.Rect(x, y, self.CELL_WIDTH, self.CELL_HEIGHT)
                cell_color = COLORS_MAPPING[self.game.board.grid[row][col]] if self.game.board.grid[row][col] else self.GRID_CELL_COLOR
                pygame.draw.rect(self.surface, cell_color, square)
                pygame.draw.rect(self.surface, self.GRID_BORDER_COLOR, square, 1)
        
    def run(self):
        running = True
        while running:
            self.surface.fill(self.BACKGROUND_COLOR)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT: self.game.move("left")
                    elif event.key == pygame.K_RIGHT: self.game.move("right")
                    elif event.key == pygame.K_DOWN: self.game.move("down")
                    elif event.key == pygame.K_UP: self.game.rotate()
                elif event.type == pygame.USEREVENT:
                    self.game.tick()

            self.draw_grid()
            pygame.display.update()
# --------------------------------------------------------------------------------
# Main: simple demo loop
# --------------------------------------------------------------------------------
if __name__ == "__main__":
    app = GameUI()
    app.run()

    quit()
    game = Game()

    print("\nFirst Shape: \n")
    game.active_shape.show()
    for i in range(17):
        game.move("down")
    game.move("left")
    game.board.show()
    

    game.test_spawn_new_shape("L")
    game.active_shape.show()
    game.rotate()
    for i in range(17):
        game.move("down")
    game.board.show()

    game.test_spawn_new_shape("I")
    game.active_shape.show()
    for i in range(4):
        game.move("right")
    for i in range(18):
        game.move("down")
    game.board.show()

    game.test_spawn_new_shape("I")
    game.active_shape.show()
    for i in range(3):
        game.move("right")
    for i in range(17):
        game.move("down")
    game.board.show()


    game.test_spawn_new_shape("Z")
    game.active_shape.show()
    for i in range(7):
        game.move("right")
    for i in range(18):
        game.move("down")
    game.board.show()


    game.test_spawn_new_shape("I")
    game.active_shape.show()
    game.rotate()
    for i in range(7):
        game.move("right")
    for i in range(15):
        game.move("down")
    game.board.show()

    game.board.clear_rows()
    game.board.show()
