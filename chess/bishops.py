import pygame
from chess.GLOBALVARIABLES import *
from chess.pieces import Pieces
pygame.init()

class Bishops(Pieces):
    def __init__(self, piece, white):
        super().__init__(piece, white, 'B')

    def draw(self, window):
        super().draw(window, 'bishop')

    def get_moves(self, whitePieces, blackPieces):
        sliders = self.pieces
        occupied = whitePieces | blackPieces
        attacks = []

        while sliders != 0b0:
            slider = sliders & -sliders

            for mask in DIAG_MASKS + ANTI_DIAG_MASKS:
                if slider & mask:
                    bishopAttacks = ((occupied & mask) - 2*slider ^ self.binary_reverse(self.binary_reverse(occupied & mask) - 2*self.binary_reverse(slider))) & mask
                    while bishopAttacks != 0b0:
                        attack = bishopAttacks & -bishopAttacks
                        attacks.append((slider, attack))
                        bishopAttacks -= attack
            
            sliders -= slider

        return Pieces.get_moves(self, whitePieces, blackPieces, attacks)

    def get_attacks(self, whitePieces, blackPieces):
        sliders = self.pieces
        occupied = whitePieces | blackPieces
        attacks = 0b0

        while sliders != 0b0:
            slider = sliders & -sliders

            for mask in DIAG_MASKS + ANTI_DIAG_MASKS:
                if slider & mask:
                    attacks |= ((occupied & mask) - 2*slider ^ self.binary_reverse(self.binary_reverse(occupied & mask) - 2*self.binary_reverse(slider))) & mask
            
            sliders -= slider
        
        return attacks