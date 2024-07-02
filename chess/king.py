import pygame
from chess.GLOBALVARIABLES import *
from chess.pieces import Pieces
pygame.init()

class King(Pieces):
    def __init__(self, piece, white):
        super().__init__(piece, white, 'K')

    def draw(self, window):
        super().draw(window, 'king')

    def get_moves(self, whitePieces, blackPieces):
        attacks = []

        # up 1 right 1
        kingAttacks = (self.pieces & ~H_FILE & ~EIGHTH_RANK) >> 7
        while kingAttacks != 0b0:
            attack = kingAttacks & -kingAttacks
            attacks.append((attack << 7, attack))
            kingAttacks -= attack

        # up 1
        kingAttacks = (self.pieces & ~EIGHTH_RANK) >> 8
        while kingAttacks != 0b0:
            attack = kingAttacks & -kingAttacks
            attacks.append((attack << 8, attack))
            kingAttacks -= attack

        # up 1 left 1
        kingAttacks = (self.pieces & ~A_FILE & ~EIGHTH_RANK) >> 9
        while kingAttacks != 0b0:
            attack = kingAttacks & -kingAttacks
            attacks.append((attack << 9, attack))
            kingAttacks -= attack

        # left 1
        kingAttacks = (self.pieces & ~A_FILE) >> 1
        while kingAttacks != 0b0:
            attack = kingAttacks & -kingAttacks
            attacks.append((attack << 1, attack))
            kingAttacks -= attack

        # down 1 left 1
        kingAttacks = (self.pieces & ~A_FILE & ~FIRST_RANK) << 7
        while kingAttacks != 0b0:
            attack = kingAttacks & -kingAttacks
            attacks.append((attack >> 7, attack))
            kingAttacks -= attack

        # down 1
        kingAttacks = (self.pieces & ~FIRST_RANK) << 8
        while kingAttacks != 0b0:
            attack = kingAttacks & -kingAttacks
            attacks.append((attack >> 8, attack))
            kingAttacks -= attack

        # down 1 right 1
        kingAttacks = (self.pieces & ~H_FILE & ~FIRST_RANK) << 9
        while kingAttacks != 0b0:
            attack = kingAttacks & -kingAttacks
            attacks.append((attack >> 9, attack))
            kingAttacks -= attack

        # right 1
        kingAttacks = (self.pieces & ~H_FILE) << 1
        while kingAttacks != 0b0:
            attack = kingAttacks & -kingAttacks
            attacks.append((attack >> 1, attack))
            kingAttacks -= attack
        
        return super().get_moves(whitePieces, blackPieces, attacks)

    def get_attacks(self, whitePieces, blackPieces):
        attacks = 0b0

        # up 1 right 1
        attacks |= (self.pieces & ~H_FILE & ~EIGHTH_RANK) >> 7

        # up 1
        attacks |= (self.pieces & ~EIGHTH_RANK) >> 8

        # up 1 left 1
        attacks |= (self.pieces & ~A_FILE & ~EIGHTH_RANK) >> 9

        # left 1
        attacks |= (self.pieces & ~A_FILE) >> 1

        # down 1 left 1
        attacks |= (self.pieces & ~A_FILE & ~FIRST_RANK) << 7

        # down 1
        attacks |= (self.pieces & ~FIRST_RANK) << 8

        # down 1 right 1
        attacks |= (self.pieces & ~H_FILE & ~FIRST_RANK) << 9

        # right 1
        attacks |= (self.pieces & ~H_FILE) << 1

        return attacks