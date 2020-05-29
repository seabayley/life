# Import the pygame module

import pygame
import random
import webbrowser

pygame.init()
pygame.display.set_caption("Game of Life")


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Images
background_image = pygame.image.load(r".\images\background.bmp")
stop_button = pygame.image.load(r".\images\stop_button.png")
clear_button = pygame.image.load(r".\images\clear_button.png")
start_button = pygame.image.load(r"D:.\images\run_button.png")
speed_up_button = pygame.image.load(
    r".\images\speed_up_button.png")
speed_down_button = pygame.image.load(
    r".\images\speed_down_button.png")
random_button = pygame.image.load(r".\images\random_button.png")
rules_button = pygame.image.load(r".\images\rules_button.png")

font = pygame.font.Font('freesansbold.ttf', 15)


running = True
sim_running = False
current_speed = 1000
current_generation = 0

# The size in pixels of the display for each cell in the grid.
tile_size = 16
grid_width = 40
grid_height = 30

# Populate a 2d array with False values
life_grid = [[False for x in range(grid_height)] for y in range(grid_width)]

# Set a timer to call userevent+1 every 1000ms. For updating the grid automatically.
pygame.time.set_timer(pygame.USEREVENT+1, 1000)


def render_life():
    for y in range(grid_height):
        for x in range(grid_width):
            current_cell = life_grid[x][y]
            map_x = x * tile_size + 22
            map_y = y * tile_size + 22
            tile = pygame.Surface((tile_size, tile_size))
            tile.fill(BLUE if current_cell == True else WHITE)
            screen.blit(tile, (map_x, map_y))
    pygame.display.flip()


def out_of_range(x, y):
    if x > grid_width - 1 or y > grid_height - 1 or x < 0 or y < 0:
        return True
    else:
        return False


def clear_grid():
    global life_grid
    life_grid = [[False for x in range(grid_height)]
                 for y in range(grid_width)]


def update_grid():
    updates = []
    global current_generation
    current_generation += 1
    for x in range(grid_width):
        for y in range(grid_height):
            count = 0
            if not out_of_range(x-1, y) and life_grid[x-1][y]:
                count += 1
            if not out_of_range(x+1, y) and life_grid[x+1][y]:
                count += 1
            if not out_of_range(x, y-1) and life_grid[x][y-1]:
                count += 1
            if not out_of_range(x, y+1) and life_grid[x][y+1]:
                count += 1
            if not out_of_range(x+1, y+1) and life_grid[x+1][y+1]:
                count += 1
            if not out_of_range(x-1, y+1) and life_grid[x-1][y+1]:
                count += 1
            if not out_of_range(x-1, y-1) and life_grid[x-1][y-1]:
                count += 1
            if not out_of_range(x+1, y-1) and life_grid[x+1][y-1]:
                count += 1

            if count < 2 or count > 3:
                updates.append([x, y, False])

            if count == 3 and life_grid[x][y] == False:
                updates.append([x, y, True])

    for update in updates:
        life_grid[update[0]][update[1]] = update[2]


def info_text(label, value, x, y):
    text = font.render(f"{label}: {value}", True, (0, 0, 0))
    screen.blit(text, (x, y))


def update_on_timer():
    if sim_running:
        update_grid()


def randomize_grid():
    for x in range(grid_width):
        for y in range(grid_height):
            z = random.randint(1, 101)
            life_grid[x][y] = True if z > 50 else False
    current_generation = 0


while running:
    screen.blit(background_image, (0, 0))
    screen.blit(start_button, (690, 22))
    screen.blit(stop_button, (690, 60))
    screen.blit(clear_button, (690, 98))
    screen.blit(speed_up_button, (690, 136))
    screen.blit(speed_down_button, (690, 174))
    screen.blit(random_button, (690, 212))
    screen.blit(rules_button, (690, 250))
    info_text('Current Generation', current_generation, 26, 510)
    info_text('Current Interval', current_speed, 26, 530)

    cursor_position = pygame.mouse.get_pos()
    render_life()

    # Look at every event in the queue

    for event in pygame.event.get():

        if event.type == pygame.USEREVENT+1:
            update_on_timer()

        # Did the user hit a key?

        if event.type == pygame.MOUSEBUTTONDOWN:
            # if the left button is pressed
            if event.button == 1:
                cursor_x, cursor_y = cursor_position
                if cursor_x > 22 and cursor_x < 662 and cursor_y > 22 and cursor_y < 502:
                    grid_x = int((cursor_x-22) / 16)
                    grid_y = int((cursor_y-22) / 16)
                    life_grid[grid_x][grid_y] = not life_grid[grid_x][grid_y]
                elif cursor_x > 690 and cursor_x < 772:
                    if cursor_y > 22 and cursor_y < 55:
                        sim_running = True
                    if cursor_y > 60 and cursor_y < 93:
                        sim_running = False
                    if cursor_y > 98 and cursor_y < 131:
                        clear_grid()
                        sim_running = False
                        current_generation = 0
                    if cursor_y > 136 and cursor_y < 169:
                        current_speed = int(
                            current_speed/2) if current_speed > 1 else 1
                        pygame.time.set_timer(
                            pygame.USEREVENT+1, current_speed)
                    if cursor_y > 174 and cursor_y < 207:
                        current_speed = int(current_speed*2)
                        pygame.time.set_timer(
                            pygame.USEREVENT+1, current_speed)
                    if cursor_y > 212 and cursor_y < 245:
                        randomize_grid()
                    if cursor_y > 250 and cursor_y < 288:
                        webbrowser.open(
                            'https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Rules', new=2)

            if event.button == 3:
                # So we can step through the game using right click
                update_grid()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.QUIT:
            running = False
