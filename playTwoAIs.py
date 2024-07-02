import pygame
import neat
import os
import pickle
from chess.GLOBALVARIABLES import *
from ChessGame import ChessGame

def play_ai(config):
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)

    chessGame = ChessGame(window, WIDTH, HEIGHT)
    chessGame.ai_play_ai(winner, config)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    play_ai(config)