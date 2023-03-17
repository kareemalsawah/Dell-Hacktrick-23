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


def eval_espisode(maze_path: str) -> int:
    """
    Evaluate an agent on a single episode

    Parameters
    ----------
    maze_path : str
        Path to the maze file

    Returns
    -------
    int
        Number of steps taken by the agent
    """
    agent = AlgorithmicAgent(visualize=False)
    riddle_solvers = {
        "cipher": cipher_solver,
        "captcha": captcha_solver,
        "pcap": pcap_solver,
        "server": server_solver,
    }

    manager = create_maze(maze_path)

    obv = manager.reset(AGENT_ID)

    while True:
        action, action_index = agent.get_action(obv)  # Random action
        if agent.visualize:
            time.sleep(0.1)

        if action_index == -1:
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
    for j in tqdm(range(100)):
        for i in range(50):
            out = eval_espisode("../mazes/maze_{}_{}.p".format(str(j), str(i)))
            vals.append(out)
    mean = np.mean(vals)
    std = np.std(vals)
    # np.save("eval_edge_unknown_09_nearest_branch.npy", vals)
    # print(mean - 2 * std, mean, mean + 2 * std)
