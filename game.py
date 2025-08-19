import pygame

pygame.init()

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

COLORS_MAPPING = {
    1: COLORS["BLUE"],
    2: COLORS["YELLOW"],
    3: COLORS["PURPLE"],
    4: COLORS["PINK"],
    5: COLORS["ORANGE"],
    6: COLORS["RED"],
    7: COLORS["GREEN"]
}

"""
WINDOW SETTINGS
"""
BACKGROUND_COLOR = COLORS["WHITE"]
WINDOW_SCALE = 0.75
WINDOW_HEIGHT = int(pygame.display.Info().current_h * WINDOW_SCALE)
WINDOW_WIDTH = int(pygame.display.Info().current_w * WINDOW_SCALE)

"""
GRID SETTINGS
"""
GRID_CELL_COLOR = COLORS["WHITE"]
GRID_BORDER_COLOR = COLORS["BLACK"]
GRID_SCALE = 0.9
ROWS = 20
COLS = 10
CELL_SIZE = min((WINDOW_WIDTH * GRID_SCALE) // COLS, (WINDOW_HEIGHT * GRID_SCALE) // ROWS)
CELL_WIDTH = CELL_HEIGHT = CELL_SIZE
GRID_WIDTH = COLS * CELL_WIDTH
GRID_HEIGHT = ROWS * CELL_HEIGHT
X_OFFSET = (WINDOW_WIDTH - GRID_WIDTH) // 2
Y_OFFSET = (WINDOW_HEIGHT - GRID_HEIGHT) // 2

# Create a surface
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Test matrix
matrix = [[0 for _ in range(COLS)] for _ in range(ROWS)]
matrix[10][5] = 1
matrix[10][6] = 1
matrix[15][7] = 2
matrix[11][5] = 3
matrix[13][4] = 4
matrix[15][5] = 5
matrix[18][1] = 6
matrix[4][3] = 7

def draw_grid(grid):
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_WIDTH + X_OFFSET
            y = row * CELL_HEIGHT + Y_OFFSET
            square = pygame.Rect(x, y, CELL_WIDTH, CELL_HEIGHT)
            cell_color = COLORS_MAPPING[grid[row][col]] if grid[row][col] else GRID_CELL_COLOR
            pygame.draw.rect(surface, cell_color, square)
            pygame.draw.rect(surface, GRID_BORDER_COLOR, square, 1)
    pygame.display.update()

while True:
    surface.fill(BACKGROUND_COLOR)
    draw_grid(matrix)
    pygame.display.update()

pygame.quit()
