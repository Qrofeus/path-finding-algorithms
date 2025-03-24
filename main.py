import pygame
from algorithm.a_star import AStar
from ui import make_grid, get_mouse_pos, PygameWindow


def main(window, algorithm):
    grid = make_grid()

    start_position = None
    end_position = None

    running = True

    while running:
        window.update(grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if pygame.mouse.get_pressed()[0]:
                # LEFT CLICK
                row, col = get_mouse_pos()
                block = grid[row][col]

                if not start_position and block != end_position:
                    block.set_start()
                    start_position = block
                    continue

                if not end_position and block != start_position:
                    block.set_end()
                    end_position = block
                    continue

                if block != start_position and block != end_position:
                    block.set_barrier()

            elif pygame.mouse.get_pressed()[2]:
                # RIGHT CLICK
                row, col = get_mouse_pos()

                block = grid[row][col]
                if block.is_start():
                    start_position = None
                if block.is_end():
                    end_position = None
                block.reset()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_position and end_position:
                    for row in grid:
                        for block in row:
                            block.update_neighbors(grid)

                    algorithm.run(grid, start_position, end_position, lambda: window.update(grid))

                if event.key == pygame.K_c:
                    start_position = None
                    end_position = None
                    grid = make_grid()

    pygame.quit()


if __name__ == '__main__':
    pygame_window = PygameWindow()
    a_star_algorithm = AStar()
    main(pygame_window, a_star_algorithm)
