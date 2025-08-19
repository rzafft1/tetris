from typing import List
from src.shape import Shape

# Type Aliases
Matrix = List[List[int]]

class GameBoard: 
    """
    Represents the Tetris board grid and handles:
    - Shape placement
    - Collision checks
    - Clearning rows
    """

    # Local Variables
    num_rows: int
    num_cols: int
    grid: Matrix

    # Constructor
    def __init__(self, num_rows: int = 20, num_cols: int = 10) -> None:
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.grid: Matrix = [[0 for _ in range(num_cols)] for _ in range(num_rows)]


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
                    if board_row < 0 or board_row >= self.num_rows or board_col < 0 or board_col >= self.num_cols:
                        print("OUT OF BOUNDS")
                        return False
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
        cleared: int = 0
        row_idx: int = self.num_rows - 1

        while row_idx >= 0:
            if all(self.grid[row_idx][col] != 0 for col in range(self.num_cols)):
                del self.grid[row_idx]
                self.grid.insert(0, [0] * self.num_cols)
                cleared += 1
            else:
                row_idx -= 1

        return cleared
