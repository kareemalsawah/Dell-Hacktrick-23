"""
Module to implement the GraphManager class
The purpose of this class is to keep track of the known edges in the maze
It can find the shortest path between any two nodes
Finally, it can draw the current state of the maze (known edges)
"""
from typing import Tuple, List
from dataclasses import dataclass


@dataclass
class Node:
    """
    Node class used to store information about a node

    Parameters
    ----------
    position: Tuple[int, int]
        Position of the node
    parent: Node
        The parent node of this node
    cost: float
        The cost from the start node to reach this node
    heuristic: float
        The heuristic value of this node
    depth: int
        The depth of this node (Depth of start node is 0)
    """

    def __init__(
        self,
        position: Tuple[int, int],
        parent=None,
        cost: float = 0,
        heuristic: float = 0,
        parent_branch_cost: float = 0,
        nearest_branch: int = 0,
        is_unsure_edge: bool = True,
        depth: int = 0,
    ):
        self.position = position
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
        self.parent_branch_cost = parent_branch_cost
        self.nearest_branch = nearest_branch
        self.is_unsure_edge = is_unsure_edge
        self.depth = depth

    def get_cost(self) -> float:
        """
        Get the cost of this node

        Returns
        -------
        float
            The cost of this node
        """
        cost = self.cost + self.heuristic + self.parent_branch_cost
        if self.is_unsure_edge:
            cost += 0.9 * self.nearest_branch
        return cost


class PathNotFound(Exception):
    """
    Raised when the A* algorithm cannot find a path
    """


class GraphManager:
    """
    Class to manage the graph of the maze

    Parameters
    ----------
    maze_size: Tuple[int, int]
        The size of the maze
    """

    def __init__(self, maze_size: Tuple[int, int] = (10, 10)):
        self.maze_size = maze_size
        self.graph = None
        self.confirmed_edges = set()

        self.initialize_graph()

    def initialize_graph(self) -> None:
        """
        Initializes the graph with all edges (neighbors) connected
        """
        self.graph = {}
        for i in range(self.maze_size[0]):
            for j in range(self.maze_size[1]):
                curr_pos = (i, j)
                neighbors = self.get_all_neighbors(curr_pos)
                for neighbor in neighbors:
                    if curr_pos not in self.graph:
                        self.graph[curr_pos] = {neighbor}
                    else:
                        self.graph[curr_pos].add(neighbor)
                    if neighbor not in self.graph:
                        self.graph[neighbor] = {curr_pos}
                    else:
                        self.graph[neighbor].add(curr_pos)

    def get_all_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Get all neighbors of a node (position) in the graph

        Parameters
        ----------
        pos : Tuple[int, int]
            The position of the node

        Returns
        -------
        List[Tuple[int, int]]
            List of neighbors
        """
        i, j = pos
        neighbors = []
        for neighbor in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
            if (
                neighbor[0] >= 0
                and neighbor[0] < self.maze_size[0]
                and neighbor[1] >= 0
                and neighbor[1] < self.maze_size[1]
            ):
                neighbors.append(neighbor)
        return neighbors

    def a_star(
        self, current_position: Tuple[int, int], goal: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        """
        A* algorithm to find the shortest path between two nodes

        Parameters
        ----------
        current_position : Tuple[int, int]
            Current position of the agent
        goal : Tuple[int, int]
            Goal position

        Returns
        -------
        List[Tuple[int, int]]
            List of positions in the shortest path

        Raises
        ------
        PathNotFound
            If no path is found
        """
        explored = [current_position]
        fringe = [Node(current_position)]

        while len(fringe) > 0:
            costs = [node.get_cost() for node in fringe]
            to_explore_idx = costs.index(min(costs))
            to_explore = fringe[to_explore_idx]

            if to_explore.position == goal:
                path_nodes = self.get_tree(to_explore)
                path_positions = [node.position for node in path_nodes]
                return path_positions

            children, heuristics = self.get_children(to_explore.position, goal)
            fringe_states = [node.position for node in fringe]
            for child, heuristic in zip(children, heuristics):
                if child not in explored and child not in fringe_states:
                    if len(children) > 1:
                        nearest_branch = 1
                    else:
                        nearest_branch = to_explore.nearest_branch + 1
                    is_unsure_edge = (
                        child,
                        to_explore.position,
                    ) not in self.confirmed_edges
                    parent_branch_cost = to_explore.parent_branch_cost
                    if to_explore.is_unsure_edge:
                        parent_branch_cost += 0.9 * to_explore.nearest_branch
                    fringe.append(
                        Node(
                            child,
                            to_explore,
                            to_explore.cost + 1,
                            heuristic,
                            parent_branch_cost,
                            nearest_branch,
                            is_unsure_edge,
                            to_explore.depth + 1,
                        )
                    )
                    explored.append(child)

            del fringe[to_explore_idx]
        raise PathNotFound("No path found")

    def get_children(
        self, position: Tuple[int, int], goal: Tuple[int, int]
    ) -> Tuple[List[Tuple[int, int]], List[float]]:
        """
        Get the children of a node (position) in the graph

        Parameters
        ----------
        position : Tuple[int, int]
            Position of the node
        goal : Tuple[int, int]
            Goal position (used for heuristic)

        Returns
        -------
        Tuple[List[Tuple[int, int]], List[float]]
            List of children and list of heuristics
        """
        children = self.graph[position]
        heuristics = []
        for neighbor in children:
            to_add = 0
            if (position, neighbor) not in self.confirmed_edges:
                to_add += 0.5
            heuristics.append(abs(neighbor[0] - goal[0]) + abs(neighbor[1] - goal[1]))
        return children, heuristics

    def remove_edge_from_graph(
        self, from_node: Tuple[int, int], to_node: Tuple[int, int]
    ) -> None:
        """
        Delete the edge between two nodes (positions) in the graph

        Parameters
        ----------
        from_node : Tuple[int, int]
            First node (position)
        to_node : Tuple[int, int]
            Second node (position)
        """
        if from_node in self.graph and to_node in self.graph[from_node]:
            self.graph[from_node].remove(to_node)
        if to_node in self.graph and from_node in self.graph[to_node]:
            self.graph[to_node].remove(from_node)

    def confirm_edge(
        self, from_node: Tuple[int, int], to_node: Tuple[int, int]
    ) -> None:
        """
        Add an edge to the confirmed edges set

        Parameters
        ----------
        from_node : Tuple[int, int]
            First node (position)
        to_node : Tuple[int, int]
            Second node (position)
        """
        self.confirmed_edges.add((from_node, to_node))
        self.confirmed_edges.add((to_node, from_node))

    def get_tree(self, path_node: Node) -> List[Node]:
        """
        Generates the solution path (recursively) as a list of states from
        the goal node to the start node

        Parameters
        ----------
        path_node: Node
            The goal node reached

        Returns
        -------
        List[Node]
            List of nodes from the goal node to the start node
        """
        if path_node.parent is None:
            return [path_node]
        return self.get_tree(path_node.parent) + [path_node]
