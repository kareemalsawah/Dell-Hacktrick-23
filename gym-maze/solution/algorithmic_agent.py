"""
Implementation of an algorithmic agent for the maze problem
"""
from typing import Tuple

from .item_locator import ItemLocator
from .item_selector import ItemSelector
from .graph_manager import GraphManager
from .mind_visualizer import MindVisualizer


class AlgorithmicAgent:
    """
    Class to implement an algorithmic agent for the maze problem

    Parameters
    ----------
    maze_size: Tuple[int, int]
        The size of the maze
    visualize: bool
        Whether to visualize the agent's mind
    """

    def __init__(self, maze_size: Tuple[int, int] = (10, 10), visualize: bool = True):
        self.graph = GraphManager(maze_size)
        self.visualize = visualize
        self.item_selector = ItemSelector()
        self.item_locator = ItemLocator(maze_size)
        if self.visualize:
            self.visualizer = MindVisualizer()

        self.count = 0
        self.curr_pos = (0, 0)
        self.closest_goal = None
        self.expected_next_pos = None
        self.planned_path = None
        self.prev_possible_locations = None
        self.actions = ["N", "S", "E", "W"]

    def get_action(self, state: list) -> Tuple[str, int]:
        """
        Get the action to take from the current state

        Parameters
        ----------
        state : list
            The current state of the environment

        Returns
        -------
        Tuple[str, int]
            The action to take (as a string and index)
        """
        self.count += 1
        new_pos = tuple(x for x in state[0])

        finished = True
        for item in self.item_locator.item_possible_locations:
            if len(list(item)) > 0:
                finished = False
                break
        if finished and new_pos == (9, 9):
            return "E", -1

        # Update the graph (representing the maze) according to the new position
        replan = True
        if self.expected_next_pos is not None:
            if self.expected_next_pos != new_pos:  # Agent didn't move, draw a wall
                self.graph.remove_edge_from_graph(self.curr_pos, self.expected_next_pos)
            else:
                self.graph.confirm_edge(self.curr_pos, self.expected_next_pos)
                replan = False
        self.curr_pos = new_pos

        # Update estimates of items, and get a path to follow
        self.item_locator.update_estimates(self.curr_pos, state[1], state[2])
        if (
            not replan
            and self.prev_possible_locations
            != self.item_locator.item_possible_locations
        ):
            self.prev_possible_locations = self.item_locator.item_possible_locations
            replan = True

        if replan:
            self.planned_path = self.item_selector.get_plan(
                self.curr_pos, self.item_locator.item_possible_locations, self.graph
            )
        else:
            self.planned_path = self.planned_path[1:]

        # Visualize the agent's mind
        if self.visualize:
            self.visualizer.draw(
                self.curr_pos,
                self.planned_path,
                self.item_locator.item_possible_locations,
                self.graph,
            )

        # Determine the action to take
        if len(self.planned_path) < 2:
            return "E", -1
        self.expected_next_pos = self.planned_path[1]
        action = self.get_action_from_pos(new_pos, self.expected_next_pos)
        return action, self.actions.index(action)

    def get_action_from_pos(
        self, curr_pos: Tuple[int, int], next_pos: Tuple[int, int]
    ) -> str:
        """
        Determine the action [N, S, E, W] from the current position and the next position

        Parameters
        ----------
        curr_pos : Tuple[int, int]
            Current position to move from
        next_pos : Tuple[int, int]
            Next position to move to

        Returns
        -------
        str
            The action to take [N, S, E, W]
        """
        if next_pos[1] < curr_pos[1]:
            return "N"
        if next_pos[1] > curr_pos[1]:
            return "S"
        if next_pos[0] < curr_pos[0]:
            return "W"
        return "E"
