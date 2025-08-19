from typing import List
from src.shape import Shape

# Type Aliases
Matrix = List[List[int]]

class GameBoard: 

    """
    Represents the Tetris board 'grid'. It stores and manages a matrix that represents
    the board (numbers greater than 0 are occupied spaces, 0's are unoccupied spaces).
    It decides whether or not shapes can be placed on the grid, manages the execution
    of placing shapes on the grid, and executes the clear clearing rows that are 
    completely occupied.

    Attributes:
    - grid (Matrix): 20x10 grid representing the tetris board
    - num_rows (int): the number of rows in the grid
    - num_cols (int): the number of columsn in the grid
    """

    def __init__(self, num_rows: int = 20, num_cols: int = 10) -> None:
        """
        Initializes the board with the given dimensions.

        Args:
        - num_rows (int): Number of rows in the board. Defaults to 20.
        - num_cols (int): Number of columns in the board. Defaults to 10.
        """
        self.num_rows: int = num_rows
        self.num_cols: int = num_cols
        self.grid: Matrix = [[0 for _ in range(num_cols)] for _ in range(num_rows)]
     
    def can_place(self, shape: Shape) -> bool:
        """
        Checks whether the given shape can be placed at its current position.

        Args:
        - shape (Shape): The shape to check.

        Returns:
        - bool: True if placement is possible, False otherwise.
        """
        for row_idx in range(len(shape.matrix)):
            for col_idx in range(len(shape.matrix[row_idx])):
                if shape.matrix[row_idx][col_idx] != 0:
                    board_row = shape.row_position + row_idx
                    board_col = shape.col_position + col_idx
                    if (board_row < 0 or board_row >= self.num_rows or
                        board_col < 0 or board_col >= self.num_cols):
                        return False # Out of bounds
                    if self.grid[board_row][board_col] != 0:
                        return False # Collision with existing block
        return True
    
    def place_shape(self, shape: Shape) -> None:
        """
        Marks the cells occupied by the shape on the board using its color key.

        Args:
        - shape (Shape): The shape to place.
        """
        for row_idx in range(len(shape.matrix)):
            for col_idx in range(len(shape.matrix[row_idx])):
                if shape.matrix[row_idx][col_idx] != 0:
                    grid_row = shape.row_position + row_idx
                    grid_col = shape.col_position + col_idx
                    if 0 <= grid_row < self.num_rows and 0 <= grid_col < self.num_cols:
                        self.grid[grid_row][grid_col] = shape.color_key

    def remove_shape(self, shape: Shape) -> None:
        """
        Removes the shape from the board, setting its occupied cells back to 0.

        Args:
        - shape (Shape): The shape to remove.
        """
        for row_idx in range(len(shape.matrix)):
            for col_idx in range(len(shape.matrix[row_idx])):
                if shape.matrix[row_idx][col_idx] != 0:
                    grid_row = shape.row_position + row_idx
                    grid_col = shape.col_position + col_idx
                    if 0 <= grid_row < self.num_rows and 0 <= grid_col < self.num_cols:
                        self.grid[grid_row][grid_col] = 0

    def clear_rows(self) -> int:
        """
        Clears all fully occupied rows and shifts rows above down.

        Returns:
        - int: number of rows that were cleared
        """
        cleared: int = 0
        row_idx: int = self.num_rows - 1
        while row_idx >= 0:
            if all(self.grid[row_idx][col] != 0 for col in range(self.num_cols)):
                del self.grid[row_idx] # Remove full row
                self.grid.insert(0, [0] * self.num_cols) # Insert empty row at the top
                cleared += 1
            else:
                row_idx -= 1
        return cleared

    def show(self) -> None:
        """
        Prints the board to the terminal.
        '*' represents occupied cells, '_' represents empty cells.
        """
        print("   " + " ".join(str(j) for j in range(self.num_cols)))
        print("  " + "-" * (self.num_cols * 2))

        for i, row in enumerate(self.grid):
            print(f"{i:<2}|", end=' ')
            print(" ".join(str(cell) if cell != 0 else "_" for cell in row))
        print("  " + "-" * (self.num_cols * 2))
        print()