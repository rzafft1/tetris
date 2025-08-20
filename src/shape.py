from typing import List

# Type Aliases
Matrix = List[List[int]]

class Shape:

    """
    Represents a single Tetris piece (shape). It stores the shape matrix and its position
    on the board and manages the execution of a shape rotation within its matrix.

    Attributes:
    - matrix (Matrix): 4x4 or 3x3 matrix representing the shape; 0 = empty, non-zero = block.
    - row_position (int): Row index of the top-left of the shape on the board.
    - col_position (int): Column index of the top-left of the shape on the board.
    - color_key (int): Non-zero value representing the shape's color.
    """

    def __init__(self, matrix: Matrix) -> None:
        self.matrix: Matrix = matrix
        self.row_position: int = 0
        self.col_position: int = (len(self.matrix[0]) // 2) + 2
        self.color_key: int = self.get_color_key()

    def get_color_key(self) -> int:
        """
        Returns the first non-zero value in the shape's matrix, used as a color key.
        
        Returns
        - int: The non-zero matrix value representing the shape's color (0 if empty)
        """
        for row in self.matrix:
            for val in row:
                if val != 0:
                    return val
        return 0

    def rotate(self) -> None:
        """
        Rotates the shape 90° clockwise in place by:
        1. Transposing the matrix.
        2. Reversing each row.
        """
        for i in range(len(self.matrix)): # Transpose the matrix
            for j in range(i, len(self.matrix[i])):
                self.matrix[i][j], self.matrix[j][i] = self.matrix[j][i], self.matrix[i][j]
        for row in self.matrix: # Reverse each row
            row.reverse()
    
    def show(self) -> None:
        """
        Prints the shape's matrix to the terminal, with '*' for blocks and '0' for empty cells.
        """
        for row in self.matrix:
            print(" ".join("*" if val != 0 else "0" for val in row))