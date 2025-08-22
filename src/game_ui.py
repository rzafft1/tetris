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
        # Determine height and width of the user's screen
        # ===============================
        self.display_info = pygame.display.Info()
        screen_w = self.display_info.current_w
        screen_h = self.display_info.current_h

        # ===============================
        # Initialize the Game Window 'Surface'
        # ===============================

        # the game window's height in proportion to the screen height
        self.window_scale = window_scale 
        self.window_height = int(screen_h * self.window_scale)

        # the grid's height in proportion to the game window's height
        self.grid_scale: float = 1 

        # the cell size based on the scrreen's dimensions
        self.cell_size: int = min(
            (int(screen_w * self.window_scale) * self.grid_scale) // self.controller.game_board.num_cols,
            (int(screen_h * self.window_scale) * self.grid_scale) // self.controller.game_board.num_rows
        )
        self.cell_width: int = self.cell_size
        self.cell_height: int = self.cell_size

        # the game window's width in proprotion to the grid width
        self.window_width = ((self.controller.game_board.num_cols + 5.6) * self.cell_width)
        if self.window_width > screen_w:
            self.window_width = screen_w
            self.window_height = self.window_width * 2
        self.surface = pygame.display.set_mode((self.window_width, self.window_height))

        # ===============================
        # Determine height and width of gameboard based on game window height
        # ===============================
        self.grid_width: int = self.controller.game_board.num_cols * self.cell_width
        self.grid_height: int = self.controller.game_board.num_rows * self.cell_height
        self.grid_left_x: int = self.grid_padding_left
        self.grid_top_y: int = (self.window_height - self.grid_height) // 2  

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

    # ===============================
    # Render UI
    # ===============================
    def draw_ui(self) -> None:

        # ===============================
        # Draw the grid
        # ===============================

        # Fill in all the cells of the grid
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
        
        # Draw the border for the grid
        grid_border = pygame.Rect(self.grid_left_x-1,self.grid_top_y-1,self.grid_width+2,self.grid_height+2)
        pygame.draw.rect(self.surface, self.grid_border_color, grid_border, 2)

        # ===============================
        # Draw the shape queue, hold box, and game score and level
        # ===============================

        boxes_padding_left = 10

        # Height of each box
        queuebox_height = self.grid_height * 0.48
        holdbox_height = self.grid_height * 0.25
        gamebox_height = self.grid_height * 0.25

        # Compute the remaining space (for gaps only)
        total_box_height = queuebox_height + holdbox_height + gamebox_height
        available_space = self.grid_height - total_box_height
        gap = available_space / 2  # Two gaps: between Queue-Hold and Hold-Game

        # X position for all boxes
        box_x_start = self.grid_left_x + self.grid_width + boxes_padding_left
        box_width = 5 * self.cell_size

        # Positions
        queuebox_y_top = self.grid_top_y
        queuebox_y_bottom = queuebox_y_top + queuebox_height
        holdbox_y_top = queuebox_y_bottom + gap
        holdbox_y_bottom = holdbox_y_top + holdbox_height
        gamebox_y_top = holdbox_y_bottom + gap
        gamebox_y_bottom = gamebox_y_top + gamebox_height

        # DRAW THE QUEUE BOX
        queuebox_border = pygame.Rect(box_x_start, queuebox_y_top, box_width, queuebox_height)
        pygame.draw.rect(self.surface, self.grid_border_color, queuebox_border, 2)

        # draw each shape inside the queue
        space_per_piece = (queuebox_y_bottom - queuebox_y_top) / len(self.controller.shape_queue)
        for i, shape in enumerate(reversed(self.controller.shape_queue)):
            shape_num_rows = len(shape.matrix)   
            shape_num_nonzero_rows = sum(1 for row in shape.matrix if any(val != 0 for val in row))  
            shapearea_x_left = box_x_start + (box_width - shape_num_rows * self.cell_size) // 2 
            shapearea_y_top = queuebox_y_bottom-(space_per_piece*(i+1)) 
            shapearea_y_bottom = queuebox_y_bottom-(space_per_piece*(i))  
            shapearea_y_middle = shapearea_y_bottom - ((shapearea_y_bottom - shapearea_y_top)/2)
            if shape_num_nonzero_rows == 1: shape_y_top = shapearea_y_middle - self.cell_size/2  
            else: shape_y_top = shapearea_y_middle - self.cell_size   
            self.draw_shape(shape, shapearea_x_left, shape_y_top, self.cell_size)

        # DRAW THE HOLD BOX
        holdbox_border = pygame.Rect(box_x_start, holdbox_y_top, box_width, holdbox_height)
        pygame.draw.rect(self.surface, self.grid_border_color, holdbox_border, 2)

        # draw the held shape inside the box
        if self.controller.hold_shape is not None:
            shape_matrix = self.controller.hold_shape.matrix
            shape_rows = len(shape_matrix)
            shape_cols = len(shape_matrix[0])

            # Shape size in pixels
            shape_width_px = shape_cols * self.cell_size
            shape_height_px = shape_rows * self.cell_size

            # Center of the hold box
            box_center_x = box_x_start + box_width // 2
            box_center_y = holdbox_y_top + holdbox_height // 2

            # Top-left position for the shape to be centered
            shape_x_left = box_center_x - shape_width_px // 2
            shape_y_top = box_center_y - shape_height_px // 2

            # Optional: draw a vertical line and a point at the vertical center
            pygame.draw.line(self.surface, (255, 0, 0),
                            (box_center_x, holdbox_y_top),
                            (box_center_x, holdbox_y_top + holdbox_height), 2)
            pygame.draw.circle(self.surface, (255, 0, 0), (box_center_x, box_center_y), 5)

            # Draw the shape
            self.draw_shape(self.controller.hold_shape, shape_x_left, shape_y_top, self.cell_size)

        # DRAW THE GAME INFORMATION BOX
        gamebox_border = pygame.Rect(box_x_start, gamebox_y_top, box_width, gamebox_height)
        pygame.draw.rect(self.surface, self.grid_border_color, gamebox_border, 2)

        # ------ Text content ------
        items = [
            ("POINTS", str(self.controller.points)),
            ("LEVEL",  str(self.controller.level)),
            ("LINES",  str(self.controller.total_rows_cleared)),
        ]

        # ------ Layout/padding ------
        pad_left = 10
        pad_top = 10
        pad_right = 10
        pad_bottom = 10

        label_value_gap = 5   # gap between label and its value
        group_gap = 20       # gap between value and next label

        # Render all at base size first
        rendered = []  # list of (label_surface, value_surface)
        max_w = 0
        total_h_text = 0

        for label, value in items:
            lbl = self.mainfont.render(label, True, COLORS["BLACK"])
            val = self.mainfont.render(value, True, COLORS["BLACK"])
            rendered.append((lbl, val))

        # Compute total text height with base gaps
        # h = (lbl1 + lv_gap + val1) + group_gap + (lbl2 + lv_gap + val2) + group_gap + (lbl3 + lv_gap + val3)
        heights = [(lbl.get_height(), val.get_height()) for (lbl, val) in rendered]
        total_h_text = (
            heights[0][0] + label_value_gap + heights[0][1] +
            group_gap +
            heights[1][0] + label_value_gap + heights[1][1] +
            group_gap +
            heights[2][0] + label_value_gap + heights[2][1]
        )

        # Compute widest element
        max_w = max(
            max(lbl.get_width(), val.get_width())
            for (lbl, val) in rendered
        )

        # Available space inside the box
        avail_h = max(1, gamebox_height - pad_top - pad_bottom)
        avail_w = max(1, box_width - pad_left - pad_right)

        # Scale factor to fit height and width
        scale_h = min(1.0, avail_h / total_h_text)
        scale_w = min(1.0, avail_w / max_w)
        scale = min(scale_h, scale_w)

        # Scale surfaces (and gaps) if needed
        if scale < 1.0:
            scaled = []
            for (lbl, val) in rendered:
                # New sizes
                nl_w, nl_h = max(1, int(lbl.get_width() * scale)), max(1, int(lbl.get_height() * scale))
                nv_w, nv_h = max(1, int(val.get_width() * scale)), max(1, int(val.get_height() * scale))
                # Rescale
                lbl_s = pygame.transform.smoothscale(lbl, (nl_w, nl_h))
                val_s = pygame.transform.smoothscale(val, (nv_w, nv_h))
                scaled.append((lbl_s, val_s))
            rendered = scaled
            # Scale gaps too
            label_value_gap = max(1, int(round(label_value_gap * scale)))
            group_gap = max(1, int(round(group_gap * scale)))

        # (Re)compute total height after scaling
        heights = [(lbl.get_height(), val.get_height()) for (lbl, val) in rendered]
        total_h_text = (
            heights[0][0] + label_value_gap + heights[0][1] +
            group_gap +
            heights[1][0] + label_value_gap + heights[1][1] +
            group_gap +
            heights[2][0] + label_value_gap + heights[2][1]
        )

        # Clamp starting y so the block stays inside (safeguard against rounding)
        start_y = gamebox_y_top + pad_top
        if start_y + total_h_text > gamebox_y_top + gamebox_height - pad_bottom:
            start_y = (gamebox_y_top + gamebox_height - pad_bottom) - total_h_text

        x_left = box_x_start + pad_left
        y = start_y

        # Blit: label/value for each group
        for i, (lbl_surf, val_surf) in enumerate(rendered):
            # label
            lbl_rect = lbl_surf.get_rect()
            lbl_rect.topleft = (x_left, y)
            self.surface.blit(lbl_surf, lbl_rect)

            # value under label
            y = lbl_rect.bottom + label_value_gap
            val_rect = val_surf.get_rect()
            val_rect.topleft = (x_left, y)
            self.surface.blit(val_surf, val_rect)

            # add group gap except after last group
            if i < len(rendered) - 1:
                y = val_rect.bottom + group_gap

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
        side_move_delay = 70  # milliseconds between left/right moves
        down_move_delay = 25   # milliseconds between down moves
        last_move_time: Dict[int, int] = {pygame.K_LEFT: 0, pygame.K_RIGHT: 0, pygame.K_DOWN: 0}

        last_move_time: Dict[int, int] = {
            pygame.K_LEFT: 0,
            pygame.K_RIGHT: 0,
            pygame.K_DOWN: 0
        }

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
                    if event.key == pygame.K_SPACE:
                        self.controller.hold_active_shape()
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
                delay = down_move_delay if direction == "down" else side_move_delay
                if keys[key] and current_time - last_move_time[key] > delay:
                    self.controller.move(direction)
                    last_move_time[key] = current_time

            # ===============================
            # Render
            # ===============================
            self.draw_ui()
            # self.draw_score()
            # self.draw_shape_queue()
            pygame.display.update()
            clock.tick(60)