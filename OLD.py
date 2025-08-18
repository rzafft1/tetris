# Importing the library
import pygame
import random

"""
pygame.display.set_mode() : initialize a surface for display. function takes size of display as parameter
pygame.display.flip() : update the content of the entire display surface of the screen
pygame.draw.rect() : draw a rectangle. function takes the surface, color, and pygame rect object as input parameters and draws a rectangle on the surface
"""

def draw_board(surface, board_width, board_height, blkSize):
    surface_width, surface_height = surface.get_size()
    x_offset = int(surface_width/3)
    y_offset = int((surface_height - board_height)/2)
    for x in range(x_offset, x_offset+board_width+1, blkSize):
        pygame.draw.line(surface, (255, 255, 255), (x,y_offset), (x,y_offset+board_height))
    for y in range(y_offset, y_offset+board_height+1, blkSize):
        pygame.draw.line(surface, (255, 255, 255), (x_offset, y), (x_offset+board_width, y)) 
    
    
def create_shape(blk_size, type):

    # draw surface and blocks for l shape
    l_shape_surface = pygame.Surface((blk_size * 2, blk_size * 3), pygame.SRCALPHA)
    l_blocks = [
        pygame.Rect(0, 0, blk_size, blk_size),  # Top-left block
        pygame.Rect(0, blk_size, blk_size, blk_size),  # Top-middle block
        pygame.Rect(0, blk_size * 2, blk_size, blk_size),  # Bottom-middle block
        pygame.Rect(blk_size, blk_size * 2, blk_size, blk_size),  # Bottom-right block
    ]
    l_color = (255,165,0)
    
    # draw surface and blocks for j shape
    j_shape_surface = pygame.Surface((blk_size * 2, blk_size * 3), pygame.SRCALPHA)
    j_blocks = [
        pygame.Rect(blk_size, 0, blk_size, blk_size),  
        pygame.Rect(blk_size, blk_size, blk_size, blk_size),  
        pygame.Rect(blk_size, blk_size * 2, blk_size, blk_size),   
        pygame.Rect(0, blk_size * 2, blk_size, blk_size),   
    ]
    j_color = (255,105,180)
    
    # draw surface and blocks for t shape
    t_shape_surface = pygame.Surface((blk_size * 3, blk_size * 2), pygame.SRCALPHA)
    t_blocks = [
        pygame.Rect(0, 0, blk_size, blk_size),
        pygame.Rect(blk_size, 0, blk_size, blk_size),  
        pygame.Rect(blk_size*2, 0, blk_size, blk_size), 
        pygame.Rect(blk_size, blk_size, blk_size, blk_size), 
    ]
    t_color = (128, 0, 128)
    
    # draw surface and blocks for o shape
    o_shape_surface = pygame.Surface((blk_size * 2, blk_size * 2), pygame.SRCALPHA)
    o_blocks = [
        pygame.Rect(0, 0, blk_size, blk_size), 
        pygame.Rect(blk_size, 0, blk_size, blk_size),   
        pygame.Rect(0, blk_size, blk_size, blk_size),  
        pygame.Rect(blk_size, blk_size, blk_size, blk_size),  
    ]
    o_color = (255, 255, 0)
    
    # draw surface and blocks for i shape
    i_shape_surface = pygame.Surface((blk_size * 1, blk_size * 4), pygame.SRCALPHA)
    i_blocks = [
        pygame.Rect(0, 0, blk_size, blk_size),   
        pygame.Rect(0, blk_size, blk_size, blk_size),  
        pygame.Rect(0, blk_size*2, blk_size, blk_size),  
        pygame.Rect(0, blk_size*3, blk_size, blk_size),  
    ]
    i_color = (0, 0, 255)
    
    # draw surface and blocks for s shape
    s_shape_surface = pygame.Surface((blk_size * 3, blk_size * 2), pygame.SRCALPHA)
    s_blocks = [
        pygame.Rect(0, blk_size, blk_size, blk_size),  
        pygame.Rect(blk_size, blk_size, blk_size, blk_size),   
        pygame.Rect(blk_size, 0, blk_size, blk_size),   
        pygame.Rect(blk_size*2, 0, blk_size, blk_size),   
    ]
    s_color = (255, 0, 0)
    
    # draw surface and blocks for z shape
    z_shape_surface = pygame.Surface((blk_size * 3, blk_size * 2), pygame.SRCALPHA)
    z_blocks = [
        pygame.Rect(0, 0, blk_size, blk_size),   
        pygame.Rect(blk_size, 0, blk_size, blk_size),  
        pygame.Rect(blk_size, blk_size, blk_size, blk_size),  
        pygame.Rect(blk_size * 2, blk_size, blk_size, blk_size), 
    ]
    z_color = (0, 255, 0)
    
    if type == "l":
        blocks = l_blocks
        color = l_color
        shape_surface = l_shape_surface
        
    if type == "j":
        blocks = j_blocks
        color = j_color
        shape_surface = j_shape_surface
      
    if type == "t":
        blocks = t_blocks
        color = t_color
        shape_surface = t_shape_surface
        
    if type == "o":
        blocks = o_blocks
        color = o_color
        shape_surface = o_shape_surface
        
    if type == "i":
        blocks = i_blocks
        color = i_color
        shape_surface = i_shape_surface
        
    if type == "s":
        blocks = s_blocks
        color = s_color
        shape_surface = s_shape_surface
        
    if type == "z":
        blocks = z_blocks
        color = z_color
        shape_surface = z_shape_surface
        
    shape_surface.fill((255, 255, 255)) 
    
    for block in blocks:
        pygame.draw.rect(shape_surface, color, block) # draw filled block  
        pygame.draw.rect(shape_surface, (255, 255, 255), block, 1) # draw outline of block

    return shape_surface
    

