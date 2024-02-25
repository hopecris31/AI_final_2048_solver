# Important disclaimers
- The project structure:
    - algorithms: hosts the algorithms we'll use to solve the problem
    - metrics: folder to write metrics (in time solved, NOT in moves, as this is unreliable given the nature of 2048)
    - game_2048: the utilities of the game, you shouldn't need to modify
    - main.py: the driver for the game
- Anything the game tries to solve >= 128 will take a significant amount of time. I have not yet tried for a full 2048, as I predict this will take an overnight run. We will see how this goes
- The game has random generation of new tiles, so there is no way to know for certain whether or not the algorithm found a minimal solution (as one doesn't strictly speaking exist, at least on a consistent level). Thus, we are trying to optimize the time to solve. Use NumPy extensively for this.
- Keep the functional nature of the program. DO NOT use classes. The game will take a significant amount of RAM to solve higher numbers, and we need to account for this
- Make sure to keep author and last edited comments up to date
- PARALLELIZE!!!!!! Very important to do this, given that the state space is immeasurably vast (ie: BFS is not feasible). MCTS, for example went from 8 minute runtimes to <7 second runtimes after being parallelized (solving for 64)

# TODO
- Create two more algorithms. Maybe a simple one and a complex one.
- Evaluate them. I want a line graph that has the following features:
    - X axis: the number you reached (ie: 16, 32, 64, 128, ... , 2048). run algorithms for all numbers between 16 and 2048
    - Y axis: average time to solve (maybe run for different test boards and average them), measured how you see fit (it is currently seconds)
    - All 4 algorithms on different lines of the same graph. Use whatever library you see fit for this
    - Repeat this for three metric: number of boards made, time to solve, and reliability of finding a solution (solved/couldn't find solution). Thus make three graphs, using averages (do like 100 iterations to get a good average). Write the results to a text file. 
- Once done with the above, we will write the writeup. 