import os
import chess.pgn
from state import State
import numpy as np

def get_dataset(num_samples=None):
    X,Y = [], []
    gn = 0
    values ={"1/2-1/2": 0, "0-1": -1, "1-0": 1}
    for fn in os.listdir("data"):
        pgn = open(os.path.join("data",fn))

        while 1:
            try:
                game = chess.pgn.read_game(pgn)

            except Exception:
                break

            res = game.headers["Result"]

            if res not in values:
               continue

            value = values[res]
            board = game.board()
            for i,move in enumerate(game.mainline_moves()):
                board.push(move)
                ser = State(board).serialize()
                X.append(ser)
                Y.append(value)
            print("parsing game %d, got %d examples" %(gn, len(X)))

            if num_samples is not None and len(X) > num_samples:
                return X,Y
            gn+=1
    X = np.array(X)
    Y = np.array(Y)
    return X,Y

if __name__ == "__main__":
    X,Y = get_dataset(1e5)
    
    np.savez("processed/dataset100k.npz", X, Y)
    