def within_bounds(shape, board_start_x, board_start_y, board_width, board_height):
    if shape.x < board_start_x:
        print("A")
        return False
    if shape.x + shape.width > board_start_x + board_width:
        print("B")
        return False
    if shape.y < board_start_y:
        print("C")
        return False
    if shape.y + shape.height > board_start_y + board_height:
        print(f"D .... {shape.y} + {shape.height} > {board_start_y} + {board_height}")
        return False
    return True
    

def rotate_shape(shape_image, shape, initial_angle, angle, sx, sy, game_surface_width, game_surface_height, blk_size):

    if (shape.y <= sy) and angle != initial_angle:
        shape.y += blk_size
        rotated_shape_image = pygame.transform.rotate(shape_image, angle)
        rotated_shape = rotated_shape_image.get_rect(center=shape.center)
        return rotated_shape, rotated_shape_image, True
    
    if (shape.x > sx and shape.x < 440):
        shape.x += blk_size
        rotated_shape_image = pygame.transform.rotate(shape_image, angle)
        rotated_shape = rotated_shape_image.get_rect(center=shape.center)
        return rotated_shape, rotated_shape_image, True
        
    if shape.x == sx and shape.y == sy and shape.width == blk_size:
        shape.x += blk_size
        rotated_shape_image = pygame.transform.rotate(shape_image, angle)
        rotated_shape = rotated_shape_image.get_rect(center=shape.center)
        return rotated_shape, rotated_shape_image, True 
        
    if shape.width == (blk_size*2) and shape.x <= (sx + (blk_size*2)) and angle != initial_angle:
        shape.x += blk_size
        rotated_shape_image = pygame.transform.rotate(shape_image, angle)
        rotated_shape = rotated_shape_image.get_rect(center=shape.center)
        return rotated_shape, rotated_shape_image, True
        
    if (shape.x > 720) and angle != initial_angle:
        shape.x -= (blk_size*2)
        rotated_shape_image = pygame.transform.rotate(shape_image, angle)
        rotated_shape = rotated_shape_image.get_rect(center=shape.center)
        return rotated_shape, rotated_shape_image, True
        
    if (shape.y >= 860 and angle != initial_angle):
        shape.y -= (blk_size*2)
        rotated_shape_image = pygame.transform.rotate(shape_image, angle)
        rotated_shape = rotated_shape_image.get_rect(center=shape.center)
        return rotated_shape, rotated_shape_image, True
        
    if (shape.y >= 820 and angle != initial_angle):
        shape.y -= (blk_size)
        rotated_shape_image = pygame.transform.rotate(shape_image, angle)
        rotated_shape = rotated_shape_image.get_rect(center=shape.center)
        return rotated_shape, rotated_shape_image, True
    
    print(f"failure with angle = {angle}")
    rotated_shape_image = pygame.transform.rotate(shape_image, angle)
    rotated_shape = rotated_shape_image.get_rect(center=shape.center)
    return rotated_shape, rotated_shape_image, False
    
 
