import numpy as np
import heapq
from math import log2
import sys
sys.path.append("..")  # This adds the parent directory to the system path
from utils import *
from game_2048 import is_goal, reconstruct_path, move, compress_board, decompress

# Author: Caleb L'Italien
# Last edited: 11/19/2023

def a_star_search(initial_board, to_reach, max_depth=10000):
    '''
    Uses A* to find a near-optimal sequence of moves that reaches the goal state.
    '''
    open_set = []
    came_from = {}
    cost_so_far = {}
    start_state = compress_board(initial_board)
    visited_states = set()  

    heapq.heappush(open_set, (0, start_state))
    came_from[start_state] = None
    cost_so_far[start_state] = 0
    visited_states.add(start_state) 

    while open_set:
        _, current_state = heapq.heappop(open_set)

        if is_goal(current_state, to_reach, True): 
            return reconstruct_path(came_from, start_state, current_state, True)

        if cost_so_far[current_state] >= max_depth:
            continue

        current_board = decompress(current_state) 
        for direction in ['up', 'down', 'left', 'right']:
            new_board, done = move(current_board, direction)
            if not done:
                continue 

            new_state = compress_board(new_board)

            if new_state in visited_states:  
                continue

            new_cost = cost_so_far[current_state] + 1 

            if new_state not in cost_so_far or new_cost < cost_so_far[new_state]:
                cost_so_far[new_state] = new_cost
                priority = new_cost + heuristic(new_state)
                heapq.heappush(open_set, (priority, new_state))
                came_from[new_state] = (current_state, direction)
                visited_states.add(new_state)  

    return None  # No path found

def heuristic(compressed_board):
    '''
    Calculates the state of the current board, and negates it (as A* wants to minimize this value). 
    '''
    score = 0
    
    board_binary = format(compressed_board, '064b')
    
    def get_tile_value(bits):
        return PLACE_DICT[bits]
    
    empty_weight = 10
    merge_weight = 5
    monotonicity_weight = 1
    smoothness_weight = 1
    max_tile_weight = 1

    empty_cells = board_binary.count('0000')
    score += empty_cells * empty_weight

    def check_monotonicity(tiles):
        return sum(abs(tiles[i] - tiles[i+1]) for i in range(len(tiles) - 1))
    
    def check_smoothness(tiles):
        return sum(abs(log2(tiles[i]) - log2(tiles[i+1])) if tiles[i] != 0 and tiles[i+1] != 0 else 0 for i in range(len(tiles) - 1))
    
    def max_tile_position_score(board):
        max_tile = max(board)
        max_index = board.index(max_tile)
        corners = [0, 3, 12, 15]
        return max_tile_weight if max_index in corners else -max_tile_weight
    
    for row_idx in range(0, 64, 16):
        row = [get_tile_value(board_binary[i:i+4]) for i in range(row_idx, row_idx + 16, 4)]
        score -= check_monotonicity(row) * monotonicity_weight
        score -= check_smoothness(row) * smoothness_weight
    
    for col_idx in range(4):
        col = [get_tile_value(board_binary[i:i+4]) for i in range(col_idx, 64, 16)]
        score -= check_monotonicity(col) * monotonicity_weight
        score -= check_smoothness(col) * smoothness_weight

    for i in range(0, 64, 4):
        if i % 16 < 12:  
            if board_binary[i:i+4] == board_binary[i+4:i+8] and board_binary[i:i+4] != '0000':
                score += merge_weight

    for i in range(0, 48):  
        if board_binary[i:i+4] == board_binary[i+16:i+20] and board_binary[i:i+4] != '0000':
            score += merge_weight

    board = [get_tile_value(board_binary[i:i+4]) for i in range(0, 64, 4)]
    score += max_tile_position_score(board)
    
    return -score  


