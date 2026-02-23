import pygame
import numpy as np

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
ROWS, COLS = int(HEIGHT / (1.5 * CELL_SIZE)), int(WIDTH / (np.sqrt(3) * CELL_SIZE))
FPS = 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def hex_neighbors(row, col):
    offsets = [(0, -1), (1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0)]
    neighbors = [(row + dr, col + dc) for dr, dc in offsets]
    return neighbors

def draw_hexagon(surface, center, size):
    points = []
    for i in range(6):
        angle = np.pi / 3 * i
        x = center[0] + size * np.cos(angle)
        y = center[1] + size * np.sin(angle)
        points.append((x, y))
    pygame.draw.polygon(surface, WHITE, points, 1)

def draw_grid(surface, grid):
    for row in range(ROWS):
        for col in range(COLS):
            center_x = int(col * np.sqrt(3) * CELL_SIZE + CELL_SIZE * (3/2) * (row % 2))
            center_y = int(row * 1.5 * CELL_SIZE)
            if grid[row, col] == 1:
                draw_hexagon(surface, (center_x, center_y), CELL_SIZE)
                pygame.draw.polygon(surface, WHITE, [(center_x, center_y - CELL_SIZE),
                                                      (center_x + np.sqrt(3) * CELL_SIZE / 2, center_y - CELL_SIZE / 2),
                                                      (center_x, center_y + CELL_SIZE),
                                                      (center_x - np.sqrt(3) * CELL_SIZE / 2, center_y - CELL_SIZE / 2)], 0)
            else:
                draw_hexagon(surface, (center_x, center_y), CELL_SIZE)
                pygame.draw.polygon(surface, BLACK, [(center_x, center_y - CELL_SIZE),
                                                      (center_x + np.sqrt(3) * CELL_SIZE / 2, center_y - CELL_SIZE / 2),
                                                      (center_x, center_y + CELL_SIZE),
                                                      (center_x - np.sqrt(3) * CELL_SIZE / 2, center_y - CELL_SIZE / 2)], 0)




def update_grid(grid):
    new_grid = grid.copy()
    for row in range(ROWS):
        for col in range(COLS):
            neighbors = hex_neighbors(row, col)
            live_neighbors = sum(grid[n[0] % ROWS, n[1] % COLS] for n in neighbors)
            if grid[row, col] == 1:
                if live_neighbors != 1 and live_neighbors != 2:
                    new_grid[row, col] = 0
            else:
                if live_neighbors == 2:
                    new_grid[row, col] = 1
    return new_grid

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Conway's Game of Life - Hexagonal Grid")

	#####################################################################
    ### use random initialization? 
    ### uncomment the following line
    ### try different values of d
    # d = 0.1
    # grid = np.random.choice([0, 1], size=(ROWS, COLS), p=[1 - d, d])
    
	### OR
	### use deterministic inititalization ?
    ### uncomment the following lines
    ### new lines with cells filled can be added
    grid = np.zeros((ROWS, COLS), dtype=int)
    grid[ROWS // 2, COLS // 2] = 1
    grid[ROWS // 2 + 1, COLS // 2 + 1] = 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        draw_grid(screen, grid)
        grid = update_grid(grid)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
