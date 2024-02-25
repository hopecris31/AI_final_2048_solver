import numpy as np
import random
sys_random = random.SystemRandom() # This is to ensure thread safety
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import *
# Author: Caleb L'Italien
# Last edited: 11/19/2023

# Basic utilities for playing 2048

BOARD_COUNTER = 0
def reconstruct_path(came_from, start, goal, decompress_boards=False):
    '''
    Reconstructs the solution path, and formats it nicely. To see how boards are stored in a compression algorithm,
    Set decompress_boards to False but use the compression anyways.
    '''
    path = []
    current_state = goal
    while current_state != start:
        previous_state, direction = came_from[current_state]
        
        if decompress_boards:
            current_state_decompressed = decompress(current_state)
            state_str = np.array2string(current_state_decompressed, separator=' ')
        else:
            state_str = np.array2string(np.array(current_state), separator=' ')
        
        path.append((state_str, direction))
        current_state = previous_state
    path.reverse()
    return path


def get_possible_moves(state, parallelize=False):
    '''
    Finds the next possible moves from a given state.
    '''
    if parallelize:
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(move, state, direction): direction for direction in ['up', 'down', 'left', 'right']}
            moves = []
            for future in as_completed(futures):
                new_board, done = future.result()
                if done:
                    moves.append(new_board)
        return moves
    else:
        moves = []
        for direction in ['up', 'down', 'left', 'right']:
            new_board, done = move(state, direction)
            if done:
                moves.append(new_board)
        return moves

def is_goal(state, to_reach, decompress_state=False):
    '''
    Checks if the current state is the goal state.
    '''
    if decompress_state: 
        # Check every block of 4 bits to see if that representation is the goal state
        to_reach_binary = format(BIT_DICT[to_reach], '04b')
        state_binary = format(state, '064b')
        for i in range(0, 64, 4):
            if state_binary[i:i+4] == to_reach_binary:
                return True  
        return False  
    return np.max(state) == to_reach


def move(state, direction):
    '''
    Perform a move in one of the four directions. Checks for merges exactly three times per move.
    Returns the new state and a boolean indicating if any tile was moved.
    '''
    global BOARD_COUNTER
    def compress(board):
        ''' 
        Push all non-zero tiles to the front of the board (relative to the move direction).
        '''
        new_board, moved = np.zeros_like(board), False
        for row in range(board.shape[0]):
            fill_position = 0
            for col in range(board.shape[1]):
                if board[row][col] != 0:
                    new_board[row][fill_position] = board[row][col]
                    if col != fill_position:
                        moved = True
                    fill_position += 1
        return new_board, moved

    def merge(board):
        ''' 
        Combine tiles of the same value. 
        '''
        moved = False
        for _ in range(3):  
            for row in range(board.shape[0]):
                for col in range(board.shape[1]-1):
                    if board[row][col] == board[row][col + 1] and board[row][col] != 0:
                        board[row][col] *= 2
                        board[row][col + 1] = 0
                        moved = True
            board, _ = compress(board)  
        return board, moved

    def reverse(board):
        ''' 
        Reverse the board.
        '''
        return np.fliplr(board)

    def transpose(board):
        ''' 
        Transpose the board.
        '''
        return np.transpose(board)

    board = np.copy(state)
    moved = False

    if direction == 'left':
        board, compressed = compress(board)
        board, merged = merge(board)
        moved = compressed or merged
    elif direction == 'right':
        board = reverse(board)
        board, compressed = compress(board)
        board, merged = merge(board)
        board = reverse(board)
        moved = compressed or merged
    elif direction == 'up':
        board = transpose(board)
        board, compressed = compress(board)
        board, merged = merge(board)
        board = transpose(board)
        moved = compressed or merged
    elif direction == 'down':
        board = transpose(board)
        board = reverse(board)
        board, compressed = compress(board)
        board, merged = merge(board)
        board = reverse(board)
        board = transpose(board)
        moved = compressed or merged
    if moved:
        BOARD_COUNTER += 1
        spawn_new_tile(board)
    return board, moved

def spawn_new_tile(board):
    '''
    Spawns a new tile onto the board
    '''
    empty_cells = [(x, y) for x in range(board.shape[0]) for y in range(board.shape[1]) if board[x][y] == 0]
    if empty_cells:
        x, y = sys_random.choice(empty_cells)
        board[x][y] = 4 if sys_random.random() < 0.1 else 2  # 10% chance to spawn a 4, 90% for a 2
    return board

def get_board_count():
    '''
    Returns the total number of boards made in this run.
    '''
    global BOARD_COUNTER
    return BOARD_COUNTER

def reset_board_count():
    '''
    Resets the number of boards made in this run. 
    '''
    global BOARD_COUNTER
    BOARD_COUNTER = 0

def generate_new_board():
    '''
    Generates a new board with two randomly placed tiles.
    '''
    board = np.zeros((4, 4), dtype=int)  
    board = spawn_new_tile(board)  
    board = spawn_new_tile(board)
    return board

def compress_board(board):
    '''
    Compresses the board into a 64 bit word representation. See utils.py or reconstruct_path to see how this works.
    '''
    bit_rep = 0
    for row in board:
        for place in row:
            bit_rep = (bit_rep << 4) | BIT_DICT[place]
    return bit_rep

def decompress(bit_string_byte):
    '''
    Takes a compressed board and reconstructs the representation
    '''
    board = np.zeros((4, 4), dtype=int)
    i = 0
    j = 0
    k = 0
    bit_string = format(bit_string_byte, '064b')
    while i < 64:
        place = bit_string[i: i+4]
        place_val = PLACE_DICT[place]
        board[j][k] = place_val
        i += 4
        k += 1
        if k == 4:
            k = 0
            j += 1
    return board
