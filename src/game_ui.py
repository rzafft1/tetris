from typing import Dict, List, Tuple
import pygame 
from src.controller import Controller

# Type Aliases
Matrix = List[List[int]]
Color = Tuple[int, int, int]

# ===============================
# Constants and Mappings
# ===============================

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

    """
    Represents the actual user interface (i.e. game window, game board, etc.).
    It manages the design of the game window, draws the game board, handles user
    input, and executes game ticks
    """

    def __init__(self, initial_tick_interval: int = 50, scale: float = 0.75): 
        """
        Initializes the game UI and Pygame display.

        Args:
        - tick_interval (int): Milliseconds per game tick (this is like the difficulty of the game)
        - scale (float): Window scaling factor based on current display size
        """

        pygame.init()

        # ===============================
        # Display and Surface Setup
        # ===============================
        self.display_info: pygame.display.Info = pygame.display.Info()
        self.window_width: int = int(self.display_info.current_w * scale)
        self.window_height: int = int(self.display_info.current_h * scale)
        self.surface: pygame.Surface = pygame.display.set_mode((self.window_width, self.window_height))

        # ===============================
        # Game Controller
        # ===============================
        self.controller: Controller = Controller()

        # ===============================
        # Grid and UI Colors
        # ===============================
        self.background_color: Color = COLORS["WHITE"]
        self.grid_cell_color: Color = COLORS["WHITE"]
        self.grid_border_color: Color = COLORS["BLACK"]

        # ===============================
        # Grid Scaling and Positioning
        # ===============================
        self.grid_scale: float = 0.9
        self.cell_size: int = min(
            (self.window_width * self.grid_scale) // self.controller.game_board.num_cols,
            (self.window_height * self.grid_scale) // self.controller.game_board.num_rows
        )
        self.cell_width: int = self.cell_size
        self.cell_height: int = self.cell_size
        self.grid_width: int = self.controller.game_board.num_cols * self.cell_width
        self.grid_height: int = self.controller.game_board.num_rows * self.cell_height
        self.x_offset: int = (self.window_width - self.grid_width) // 2
        self.y_offset: int = (self.window_height - self.grid_height) // 2


        # ===============================
        # Initial Game Difficulty
        # ===============================
        self.tick_interval: int = initial_tick_interval


    # ===============================
    # Rendering Methods
    # ===============================
    def draw_grid(self) -> None:
        """
        Draws the Tetris board grid and the shapes currently placed.
        """
        for row in range(self.controller.game_board.num_rows):
            for col in range(self.controller.game_board.num_cols):
                x = col * self.cell_width + self.x_offset
                y = row * self.cell_height + self.y_offset
                square = pygame.Rect(x, y, self.cell_width, self.cell_height)
                cell_color = COLORS_MAPPING[self.controller.game_board.grid[row][col]] \
                    if self.controller.game_board.grid[row][col] else self.grid_cell_color
                pygame.draw.rect(self.surface, cell_color, square)
                pygame.draw.rect(self.surface, self.grid_border_color, square, 1)

    # ===============================
    # Event Handling Methods
    # ===============================
    def handle_key_event(self, key: int) -> None:
        """
        Handles keyboard input for moving and rotating the active shape.
        """
        if key == pygame.K_LEFT:
            self.controller.move("left")
        elif key == pygame.K_RIGHT:
            self.controller.move("right")
        elif key == pygame.K_DOWN:
            self.controller.move("down")
        elif key == pygame.K_UP:
            self.controller.rotate()

    # ===============================
    # Game Loop
    # ===============================
    def run(self) -> None:
        """
        Starts the game loop.
        - Processes user input
        - Advances the game via ticks
        - Draws the updated game state
        """
        TICK_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(TICK_EVENT, self.tick_interval)

        running = True
        clock = pygame.time.Clock()
        move_delay = 50  # milliseconds between moves when holding a key
        last_move_time: Dict[int, int] = {pygame.K_LEFT: 0, pygame.K_RIGHT: 0, pygame.K_DOWN: 0}

        while running:
            self.surface.fill(self.background_color)
            current_time = pygame.time.get_ticks()

            # ===============================
            # Event Handling
            # ===============================
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.controller.rotate()
                elif event.type == TICK_EVENT:
                    running = self.controller.tick()

            # ===============================
            # Handle held-down keys
            # ===============================
            keys = pygame.key.get_pressed()
            for key, direction in [(pygame.K_LEFT, "left"), 
                                (pygame.K_RIGHT, "right"), 
                                (pygame.K_DOWN, "down")]:
                if keys[key] and current_time - last_move_time[key] > move_delay:
                    self.controller.move(direction)
                    last_move_time[key] = current_time

            # ===============================
            # Render
            # ===============================
            self.draw_grid()
            pygame.display.update()
            clock.tick(60)