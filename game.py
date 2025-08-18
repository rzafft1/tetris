import pygame

pygame.init()

COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255)
}

"""
SETTINGS
"""
BACKGROUND_COLOR = COLORS["WHITE"]
WINDOW_HEIGHT = int(pygame.display.Info().current_h / 1.5)
WINDOW_WIDTH = int(pygame.display.Info().current_w / 1.5)
ROWS = 20
COLS = 10
GRID_WIDTH = WINDOW_WIDTH // 1.5
GRID_HEIGHT = WINDOW_HEIGHT // 1.5
CELL_SIZE = min(GRID_WIDTH // COLS, GRID_HEIGHT // ROWS)
CELL_WIDTH = CELL_SIZE
CELL_HEIGHT = CELL_SIZE

# Get the current display size
info = pygame.display.Info()

# Create a surface object to draw on
surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

# Grid info


# Matrix to test with
matrix = [[0 for _ in range(COLS)] for _ in range(ROWS)]
manual_positions = [(0, 0), (5, 3), (10, 7), (19, 9), (2, 4)]
for r, c in manual_positions:
    matrix[r][c] = 1

while True:
    surface.fill(BACKGROUND_COLOR)

    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_WIDTH
            y = row * CELL_HEIGHT
            rect = pygame.Rect(x, y, CELL_WIDTH, CELL_HEIGHT)
            color = COLORS["BLACK"] if matrix[row][col] else COLORS["WHITE"]
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (0, 0, 0), rect, 1)

    pygame.display.update()

pygame.quit()