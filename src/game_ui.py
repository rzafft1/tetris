from typing import Dict, List, Tuple
import pygame 
from src.controller import Controller

# Type Aliases
Matrix = List[List[int]]

# Colors for UI
COLORS: Dict[str, Tuple[int, int, int]] = {
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

# Tetris shape key mapping to color
COLORS_MAPPING: Dict[int, Tuple[int, int, int]] = {
    1: COLORS["BLUE"],
    2: COLORS["YELLOW"],
    3: COLORS["PURPLE"],
    4: COLORS["PINK"],
    5: COLORS["ORANGE"],
    6: COLORS["RED"],
    7: COLORS["GREEN"]
}


class GameUI:

    # Local Variables
    WINDOW_SCALE: float
    WINDOW_HEIGHT: int
    WINDOW_WIDTH: int
    surface: pygame.Surface

    controller: Controller

    BACKGROUND_COLOR: Tuple[int, int, int]
    GRID_CELL_COLOR: Tuple[int, int, int]
    GRID_BORDER_COLOR: Tuple[int, int, int]

    GRID_SCALE: float
    CELL_SIZE: int
    CELL_WIDTH: int
    CELL_HEIGHT: int
    GRID_WIDTH: int
    GRID_HEIGHT: int
    X_OFFSET: int
    Y_OFFSET: int

    TICK_INTERVAL: int

    def __init__(self):
        pygame.init()
        self.WINDOW_SCALE = 0.75
        self.WINDOW_HEIGHT = int(pygame.display.Info().current_h * self.WINDOW_SCALE)
        self.WINDOW_WIDTH = int(pygame.display.Info().current_w * self.WINDOW_SCALE)
        self.surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        self.controller = Controller()

        self.BACKGROUND_COLOR = COLORS["WHITE"]
        self.GRID_CELL_COLOR = COLORS["WHITE"]
        self.GRID_BORDER_COLOR = COLORS["BLACK"]

        self.GRID_SCALE = 0.9
        self.CELL_SIZE = min(
            (self.WINDOW_WIDTH * self.GRID_SCALE) // self.controller.game_board.num_cols,
            (self.WINDOW_HEIGHT * self.GRID_SCALE) // self.controller.game_board.num_rows
        )
        self.CELL_WIDTH = self.CELL_HEIGHT = self.CELL_SIZE
        self.GRID_WIDTH = self.controller.game_board.num_cols * self.CELL_WIDTH
        self.GRID_HEIGHT = self.controller.game_board.num_rows * self.CELL_HEIGHT
        self.X_OFFSET = (self.WINDOW_WIDTH - self.GRID_WIDTH) // 2
        self.Y_OFFSET = (self.WINDOW_HEIGHT - self.GRID_HEIGHT) // 2

        self.TICK_INTERVAL = 500  # e.g., 500ms = half a second

    def draw_grid(self) -> None:
        for row in range(self.controller.game_board.num_rows):
            for col in range(self.controller.game_board.num_cols):
                x = col * self.CELL_WIDTH + self.X_OFFSET
                y = row * self.CELL_HEIGHT + self.Y_OFFSET
                square = pygame.Rect(x, y, self.CELL_WIDTH, self.CELL_HEIGHT)
                cell_color = COLORS_MAPPING[self.controller.game_board.grid[row][col]] \
                    if self.controller.game_board.grid[row][col] else self.GRID_CELL_COLOR
                pygame.draw.rect(self.surface, cell_color, square)
                pygame.draw.rect(self.surface, self.GRID_BORDER_COLOR, square, 1)
        
    def run(self) -> None:
        """
        Starts the actual game
        - Determines the time interval for each tick
        - Executes each tick
        - Listens for user controls
        - Executes user controls
        """
        # Set up a userevent to occur every tick_interval ms
        pygame.time.set_timer(pygame.USEREVENT, self.TICK_INTERVAL)
        running = True
        while running:
            self.surface.fill(self.BACKGROUND_COLOR)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.controller.move("left")
                    elif event.key == pygame.K_RIGHT:
                        self.controller.move("right")
                    elif event.key == pygame.K_DOWN:
                        self.controller.move("down")
                    elif event.key == pygame.K_UP:
                        self.controller.rotate()
                elif event.type == pygame.USEREVENT:
                    self.controller.tick()

            self.draw_grid()
            pygame.display.update()
