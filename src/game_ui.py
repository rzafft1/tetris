from typing import Dict, List, Tuple
import pygame 
from src.controller import Controller
from src.shape import Shape

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

    def __init__(self, initial_tick_interval: int = 500, scale: float = 0.75): 
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
        # Fonts
        # ===============================
        self.mainfont = pygame.font.SysFont('Arial', 30)

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

    def draw_score(self) -> None:
        """
        Draws the current score above the grid, centered horizontally
        """
        score_text = f"Points: {self.controller.points}"
        text_surface = self.mainfont.render(score_text, True, COLORS["BLACK"])
        text_rect = text_surface.get_rect()
        text_rect.centerx = self.window_width // 2
        self.surface.blit(text_surface, text_rect)

    def draw_shape(self, shape: Shape, top_left_x: int, top_left_y: int, cell_size: int) -> None:
        """
        Draws a single shape at a given position

        Args:
        - Shape: the shape that will be drawn
        - int: top left x position in the window
        - int: top left y position in the window
        """
        for r, row in enumerate(shape.matrix):
            for c, val in enumerate(row):
                if val != 0:
                    rect = pygame.Rect(
                        top_left_x + c * cell_size,
                        top_left_y + r * cell_size,
                        cell_size,
                        cell_size
                    )
                    pygame.draw.rect(self.surface, COLORS_MAPPING[val], rect)
                    pygame.draw.rect(self.surface, COLORS["BLACK"], rect, 1)

    def draw_shape_queue(self) -> None:
        """
        Draws the next three shapes to the right of the Tetris board,
        centered horizontally in the queue area, with a border.
        """
        cell_size = self.cell_width
        num_shapes = len(self.controller.shape_queue)
        padding_top = 15
        padding_bottom = 15

        # Queue area width (max shape width is 4 cells)
        queue_width = 5 * cell_size
        queue_height = int(self.grid_height * 0.8)  # 80% of the board height

        # Align bottom of queue with bottom of the grid
        queue_x = self.x_offset + self.grid_width + 25
        queue_y = self.y_offset + self.grid_height - queue_height

        # Draw border rectangle
        border_rect = pygame.Rect(queue_x - 5, queue_y - 5, queue_width + 10, queue_height + 10)
        pygame.draw.rect(self.surface, COLORS["BLACK"], border_rect, 1)

        # Draw label above the queue
        label_surface = self.mainfont.render("Queue", True, COLORS["BLACK"])
        label_rect = label_surface.get_rect()
        label_rect.centerx = queue_x + queue_width // 2
        label_rect.bottom = queue_y - 5
        self.surface.blit(label_surface, label_rect)

        # Compute vertical spacing inside the queue
        available_height = queue_height - padding_top - padding_bottom
        spacing = (available_height - num_shapes * 4 * cell_size) // (num_shapes - 1)

        # Draw each shape
        for i, shape in enumerate(self.controller.shape_queue):
            shape_height = len(shape.matrix)
            shape_width = len(shape.matrix[0])

            # Horizontal centering
            shape_x = queue_x + (queue_width - shape_width * cell_size) // 2
            # Vertical positioning with top padding + spacing
            shape_y = queue_y + padding_top + i * (4 * cell_size + spacing)

            self.draw_shape(shape, shape_x, shape_y, cell_size)

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
            self.draw_score()
            self.draw_shape_queue()
            pygame.display.update()
            clock.tick(60)