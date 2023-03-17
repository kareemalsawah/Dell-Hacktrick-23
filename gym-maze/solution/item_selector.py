"""
Class to choose which item to rescue next
"""
from itertools import permutations
from typing import List, Tuple, Set

from .graph_manager import GraphManager


class ItemSelector:
    """
    Class to choose which item to rescue next

    Parameters
    ----------
    exit_pos: Tuple[int, int]
        The position of the exit
    """

    def __init__(self, exit_pos: Tuple[int, int] = (9, 9)):
        self.exit_pos = exit_pos

    def get_plan(
        self,
        curr_pos: Tuple[int, int],
        item_possible_locs: List[Set[Tuple[int, int]]],
        graph: GraphManager,
    ) -> List[Tuple[int, int]]:
        """
        Select the item to rescue next

        Parameters
        ----------
        curr_pos : Tuple[int, int]
            The current position of the agent
        item_possible_locs : List[Set[Tuple[int, int]]]
            For each item, a set of possible locations consistent with the observations
        graph: GraphManager
            The graph representing the maze

        Returns
        -------
        List[Tuple[int, int]]
            The path to follow to rescue all items and exit the maze
        """
        memory = {}

        # Create a minimized graph containing curr_pos, items, and exit
        positions = [curr_pos]
        for item_locs in item_possible_locs:
            if len(list(item_locs)) > 0:
                all_item_locs = list(item_locs)
                # min_dist = float("inf")
                # min_item_loc = None
                # for item_loc in all_item_locs:
                #     if (curr_pos, item_loc) in memory:
                #         dist = len(memory[(curr_pos, item_loc)]) - 1
                #     else:
                #         memory[(curr_pos, item_loc)] = graph.a_star(curr_pos, item_loc)
                #         dist = len(memory[(curr_pos, item_loc)]) - 1
                #     if dist < min_dist:
                #         min_dist = dist
                #         min_item_loc = item_loc
                # positions.append(min_item_loc)
                positions.append(all_item_locs[0])
        positions.append(self.exit_pos)

        order_items = list(permutations(positions[1:-1]))
        min_cost = float("inf")
        min_solution = None
        for order in order_items:
            order = list(order)
            order.insert(0, curr_pos)
            order.append(self.exit_pos)
            cost = 0
            solution_cells = [order[0]]
            for i in range(len(order) - 1):
                if (order[i], order[i + 1]) in memory:
                    sol = memory[(order[i], order[i + 1])]
                else:
                    sol = graph.a_star(order[i], order[i + 1])
                    memory[(order[i], order[i + 1])] = sol
                    memory[(order[i + 1], order[i])] = sol[::-1]
                solution_cells.extend(sol[1:])
                cost += len(sol) - 1
            if cost < min_cost:
                min_cost = cost
                min_solution = solution_cells
        return min_solution
