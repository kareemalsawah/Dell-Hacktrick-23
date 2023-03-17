"""
Class to estimate the locations of the items in the maze given
the observations (distance and direction)
"""
from typing import List, Tuple


class ItemLocator:
    """
    Class to estimate the locations of the items in the maze
    """

    def __init__(self, maze_size: Tuple[int, int] = (10, 10), n_items: int = 4):
        self.maze_size = maze_size
        self.is_item_available = [True] * n_items  # False, if item is found
        self.item_possible_locations = [
            set() for _ in range(n_items)
        ]  # List of possible locations (compatible with all observations) for each item

        for i in range(maze_size[0]):
            for j in range(maze_size[1]):
                for item in self.item_possible_locations:
                    item.add((i, j))

    def update_estimates(
        self,
        curr_pos: Tuple[int, int],
        distances: List[int],
        directions: List[Tuple[int, int]],
    ) -> None:
        """
        Update the estimates of the locations of the items

        Parameters
        ----------
        curr_pos : Tuple[int, int]
            The current position of the agent
        distances : List[int]
            The distances to each item
        directions : List[Tuple[int, int]]
            The directions to each item
        """
        for idx, is_available in enumerate(self.is_item_available):
            if is_available:
                if distances[idx] == -1:
                    self.item_possible_locations[idx] = set()
                    self.is_item_available[idx] = False
                else:
                    possible_locs = self.get_locs_from_obs(
                        curr_pos, distances[idx], directions[idx]
                    )
                    new_locs = set()
                    for loc in possible_locs:
                        if loc in self.item_possible_locations[idx]:
                            new_locs.add(loc)
                    self.item_possible_locations[idx] = new_locs

    def get_locs_from_obs(
        self, curr_pos: Tuple[int, int], distance: int, direction: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        """
        Get the possible locations of an item from the distance and direction

        Parameters
        ----------
        curr_pos : Tuple[int, int]
            The current position of the agent
        distance : int
            Manhattan distance to the item
        direction : Tuple[int, int]
            Direction to the item

        Returns
        -------
        List[Tuple[int, int]]
            List of possible locations of the item
        """
        possible_locs = []
        if 0 in direction:  # Exact location of the item is known
            possible_locs.append(
                (
                    curr_pos[0] + direction[0] * distance,
                    curr_pos[1] + direction[1] * distance,
                )
            )
            return possible_locs
        for i in range(1, distance):
            possible_locs.append(
                (
                    curr_pos[0] + direction[0] * i,
                    curr_pos[1] + direction[1] * (distance - i),
                )
            )
        return possible_locs

    def get_estimates(self, item_idx: int) -> List[Tuple[int, int]]:
        """
        Get the estimates of the locations of the items

        Parameters
        ----------
        item_idx : int
            The index of the item

        Returns
        -------
        List[Tuple[int, int]]
            List of possible locations of the item
        """
        return list(self.item_possible_locations[item_idx])
