import neat
import os
import pickle
from chess.GLOBALVARIABLES import *
from chess.Game import Game
import neat
import random
from math import pow
from chess.GLOBALVARIABLES import *
import concurrent.futures

# function used to train AI
def train_ai(packet):
    genome1 = packet[0]
    genome2 = packet[1]
    config = packet[2]
    genome1ID = packet[3]
    genome2ID = packet[4]

    game = Game(None, None, None)
    net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
    net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
    lastLastMoves = []
    lastMoves = []

    gameInfo = game.loop([])
    swapColors = not random.getrandbits(1)
    run = True
    while run:
        if game.whitesTurn == True and not swapColors or not game.whitesTurn and swapColors:
            if not swapColors:
                maxOutput = -1.7976931348623157e+308
            else:
                minOutput = 1.7976931348623157e+308
            bestMove = gameInfo.possibleMoves
            for moves in gameInfo.possibleMoves:
                for move in moves:
                    output1 = net1.activate(game.try_move(move))[0]
                    if not swapColors:
                        if output1 > maxOutput:
                            maxOutput = output1
                            bestMove = move
                    else:
                        if output1 < minOutput:
                            minOutput = output1
                            bestMove = move
            game.make_move(bestMove)
        else:
            if swapColors:
                maxOutput = -1.7976931348623157e+308
            else:
                minOutput = 1.7976931348623157e+308
            bestMove = gameInfo.possibleMoves
            for moves in gameInfo.possibleMoves:
                for move in moves:
                    output2 = net2.activate(game.try_move(move))[0]
                    if swapColors:
                        if output2 > maxOutput:
                            maxOutput = output2
                            bestMove = move
                    else:
                        if output2 < minOutput:
                            minOutput = output2
                            bestMove = move
            game.make_move(bestMove)

        lastLastMoves = lastMoves
        lastMoves = gameInfo.possibleMoves
        gameInfo = game.loop(lastLastMoves)

        if gameInfo.gameStatus == 'B' or gameInfo.gameStatus == 'W' or gameInfo.gameStatus == 'D':
            return calculate_fitness(genome1, genome2, gameInfo, genome1ID, genome2ID, swapColors)

def calculate_fitness(genome1, genome2, gameInfo, genome1ID, genome2ID, swapColors):
    genome1Effective = genome1.fitness
    genome2Effective = genome2.fitness
    if abs(genome1Effective - 1200.0) < 1.0:
        genome1Effective = 1000.0
    if abs(genome2Effective - 1200.0) < 1.0:
        genome2Effective = 1000.0

    expectedOutcome = 1/(1+pow(10, (genome2Effective - genome1Effective)/DAMPINGFACTOR))
    actualOutcome = 0
    if gameInfo.gameStatus == 'B':
        if swapColors:
            actualOutcome = 1
        else:
            actualOutcome = 0
    elif gameInfo.gameStatus == 'W':
        if swapColors:
            actualOutcome = 0
        else:
            actualOutcome = 1
    elif gameInfo.gameStatus == 'D':
        actualOutcome = 0.5
    genomeBonus = SCALINGFACTOR*(actualOutcome - expectedOutcome)
    return(genomeBonus, -genomeBonus, genome1ID, genome2ID)

def eval_genomes(genomes, config):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        fitnesses = []
        gamesPlayed = []
        for i in range(len(genomes)):
            if genomes[i][1].fitness == None:
                genomes[i][1].fitness = INITIALELO
            gamesPlayed.append(0)
            for j in range(len(genomes[i+1:])):
                if genomes[j][1].fitness == None:
                    genomes[j][1].fitness = INITIALELO
                if random.random() < GAMESPLAYEDFRACTION:
                    fitnesses.append(executor.submit(train_ai, (genomes[i][1], genomes[j][1], config, i, j)))

        for f in concurrent.futures.as_completed(fitnesses):
            fitness = f.result()
            genomes[fitness[2]][1].fitness += fitness[0]
            genomes[fitness[3]][1].fitness += fitness[1]

def run_neat(config):
    # train from a certain generation
    p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-0")
    #
    # train from start
    # p = neat.Population(config)
    
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 1)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

if __name__ == "__main__":
    localDirectory = os.path.dirname(__file__)
    configPath = os.path.join(localDirectory, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPath)
    run_neat(config)

# i must not fear. fear is the mind killer.
#   - Aiden Yu 6/12/2024