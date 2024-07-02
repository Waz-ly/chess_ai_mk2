import pygame
from chess.GLOBALVARIABLES import *
from chess.pieces import Pieces
pygame.init()

class Knights(Pieces):
    def __init__(self, piece, white):
        super().__init__(piece, white, 'N')

    def draw(self, window):
        super().draw(window, 'knight')

    def get_moves(self, whitePieces, blackPieces):
        attacks = []

        # up 2 right 1
        knightAttacks = (self.pieces & ~H_FILE & ~EIGHTH_RANK & ~SEVENTH_RANK) >> 15
        while knightAttacks != 0b0:
            attack = knightAttacks & -knightAttacks
            attacks.append((attack << 15, attack))
            knightAttacks -= attack

        # up 2 left 1
        knightAttacks = (self.pieces & ~A_FILE & ~EIGHTH_RANK & ~SEVENTH_RANK) >> 17
        while knightAttacks != 0b0:
            attack = knightAttacks & -knightAttacks
            attacks.append((attack << 17, attack))
            knightAttacks -= attack

        # up 1 right 2
        knightAttacks = (self.pieces & ~H_FILE & ~G_FILE & ~EIGHTH_RANK) >> 6
        while knightAttacks != 0b0:
            attack = knightAttacks & -knightAttacks
            attacks.append((attack << 6, attack))
            knightAttacks -= attack

        # up 1 left 2
        knightAttacks = (self.pieces & ~A_FILE & ~B_FILE & ~EIGHTH_RANK) >> 10
        while knightAttacks != 0b0:
            attack = knightAttacks & -knightAttacks
            attacks.append((attack << 10, attack))
            knightAttacks -= attack

        # down 2 right 1
        knightAttacks = (self.pieces & ~H_FILE & ~FIRST_RANK & ~SECOND_RANK) << 17
        while knightAttacks != 0b0:
            attack = knightAttacks & -knightAttacks
            attacks.append((attack >> 17, attack))
            knightAttacks -= attack

        # down 2 left 1
        knightAttacks = (self.pieces & ~A_FILE & ~FIRST_RANK & ~SECOND_RANK) << 15
        while knightAttacks != 0b0:
            attack = knightAttacks & -knightAttacks
            attacks.append((attack >> 15, attack))
            knightAttacks -= attack

        # down 1 right 2
        knightAttacks = (self.pieces & ~H_FILE & ~G_FILE & ~FIRST_RANK) << 10
        while knightAttacks != 0b0:
            attack = knightAttacks & -knightAttacks
            attacks.append((attack >> 10, attack))
            knightAttacks -= attack

        # down 1 left 2
        knightAttacks = (self.pieces & ~A_FILE & ~B_FILE & ~FIRST_RANK) << 6
        while knightAttacks != 0b0:
            attack = knightAttacks & -knightAttacks
            attacks.append((attack >> 6, attack))
            knightAttacks -= attack
        
        return super().get_moves(whitePieces, blackPieces, attacks)
    
    def get_attacks(self, whitePieces, blackPieces):
        attacks = 0b0

        # up 2 right 1
        attacks |= (self.pieces & ~H_FILE & ~EIGHTH_RANK & ~SEVENTH_RANK) >> 15

        # up 2 left 1
        attacks |= (self.pieces & ~A_FILE & ~EIGHTH_RANK & ~SEVENTH_RANK) >> 17

        # up 1 right 2
        attacks |= (self.pieces & ~H_FILE & ~G_FILE & ~EIGHTH_RANK) >> 6

        # up 1 left 2
        attacks |= (self.pieces & ~A_FILE & ~B_FILE & ~EIGHTH_RANK) >> 10

        # down 2 right 1
        attacks |= (self.pieces & ~H_FILE & ~FIRST_RANK & ~SECOND_RANK) << 17

        # down 2 left 1
        attacks |= (self.pieces & ~A_FILE & ~FIRST_RANK & ~SECOND_RANK) << 15

        # down 1 right 2
        attacks |= (self.pieces & ~H_FILE & ~G_FILE & ~FIRST_RANK) << 10

        # down 1 left 2
        attacks |= (self.pieces & ~A_FILE & ~B_FILE & ~FIRST_RANK) << 6

        return attacks