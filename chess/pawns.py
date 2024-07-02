import pygame
from chess.GLOBALVARIABLES import *
from chess.pieces import Pieces
pygame.init()

class Pawns(Pieces):
    def __init__(self, piece, white):
        super().__init__(piece, white, 'P')

    def draw(self, window):
        super().draw(window, 'pawn')

    def get_moves(self, whitePieces, blackPieces):
        moves = []

        # white pawn moves
        if self.white:
            # 1 square forward
            pawnMoves = (self.pieces >> 8) & ~whitePieces & ~blackPieces
            while pawnMoves != 0b0:
                move = pawnMoves & -pawnMoves
                moves.append((move << 8, move))
                pawnMoves -= move

            # 2 squares forward
            pawnMoves = (self.pieces >> 16) & FOURTH_RANK & ~whitePieces & ~blackPieces & (~whitePieces >> 8) & (~blackPieces >> 8)
            while pawnMoves != 0b0:
                move = pawnMoves & -pawnMoves
                moves.append((move << 16, move))
                pawnMoves -= move

            # attack to the right
            pawnMoves = (self.pieces >> 7) & ~A_FILE & blackPieces
            while pawnMoves != 0b0:
                attack = pawnMoves & -pawnMoves
                moves.append((attack << 7, attack))
                pawnMoves -= attack

            # attack to the left
            pawnMoves = (self.pieces >> 9) & ~H_FILE & blackPieces
            while pawnMoves != 0b0:
                attack = pawnMoves & -pawnMoves
                moves.append((attack << 9, attack))
                pawnMoves -= attack

        #black pawn moves
        else:
            # 1 square forward
            pawnMoves = (self.pieces << 8) & ~(FIRST_RANK << 8) & ~whitePieces & ~blackPieces
            while pawnMoves != 0b0:
                move = pawnMoves & -pawnMoves
                moves.append((move >> 8, move))
                pawnMoves -= move

            # 2 squares forward
            pawnMoves = (self.pieces << 16) & FIFTH_RANK & ~whitePieces & ~blackPieces & (~whitePieces << 8) & (~blackPieces << 8)
            while pawnMoves != 0b0:
                move = pawnMoves & -pawnMoves
                moves.append((move >> 16, move))
                pawnMoves -= move

            # attack to the left
            pawnMoves = (self.pieces << 7) & ~H_FILE & whitePieces
            while pawnMoves != 0b0:
                attack = pawnMoves & -pawnMoves
                moves.append((attack >> 7, attack))
                pawnMoves -= attack

            # attack to the right
            pawnMoves = (self.pieces << 9) & ~A_FILE & whitePieces
            while pawnMoves != 0b0:
                attack = pawnMoves & -pawnMoves
                moves.append((attack >> 9, attack))
                pawnMoves -= attack
        
        return moves

    def get_attacks(self, whitePieces, blackPieces):
        attacks = 0b0

        # white pawn attacks
        if self.white:
            # to the right
            attacks |= (self.pieces >> 7) & ~A_FILE

            # to the left
            attacks |= (self.pieces >> 9) & ~H_FILE

        #black pawn attacks
        else:
            # to the left
            attacks |= (self.pieces << 7) & ~H_FILE

            # to the right
            attacks |= (self.pieces << 9) & ~A_FILE

        return attacks