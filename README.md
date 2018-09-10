# reversi

Download and run \_\_main\_\_.py to play against the computer!

After repeatedly losing to a friend, I decided to program a computer to play the game “Reversi” (also known as “Othello”). The program, written in Python, uses the minimax algorithm with alpha-beta pruning based on a simple evaluation function. The program can play strongly given as little as 0.5 seconds of evaluation time per move.

I’ve also used the Tkinter package to create a simple user interface, allowing me to challenge my friends to matches (which I do frequently)!

## Rules of Reversi
Reversi is a game played on an 8x8 board between two players—“Black” and “White”—with Black moving first. The board starts with two black and two white counters placed diagonally at the center.
During their move, each player places a counter of their color on the board. If this counter and another of the same color lie on the same row, column, or diagonal, with every space in between filled with counters of the opposite color, all the counters in between change (’reverse”) to the player’s color. A player may only make a move if it causes at least one piece to be reversed; if no such move is available, the player is obligated to pass.
Clearly, the number of counters on the board strictly increases as the game progresses. When the board is filled or when no moves are available for either player, the player with the most counters of their color on the board wins.

## Evaluation Function
A naive strategy when playing Reversi is to try and maximize the number of your pieces on the board. However, the nature of the game is that large numbers of pieces can switch sides very quickly, when an opponent controls the surrounding area.
Instead, my evaluation function aims to maximize the number of moves available to the player, and minimize the number available to the opponent. In addition, it places a high value on capturing the corners of the board, since they cannot be surrounded and re-captured by an opponent.

## Minimax
Each possible configuration of the board is known as a “state”. We can construct a graph of states connected by moves, known as the “game tree”. The minimax algorithm is a method of selecting the optimal move from a given state, looking a fixed number of moves ahead in the game tree. In essence, it allows us to select the move that “maximizes the minimum guaranteed value”—equivalently, that “minimizes the maximum possible loss”, hence the term “minimax”.
Alpha-beta pruning is an optimization that can be applied to the minimax algorithm. In essence, it allows us to discard particular moves that can be said with certainty to be suboptimal. This allows us to look more moves ahead into the game tree without compromising run time.
