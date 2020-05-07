from random import choice
from math import ceil
import pygame


class Cell(object):
    border_size = 3

    def __init__(self, screen, size, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self._visited = False
        self.screen = screen
        self.size = size
        self.borders = [True, True, True, True]  # top, right, bottom, left
        self.color = None

    def draw(self):
        if self.visited:
            self._fill((0, 0, 255) if self.color is None else self.color)

        if self._visited:
            x, y = self.x * self.size, self.y * self.size
            # top
            if self.borders[0]:
                self._border((x, y), (x + self.size, y))
            # right
            if self.borders[1]:
                self._border((x + self.size, y),
                             (x + self.size, y + self.size))
            # bottom
            if self.borders[2]:
                self._border((x, y + self.size),
                             (x + self.size, y + self.size))
            # left
            if self.borders[3]:
                self._border((x, y), (x, y + self.size))

    def highlight(self):
        self._fill((0, 255, 0))

    def remove_wall(self, b):
        x = self.x - b.x
        if x == 1:
            self.borders[3] = False
            b.borders[1] = False
        elif x == -1:
            self.borders[1] = False
            b.borders[3] = False

        y = self.y - b.y
        if y == 1:
            self.borders[0] = False
            b.borders[2] = False
        elif y == -1:
            self.borders[2] = False
            b.borders[0] = False

    def _border(self, start_pos, end_pos):
        pygame.draw.line(self.screen, (255, 255, 255), start_pos,
                         end_pos, Cell.border_size)

    def _fill(self, color):
        pygame.draw.rect(self.screen, color, pygame.Rect(
            self.x * self.size, self.y * self.size, self.size + self.border_size, self.size + self.border_size))


def has_unvisited_neighbors(maze, cell):
    neighbors = []
    number_of_cells = len(maze)
    # top
    if cell.y - 1 >= 0 and not maze[cell.y - 1][cell.x]._visited:
        neighbors.append(maze[cell.y - 1][cell.x])
    # left
    if cell.x - 1 >= 0 and not maze[cell.y][cell.x - 1]._visited:
        neighbors.append(maze[cell.y][cell.x - 1])
    # bottom
    if cell.y + 1 < number_of_cells and not maze[cell.y + 1][cell.x]._visited:
        neighbors.append(maze[cell.y + 1][cell.x])
    # right
    if cell.x + 1 < number_of_cells and not maze[cell.y][cell.x + 1]._visited:
        neighbors.append(maze[cell.y][cell.x + 1])

    return neighbors


def make_matrix(screen, cell_size):
    # Create matrix of cells
    screen_w = screen.get_width()

    number_of_cells = ceil(screen_w / cell_size)
    maze = []
    for i in range(number_of_cells):
        maze.append([])
        for j in range(number_of_cells):
            maze[i].append(
                Cell(screen, cell_size - ((cell_size + Cell.border_size) / screen_w), j, i))

    return maze


def make_maze(screen, cell_size):
    stack = []
    maze = make_matrix(screen, cell_size)
    current = maze[0][0]
    current._visited = True
    stack.append(current)

    while len(stack) > 0:
        current = stack.pop()
        neighbours = has_unvisited_neighbors(maze, current)
        if len(neighbours) > 0:
            neighbour = choice(neighbours)
            neighbour._visited = True
            current.remove_wall(neighbour)
            stack.append(current)
            stack.append(neighbour)

    return maze
