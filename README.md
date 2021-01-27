* Establish the search tree
* Use a neural net to prune the search tree

Define : Value Network
V - f(state)

What is V?
V = -1 black wins the board state
V = 0 draw board state
V = 1 white wins board state



State(Board):

Pieces(2+7* 2 = 16)

* Universal
** Blank
** Blank (En passant)
* Pieces
** Pawn
** Bishop
** Knight
** Rook
** Rook(can castle)
** Queen
** King

Extra State:
* To move

8x8x4 +  1 = 257 bits(vector of 0 or 1)
