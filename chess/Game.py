import pygame
from chess.GLOBALVARIABLES import *
from copy import copy
from chess.pawns import Pawns
from chess.bishops import Bishops
from chess.rooks import Rooks
from chess.knights import Knights
from chess.king import King
from chess.queens import Queens
pygame.init()

class GameInformation:
    def __init__(self, gameStatus, possibleMoves):
        self.gameStatus = gameStatus
        self.possibleMoves = possibleMoves
        self.whiteKingMoved = False
        self.blackKingMoved = False
        self.A1RookMoved = False
        self.A8RookMoved = False
        self.H1RookMoved = False
        self.H8RookMoved = False
        self.enpessantAvailable = 0b0
        self.fiftyMoveRuleCounter = 0
        self.moveCounter = 0
        self.previousWhiteMove = (0b0, 0b0)
        self.previousBlackMove = (0b0, 0b0)
        self.previousWhitePosition = [Pawns(0b0, True), Pawns(0b0, False), Rooks(0b0, True), Rooks(0b0, False),
                                      Knights(0b0, True), Knights(0b0, False), Bishops(0b0, True), Bishops(0b0, False),
                                      Queens(0b0, True), Queens(0b0, False), King(0b0, True), King(0b0, False)]
        self.previousBlackPosition = [Pawns(0b0, True), Pawns(0b0, False), Rooks(0b0, True), Rooks(0b0, False),
                                      Knights(0b0, True), Knights(0b0, False), Bishops(0b0, True), Bishops(0b0, False),
                                      Queens(0b0, True), Queens(0b0, False), King(0b0, True), King(0b0, False)]

