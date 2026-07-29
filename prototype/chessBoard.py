from typing import List
from chessPiece import ChessPiece
from copy import deepcopy
class ChessBoard:
    def __init__(self):
        self.pieces:List[ChessPiece] = []
    def addPiece(self,chessPiece: 'ChessPiece'):
        self.pieces.append(chessPiece)
    def showBoard(self):
        print('----------------')
        print('Printing the board')
        for p in self.pieces:
            p.info()
    def cloneBoard(self):
        return deepcopy(self)

king = ChessPiece('king','e4')
queen = ChessPiece('queen','h1')
soldier = ChessPiece('soldier','a5')

cb = ChessBoard()
cb.addPiece(king)
cb.addPiece(queen)
cb.addPiece(soldier)
cb.showBoard()

cbb = cb.cloneBoard()

eleph = ChessPiece('eleph','f1')
cbb.addPiece(eleph)
cbb.showBoard()
