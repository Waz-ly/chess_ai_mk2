import pygame
from chess.Game import Game
import neat
from random import getrandbits
from chess.GLOBALVARIABLES import *

class ChessGame:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.lastMoves = []
        self.lastLastMoves = []

    # function used to play against one's self
    def play_self(self):
        clock = pygame.time.Clock()
        run = True
        pressed = False
        clicked = False
        moveMade = False
        gameInfo = self.game.loop([])
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pressed = True
                elif event.type == pygame.MOUSEBUTTONUP and pygame.mouse.get_pos()[0] > 0 and pygame.mouse.get_pos()[1] > 0 and pygame.mouse.get_pos()[0] < WIDTH and pygame.mouse.get_pos()[1] < HEIGHT and pressed:
                    pressed = False
                    clicked = not clicked
                    if pygame.mouse.get_pos()[0] - BUFFER < BOARDSIZE and pygame.mouse.get_pos()[1] - BUFFER < BOARDSIZE and pygame.mouse.get_pos()[1] - BUFFER > 0 and pygame.mouse.get_pos()[0] - BUFFER > 0:
                        if clicked:
                            square1 = 0b1
                            square1 <<= (pygame.mouse.get_pos()[0] - BUFFER) // PIECESIZE + 8 * ((pygame.mouse.get_pos()[1] - BUFFER) // PIECESIZE)
                        if not clicked:
                            square2 = 0b1
                            square2 <<= (pygame.mouse.get_pos()[0] - BUFFER) // PIECESIZE + 8 * ((pygame.mouse.get_pos()[1] - BUFFER) // PIECESIZE)

                            move = (square1, square2)
                            for moves in gameInfo.possibleMoves:
                                if move in moves:
                                    self.game.make_move(move)
                                    moveMade = True

            if moveMade:
                self.lastLastMoves = self.lastMoves
                self.lastMoves = gameInfo.possibleMoves
                gameInfo = self.game.loop(self.lastLastMoves)
                moveMade = False
            self.game.draw()

            if gameInfo.gameStatus == 'B':
                pygame.draw.rect(self.game.window, BLACK, (BUFFER + BOARDSIZE//2 - PIECESIZE*10//3, BUFFER + BOARDSIZE//2 - PIECESIZE//2, PIECESIZE*20//3, PIECESIZE))
                game_end_text = FONT_END.render(f"BLACK WINS", 1, WHITE)
                self.game.window.blit(game_end_text, (BUFFER + BOARDSIZE//2 - PIECESIZE*3, BUFFER + BOARDSIZE//2 - PIECESIZE//2))
            elif gameInfo.gameStatus == 'W':
                pygame.draw.rect(self.game.window, BLACK, (BUFFER + BOARDSIZE//2 - PIECESIZE*7//2, BUFFER + BOARDSIZE//2 - PIECESIZE//2, PIECESIZE*7, PIECESIZE))
                game_end_text = FONT_END.render(f"WHITE WINS", 1, WHITE)
                self.game.window.blit(game_end_text, (BUFFER + BOARDSIZE//2 - PIECESIZE*3, BUFFER + BOARDSIZE//2 - PIECESIZE//2))
            elif gameInfo.gameStatus == 'D':
                pygame.draw.rect(self.game.window, BLACK, (BUFFER + BOARDSIZE//2 - PIECESIZE*3//2, BUFFER + BOARDSIZE//2 - PIECESIZE//2, PIECESIZE*3, PIECESIZE))
                game_end_text = FONT_END.render(f"DRAW", 1, WHITE)
                self.game.window.blit(game_end_text, (BUFFER + BOARDSIZE//2 - 3*PIECESIZE//2, BUFFER + BOARDSIZE//2 - PIECESIZE//2))

            pygame.display.update()

        pygame.quit()

    # function used to play against a trained AI
    def play_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        clock = pygame.time.Clock()
        run = True
        pressed = False
        clicked = False
        gameInfo = self.game.loop([])
        moveMade = False
        while run:
            clock.tick(60)

            if not self.game.whitesTurn:
                minOutput = 1.7976931348623157e+308
                bestMove = gameInfo.possibleMoves[0]
                for moves in gameInfo.possibleMoves:
                    for move in moves:
                        output2 = net.activate(self.game.try_move(move))[0]
                        if output2 < minOutput:
                            minOutput = output2
                            bestMove = move
                self.game.make_move(bestMove)
                moveMade = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pressed = True
                elif event.type == pygame.MOUSEBUTTONUP and pygame.mouse.get_pos()[0] > 0 and pygame.mouse.get_pos()[1] > 0 and pygame.mouse.get_pos()[0] < WIDTH and pygame.mouse.get_pos()[1] < HEIGHT and pressed:
                    pressed = False
                    clicked = not clicked
                    if pygame.mouse.get_pos()[0] - BUFFER < BOARDSIZE and pygame.mouse.get_pos()[1] - BUFFER < BOARDSIZE:
                        if clicked:
                            square1 = 0b1
                            square1 <<= (pygame.mouse.get_pos()[0] - BUFFER) // PIECESIZE + 8 * ((pygame.mouse.get_pos()[1] - BUFFER) // PIECESIZE)
                        if not clicked:
                            square2 = 0b1
                            square2 <<= (pygame.mouse.get_pos()[0] - BUFFER) // PIECESIZE + 8 * ((pygame.mouse.get_pos()[1] - BUFFER) // PIECESIZE)

                            move = (square1, square2)
                            if self.game.whitesTurn:
                                for moves in gameInfo.possibleMoves:
                                    if move in moves:
                                        self.game.make_move(move)
                                        moveMade = True

            if moveMade:
                self.lastLastMoves = self.lastMoves
                self.lastMoves = gameInfo.possibleMoves
                gameInfo = self.game.loop(self.lastLastMoves)
                moveMade = False
            self.game.draw()

            if gameInfo.gameStatus == 'B':
                pygame.draw.rect(self.game.window, BLACK, (BUFFER + BOARDSIZE//2 - PIECESIZE*10//3, BUFFER + BOARDSIZE//2 - PIECESIZE//2, PIECESIZE*20//3, PIECESIZE))
                game_end_text = FONT_END.render(f"BLACK WINS", 1, WHITE)
                self.game.window.blit(game_end_text, (BUFFER + BOARDSIZE//2 - PIECESIZE*3, BUFFER + BOARDSIZE//2 - PIECESIZE//2))
                run = False
            elif gameInfo.gameStatus == 'W':
                pygame.draw.rect(self.game.window, BLACK, (BUFFER + BOARDSIZE//2 - PIECESIZE*7//2, BUFFER + BOARDSIZE//2 - PIECESIZE//2, PIECESIZE*7, PIECESIZE))
                game_end_text = FONT_END.render(f"WHITE WINS", 1, WHITE)
                self.game.window.blit(game_end_text, (BUFFER + BOARDSIZE//2 - PIECESIZE*3, BUFFER + BOARDSIZE//2 - PIECESIZE//2))
                run = False
            elif gameInfo.gameStatus == 'D':
                pygame.draw.rect(self.game.window, BLACK, (BUFFER + BOARDSIZE//2 - PIECESIZE*3//2, BUFFER + BOARDSIZE//2 - PIECESIZE//2, PIECESIZE*3, PIECESIZE))
                game_end_text = FONT_END.render(f"DRAW", 1, WHITE)
                self.game.window.blit(game_end_text, (BUFFER + BOARDSIZE//2 - 3*PIECESIZE//2, BUFFER + BOARDSIZE//2 - PIECESIZE//2))
                run = False

            pygame.display.update()

        run = True
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

        pygame.quit()

    def ai_play_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        clock = pygame.time.Clock()
        run = True
        gameInfo = self.game.loop([])
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            if not self.game.whitesTurn:
                minOutput = 1.7976931348623157e+308
                bestMove = gameInfo.possibleMoves[0]
                for moves in gameInfo.possibleMoves:
                    for move in moves:
                        output2 = net.activate(self.game.try_move(move))[0]
                        if output2 < minOutput:
                            minOutput = output2
                            bestMove = move
                self.game.make_move(bestMove)

            else:
                maxOutput = -1.7976931348623157e+308
                bestMove = gameInfo.possibleMoves[0]
                for moves in gameInfo.possibleMoves:
                    for move in moves:
                        output2 = net.activate(self.game.try_move(move))[0]
                        if output2 > maxOutput:
                            maxOutput = output2
                            bestMove = move
                self.game.make_move(bestMove)

            self.lastLastMoves = self.lastMoves
            self.lastMoves = gameInfo.possibleMoves
            gameInfo = self.game.loop(self.lastLastMoves)
            self.game.draw()

            if gameInfo.gameStatus == 'B':
                pygame.draw.rect(self.game.window, BLACK, (BUFFER + BOARDSIZE//2 - PIECESIZE*10//3, BUFFER + BOARDSIZE//2 - PIECESIZE//2, PIECESIZE*20//3, PIECESIZE))
                game_end_text = FONT_END.render(f"BLACK WINS", 1, WHITE)
                self.game.window.blit(game_end_text, (BUFFER + BOARDSIZE//2 - PIECESIZE*3, BUFFER + BOARDSIZE//2 - PIECESIZE//2))
                run = False
            elif gameInfo.gameStatus == 'W':
                pygame.draw.rect(self.game.window, BLACK, (BUFFER + BOARDSIZE//2 - PIECESIZE*7//2, BUFFER + BOARDSIZE//2 - PIECESIZE//2, PIECESIZE*7, PIECESIZE))
                game_end_text = FONT_END.render(f"WHITE WINS", 1, WHITE)
                self.game.window.blit(game_end_text, (BUFFER + BOARDSIZE//2 - PIECESIZE*3, BUFFER + BOARDSIZE//2 - PIECESIZE//2))
                run = False
            elif gameInfo.gameStatus == 'D':
                pygame.draw.rect(self.game.window, BLACK, (BUFFER + BOARDSIZE//2 - PIECESIZE*3//2, BUFFER + BOARDSIZE//2 - PIECESIZE//2, PIECESIZE*3, PIECESIZE))
                game_end_text = FONT_END.render(f"DRAW", 1, WHITE)
                self.game.window.blit(game_end_text, (BUFFER + BOARDSIZE//2 - 3*PIECESIZE//2, BUFFER + BOARDSIZE//2 - PIECESIZE//2))
                run = False

            pygame.display.update()
            pygame.time.delay(50)

        run = True
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

        pygame.quit()

    # function used to train AI
    def train_ai(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        gameInfo = self.game.loop([])
        swapColors = not getrandbits(1)
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            if self.game.whitesTurn == True and not swapColors or not self.game.whitesTurn and swapColors:
                if not swapColors:
                    maxOutput = -1.7976931348623157e+308
                else:
                    minOutput = 1.7976931348623157e+308
                bestMove = gameInfo.possibleMoves
                for moves in gameInfo.possibleMoves:
                    for move in moves:
                        output1 = net1.activate(self.game.try_move(move))[0]
                        if not swapColors:
                            if output1 > maxOutput:
                                maxOutput = output1
                                bestMove = move
                        else:
                            if output1 < minOutput:
                                minOutput = output1
                                bestMove = move
                self.game.make_move(bestMove)
            else:
                if swapColors:
                    maxOutput = -1.7976931348623157e+308
                else:
                    minOutput = 1.7976931348623157e+308
                bestMove = gameInfo.possibleMoves
                for moves in gameInfo.possibleMoves:
                    for move in moves:
                        output2 = net2.activate(self.game.try_move(move))[0]
                        if swapColors:
                            if output2 > maxOutput:
                                maxOutput = output2
                                bestMove = move
                        else:
                            if output2 < minOutput:
                                minOutput = output2
                                bestMove = move
                self.game.make_move(bestMove)

            self.lastLastMoves = self.lastMoves
            self.lastMoves = gameInfo.possibleMoves
            gameInfo = self.game.loop(self.lastLastMoves)

            if gameInfo.gameStatus == 'B' or gameInfo.gameStatus == 'W' or gameInfo.gameStatus == 'D':
                return self.calculate_fitness(genome1, genome2, gameInfo)

    def calculate_fitness(self, genome1, genome2, gameInfo):
        if gameInfo.gameStatus == 'B':
            genome2.fitness += WINBONUS
            # genome2.fitness += 400 // gameInfo.moveCounter
        elif gameInfo.gameStatus == 'W':
            genome1.fitness += WINBONUS
            # genome1.fitness += 400 // gameInfo.moveCounter
        elif gameInfo.gameStatus == 'D':
            genome1.fitness += DRAWBONUS
            genome2.fitness += DRAWBONUS
        return(genome1.fitness, genome2.fitness)
            
    # i must not fear. fear is the mind killer.
    #   - Aiden Yu 6/12/2024