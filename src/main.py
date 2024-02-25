import traceback
import numpy as np
import sys
import os
from algorithms.a_star_search import a_star_search
from algorithms.monte_carlo_tree_search import monte_carlo_tree_search
from algorithms.minimax_search import minimax_search
from algorithms.dijkstra_search import dijkstra_search
from game_2048 import get_board_count, generate_new_board, reset_board_count
import time

# Author: Caleb L'Italien
# Last edited: 11/19/2023

def main(search_algorithm, to_reach, starting_board):
    '''
    Runs the algorithm on the starting board, aiming for to_reach. Prints metrics on the run
    '''
    algorithm_name = str(search_algorithm).split()[1].split('_at_')[0]
    results_filename = os.path.join("..", "metrics", f"{algorithm_name}_results.txt") 
    reset_board_count()

    try:
        with open(results_filename, 'a') as file:
            print("----------------------------")
            print("Goal:", to_reach)
            print("Starting board:")
            print(np.array2string(starting_board, separator=' '), "\n")

            start_time = time.time()
            path = search_algorithm(starting_board, to_reach)
            end_time = time.time()

            if isinstance(path, list):
                print("Path to solution:")
                for state_str, direction in path:
                    print(f"Move: {direction}")
                    print(state_str, "\n")
                print("Total moves: ", len(path))
            elif path is not None:
                print("Best move: ", path)
            else:
                print("No solution found.")

            if path:
                print("Path to solution:")
                print(path)
                for state_str, direction in path:
                    print(f"Move: {direction}")
                    print(state_str, "\n")
                print("Total moves: ", len(path))

                file.write(f"Goal: {to_reach}\n")
                file.write(f"Total moves: {len(path)}\n")
                file.write(f"Time to solve: {end_time - start_time:.2f} seconds\n")
                file.write(f"Number of boards made: {get_board_count()}\n\n")
            else:
                print("Number of boards made:", get_board_count())
                print("No solution found.")

                file.write(f"Goal: {to_reach}\n")
                file.write("No solution found.\n\n")

            print("Time to solve: {:.2f} seconds".format(end_time - start_time))
            print("Number of boards made:", get_board_count())
            print("----------------------------")

    except Exception as e:
        print("An error occurred:")
        traceback.print_exc()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py <algorithm> <number_of_runs> <to_reach>")
        sys.exit(1)

    algo_name = sys.argv[1]
    num_runs = int(sys.argv[2])
    to_reach = int(sys.argv[3])

    algorithms = {
        'a_star_search': a_star_search,
        'monte_carlo_tree_search': monte_carlo_tree_search,
        'minimax_search': minimax_search,
        'dijkstra_search': dijkstra_search,
    }

    if algo_name in algorithms:
        main(algorithms[algo_name], to_reach, generate_new_board())
    else:
        print(f"Algorithm '{algo_name}' not found.")
        sys.exit(1)
