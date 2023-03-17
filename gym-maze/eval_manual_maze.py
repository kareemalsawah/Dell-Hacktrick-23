"""
Module to empirically evaluate an agent on multiple maps
"""
import time
import pickle
import numpy as np
from tqdm import tqdm
from solution import AlgorithmicAgent
from gym_maze.envs.maze_manager import MazeManager

from riddle_solvers import cipher_solver, captcha_solver, pcap_solver, server_solver


AGENT_ID = "9"


def create_maze(maze_path: str) -> MazeManager:
    """
    Create a maze manager from a saved maze (pickle file)

    Parameters
    ----------
    maze_path: str
        Path to the maze file containing a dict
        maze_path['maze'] is a numpy array of shape (10, 10)
        maze_path['rescue items'] is a dict with the recuse items

    Returns
    -------
    MazeManager
    """
    saved_maze = pickle.load(open(maze_path, "rb"))

    manager = MazeManager()
    manager.rescue_items_dict = saved_maze["rescue_items"]
    manager.init_maze(AGENT_ID, maze_cells=saved_maze["maze"])
    return manager


def eval_espisode(manager: MazeManager()) -> int:
    """
    Evaluate an agent on a single episode

    Parameters
    ----------
    manager: MazeManager
        The maze manager

    Returns
    -------
    int
        Number of steps taken by the agent
    """
    agent = AlgorithmicAgent(visualize=True)
    riddle_solvers = {
        "cipher": cipher_solver,
        "captcha": captcha_solver,
        "pcap": pcap_solver,
        "server": server_solver,
    }

    obv = manager.reset(AGENT_ID)

    while True:
        action, action_index = agent.get_action(obv)  # Random action
        if agent.visualize:
            time.sleep(0.005)

        if action_index == -1:
            # time.sleep(500)
            manager.set_done(AGENT_ID)
            break

        obv, _, _, _, info = manager.step(AGENT_ID, action)

        if info["riddle_type"] is not None:
            solution = "none"
            obv, _, _, _, _ = manager.solve_riddle(
                info["riddle_type"], AGENT_ID, solution
            )

    return agent.count


if __name__ == "__main__":
    tic = time.time()
    vals = []

    # 10x10 zeros
    bad_maze = [
        [4, 8, 4, 8, 8, 8, 8, 8, 8, 8],
        [4, 8, 8, 8, 8, 2, 2, 2, 2, 4],
        [4, 1, 2, 2, 2, 1, 2, 2, 4, 8],
        [2, 4, 1, 2, 2, 2, 2, 2, 1, 4],
        [4, 4, 1, 2, 2, 2, 2, 2, 1, 4],
        [2, 4, 1, 1, 8, 2, 4, 8, 8, 4],
        [2, 2, 1, 4, 1, 8, 8, 2, 1, 4],
        [1, 4, 8, 4, 4, 8, 2, 1, 2, 4],
        [1, 4, 1, 4, 8, 1, 1, 8, 8, 4],
        [1, 8, 1, 8, 2, 1, 8, 8, 1, 8],
    ]
    bad_maze_2 = [
        [2, 4, 4, 8, 8, 8, 8, 8, 4, 8],
        [4, 8, 4, 2, 2, 2, 4, 1, 8, 1],
        [2, 4, 4, 1, 2, 1, 2, 4, 2, 1],
        [4, 8, 4, 1, 1, 8, 4, 8, 1, 8],
        [2, 4, 4, 1, 2, 1, 2, 4, 2, 1],
        [4, 8, 4, 1, 1, 8, 4, 8, 1, 8],
        [2, 4, 4, 1, 2, 1, 2, 4, 2, 1],
        [4, 8, 2, 1, 1, 8, 4, 8, 1, 8],
        [4, 2, 4, 2, 4, 1, 2, 4, 2, 1],
        [2, 1, 2, 1, 2, 1, 8, 8, 1, 8],
    ]

    """
        1
    8       2
        4
    """
    bad_maze_3 = [
        [2, 4, 2, 2, 2, 4, 2, 2, 2, 4],
        [4, 8, 1, 8, 4, 8, 2, 1, 4, 8],
        [2, 4, 2, 1, 2, 4, 1, 8, 2, 4],
        [4, 8, 1, 8, 4, 8, 2, 1, 4, 8],
        [2, 4, 2, 1, 2, 4, 1, 8, 2, 4],
        [4, 8, 1, 8, 2, 2, 2, 1, 4, 8],
        [2, 4, 2, 1, 1, 4, 8, 4, 2, 4],
        [4, 8, 1, 8, 8, 8, 1, 4, 4, 8],
        [4, 2, 4, 2, 4, 1, 1, 4, 2, 4],
        [2, 1, 2, 1, 2, 2, 1, 2, 1, 1],
    ]
    bad_maze = np.array(bad_maze).T
    bad_maze_2 = np.array(bad_maze_2).T
    bad_maze_3 = np.array(bad_maze_3).T
    maze = pickle.load(open("../mazes/maze_{}_{}.p".format(str(79), str(0)), "rb"))[
        "maze"
    ]
    maze = np.array(maze)
    rescue_items = pickle.load(open("maze_gen_rescue_items.p", "rb"))
    for i in tqdm(range(500)):
        manager = MazeManager()
        manager.rescue_items_dict = rescue_items[i]
        manager.init_maze(AGENT_ID, maze_cells=bad_maze_3)
        out = eval_espisode(manager)
        vals.append(out)
        # print(out)
    np.save("maze_79.npy", vals)
    # np.save("evaluating_worst_5_mazes.npy", vals)
    # print(mean - 2 * std, mean, mean + 2 * std)
