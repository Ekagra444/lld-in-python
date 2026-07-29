from copy import deepcopy
class ChessPiece:
    def __init__(self, piecename:str,pieceposition:str):
        self.piecename = piecename
        self.pieceposition = pieceposition
    def clone(self):
        return deepcopy(self)
    def info(self):
        print(f'{self.piecename} is at {self.pieceposition}')

# cp = ChessPiece("king","e4")

# cpp= cp.clone()

# print(id(cp))
# print(id(cpp))
