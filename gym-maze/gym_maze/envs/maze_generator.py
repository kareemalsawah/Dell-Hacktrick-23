import random
import pickle
from gym_maze.envs.maze_view_2d import Maze
import numpy as np
import json
from collections import deque
from tqdm import tqdm


def get_move(cell, r, c, rows_length, cols_length):
    next_state = None
    if cell == 1 and r - 1 >= 0:
        next_state = r - 1, c
    elif cell == 2 and c + 1 < cols_length:
        next_state = r, c + 1
    elif cell == 4 and r + 1 < rows_length:
        next_state = r + 1, c
    elif cell == 8 and c - 1 >= 0:
        next_state = r, c - 1
    return next_state


def get_possible_children(r, c, rows_length, cols_length):
    children = []
    if r - 1 >= 0:
        children.append((r - 1, c))
    if c - 1 >= 0:
        children.append((r, c - 1))
    if c + 1 < cols_length:
        children.append((r, c + 1))
    if r + 1 < rows_length:
        children.append((r + 1, c))
    return children


def get_possible_moves(maze, r, c):
    rows_length, cols_length = maze.shape
    next_states = set()
    cell = maze[r][c]
    next_state = get_move(cell, r, c, rows_length, cols_length)
    if next_state is not None:
        next_states.add(next_state)
    possible_children = get_possible_children(r, c, rows_length, cols_length)
    for child in possible_children:
        child_r, child_c = child
        cell = maze[child_r][child_c]
        next_state = get_move(cell, child_r, child_c, rows_length, cols_length)
        if next_state is None:
            continue
        r_new, c_new = next_state
        if r_new == r and c_new == c:
            next_states.add(child)
    return next_states


def maze_has_blockers(maze):
    maze = maze.T
    queue = deque()
    queue.append((0, 0))
    optimizedQueue = set()  # for faster search
    explored = set()
    while len(queue) > 0:
        currentState = queue.popleft()
        explored.add(currentState)
        r, c = currentState
        children = get_possible_moves(maze, r, c)
        for child in children:
            if child not in optimizedQueue and child not in explored:
                queue.append(child)
                optimizedQueue.add(child)
    return len(explored) != np.prod(maze.shape)


def validate_maze(maze):
    # Check if the maze is a 2D numpy array
    if not isinstance(maze, np.ndarray) or maze.ndim != 2:
        return False

    # Check if the maze is 10x10
    if maze.shape[0] != 10 or maze.shape[1] != 10:
        return False

    # Check if each entry in the array is 1, 2, 4 or 8
    if not np.all(np.isin(maze, [1, 2, 4, 8])):
        return False
    if maze_has_blockers(maze):
        return False
    # If all checks pass, the maze is valid
    return True


if __name__ == "__main__":
    # DO NOT CHANGE
    # USE ONLY FOR GENERATING RANDOM/SAMPLE MAZES
    maze_size = 10
    for j in tqdm(range(100)):
        maze_id = j
        while True:
            maze = Maze(
                maze_size=(maze_size, maze_size), rescue_item_locations=[(10, 10)]
            )
            is_validated = validate_maze(maze.maze_cells)
            if is_validated:
                break

        to_save = {}
        to_save["maze"] = maze.maze_cells

        for i in range(50):
            riddle_types = ["server", "cipher", "pcap", "captcha"]
            rescue_items_dict = {}
            random.shuffle(riddle_types)

            for riddle_type in riddle_types:
                position = (
                    random.randrange(0, maze_size - 1),
                    random.randrange(0, maze_size - 1),
                )
                while (
                    position == (0, 0)
                    or position == (9, 9)
                    or position in rescue_items_dict
                ):
                    position = (
                        random.randrange(0, maze_size - 1),
                        random.randrange(0, maze_size - 1),
                    )
                rescue_items_dict[position] = riddle_type
            to_save["rescue_items"] = rescue_items_dict
            # pickle.dump(
            #     to_save, open("./mazes/maze_{}_{}.p".format(str(maze_id), str(i)), "wb")
            # )
