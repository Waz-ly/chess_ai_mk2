import pygame
from chess.GLOBALVARIABLES import *
from chess.pieces import Pieces
pygame.init()

class Rooks(Pieces):
    def __init__(self, piece, white):
        super().__init__(piece, white, 'R')

    def draw(self, window):
        super().draw(window, 'rook')

    def get_moves(self, whitePieces, blackPieces):
        sliders = self.pieces
        occupied = whitePieces | blackPieces
        attacks = []

        while sliders != 0b0:
            slider = sliders & -sliders

            for mask in FILE_MASKS + RANK_MASKS:
                if slider & mask:
                    rookAttacks = ((occupied & mask) - 2*slider ^ self.binary_reverse(self.binary_reverse(occupied & mask) - 2*self.binary_reverse(slider))) & mask
                    while rookAttacks != 0b0:
                        attack = rookAttacks & -rookAttacks
                        attacks.append((slider, attack))
                        rookAttacks -= attack
            
            sliders -= slider
        
        return Pieces.get_moves(self, whitePieces, blackPieces, attacks)

    def get_attacks(self, whitePieces, blackPieces):
        sliders = self.pieces
        occupied = whitePieces | blackPieces
        attacks = 0b0

        while sliders != 0b0:
            slider = sliders & -sliders

            for mask in FILE_MASKS + RANK_MASKS:
                if slider & mask:
                    attacks |= ((occupied & mask) - 2*slider ^ self.binary_reverse(self.binary_reverse(occupied & mask) - 2*self.binary_reverse(slider))) & mask
            
            sliders -= slider
        
        return attacks