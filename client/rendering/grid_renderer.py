import pygame

from client.config import GRID_CELL_SIZE, GRID_COLOR

def render_grid(screen):
    for x in range(0, screen.get_width(), GRID_CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, screen.get_height()))

    for y in range(0, screen.get_height(), GRID_CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (screen.get_width(), y))
