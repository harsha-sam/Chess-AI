# Chess AI
Implemented an AI which plays chess optimally using **Minimax** algorithm and **Alpha-beta pruning** for optimization.

## Requirements
* Python 3.x

## Instructions
* Run **runner.py** file

## Minimax Algorithm
A search algorithm that helps in decison making. It provides an optimal move for a player by trying to minimize/maximize a possible loss/gain.
It is widely used in two-player games to develop an AI which is almost impossible to defeat.

In Minimax we have two players:
  * **Maximizer** - It tries to get the maximum score from all possible actions assuming that opposite player plays optimally.
  * **Minimizer** - It tries to get the minimum score from all possible actions assuming that opposite player plays optimally.

Every board state has some value. If the state has some positive value, then the maximizer has upper hand in the game. The board state will tend to be negative, if
the minimizer has upper hand in the game.

## Depth-Limited Minimax
Same as minimax but it allows you to specify a depth and then estimates the utility of the next states upto that depth. 
There is a total of 255,168 possible Tic Tac Toe games, and 10²⁹⁰⁰⁰ possible games in Chess. Evaluating all the possible games in chess is practically impossible.
So we use depth-limited minimax instead.

## Alpha-beta Pruning
A way to optimize Minimax, Alpha-Beta Pruning skips some of the recursive computations that are decidedly unfavorable. 
It stops evaluating a move when at least one possibility has been found that proves the move to be worse than a previously examined move. 
Such moves need not be evaluated further. 
When applied to a standard minimax tree, it returns the same move as minimax would, but prunes away branches that cannot possibly influence the final decision.

## Known Bugs
* Checkmate condition
* Game-Draw condiion
* Special Moves (Promotion, Castling, Enpassant)