def locate_shape(shape, shape_image):
    print(f"top left corner of shape located at ({shape.x}, {shape.y})")
    print(f"shape width is {shape.width}")
    print(f"shape height is {shape.height}")
    
    
    
    
    
    
    
    
    
    
# initialize pygame
pygame.init()

# create black window surface
window_surface_width = 1200
window_surface_height = 1000
surface = pygame.display.set_mode((window_surface_width,window_surface_height))
surface.fill((0, 0, 0))

# create black and white board surface
game_surface_width = 400
game_surface_height = int(game_surface_width * 2)
blk_size = int(game_surface_width / 10)
draw_board(surface, game_surface_width, game_surface_height, blk_size)
pygame.display.flip()

# x and y coordinates for top left corner of the board
sx = int(window_surface_width/3)
sy = int((window_surface_height - game_surface_height)/2)

######################################### NOTES ABOUT GAME UI
"""
Dimensions are as follows...

- Game window width = 1200
- Game window height = 1000

- Board width = 400 (10 blocks wide)
- Board height = 800 (20 blocks tall)
- Grid block width & height = 40 

- Board start x position in window = 400
- Board start y position in window = 100
- Board end x position = 800
- Board end y position = 900
"""
#########################################

# create shape
shapes = ["l", "j", "t", "o", "i", "s", "z"]
random_number = random.randint(0, len(shapes)-1)
current_shape = shapes[random_number]
shape_image = create_shape(blk_size, current_shape)
shape = shape_image.get_rect(topleft=(sx, sy))

# Event loop to keep the window open
angle = 0
running = True
while running:

    # clear surface
    surface.fill((0, 0, 0))
    draw_board(surface, game_surface_width, game_surface_height, blk_size)
    
    # store initial shape position and angle
    initial_x = shape.x
    initial_y = shape.y
    initial_angle = angle
    
    can_move = True

    for event in pygame.event.get():
    
        # quit game 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        
        if event.type == pygame.KEYDOWN:
        
            # ROTATE ACTION (90 degrees clockwise)
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if current_shape != "o":
                    angle = (angle + 90) % 360
                    if angle == 90 or angle == 270:
                        shape.y -= (blk_size/2)
                        shape.x += (blk_size/2)
                    else:
                        shape.y += (blk_size/2)
                        shape.x -= (blk_size/2)

            # MOVE DOWN ACTION
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                shape.y += blk_size

            # MOVE RIGHT ACTION
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                shape.x += blk_size

            # MOVE LEFT ACTION
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                shape.x -= blk_size
   
        print("---location before rotation")
        locate_shape(shape, shape_image)
        print("--------------")
        
        # if there was no rotation, just execute the translation, otherwise, rotate the shape
        if angle == initial_angle and not within_bounds(shape, sx, sy, game_surface_width, game_surface_height):
            print("not within bounds")
            shape.x = initial_x
            shape.y = initial_y
            
        else:
            # try to rotate the shape, if it is not valid, revert to the initial position
            rotated_shape, rotated_shape_image, rotated = rotate_shape(shape_image, shape, initial_angle, angle, sx, sy, game_surface_width, game_surface_height, blk_size)
            rotated = True
            
            if rotated and within_bounds(rotated_shape, sx, sy, game_surface_width, game_surface_height):
            
                # execute rotation  
                surface.blit(rotated_shape_image, rotated_shape.topleft)
                pygame.display.flip()
                shape.width = rotated_shape.width  
                shape.height = rotated_shape.height   
                shape.x = rotated_shape.x   
                shape.y = rotated_shape.y  
                        
            else:
                # cannot rotate, revert to initial position
                angle = initial_angle
                shape.x = initial_x
                shape.y = initial_y

            
# Quitting Pygame
pygame.quit()