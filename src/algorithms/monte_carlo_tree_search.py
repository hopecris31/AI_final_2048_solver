import numpy as np
from concurrent.futures import ThreadPoolExecutor

import sys
sys.path.append("..")

from game_2048 import is_goal, reconstruct_path, move, get_possible_moves

# Author: Caleb L'Italien
# Last edited: 11/19/2023

PARALLELIZE = False
def monte_carlo_tree_search(initial_board, to_reach, max_iters=1000):
    '''
    Uses MCTS to find the best possible move until no moves are left or the goal is reached.
    '''
    def rollout(board):
        '''
        Repeatedly makes the best found move.
        '''
        moves = get_possible_moves(board, PARALLELIZE)
        while moves:
            moves = sorted(moves, key=heuristic, reverse=True)
            board = moves[0]
            if is_goal(board, to_reach):
                return True
            moves = get_possible_moves(board, PARALLELIZE)
        return False

    def find_best_move(board, max_iters=1000):
        '''
        Tries to select the best possible move.
        '''
        move_scores = {move: 0 for move in ['up', 'left', 'down', 'right']}

        def rollout_score(possible_move):
            new_board, done = move(board, possible_move)
            if not done:
                return possible_move, 0
            rollout_success = rollout(np.copy(new_board))
            final_heuristic = heuristic(new_board) if rollout_success else 0
            return possible_move, final_heuristic

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(rollout_score, move) for move in move_scores]
            for future in futures:
                possible_move, score = future.result()
                move_scores[possible_move] += score

        best_move, best_score = max(move_scores.items(), key=lambda item: item[1])
        return best_move if best_score > 0 else None

    came_from = {}
    current_state = tuple(map(tuple, initial_board))
    came_from[current_state] = None

    while not is_goal(np.array(current_state), to_reach):
        move_direction = find_best_move(np.array(current_state), max_iters)
        if move_direction is None:
            return None
        new_board, _ = move(np.array(current_state), move_direction)
        new_state = tuple(map(tuple, new_board))
        came_from[new_state] = (current_state, move_direction)
        current_state = new_state

    return reconstruct_path(came_from, tuple(map(tuple, initial_board)), current_state)


def heuristic(board):
    '''
    Scores the given board based on where the maximum tile is, the number of empty 
    tiles, and the maximum tile's value. 
    '''
    empty_weight = 2.7
    max_tile_weight = 1.0
    corner_weight = 10.0
    empty_count = len(board[board == 0])
    max_tile = np.max(board)

    max_tile_in_corner_bonus = 0
    if (board[0, 0] == max_tile or board[0, -1] == max_tile or
        board[-1, 0] == max_tile or board[-1, -1] == max_tile):
        max_tile_in_corner_bonus = corner_weight

    score = (empty_weight * empty_count) + \
            (max_tile_weight * max_tile) + \
            max_tile_in_corner_bonus
    return score