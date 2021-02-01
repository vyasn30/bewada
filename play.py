from state import State
import torch
from train import Net
from flask import Flask, Response
import time
import chess.svg



class Valuator(object):
    def __init__(self):
        vals = torch.load("nets/value.pth", map_location = lambda storage, loc : storage)
        self.model = Net()
        self.model.load_state_dict(vals)

    def __call__(self, s):
        brd = s.serialize()[None]
        output = self.model(torch.tensor(brd).float())
        return float(output.data[0][0])



def explore_leaves(s, v):
    ret = []
    for e in s.edges():
        s.board.push(e)
        ret.append((v(s), e))
        s.board.pop()
    return ret


s = State()
v = Valuator()




def computer_move():
    move = sorted(explore_leaves(s, v), key = lambda x: x[0], reverse=s.board.turn)[0]
    print(move)
    s.board.push(move[1])

app = Flask(__name__)

@app.route("/")
def hello():
    ret = '<html><head>'
    ret+= '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>'
    ret+= '<style>button { font-size: 30px; } </style>'
    ret += '</head><body>'
    ret += '<img width=500 height=500 src="/board.svg?%f"></img><br/>' % time.time()
    ret += "<button onclick=\'$.post('/move'); location.reload();\'>Make Computer move</button>"
    return ret


@app.route("/board.svg")
def board():
        return Response(chess.svg.board(board=s.board), mimetype = "image/svg+xml")

@app.route("/move", methods = ["POST"])
def move():
    computer_move()
    return ""


if __name__ == "__main__":
    app.run(debug = True)


#if __name__ == "__main__":
#    v = Valuator()
 #   s = State()
    
  #  while not s.board.is_game_over():
   #     l = sorted(explore_leaves(s, v), key=lambda x: x[0], reverse=s.board.turn)
    #    move = l[0]
     #   print(move)
      #  s.board.push(move[1])

#    print(s.board.result())
