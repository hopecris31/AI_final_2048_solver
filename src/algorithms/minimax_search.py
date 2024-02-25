# minimax_search.py
import numpy as np
import src.game_2048 as game

# Author: Hope Crisafi
# Last edited: 11/19/2023


def minimax(board, depth, is_maximizing_player, alpha, beta, to_reach):
    if game.is_goal(board, to_reach) or depth == 0:
        return heuristic(board), None

    if is_maximizing_player:
        best_value = float('-inf')
        best_move = None
        for direction in ['up', 'down', 'left', 'right']:
            new_board, done = game.move(board, direction)
            if done:
                value, _ = minimax(new_board, depth-1, False, alpha, beta, to_reach)
                if value > best_value:
                    best_value = value
                    best_move = direction
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
        return best_value, best_move
    else:
        best_value = float('inf')
        possible_boards = game.get_possible_moves(board)
        for new_board in possible_boards:
            value, _ = minimax(new_board, depth-1, True, alpha, beta, to_reach)
            best_value = min(best_value, value)
            beta = min(beta, value)
            if beta <= alpha:
                break
        return best_value, None


def heuristic(board):
    score = 0

    empty_cells = np.count_nonzero(board == 0)
    score += empty_cells * 10

    for row in board:
        if np.any(np.diff(row) < 0):
            score -= 1

    for col in board.T:
        if np.any(np.diff(col) < 0):
            score -= 1

    merge_opportunities = 0
    for row in range(board.shape[0]):
        for col in range(board.shape[1]):
            if row < board.shape[0] - 1 and board[row][col] == board[row + 1][col]:
                merge_opportunities += 1
            if col < board.shape[1] - 1 and board[row][col] == board[row][col + 1]:
                merge_opportunities += 1
    score += merge_opportunities * 5

    return -score


def minimax_search(initial_board, to_reach, max_depth=1000):
    path = []
    board = initial_board
    while not game.is_goal(board, to_reach) and max_depth > 0:
        score, best_move = minimax(board, max_depth, True, float('-inf'), float('inf'), to_reach)
        if best_move is None:
            break
        new_board, done = game.move(board, best_move)
        if not done:
            break
        path.append((np.array2string(board, separator=' '), best_move))
        board = new_board
        max_depth -= 1
    return path


