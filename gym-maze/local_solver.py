import time
import pickle
import json
import numpy as np
from riddle_solvers import *
from gym_maze.envs.maze_manager import MazeManager
from solution import AlgorithmicAgent


agent = AlgorithmicAgent(visualize=False)
# try:
#     agent.graph.graph = pickle.load(open("map.pkl", "rb"))
# except FileNotFoundError:
#     pass


def local_inference(riddle_solvers):
    obv = manager.reset(agent_id)

    for timestep in range(MAX_T):
        # Select an action
        # time.sleep(0.1)
        print(agent.count)
        state_0 = obv
        action, action_index = agent.get_action(state_0)  # Random action
        if action_index == -1:
            manager.set_done(agent_id)
            break
        # if agent.count == 1:
        #     time.sleep(1)
        # time.sleep(0.1)
        obv, reward, terminated, truncated, info = manager.step(agent_id, action)

        if info["riddle_type"] is not None:
            tic = time.time()
            solution = riddle_solvers[info["riddle_type"]](info["riddle_question"])
            toc = time.time()
            print(info["riddle_type"], toc - tic)
            obv, reward, terminated, truncated, info = manager.solve_riddle(
                info["riddle_type"], agent_id, solution
            )

        # THIS IS A SAMPLE TERMINATING CONDITION WHEN THE AGENT REACHES THE EXIT
        # IMPLEMENT YOUR OWN TERMINATING CONDITION
        # if np.array_equal(obv[0], (9, 9)):
        #     manager.set_done(agent_id)
        #     break  # Stop Agent

        if RENDER_MAZE:
            manager.render(agent_id)

        states[timestep] = [
            obv[0].tolist(),
            action_index,
            str(manager.get_rescue_items_status(agent_id)),
        ]


if __name__ == "__main__":

    sample_maze = np.load("hackathon_sample.npy")
    agent_id = "9"  # add your agent id here
    riddle_solvers = {
        "cipher": cipher_solver,
        "captcha": captcha_solver,
        "pcap": pcap_solver,
        "server": server_solver,
    }

    manager = MazeManager()
    manager.init_maze(agent_id, maze_cells=sample_maze)
    env = manager.maze_map[agent_id]
    maze = {}
    states = {}

    maze["maze"] = env.maze_view.maze.maze_cells.tolist()
    maze["rescue_items"] = list(manager.rescue_items_dict.keys())

    MAX_T = 5000
    RENDER_MAZE = False

    local_inference(riddle_solvers)

    with open("./states.json", "w") as file:
        json.dump(states, file)

    with open("./maze.json", "w") as file:
        json.dump(maze, file)
