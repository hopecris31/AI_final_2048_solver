## Proposal

* Project Title: 2048 State Space Search
* Your Names: Caleb L'Italien, Hope Crisafi

## Project Description

In this project, we aim to develop an AI that calculates the minimum number of moves required to win the game 2048. This involves simulating the game, implementing search algorithms, and crafting heuristic functions to evaluate game states effectively. The challenge is to search through the vast state space of the 2048 game to find the most efficient path to the winning state (a tile with the number 2048). The game's dynamic nature, random tile placements, and vast state space make this a complex problem. This project interests me as it combines game theory, heuristic search algorithms, and optimization in a practical application. Plus, 2048 is a popular game, and achieving this would be a notable accomplishment in AI game-solving. Handling the vast state space of the game and predicting the randomness introduced by new tile placements will likely be the most challenging aspect.

## Planning

We plan to use heuristic search algorithms, like the A* algorithm. The game's state will be represented using a 2D matrix, and priority queues will likely be essential for efficient state evaluations based on the heuristic. Considering Hofstadter's Law ("It always takes longer than you expect, even when you take into account Hofstadter's Law."), we aim to begin work immediately on this project. Initial runs may take hours due to the vast state space; however, with optimization and effective heuristics, we aim to reduce this significantly. I aim to have the code done at least five days before the due date to allow for testing, analysis, and report writing, as well as two days for analyzing results, tweaking, and finalizing the report.

## Logistics

We plan to use Python with numpy for efficient matrix operations.

## Testing:

Solutions will be verified by simulating the AI's moves in the 2048 environment. If the AI consistently reaches the 2048 tile with the computed number of moves, it's correct.

## Evaluation:

Success will be measured by the AI's ability to consistently calculate and achieve the win in the predicted number of moves across multiple game simulations.

## Risk Abatement and Triage:
Ensure a basic but effective heuristic is in place first before attempting optimizations. Regular testing at each phase to ensure functionality. If calculating the minimum moves proves too complex, pivot to a general AI player for 2048 that uses heuristics to play the game efficiently but not necessarily in the minimum moves.

Gold: AI calculates the minimum moves and wins consistently.
Silver: AI plays the game with high efficiency, reaching 2048 most of the time, but not always in minimal moves.
Bronze: AI understands and plays the game with a decent win rate but may not always reach 2048.

## Assessment (Teams Only)
There will be a total of four different algorithms trying to solve 2048. Each team member (Caleb and Hope) will write 2
algorithms each.  Once completed, each algorithm will run the game and we will see whos algorithm can solve the game the 
fastest.  Algorithms will be assessed based on if they can solve the game, and if they can, they will be ranked
against the other algorithms based on how fast they can solve it and how many steps it took to solve.

## Score Sheet

| Item                    |     Expected Deadline| Achieved Date   |
|-------------------------|-------------------:|-----------------|
| Implementation |                    |                 |
| Writeup/Analysis        | |                    |                 |
| Utility                 | |                   |                 |
| Sub-Total               | |                   |                 |
| Challenge Modifier |              (John will fill out)    |                |
| Total              |                   |                 |