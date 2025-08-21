from typing import Dict, List, Tuple
import pygame 
from src.controller import Controller
from src.shape import Shape
import copy 

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

    def __init__(self, window_scale: float = 0.9, difficulty = 1): 
        """
        Initializes the game UI and Pygame display.

        Args:
        - tick_interval (int): Milliseconds per game tick (this is like the difficulty of the game)
        - scale (float): Window scaling factor based on current display size
        """

        pygame.init()


       # ===============================
        # Initial Game Difficulty
        # ===============================
        self.starting_level = difficulty
        self.initial_level_speed = 500

        # ===============================
        # Game Controller
        # ===============================
        self.controller: Controller = Controller(initial_level=self.starting_level)
        self.tick_interval = self.initial_level_speed
        self.update_tick_interval()

        # ===============================
        # Custom Padding
        # ===============================
        self.grid_padding_left = 10
        self.queue_padding_left = 10
        self.queue_padding_bottom = 0

        # ===============================
        # Display and Surface Setup
        # ===============================
        self.display_info = pygame.display.Info()
        screen_w = self.display_info.current_w
        screen_h = self.display_info.current_h

        # Height = as tall as possible (scaled)
        self.window_height = int(screen_h * window_scale)

        # Width = exactly half of height
        self.window_width = int(self.window_height * 0.7)

        # Ensure it fits in screen width
        if self.window_width > screen_w:
            self.window_width = screen_w
            self.window_height = self.window_width * 2

        self.surface = pygame.display.set_mode((self.window_width, self.window_height))

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
        self.grid_left_x: int = self.grid_padding_left
        self.grid_top_y: int = (self.window_height - self.grid_height) // 2  

        self.previous_level = self.controller.level

    # ===============================
    # Changing Level Methods
    # ===============================

    def update_tick_interval(self) -> None:
        """
        Update tick interval based on controller's level.
        - Each level will increase the speed of the tick interval by 10%, with max speed of 50ms
        """
        self.tick_interval = max(50, int(self.initial_level_speed * (0.9 ** (self.controller.level - 1))))
        TICK_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(TICK_EVENT, self.tick_interval)

    # ===============================
    # Rendering Methods
    # ===============================
    def draw_grid(self) -> None:
        """
        Draws the Tetris board grid and the shapes currently placed.
        """

        pygame.draw.circle(self.surface, COLORS["RED"], (self.grid_left_x, self.grid_top_y), 10)

        for row in range(self.controller.game_board.num_rows):
            for col in range(self.controller.game_board.num_cols):

                x = col * self.cell_width + self.grid_left_x
                y = row * self.cell_height + self.grid_top_y
                square = pygame.Rect(x, y, self.cell_width, self.cell_height)
                square = pygame.Rect(x, y, self.cell_width, self.cell_height)
                cell_color = COLORS_MAPPING[self.controller.game_board.grid[row][col]] \
                    if self.controller.game_board.grid[row][col] else self.grid_cell_color
                pygame.draw.rect(self.surface, cell_color, square)
                pygame.draw.rect(self.surface, self.grid_border_color, square, 1)

        outer_rect = pygame.Rect(
            self.grid_left_x - 1,  # move 1 pixel left
            self.grid_top_y - 1,  # move 1 pixel up
            self.controller.game_board.num_cols * self.cell_width + 2,  # extend width by 2 pixels
            self.controller.game_board.num_rows * self.cell_height + 2   # extend height by 2 pixels
        )
        pygame.draw.rect(self.surface, self.grid_border_color, outer_rect, 2)

    def draw_score(self) -> None:
        """
        Draws the score, level, and lines cleared info to the right of the board.
        """
        # First line: POINTS label
        label_surface = self.mainfont.render("POINTS", True, COLORS["BLACK"])
        label_rect = label_surface.get_rect()
        label_rect.left = self.grid_left_x + self.grid_width + self.queue_padding_left
        label_rect.top = self.grid_top_y

        # Second line: points value
        value_surface = self.mainfont.render(str(self.controller.points), True, COLORS["BLACK"])
        value_rect = value_surface.get_rect()
        value_rect.left = label_rect.left
        value_rect.top = label_rect.bottom + 5  # 5px spacing under POINTS label

        # Third line: LEVEL label
        level_label_surface = self.mainfont.render("LEVEL", True, COLORS["BLACK"])
        level_label_rect = level_label_surface.get_rect()
        level_label_rect.left = label_rect.left
        level_label_rect.top = value_rect.bottom + 20  # 20px spacing under points value

        # Fourth line: LEVEL value (currently 0)
        level_value_surface = self.mainfont.render(str(self.controller.level), True, COLORS["BLACK"])
        level_value_rect = level_value_surface.get_rect()
        level_value_rect.left = level_label_rect.left
        level_value_rect.top = level_label_rect.bottom + 5  # 5px spacing under LEVEL label

        # Fifth line: LINES CLEARED label
        lines_label_surface = self.mainfont.render("LINES", True, COLORS["BLACK"])
        lines_label_rect = lines_label_surface.get_rect()
        lines_label_rect.left = level_label_rect.left
        lines_label_rect.top = level_value_rect.bottom + 20  # 20px spacing under level value

        # Sixth line: LINES CLEARED value (currently 0)
        lines_value_surface = self.mainfont.render(str(self.controller.total_rows_cleared), True, COLORS["BLACK"])
        lines_value_rect = lines_value_surface.get_rect()
        lines_value_rect.left = lines_label_rect.left
        lines_value_rect.top = lines_label_rect.bottom + 5  # 5px spacing under LINES label

        # Draw all
        self.surface.blit(label_surface, label_rect)           # POINTS label
        self.surface.blit(value_surface, value_rect)           # POINTS value
        self.surface.blit(level_label_surface, level_label_rect)  # LEVEL label
        self.surface.blit(level_value_surface, level_value_rect)  # LEVEL value
        self.surface.blit(lines_label_surface, lines_label_rect)  # LINES label
        self.surface.blit(lines_value_surface, lines_value_rect)  # LINES value

    def draw_shape(self, shape: Shape, top_left_x: int, top_left_y: int, cell_size: int) -> None:
        """
        Draws a single shape at a given position

        Args:
        - Shape: the shape that will be drawn
        - int: top left x position in the window
        - int: top left y position in the window
        """
        # first, strip any rows from the matrix that are all zero
        shape_matrix = copy.deepcopy(shape.matrix)
        shape_matrix = [row for row in shape_matrix if any(cell != 0 for cell in row)]
        for r, row in enumerate(shape_matrix):
            for c, val in enumerate(row):
                if val != 0:
                    rect = pygame.Rect(top_left_x + c * cell_size,top_left_y + r * cell_size,cell_size,cell_size)
                    pygame.draw.rect(self.surface, COLORS_MAPPING[val], rect)
                    pygame.draw.rect(self.surface, COLORS["BLACK"], rect, 1)

    def draw_shape_queue(self) -> None:
        """
        Draws the next three shapes to the right of the Tetris board,
        centered horizontally in the queue area, with a border.
        """
        
        # Queue dimensions
        queue_width = 5 * self.cell_size
        queue_height = 10 * self.cell_size

        # Queue position
        queue_x_left = self.grid_left_x + self.grid_width + self.queue_padding_left                                  
        queue_y_top = self.grid_top_y + self.grid_height - queue_height - self.queue_padding_bottom    
        queue_y_bottom = self.grid_top_y + self.grid_height - self.queue_padding_bottom         

        # Draw queue border 
        border_rect = pygame.Rect(queue_x_left, queue_y_top, queue_width, queue_height)
        pygame.draw.rect(self.surface, COLORS["BLACK"], border_rect, 2)

        # calculate the available space for each piece inside the queue
        space_per_piece = (queue_y_bottom - queue_y_top) / len(self.controller.shape_queue)

        # draw each shape inside the queue
        for i, shape in enumerate(reversed(self.controller.shape_queue)):

            shape_num_rows = len(shape.matrix)   
            shape_num_nonzero_rows = sum(1 for row in shape.matrix if any(val != 0 for val in row))  

            shapearea_x_left = queue_x_left + (queue_width - shape_num_rows * self.cell_size) // 2 
            shapearea_y_top = queue_y_bottom-(space_per_piece*(i+1)) 
            shapearea_y_bottom = queue_y_bottom-(space_per_piece*(i))  
            shapearea_y_middle = shapearea_y_bottom - ((shapearea_y_bottom - shapearea_y_top)/2)

            if shape_num_nonzero_rows == 1: shape_y_top = shapearea_y_middle - self.cell_size/2  
            else: shape_y_top = shapearea_y_middle - self.cell_size   

            self.draw_shape(shape, shapearea_x_left, shape_y_top, self.cell_size)

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
                    self.update_tick_interval()

                    if self.controller.level > self.previous_level:
                        print(f"Level up! Now Level {self.controller.level}")
                        self.previous_level = self.controller.level

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