import sys
import numpy as np
import math
import random
import json
import requests
import copy
import time

from riddle_solvers import *

### the api calls must be modified by you according to the server IP communicated with you
#### students track --> 16.170.85.45
#### working professionals track --> 13.49.133.141
server_ip = "16.170.85.45"

from solution import AlgorithmicAgent

agent = AlgorithmicAgent(visualize=False)


def move(agent_id, action):
    response = requests.post(
        f"http://{server_ip}:5000/move", json={"agentId": agent_id, "action": action}
    )
    return response


def solve(agent_id, riddle_type, solution):
    response = requests.post(
        f"http://{server_ip}:5000/solve",
        json={"agentId": agent_id, "riddleType": riddle_type, "solution": solution},
    )
    try:
        print(response)
        #print(response.json())
    except Exception:
        print("Failed to parse json")
    return response


def get_obv_from_response(response):
    directions = response.json()["directions"]
    distances = response.json()["distances"]
    position = response.json()["position"]
    obv = [position, distances, directions]
    return obv


def submission_inference(riddle_solvers):

    response = requests.post(
        f"http://{server_ip}:5000/init", json={"agentId": agent_id}
    )
    obv = get_obv_from_response(response)

    while True:
        # Select an action
        state_0 = obv
        action, action_index = agent.get_action(state_0)  # Random action
        print(agent.count)
        if action_index == -1:
            print(state_0[0])
            response = requests.post(
                f"http://{server_ip}:5000/leave", json={"agentId": agent_id}
            )
            print(agent.graph.graph)
            break

        response = move(agent_id, action)
        if not response.status_code == 200:
            print(response)
            break

        obv = get_obv_from_response(response)
        #print(response.json())

        if not response.json()["riddleType"] == None:
            try:
                tic = time.time()
                solution = riddle_solvers[response.json()["riddleType"]](
                    response.json()["riddleQuestion"]
                )
                response = solve(agent_id, response.json()["riddleType"], solution)
                toc = time.time()
                print((toc-tic)*1000, " ms")
            except Exception:
                print("Error in solving riddle")
                raise Exception("helooz")


if __name__ == "__main__":

    agent_id = "YpL5hTnG2w"
    riddle_solvers = {
        "cipher": cipher_solver,
        "captcha": captcha_solver,
        "pcap": pcap_solver,
        "server": server_solver,
    }
    submission_inference(riddle_solvers)
