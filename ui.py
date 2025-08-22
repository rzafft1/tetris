import pygame

# CONSTANTS
GAMEBOARD_NUM_ROWS = 20
GAMEBOARD_NUM_COLS = 10
window_scale = 1 # window height relative to screen height
grid_scale = 1 # grid height relative to window height
grid_padding_left = 0

# CODE
pygame.init()
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
print(f"screen width : {screen_width}")
print(f"screen height : {screen_height}")

window_height = screen_height * window_scale

"""
Calculate the dimensions for the grid
- We want the largest gameboard possible that will fit in the window
"""
cell_size = min(
    (screen_width * window_scale * grid_scale) / GAMEBOARD_NUM_ROWS, 
    (screen_height * window_scale * grid_scale) / GAMEBOARD_NUM_COLS,
)
print(f"cell size : {cell_size}")
grid_width = GAMEBOARD_NUM_COLS * cell_size
grid_height = GAMEBOARD_NUM_COLS * cell_size
grid_x_start = grid_padding_left
grid_y_start = (window_height - grid_height)/2

window_width = screen_width * window_scale
surface = pygame.display.set_mode((window_width, window_height))


pygame.display.set_caption("Full Screen Pygame Window")






# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False
    surface.fill((50, 150, 200))  

    grid_border = pygame.Rect(grid_x_start, grid_y_start, grid_width, grid_height)
    pygame.draw.rect(surface, (0, 0, 0), grid_border, 2)

    pygame.display.flip()
pygame.quit()