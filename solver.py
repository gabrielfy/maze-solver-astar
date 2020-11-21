import pygame
from math import sqrt, pow
from maze import make_maze, Cell


def has_unvisited(maze, cell):
    neighbors = []
    number_of_cells = len(maze)

    # top
    if cell.y - 1 >= 0 and not maze[cell.y - 1][cell.x].visited:
        top = maze[cell.y - 1][cell.x]
        if not top.borders[2]:
            neighbors.append(top)
    # left
    if cell.x - 1 >= 0 and not maze[cell.y][cell.x - 1].visited:
        left = maze[cell.y][cell.x - 1]
        if not left.borders[1]:
            neighbors.append(left)
    # bottom
    if cell.y + 1 < number_of_cells and not maze[cell.y + 1][cell.x].visited:
        bottom = maze[cell.y + 1][cell.x]
        if not bottom.borders[0]:
            neighbors.append(bottom)
    # right
    if cell.x + 1 < number_of_cells and not maze[cell.y][cell.x + 1].visited:
        right = maze[cell.y][cell.x + 1]
        if not right.borders[3]:
            neighbors.append(right)

    return neighbors


def sorted_neighbors(neighbors, goal):
    return sorted(neighbors, key=lambda neighbor: sqrt(pow(
        neighbor.x - goal.x, 2) + pow(neighbor.y - goal.y, 2)))


if __name__ == '__main__':
    # Define window
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Maze solver')
    clock = pygame.time.Clock()

    maze = make_maze(screen, 20)

    stack = []

    goal = maze[-1][-1]
    goal.color = (255, 0, 0)
    start = maze[0][0]
    start.visited = True
    stack.append(start)

    found = False
    running = True
    while running:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Close window
                running = False

        # Set background color to black
        screen.fill((0, 0, 0))

        # Draw cells
        for i in maze:
            for cell in i:
                cell.draw()

        if not found:
            if len(stack) > 0:
                current = stack.pop()
                current.highlight()

                if current != goal:
                    neighbors = sorted_neighbors(
                        has_unvisited(maze, current), goal)

                    if len(neighbors) > 0:
                        neighbor = neighbors[0]
                        neighbor.visited = True
                        stack.append(current)
                        stack.append(neighbor)
                else:
                    stack.append(current)
                    found = True
                    for cell in stack:
                        cell.color = (0, 255, 0)

        # Update window
        pygame.display.update()

        clock.tick(30)

    pygame.quit()
