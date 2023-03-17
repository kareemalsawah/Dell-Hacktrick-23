"""
Class to visualize the mind of the agent
"""
from typing import List, Tuple, Set

import pygame

from .graph_manager import GraphManager


class MindVisualizer:
    """
    Class to visualize the mind of the agent

    Parameters
    ----------
    width: int
        The width of the window
    height: int
        The height of the window
    maze_size: Tuple[int, int]
        The size of the maze
    """

    def __init__(
        self, width: int = 400, height: int = 400, maze_size: Tuple[int, int] = (10, 10)
    ):
        self.window_width = width
        self.window_height = height
        self.maze_size = maze_size

        # Initialize pygame screen
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()
        self.screen.fill((255, 255, 255))

    def fill_closed_grid(self, block_size: Tuple[int, int]) -> None:
        """
        Fill the screen with a grid where all cells are closed

        Parameters
        ----------
        block_size : Tuple[int, int]
            The size of a cell in the grid
        """
        self.screen.fill((255, 255, 255))
        for grid_x in range(self.maze_size[0]):
            for grid_y in range(self.maze_size[1]):
                rect = pygame.Rect(
                    grid_x * block_size[0],
                    grid_y * block_size[1],
                    block_size[0],
                    block_size[1],
                )
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

    def add_neighboring_cells(
        self,
        from_cell: Tuple[int, int],
        to_cell: Tuple[int, int],
        block_size: Tuple[int, int],
    ) -> None:
        """
        Add the neighboring cells to the graph. This deletes the edge between the two cells

        Parameters
        ----------
        from_cell : Tuple[int, int]
            The cell from which the edge is added
        to_cell : Tuple[int, int]
            The cell to which the edge is added
        block_size : Tuple[int, int]
            The size of a cell in the grid
        """
        if from_cell[0] > to_cell[0]:
            rect = pygame.Rect(
                1 + from_cell[0] * block_size[0] - (block_size[0] - 2),
                1 + from_cell[1] * block_size[1],
                (block_size[0] - 2),
                (block_size[1] - 2),
            )
        elif from_cell[0] < to_cell[0]:
            rect = pygame.Rect(
                1 + from_cell[0] * block_size[0],
                1 + from_cell[1] * block_size[1],
                2 * (block_size[0] - 2),
                (block_size[1] - 2),
            )
        elif from_cell[1] > to_cell[1]:
            rect = pygame.Rect(
                1 + from_cell[0] * block_size[0],
                1 + from_cell[1] * block_size[1] - (block_size[1] - 2),
                (block_size[0] - 2),
                (block_size[1] - 2),
            )
        else:
            rect = pygame.Rect(
                1 + from_cell[0] * block_size[0],
                1 + from_cell[1] * block_size[1],
                (block_size[0] - 2),
                2 * (block_size[1] - 2),
            )

        pygame.draw.rect(self.screen, (255, 255, 255), rect, 0)

    def draw_square(
        self,
        pos: Tuple[int, int],
        block_size: Tuple[int, int],
        color: Tuple[int, int, int],
    ) -> None:
        """
        Draw a square at the given position

        Parameters
        ----------
        pos : Tuple[int, int]
            The position of the square
        block_size: Tuple[int, int]
            The size of a cell in the grid
        color: Tuple[int, int, int]
            The color of the square
        """
        rect = pygame.Rect(
            pos[0] * block_size[0] + 1,
            pos[1] * block_size[1] + 1,
            block_size[0] - 2,
            block_size[1] - 2,
        )
        pygame.draw.rect(self.screen, color, rect, 0)

    def draw_path(
        self, planned_path: List[Tuple[int, int]], block_size: Tuple[int, int]
    ) -> None:
        """
        Draw the current planned path

        Parameters
        ----------
        planned_path : List[Tuple[int, int]]
            The current planned path
        block_size : Tuple[int, int]
            The size of a cell in the grid
        """

        def pos_to_pixel(x, y):
            x = x * block_size[0] + block_size[0] // 2
            y = y * block_size[1] + block_size[1] // 2
            return x, y

        for i in range(len(planned_path) - 1):
            pygame.draw.line(
                self.screen,
                (0, 0, 255),
                pos_to_pixel(*planned_path[i]),
                pos_to_pixel(*planned_path[i + 1]),
                2,
            )

    def draw(
        self,
        current_pos: Tuple[int, int],
        planned_path: List[Tuple[int, int]],
        goal_possible_locations: List[Set[Tuple[int, int]]],
        graph: GraphManager,
    ) -> None:
        """
        Draw the current maze in the mind of the agent
        The current planned path and the estimated position of the closest goal

        Parameters
        ----------
        current_pos: Tuple[int, int]
            The current position of the agent
        planned_path : List[Tuple[int, int]]
            The current planned path
        goal_possible_locations: List[Set[Tuple[int, int]]]
            For each goal, the set of possible locations consistent with the observations
        graph: GraphManager
            The graph representing the maze
        """
        pygame.event.get()
        block_size = (
            self.window_width // self.maze_size[0],
            self.window_height // self.maze_size[1],
        )
        self.fill_closed_grid(block_size)

        for from_cell in graph.graph.keys():
            for to_cell in graph.graph[from_cell]:
                self.add_neighboring_cells(from_cell, to_cell, block_size)

        # self.draw_square(closest_goal, block_size, (255, 0, 0))
        self.draw_square(current_pos, block_size, (0, 255, 0))

        # yellow, purple, red, blue
        colors = [(255, 255, 0), (255, 0, 255), (255, 0, 0), (0, 0, 255)]
        for idx, possible_locations in enumerate(goal_possible_locations):
            goal_color = colors[idx]
            for goal in possible_locations:
                self.draw_square(
                    goal,
                    block_size,
                    (
                        goal_color[0] / len(possible_locations),
                        goal_color[1] / len(possible_locations),
                        goal_color[2] / len(possible_locations),
                    ),
                )
        self.draw_path(planned_path, block_size)
        pygame.display.update()
