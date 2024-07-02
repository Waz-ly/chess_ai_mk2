import pygame
from chess.GLOBALVARIABLES import *
from ChessGame import ChessGame

def play_self():
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    chessGame = ChessGame(window, WIDTH, HEIGHT)
    chessGame.play_self()

if __name__ == "__main__":
    play_self()