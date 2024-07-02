import pygame
from chess.GLOBALVARIABLES import *
from chess.pieces import Pieces
from chess.bishops import Bishops
from chess.rooks import Rooks
pygame.init()

class Queens(Bishops, Rooks, Pieces):
    def __init__(self, piece, white):
        Pieces.__init__(self, piece, white, 'Q')

    def draw(self, window):
        Pieces.draw(self, window, 'queen')

    def get_moves(self, whitePieces, blackPieces):
        return Bishops.get_moves(self, whitePieces, blackPieces) + Rooks.get_moves(self, whitePieces, blackPieces)

    def get_attacks(self, whitePieces, blackPieces):
        return Bishops.get_attacks(self, whitePieces, blackPieces) | Rooks.get_attacks(self, whitePieces, blackPieces)