class Game:
    def __init__(self, window, width, height):
        self.width = width
        self.height = height
        self.window = window

        self.whitePawns   = Pawns(INITWHITEPAWNS, True)
        self.blackPawns   = Pawns(INITBLACKPAWNS, False)
        self.whiteRooks   = Rooks(INITWHITEROOKS, True)
        self.blackRooks   = Rooks(INITBLACKROOKS, False)
        self.whiteKnights = Knights(INITWHITEKNIGHTS, True)
        self.blackKnights = Knights(INITBLACKKNIGHTS, False)
        self.whiteBishops = Bishops(INITWHITEBISHOPS, True)
        self.blackBishops = Bishops(INITBLACKBISHOPS, False)
        self.whiteQueens  = Queens(INITWHITEQUEENS, True)
        self.blackQueens  = Queens(INITBLACKQUEENS, False)
        self.whiteKing    = King(INITWHITEKING, True)
        self.blackKing    = King(INITBLACKKING, False)
        
        self.pieces = [self.whitePawns, self.blackPawns, self.whiteRooks, self.blackRooks, self.whiteKnights, self.blackKnights, 
                       self.whiteBishops, self.blackBishops, self.whiteQueens, self.blackQueens, self.whiteKing, self.blackKing]

        self.whitePieces = (self.whitePawns.get_pieces() | self.whiteRooks.get_pieces() | self.whiteKnights.get_pieces() | 
                            self.whiteBishops.get_pieces() | self.whiteQueens.get_pieces() | self.whiteKing.get_pieces())
        self.blackPieces = (self.blackPawns.get_pieces() | self.blackRooks.get_pieces() | self.blackKnights.get_pieces() | 
                            self.blackBishops.get_pieces() | self.blackQueens.get_pieces() | self.blackKing.get_pieces())

        self.gameInfo = GameInformation('O', [])
        self.whitesTurn = True

    def draw(self):
        self.window.fill(BACKROUND)
        for square in range(64):
            if (square % 8 + square // 8) % 2 == 1:
                pygame.draw.rect(self.window, DARK_SQUARES, (BUFFER + square % 8 * SQUARESIZE, 
                                                             BUFFER + square // 8 * SQUARESIZE, 
                                                             SQUARESIZE, SQUARESIZE))
            else:
                pygame.draw.rect(self.window, LIGHT_SQUARES, (BUFFER + square % 8 * SQUARESIZE, 
                                                              BUFFER + square // 8 * SQUARESIZE, 
                                                              SQUARESIZE, SQUARESIZE))

        for piece in self.pieces:
            piece.draw(self.window)

    # checks if the game is over
    def loop(self, previousMoves):
        movesAvailable = False
        possibleMoves = []
        if self.whitesTurn:
            possibleMoves = self.get_white_moves(previousMoves)
            for moves in possibleMoves:
                if moves:
                    movesAvailable = True
        else:
            possibleMoves = self.get_black_moves(previousMoves)
            for moves in possibleMoves:
                if moves:
                    movesAvailable = True
        self.gameInfo.possibleMoves = possibleMoves
        
        if not movesAvailable:
            attacks = 0b0
            for piece in self.pieces:
                if piece.white != self.whitesTurn:
                    attacks |= piece.get_attacks(self.whitePieces, self.blackPieces)

            if self.whitesTurn and self.whiteKing.get_pieces() & attacks:
                self.gameInfo.gameStatus = 'B'
            elif not self.whitesTurn and self.blackKing.get_pieces() & attacks:
                self.gameInfo.gameStatus = 'W'
            else:
                self.gameInfo.gameStatus = 'D'
        
        if self.gameInfo.fiftyMoveRuleCounter == 100:
            self.gameInfo.gameStatus = 'D'

        return self.gameInfo

    # checks that the move doesn't put the king into check, but not if it is psuedo-legal
    def test_move(self, move, attacks):
        # creates phantom board
        newPieces = []
        for piece in self.pieces:
            newPieces.append(copy(piece))

        # makes the move on the phantom board
        for piece in newPieces:
            if move[0] & piece.get_pieces():
                piece.make_move(move)
                for oppPiece in newPieces:
                    if piece.white != oppPiece.white:
                        oppPiece.remove_piece(move[1])
                break
        
        recalcAll = False
        # special moves
        if self.whitesTurn:
            if not self.gameInfo.whiteKingMoved:
                if not self.gameInfo.A1RookMoved and move == (INITWHITEKING, INITWHITEKING >> 2):
                    newPieces[2].make_move((A_FILE & FIRST_RANK, INITWHITEKING >> 1))
                    recalcAll = True
                elif not self.gameInfo.H1RookMoved and move == (INITWHITEKING, INITWHITEKING << 2):
                    newPieces[2].make_move((H_FILE & FIRST_RANK, INITWHITEKING << 1))
                    recalcAll = True

            elif self.gameInfo.enpessantAvailable:
                if move == (self.gameInfo.enpessantAvailable << 1, self.gameInfo.enpessantAvailable >> 8):
                    newPieces[1].remove_piece(self.gameInfo.enpessantAvailable)
                    recalcAll = True
                elif move == (self.gameInfo.enpessantAvailable >> 1, self.gameInfo.enpessantAvailable >> 8):
                    newPieces[1].remove_piece(self.gameInfo.enpessantAvailable)
                    recalcAll = True
            
            elif move[1] & newPieces[0].get_pieces() & EIGHTH_RANK:
                newPieces[0].remove_piece(move[1])
                newPieces[8].add_piece(move[1])
                recalcAll = True
        else:
            if not self.gameInfo.blackKingMoved:
                if not self.gameInfo.A8RookMoved and move == (INITBLACKKING, INITBLACKKING >> 2):
                    newPieces[3].make_move((A_FILE & EIGHTH_RANK, INITBLACKKING >> 1))
                    recalcAll = True
                elif not self.gameInfo.H8RookMoved and move == (INITBLACKKING, INITBLACKKING << 2):
                    newPieces[3].make_move((H_FILE & EIGHTH_RANK, INITBLACKKING << 1))
                    recalcAll = True

            elif self.gameInfo.enpessantAvailable:
                if move == (self.gameInfo.enpessantAvailable << 1, self.gameInfo.enpessantAvailable << 8):
                    newPieces[0].remove_piece(self.gameInfo.enpessantAvailable)
                    recalcAll = True
                elif move == (self.gameInfo.enpessantAvailable >> 1, self.gameInfo.enpessantAvailable << 8):
                    newPieces[0].remove_piece(self.gameInfo.enpessantAvailable)
                    recalcAll = True

            elif move[1] & newPieces[1].get_pieces() & FIRST_RANK:
                newPieces[1].remove_piece(move[1])
                newPieces[9].add_piece(move[1])
                recalcAll = True
        
        # determines white and black pieces on the phantom board
        whitePieces = 0b0
        blackPieces = 0b0
        if self.whitesTurn:
            whitePieces = self.whitePieces & ~move[0] | move[1]
            blackPieces = self.blackPieces & ~move[1]
        else:
            whitePieces = self.whitePieces & ~move[1]
            blackPieces = self.blackPieces & ~move[0] | move[1]

        # determines unsafe squares
        unsafeSquares = attacks[-1]

        if self.whitesTurn:
            addOne = 1
        else:
            addOne = 0

        recalcBishops = newPieces[6 + addOne].get_pieces() != self.pieces[6 + addOne].get_pieces()
        recalcQueens = newPieces[8 + addOne].get_pieces() != self.pieces[8 + addOne].get_pieces()
        recalcRooks = newPieces[2 + addOne].get_pieces() != self.pieces[2 + addOne].get_pieces()
        
        for mask in DIAG_MASKS + ANTI_DIAG_MASKS:
            if mask & (move[0] | move[1]) and mask & newPieces[6 + addOne].get_pieces() and mask & newPieces[-1 - addOne].get_pieces():
                recalcBishops = True
            if mask & (move[0] | move[1]) and mask & newPieces[8 + addOne].get_pieces() and mask & newPieces[-1 - addOne].get_pieces():
                recalcQueens = True
        for mask in FILE_MASKS + RANK_MASKS:
            if mask & (move[0] | move[1]) and mask & newPieces[2 + addOne].get_pieces() and mask & newPieces[-1 - addOne].get_pieces():
                recalcRooks = True
            if mask & (move[0] | move[1]) and mask & newPieces[8 + addOne].get_pieces() and mask & newPieces[-1 - addOne].get_pieces():
                recalcQueens = True

        if move[1] & self.pieces[0 + addOne].get_pieces() or recalcAll:
            unsafeSquares |= newPieces[0 + addOne].get_attacks(whitePieces, blackPieces)
        else:
            unsafeSquares |= attacks[0]

        if move[1] & self.pieces[4 + addOne].get_pieces() or recalcAll:
            unsafeSquares |= newPieces[4 + addOne].get_attacks(whitePieces, blackPieces)
        else:
            unsafeSquares |= attacks[2]

        if recalcBishops or recalcAll:
            unsafeSquares |= newPieces[6 + addOne].get_attacks(whitePieces, blackPieces)
        else:
            unsafeSquares |= attacks[3]

        if recalcQueens or recalcAll:
            unsafeSquares |= newPieces[8 + addOne].get_attacks(whitePieces, blackPieces)
        else:
            unsafeSquares |= attacks[4]
        
        if recalcRooks or recalcAll:
            unsafeSquares |= newPieces[2 + addOne].get_attacks(whitePieces, blackPieces)
        else:
            unsafeSquares |= attacks[1]

        # determines if the king is on an unsafe square
        if newPieces[-1 - addOne].get_pieces() & unsafeSquares:
            return False
            
        # special moves
        if self.whitesTurn:
            if not self.gameInfo.whiteKingMoved:
                if not self.gameInfo.A1RookMoved and move == (INITWHITEKING, INITWHITEKING >> 2):
                    if INITWHITEKING*0b11 >> 2 & unsafeSquares:
                        return False
                elif not self.gameInfo.H1RookMoved and move == (INITWHITEKING, INITWHITEKING << 2):
                    if INITWHITEKING*0b11 << 1 & unsafeSquares:
                        return False
        else:
            if not self.gameInfo.blackKingMoved:
                if not self.gameInfo.A8RookMoved and move == (INITBLACKKING, INITBLACKKING >> 2):
                    if INITBLACKKING*0b11 >> 2 & unsafeSquares:
                        return False
                elif not self.gameInfo.H8RookMoved and move == (INITBLACKKING, INITBLACKKING << 2):
                    if INITBLACKKING*0b11 << 1 & unsafeSquares:
                        return False

        return True

    # returns an array of the pieces
    # only used as input to AI
    def try_move(self, move):
        # create phantom board
        newPieces = []
        board = []
        for piece in self.pieces:
            newPieces.append(piece.get_pieces())

        # makes the move on the phantom board
        for i in range(len(newPieces)):
            if move[0] & newPieces[i]:
                newPieces[i] &= ~move[0]
                newPieces[i] |= move[1]
                for j in range(len(newPieces)):
                    if (i + j) % 2 == 1:
                        newPieces[j] &= ~move[1]
        
        for i in range(64):
            square = 0b1 << i
            if newPieces[0] & square:
                board.append(PAWNVALUEBOARD[i])
            elif newPieces[1] & square:
                board.append(-PAWNVALUEBOARD[63 - i])
            elif newPieces[2] & square:
                board.append(5.63)
            elif newPieces[3] & square:
                board.append(-5.63)
            elif newPieces[4] & square:
                board.append(KNIGHTVALUEBOARD[i])
            elif newPieces[5] & square:
                board.append(-KNIGHTVALUEBOARD[i])
            elif newPieces[6] & square:
                board.append(BISHOPVALUEBOARD[i])
            elif newPieces[7] & square:
                board.append(-BISHOPVALUEBOARD[i])
            elif newPieces[8] & square:
                board.append(6.0 + BISHOPVALUEBOARD[i])
            elif newPieces[9] & square:
                board.append(-6.0 - BISHOPVALUEBOARD[i])
            elif newPieces[-2] & square:
                board.append(KINGVALUEBOARD[i])
            elif newPieces[-1] & square:
                board.append(-KINGVALUEBOARD[63 - (7 - i%8) - i//8])
            else:
                board.append(0.0)

        board.append(float(not self.whitesTurn) - 0.5)

        return tuple(board)

    # makes the move, doesn't check for any sort of legality
    def make_move(self, move):
        incrementFiftyMoveRuleCounter = True
        if self.whitesTurn:
            self.gameInfo.previousWhitePosition = []
            for piece in self.pieces:
                self.gameInfo.previousWhitePosition.append(copy(piece))
        else:
            self.gameInfo.previousBlackPosition = []
            for piece in self.pieces:
                self.gameInfo.previousBlackPosition.append(copy(piece))

        for piece in self.pieces:
            if move[0] & piece.get_pieces():
                piece.make_move(move)
                if self.whitesTurn:
                    self.whitePieces &= ~move[0]
                    self.whitePieces |= move[1]
                    self.blackPieces &= ~move[1]
                    self.gameInfo.previousWhiteMove = move
                else:
                    self.blackPieces &= ~move[0]
                    self.blackPieces |= move[1]
                    self.whitePieces &= ~move[1]
                    self.gameInfo.previousBlackMove = move
                for oppPiece in self.pieces:
                    if oppPiece.white != piece.white and oppPiece.get_pieces() & move[1]:
                        oppPiece.remove_piece(move[1])
                        incrementFiftyMoveRuleCounter = False
                if piece.pieceType == 'P':
                    incrementFiftyMoveRuleCounter = False
                break

        # special moves
        if self.whitesTurn:
            if not self.gameInfo.whiteKingMoved:
                if not self.gameInfo.A1RookMoved and move == (INITWHITEKING, INITWHITEKING >> 2):
                    self.pieces[2].make_move((A_FILE & FIRST_RANK, INITWHITEKING >> 1))
                    self.whitePieces &= ~(A_FILE & FIRST_RANK)
                    self.whitePieces |= INITWHITEKING >> 1
                elif not self.gameInfo.H1RookMoved and move == (INITWHITEKING, INITWHITEKING << 2):
                    self.pieces[2].make_move((H_FILE & FIRST_RANK, INITWHITEKING << 1))
                    self.whitePieces &= ~(H_FILE & FIRST_RANK)
                    self.whitePieces |= INITWHITEKING << 1

            if self.gameInfo.enpessantAvailable:
                if move[1] & self.gameInfo.enpessantAvailable >> 8 & self.pieces[0].get_pieces():
                    self.pieces[1].remove_piece(self.gameInfo.enpessantAvailable)
                    self.blackPieces &= ~self.gameInfo.enpessantAvailable

            elif move[1] & self.pieces[0].get_pieces() & EIGHTH_RANK:
                self.pieces[0].remove_piece(move[1])
                self.pieces[8].add_piece(move[1])
        else:
            if not self.gameInfo.blackKingMoved:
                if not self.gameInfo.A8RookMoved and move == (INITBLACKKING, INITBLACKKING >> 2):
                    self.pieces[3].make_move((A_FILE & EIGHTH_RANK, INITBLACKKING >> 1))
                    self.blackPieces &= ~(A_FILE & EIGHTH_RANK)
                    self.blackPieces |= INITBLACKKING >> 1
                elif not self.gameInfo.H8RookMoved and move == (INITBLACKKING, INITBLACKKING << 2):
                    self.pieces[3].make_move((H_FILE & EIGHTH_RANK, INITBLACKKING << 1))
                    self.blackPieces &= ~(H_FILE & EIGHTH_RANK)
                    self.blackPieces |= INITBLACKKING << 1

            if self.gameInfo.enpessantAvailable:
                if move[1] & self.gameInfo.enpessantAvailable << 8 & self.pieces[1].get_pieces():
                    self.pieces[0].remove_piece(self.gameInfo.enpessantAvailable)
                    self.whitePieces &= ~self.gameInfo.enpessantAvailable

            elif move[1] & self.pieces[1].get_pieces() & FIRST_RANK:
                self.pieces[1].remove_piece(move[1])
                self.pieces[9].add_piece(move[1])
        
        # updates game info about special moves
        self.gameInfo.enpessantAvailable = 0b0
        if self.whitesTurn:
            if move[0] & INITWHITEKING:
                self.gameInfo.whiteKingMoved = True
            elif move[0] & FIRST_RANK:
                if move[0] & H_FILE:
                    self.gameInfo.H1RookMoved = True
                elif move[0] & A_FILE:
                    self.gameInfo.A1RookMoved = True
            elif move[1] == move[0] >> 16 and move[1] & self.pieces[0].get_pieces():
                self.gameInfo.enpessantAvailable = move[1]
        else:
            if move[0] & INITBLACKKING:
                self.gameInfo.blackKingMoved = True
            elif move[0] & EIGHTH_RANK:
                if move[0] & H_FILE:
                    self.gameInfo.H8RookMoved = True
                elif move[0] & A_FILE:
                    self.gameInfo.A8RookMoved = True
            elif move[1] == move[0] << 16 and move[1] & self.pieces[1].get_pieces():
                self.gameInfo.enpessantAvailable = move[1]

        self.whitesTurn = not self.whitesTurn
        self.gameInfo.moveCounter += 1
        if incrementFiftyMoveRuleCounter:
            self.gameInfo.fiftyMoveRuleCounter += 1
        else:
            self.gameInfo.fiftyMoveRuleCounter = 0

    # returns all legal moves for white
    def get_white_moves(self, previousMoves):
        psuedoMoves = []
        recalcRooks = True
        recalcPawns = True
        recalcQueens = True
        recalcBishops = True
        recalcKnights = True
        recalcPawns = True
        recalcKing = True
        changedSquares = (self.gameInfo.previousBlackMove[0] | self.gameInfo.previousBlackMove[1] | 
                          self.gameInfo.previousWhiteMove[0] | self.gameInfo.previousWhiteMove[1])

        # pawns
        if self.pieces[0].get_pieces() == self.gameInfo.previousWhitePosition[0].get_pieces():
            if changedSquares & (self.pieces[0].get_pieces() >> 8 | self.pieces[0].get_pieces() >> 16 & FOURTH_RANK |
                                 self.pieces[0].get_pieces() >> 7 & ~A_FILE | self.pieces[0].get_pieces() >> 9 & ~H_FILE):
                recalcPawns = True
        else:
            recalcPawns = True
        if recalcPawns == True:
            psuedoMoves.append(self.pieces[0].get_moves(self.whitePieces, self.blackPieces))
        else:
            psuedoMoves.append(previousMoves[0])

        # rook
        if self.pieces[2].get_pieces() == self.gameInfo.previousWhitePosition[2].get_pieces():
            for mask in FILE_MASKS + RANK_MASKS:
                if changedSquares & mask and mask & self.pieces[2].get_pieces():
                    recalcRooks = True
                    break
        else:
            recalcRooks = True
        if recalcRooks == True:
            psuedoMoves.append(self.pieces[2].get_moves(self.whitePieces, self.blackPieces))
        else:
            psuedoMoves.append(previousMoves[1])

        # knight
        if self.pieces[4].get_pieces() == self.gameInfo.previousWhitePosition[4].get_pieces():
            if self.pieces[4].get_attacks(self.whitePieces, self.blackPieces) & changedSquares:
                recalcKnights = True
        else:
            recalcKnights = True
        if recalcKnights:
            psuedoMoves.append(self.pieces[4].get_moves(self.whitePieces, self.blackPieces))
        else:
            psuedoMoves.append(previousMoves[2])

        # bishop
        if self.pieces[6].get_pieces() == self.gameInfo.previousWhitePosition[6].get_pieces():
            for mask in DIAG_MASKS + ANTI_DIAG_MASKS:
                if changedSquares & mask and mask & self.pieces[6].get_pieces():
                    recalcBishops = True
                    break
        else:
            recalcBishops = True
        if recalcBishops:
            psuedoMoves.append(self.pieces[6].get_moves(self.whitePieces, self.blackPieces))
        else:
            psuedoMoves.append(previousMoves[3])

        # queen
        if self.pieces[8].get_pieces() == self.gameInfo.previousWhitePosition[8].get_pieces():
            for mask in DIAG_MASKS + ANTI_DIAG_MASKS + RANK_MASKS + FILE_MASKS:
                if changedSquares & mask and mask & self.pieces[8].get_pieces():
                    recalcQueens = True
                    break
        else:
            recalcQueens = True
        if recalcQueens == True:
            psuedoMoves.append(self.pieces[8].get_moves(self.whitePieces, self.blackPieces))
        else:
            psuedoMoves.append(previousMoves[4])

        # king
        if self.pieces[-2].get_pieces() == self.gameInfo.previousWhitePosition[-2].get_pieces():
            if self.pieces[-2].get_attacks(self.whitePieces, self.blackPieces) & changedSquares:
                recalcKing = True
        else:
            recalcKing = True
        if recalcKing:
            psuedoMoves.append(self.pieces[-2].get_moves(self.whitePieces, self.blackPieces))
        else:
            psuedoMoves.append(previousMoves[-1])

        # special moves
        if not self.gameInfo.whiteKingMoved:
            if not self.gameInfo.A1RookMoved and not INITWHITEKING*0b11 >> 2 & (self.whitePieces | self.blackPieces):
                psuedoMoves[5].append((INITWHITEKING, INITWHITEKING >> 2))
            if not self.gameInfo.H1RookMoved and not INITWHITEKING*0b11 << 1 & (self.whitePieces | self.blackPieces):
                psuedoMoves[5].append((INITWHITEKING, INITWHITEKING << 2))

        if self.gameInfo.enpessantAvailable:
            if self.gameInfo.enpessantAvailable << 1 & ~A_FILE & self.pieces[0].get_pieces():
                psuedoMoves[0].append((self.gameInfo.enpessantAvailable << 1, self.gameInfo.enpessantAvailable >> 8))
            elif self.gameInfo.enpessantAvailable >> 1 & ~H_FILE & self.pieces[0].get_pieces():
                psuedoMoves[0].append((self.gameInfo.enpessantAvailable >> 1, self.gameInfo.enpessantAvailable >> 8))

        # preprocessing
        # all attacks
        attacks = [self.pieces[1].get_attacks(self.whitePieces, self.blackPieces),
                   self.pieces[3].get_attacks(self.whitePieces, self.blackPieces),
                   self.pieces[5].get_attacks(self.whitePieces, self.blackPieces),
                   self.pieces[7].get_attacks(self.whitePieces, self.blackPieces),
                   self.pieces[9].get_attacks(self.whitePieces, self.blackPieces),
                   self.pieces[-1].get_attacks(self.whitePieces, self.blackPieces)]
        
        for i in range(len(psuedoMoves)):
            numberOfPsuedoMoves = len(psuedoMoves[i])
            for j in range(numberOfPsuedoMoves):
                if not self.test_move(psuedoMoves[i][numberOfPsuedoMoves - j - 1], attacks):
                    psuedoMoves[i].pop(numberOfPsuedoMoves - j - 1)
        
        return psuedoMoves

    # returns all legal moves for black
    def get_black_moves(self, previousMoves):
        psuedoMoves = []
        recalcRooks = True
        recalcPawns = True
        recalcQueens = True
        recalcBishops = True
        recalcKnights = True
        recalcPawns = True
        recalcKing = True
        changedSquares = (self.gameInfo.previousBlackMove[0] | self.gameInfo.previousBlackMove[1] | 
                          self.gameInfo.previousWhiteMove[0] | self.gameInfo.previousWhiteMove[1])

        # pawns
        if self.pieces[1].get_pieces() == self.gameInfo.previousBlackPosition[1].get_pieces():
            if changedSquares & (self.pieces[1].get_pieces() << 8 | self.pieces[1].get_pieces() << 16 & FIFTH_RANK |
                                 self.pieces[1].get_pieces() << 7 & ~H_FILE | self.pieces[1].get_pieces() << 9 & ~A_FILE):
                recalcPawns = True
        else:
            recalcPawns = True
        if recalcPawns == True:
            psuedoMoves.append(self.pieces[1].get_moves(self.whitePieces, self.blackPieces))
        else:
            psuedoMoves.append(previousMoves[0])

        # rook
        if self.pieces[3].get_pieces() == self.gameInfo.previousBlackPosition[3].get_pieces():
            for mask in FILE_MASKS + RANK_MASKS:
                if changedSquares & mask and mask & self.pieces[3].get_pieces():
                    recalcRooks = True
                    break
        else:
            recalcRooks = True
        if recalcRooks == True:
            psuedoMoves.append(self.pieces[3].get_moves(self.whitePieces, self.blackPieces))
        else:
            psuedoMoves.append(previousMoves[1])

        # knight
        if self.pieces[5].get_pieces() == self.gameInfo.previousBlackPosition[5].get_pieces():
            if self.pieces[5].get_attacks(self.whitePieces, self.blackPieces) & changedSquares:
                recalcKnights = True
        else:
            recalcKnights = True
        if recalcKnights:
            psuedoMoves.append(self.pieces[5].get_moves(self.whitePieces, self.blackPieces))
        else:
            psuedoMoves.append(previousMoves[2])

        # bishop
        if self.pieces[7].get_pieces() == self.gameInfo.previousBlackPosition[7].get_pieces():
            for mask in DIAG_MASKS + ANTI_DIAG_MASKS:
                if changedSquares & mask and mask & self.pieces[7].get_pieces():
                    recalcBishops = True
                    break
        else:
            recalcBishops = True
        if recalcBishops == True:
            psuedoMoves.append(self.pieces[7].get_moves(self.whitePieces, self.blackPieces))
        else:
            psuedoMoves.append(previousMoves[3])

        # queen
        if self.pieces[9].get_pieces() == self.gameInfo.previousBlackPosition[9].get_pieces():
            for mask in DIAG_MASKS + ANTI_DIAG_MASKS + FILE_MASKS + RANK_MASKS:
                if changedSquares & mask and mask & self.pieces[9].get_pieces():
                    recalcQueens = True
                    break
        else:
            recalcQueens = True
        if recalcQueens == True:
            psuedoMoves.append(self.pieces[9].get_moves(self.whitePieces, self.blackPieces))
        else:
            psuedoMoves.append(previousMoves[4])

        # king
        if self.pieces[-1].get_pieces() == self.gameInfo.previousBlackPosition[-1].get_pieces():
            if self.pieces[-1].get_attacks(self.whitePieces, self.blackPieces) & changedSquares:
                recalcKing = True
        else:
            recalcKing = True
        if recalcKing:
            psuedoMoves.append(self.pieces[-1].get_moves(self.whitePieces, self.blackPieces))
        else:
            psuedoMoves.append(previousMoves[-1])

        # special moves
        if not self.gameInfo.blackKingMoved:
            if not self.gameInfo.A8RookMoved and not INITBLACKKING*0b111 >> 3 & (self.whitePieces | self.blackPieces):
                psuedoMoves[5].append((INITBLACKKING, INITBLACKKING >> 2))
            if not self.gameInfo.H8RookMoved and not INITBLACKKING*0b110 << 2 & (self.whitePieces | self.blackPieces):
                psuedoMoves[5].append((INITBLACKKING, INITBLACKKING << 2))

        if self.gameInfo.enpessantAvailable:
            if self.gameInfo.enpessantAvailable << 1 & ~A_FILE & self.pieces[1].get_pieces():
                psuedoMoves[0].append((self.gameInfo.enpessantAvailable << 1, self.gameInfo.enpessantAvailable << 8))
            elif self.gameInfo.enpessantAvailable >> 1 & ~H_FILE & self.pieces[1].get_pieces():
                psuedoMoves[0].append((self.gameInfo.enpessantAvailable >> 1, self.gameInfo.enpessantAvailable << 8))
        
        # preprocessing
        # all attacks
        attacks = [self.pieces[0].get_attacks(self.whitePieces, self.blackPieces),
                   self.pieces[2].get_attacks(self.whitePieces, self.blackPieces),
                   self.pieces[4].get_attacks(self.whitePieces, self.blackPieces),
                   self.pieces[6].get_attacks(self.whitePieces, self.blackPieces),
                   self.pieces[8].get_attacks(self.whitePieces, self.blackPieces),
                   self.pieces[-2].get_attacks(self.whitePieces, self.blackPieces)]

        for i in range(len(psuedoMoves)):
            numberOfPsuedoMoves = len(psuedoMoves[i])
            for j in range(numberOfPsuedoMoves):
                if not self.test_move(psuedoMoves[i][numberOfPsuedoMoves - j - 1], attacks):
                    psuedoMoves[i].pop(numberOfPsuedoMoves - j - 1)
        
        return psuedoMoves
    
    def reset(self):
        self.whitePawns   = Pawns(INITWHITEPAWNS, True)
        self.blackPawns   = Pawns(INITBLACKPAWNS, False)
        self.whiteRooks   = Rooks(INITWHITEROOKS, True)
        self.blackRooks   = Rooks(INITBLACKROOKS, False)
        self.whiteKnights = Knights(INITWHITEKNIGHTS, True)
        self.blackKnights = Knights(INITBLACKKNIGHTS, False)
        self.whiteBishops = Bishops(INITWHITEBISHOPS, True)
        self.blackBishops = Bishops(INITBLACKBISHOPS, False)
        self.whiteQueens  = Queens(INITWHITEQUEENS, True)
        self.blackQueens  = Queens(INITBLACKQUEENS, False)
        self.whiteKing    = King(INITWHITEKING, True)
        self.blackKing    = King(INITBLACKKING, False)
        
        self.pieces = [self.whitePawns, self.blackPawns, self.whiteRooks, self.blackRooks, self.whiteKnights, self.blackKnights, 
                       self.whiteBishops, self.blackBishops, self.whiteQueens, self.blackQueens, self.whiteKing, self.blackKing]

        self.whitePieces = (self.whitePawns.get_pieces() | self.whiteRooks.get_pieces() | self.whiteKnights.get_pieces() | 
                            self.whiteBishops.get_pieces() | self.whiteQueens.get_pieces() | self.whiteKing.get_pieces())
        self.blackPieces = (self.blackPawns.get_pieces() | self.blackRooks.get_pieces() | self.blackKnights.get_pieces() | 
                            self.blackBishops.get_pieces() | self.blackQueens.get_pieces() | self.blackKing.get_pieces())

        self.gameInfo = GameInformation('O', [])
        self.whitesTurn = True