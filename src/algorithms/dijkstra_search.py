import numpy as np
import heapq
from src.game_2048 import is_goal, move

# Author: Hope Crisafi
# Last edited: 11/19/2023


def dijkstra_search(initial_board, to_reach, max_depth=100000):
    open_set = []
    came_from = {}
    cost_so_far = {}
    start_state = tuple(map(tuple, initial_board))
    visited_states = set()

    heapq.heappush(open_set, (0, start_state))
    came_from[start_state] = None
    cost_so_far[start_state] = 0
    visited_states.add(start_state)

    while open_set:
        _, current_state = heapq.heappop(open_set)
        current_board = np.array(current_state)

        if is_goal(current_board, to_reach):
            return reconstruct_path(came_from, start_state, current_state)

        if cost_so_far[current_state] >= max_depth:
            continue

        for direction in ['up', 'down', 'left', 'right']:
            new_board, done = move(current_board, direction)
            if not done:
                continue

            new_state = tuple(map(tuple, new_board))
            if new_state in visited_states:
                continue

            new_cost = cost_so_far[current_state] + 1

            if new_state not in cost_so_far or new_cost < cost_so_far[new_state]:
                cost_so_far[new_state] = new_cost
                heapq.heappush(open_set, (new_cost, new_state))
                came_from[new_state] = (current_state, direction)
                visited_states.add(new_state)

    return None


def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        prev, direction = came_from[current]
        path.append((current, direction))
        current = prev
    path.reverse()
    return path
