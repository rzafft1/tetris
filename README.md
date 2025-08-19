# Tetris

Author: Ryan Zafft

Below is a simple rundown of the modular hierarchal structure of our Tetris project.

### 1. App (app.py)

Instantiates the GameUI class and starts the game loop by calling run(). It’s the entry point of the application.

To run the game, simply run 'python app.py'

### 2. GameUI (src/game_ui.py)

Handles the graphical interface using Pygame. Draws the grid, manages user input, and updates the display. It uses the Controller class to manipulate the game state.

* Libraries: Pygame, src.controller.Controller
* Records: COLORS (Dict[str, Tuple[int, int, int]]), COLORS_MAPPING (Dict[int, Tuple[int, int, int]])
* Defines Class: GameUI
    * init(void)
    * void draw_grid(void)
    * void run(void)
* Uses/Imports Class: Controller 

### 3. Controller (src/controller.py)

Manages the game logic: spawning shapes, moving them, rotating them, and advancing the game state each tick. It communicates with GameBoard and Shape classes to perform actions.

* Libraries: random, copy, typing, src.gameboard.GameBoard, src.shape.Shape
* Defines Record: SHAPES (Dict[str, Matrix])
* Defines Class: Controller
    * init(void)
    * void spawn_new_shape(void)
    * bool move(Literal['left', 'right', 'down'])
    * bool rotate(void)
* Uses/Imports Class: GameBoard, Shape

### 4. GameBoard (src/gameboard.py)

Represents the Tetris board, handles placing and removing shapes, checking collisions, and clearing full rows. It ensures the shapes interact correctly with the board grid.

* Libraries: typing, src.shape.Shape
* Defines Class: GameBoard
    * init(int, int)
    * void show(void)
    * bool can_place(Shape, int, int)
    * void place_shape(Shape)
    * void remove_shape(Shape)
    * int clear_rows(void)
* Uses/Imports Class: Shape

### 5. Shape (src/shape.py)

Represents individual Tetris pieces, storing their matrix, position, rotation state, and key/color. Handles rotation of the piece and can display itself in the terminal.

* Libraries: typing, src.shape.Shape
* Defines Class: Shape
    * init(Matrix)
    * void show(void)
    * Matrix rotate(void)
* Uses/Imports Class: Shape