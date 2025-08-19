from typing import Dict, List, Optional

# Type Aliases
Matrix = List[List[int]]

class Shape:

    """
    Represents a Tetris piece, including:
    - The shape matrix (4x4)
    - The top left position of the shape matrix on the board
    - The current rotation state of the matrix
    - the color of the shape
    """

    # Local Variables
    matrix: Matrix
    rotation_state: int
    row_position: int
    col_position: int
    key: Optional[int] # the key is mapped to the color

    def __init__(self, matrix: Matrix) -> None:
        self.matrix = matrix
        self.rotation_state = 0
        self.row_position = 0
        self.col_position = 0

        # Determine the key of the shape (first non-zero value)
        self.key: Optional[int] = None
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
    