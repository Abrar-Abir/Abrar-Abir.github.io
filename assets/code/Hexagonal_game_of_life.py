import pygame
import numpy as np

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
ROWS = int(HEIGHT / (1.5 * CELL_SIZE))
COLS = int(WIDTH / (np.sqrt(3) * CELL_SIZE))
FPS = 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def hex_neighbors(row, col):
    offsets = [(0, -1), (1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0)]
    return [(row + dr, col + dc) for dr, dc in offsets]


def draw_hexagon(surface, center, size):
    points = [
        (center[0] + size * np.cos(np.pi / 3 * i), center[1] + size * np.sin(np.pi / 3 * i))
        for i in range(6)
    ]
    pygame.draw.polygon(surface, WHITE, points, 1)


def draw_grid(surface, grid):
    for row in range(ROWS):
        for col in range(COLS):
            cx = int(col * np.sqrt(3) * CELL_SIZE + CELL_SIZE * (3 / 2) * (row % 2))
            cy = int(row * 1.5 * CELL_SIZE)
            half_w = np.sqrt(3) * CELL_SIZE / 2
            fill_color = WHITE if grid[row, col] == 1 else BLACK
            pygame.draw.polygon(
                surface,
                fill_color,
                [(cx, cy - CELL_SIZE), (cx + half_w, cy - CELL_SIZE / 2), (cx, cy + CELL_SIZE), (cx - half_w, cy - CELL_SIZE / 2)],
                0,
            )
            draw_hexagon(surface, (cx, cy), CELL_SIZE)


def update_grid(grid):
    new_grid = grid.copy()
    for row in range(ROWS):
        for col in range(COLS):
            neighbors = hex_neighbors(row, col)
            live_neighbors = sum(grid[r % ROWS, c % COLS] for r, c in neighbors)
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

    # Random initialization (uncomment and adjust d):
    # d = 0.1
    # grid = np.random.choice([0, 1], size=(ROWS, COLS), p=[1 - d, d])

    # Deterministic initialization (add more cells as needed):
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
