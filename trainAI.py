import pygame
import neat
import os
import pickle
from chess.GLOBALVARIABLES import *
from ChessGame import ChessGame

def eval_genomes(genomes, config):
    window = pygame.display.set_mode((28, 0))
    for i in range(len(genomes)):
        genomes[i][1].fitness = 0
        for j in range(len(genomes[i+1:])):
            if genomes[j][1].fitness == None:
                genomes[j][1].fitness = 0
            game = ChessGame(window, 28, 0)
            game.train_ai(genomes[i][1], genomes[j][1], config)

def run_neat(config):
    # train from a certain generation
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-0')
    #
    # train from start
    p = neat.Population(config)
    
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 6)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

if __name__ == "__main__":
    localDirectory = os.path.dirname(__file__)
    configPath = os.path.join(localDirectory, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPath)
    run_neat(config)