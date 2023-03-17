import numpy as np

# vals = np.load("eval_edge_unknown_09_nearest_branch.npy").reshape(-1)

# mean = np.mean(vals)
# std = np.std(vals)
# print(mean - 2 * std, mean, mean + 2 * std)
maze_submission = [
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
maze_submission = np.array(maze_submission).T
np.save("maze_submission.npy", maze_submission)
