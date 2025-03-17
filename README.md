Connected Four: The Game

Connect Four is a two-player strategy game similar to tic-tac-toe. It is played using 42 tokens
(usually 21 red tokens for one player and 21 black tokens for the other player), and a vertical grid that
is 7 columns wide. Each column can hold a maximum of 6 tokens. The two players take turns. A
move consists of a player dropping one of his/her tokens into the column of his/her choice. When a
token is dropped into a column, it falls until it hits the bottom or the top token in that column. A
player wins by creating an arrangement in which at least four of his/her tokens are aligned in a row,
column, or diagonal. A game of Connect Four can end in a draw, i.e., in a
state where all 42 tokens have been used, the grid is full, but there are not four tokens of either colour
aligned in any direction at any location.

The interface for the game can be something like this (spaces are only used here for better understanding, not in the final code):
- - - - - - -
- - - - - - -
- - - - - - -
- - - - - - -
X - - O - X O
X - O X O X O

It is now X’s turn.
Make a move by choosing your coordinates to play.

After X makes a move, the computer takes this new board with X move added and uses one of the
two algorithms to be implemented. When the computer finishes choosing the best move among the
possible ones, it will then exhibit a new board with the computer’s move (in this case a new ’O’ will
show in the position chosen by your program), and wait for the human to play.
Our implementation will  support the following three game scenarios:
1. human vs. human
2. human vs. computer
3. computer vs. computer (2 different algorithms)

It will be used the Monte Carlo Tree Search and Decision Trees, with an auxiliary dataset.
