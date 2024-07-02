import pygame
import os
from chess.GLOBALVARIABLES import *
pygame.init()

class Pieces:
    def __init__(self, pieces, white, pieceType):
        self.pieces = pieces
        self.white = white
        self.pieceType = pieceType

    def draw(self, window, piece_type):
        piece_checker = self.pieces
        color = ''
        if self.white:
            color = 'white'
        else:
            color = 'black'
            
        for square in range(64):
            if piece_checker % 2:
                square_x = square%8
                square_y = square//8

                piece_image = pygame.image.load(os.path.join('assets', color + '_' + piece_type + '.webp'))
                piece_image = pygame.transform.scale(piece_image, (PIECESIZE, PIECESIZE))
                window.blit(piece_image, (BUFFER + square_x * PIECESIZE, BUFFER + square_y * PIECESIZE))
            piece_checker >>= 1

    def get_pieces(self):
        return self.pieces

    # not necessarily legal moves, but is psuedo-legal, ie could put the king into check
    def get_moves(self, whitePieces, blackPieces, attacks):
        numberOfAttacks = len(attacks)
        for i in range(numberOfAttacks):
            if self.white:
                if attacks[numberOfAttacks - i - 1][1] & whitePieces:
                    attacks.pop(numberOfAttacks - i - 1)
            else:
                if attacks[numberOfAttacks - i - 1][1] & blackPieces:
                    attacks.pop(numberOfAttacks - i - 1)
        
        return attacks

    def get_attacks(self, whitePieces, blackPieces):
        return []

    # doesn't check if the move is legal
    def make_move(self, move):
        self.remove_piece(move[0])
        self.add_piece(move[1])
    
    def remove_piece(self, square):
        self.pieces &= ~square

    def add_piece(self, square):
        self.pieces |= square

    def binary_reverse(self, number):
        number = (number & 0b1111111111111111111111111111111100000000000000000000000000000000) >> 32 | (number & 0b0000000000000000000000000000000011111111111111111111111111111111) << 32
        number = (number & 0b1111111111111111000000000000000011111111111111110000000000000000) >> 16 | (number & 0b0000000000000000111111111111111100000000000000001111111111111111) << 16
        number = (number & 0b1111111100000000111111110000000011111111000000001111111100000000) >> 8  | (number & 0b0000000011111111000000001111111100000000111111110000000011111111) << 8
        number = (number & 0b1111000011110000111100001111000011110000111100001111000011110000) >> 4  | (number & 0b0000111100001111000011110000111100001111000011110000111100001111) << 4
        number = (number & 0b1100110011001100110011001100110011001100110011001100110011001100) >> 2  | (number & 0b0011001100110011001100110011001100110011001100110011001100110011) << 2
        number = (number & 0b1010101010101010101010101010101010101010101010101010101010101010) >> 1  | (number & 0b0101010101010101010101010101010101010101010101010101010101010101) << 1
        return number