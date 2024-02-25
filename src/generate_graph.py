import algorithms.monte_carlo_tree_search as mts
import algorithms.a_star_search as ass
import algorithms.minimax_search as ms
import algorithms.dijkstra_search as ds
import game_2048 as game
import os

file_path_avg_moves = os.path.join("..", "metrics", "avg_moves_results.txt")

TO_REACH_VALUES = [8, 16, 32, 64, 128, 256, 512, 1024, 2048]

MONTE_CARLO_AVERAGES = []
mc_moves_per_tile = {8: 0, 16: 0, 32: 0, 64: 0, 128: 0, 256: 0, 512: 0, 1024: 0, 2048: 0}

ASTAR_AVERAGES = []
as_moves_per_tile = {8: 0, 16: 0, 32: 0, 64: 0, 128: 0, 256: 0, 512: 0, 1024: 0, 2048: 0}

MINIMAX_AVERAGES = []
mm_moves_per_tile = {8: 0, 16: 0, 32: 0, 64: 0, 128: 0, 256: 0, 512: 0, 1024: 0, 2048: 0}

DIJKSTRA_AVERAGES = []
di_moves_per_tile = {8: 0, 16: 0, 32: 0, 64: 0, 128: 0, 256: 0, 512: 0, 1024: 0, 2048: 0}


def get_avg_moves_results(algorithm, result_list):
    """
    :param algorithm: search algorithm to run
    :param result_list: list to add the results to
    :return: the average number of moves per tile
    """
    for target_tile in TO_REACH_VALUES:
        result_list.append(avg_per_target_val(algorithm, target_tile))


def avg_per_target_val(algo, target_val):
    """
    @param algo: search algorithm to run
    @param target_val: target tile value to reach
    @return: the average number of moves the algorithm took to reach the target value
    """
    moves_per_run = []
    for i in range(10):
        print(f"iteration {i} of target tile {target_val}")
        result = algo(game.generate_new_board(), target_val)
        if result is not None:
            total_moves = len(result)
            moves_per_run.append(total_moves)
        else:
            print(f"No result for iteration {i}, target tile {target_val}")
    if moves_per_run:
        return sum(moves_per_run) // len(moves_per_run)
    else:
        return 0


def save_results_to_file(file_path, data):
    with open(file_path, 'w') as file:
        for key, value in data.items():
            file.write(f'{key}: {value}\n')


def update_dict(dictionary, avgs_list):
    for i in range(len(TO_REACH_VALUES)):
        dictionary[i] = avgs_list[i]


if __name__ == "__main__":
    print("RUNNING MONTE CARLO TREE SEARCH")
    get_avg_moves_results(mts.monte_carlo_tree_search, MONTE_CARLO_AVERAGES)
    update_dict(mc_moves_per_tile, MONTE_CARLO_AVERAGES)
    print(MONTE_CARLO_AVERAGES)
    print(mc_moves_per_tile)

    print("RUNNING A* SEARCH")
    get_avg_moves_results(ass.a_star_search, ASTAR_AVERAGES)
    update_dict(as_moves_per_tile, ASTAR_AVERAGES)
    print(ASTAR_AVERAGES)
    print(as_moves_per_tile)

    (print("RUNNING MINIMAX SEARCH"))
    get_avg_moves_results(ms.minimax_search, MINIMAX_AVERAGES)
    update_dict(mm_moves_per_tile, MINIMAX_AVERAGES)
    print(MINIMAX_AVERAGES)
    print(mm_moves_per_tile)


    print("RUNNING DIJKSTRA'S SEARCH")
    get_avg_moves_results(ds.dijkstra_search, DIJKSTRA_AVERAGES)
    update_dict(di_moves_per_tile, DIJKSTRA_AVERAGES)
    print(DIJKSTRA_AVERAGES)
    print(di_moves_per_tile)

    print("Saving results to file...")
    with open(file_path_avg_time, 'w') as file:
        file.write("Monte Carlo Tree Search Averages:\n")
        file.write(str(MONTE_CARLO_AVERAGES) + '\n')
        file.write(str(mc_moves_per_tile) + '\n\n')

        file.write("A* Search Averages:\n")
        file.write(str(ASTAR_AVERAGES) + '\n')
        file.write(str(as_moves_per_tile) + '\n\n')

        file.write("Minimax Search Averages:\n")
        file.write(str(MINIMAX_AVERAGES) + '\n')
        file.write(str(mm_moves_per_tile) + '\n\n')

        file.write("Dijkstra's Search Averages:\n")
        file.write(str(DIJKSTRA_AVERAGES) + '\n')
        file.write(str(di_moves_per_tile) + '\n')

    print("Results saved successfully.")
