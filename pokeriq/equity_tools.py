from .card import Card
from .made_hand import Hand
from .deck import Deck
from .player import Player
from .runout_simulation import Simulation
from itertools import product, combinations, permutations
from typing import Self
import copy
import builtins

# equity_tools.py
# This file contains a class which calculates the hand equity for players
# in a poker game. The class handles player setup, deck definition, and simulating hands
# to determine equity percentages based on a given board state and players' hole cards.

class EquitySolver:
    def __init__(self) -> Self:
        """
        Initializes the EquitySolver instance with empty player list, 
        no community cards, and a new deck.

        :param players: A list of Player objects participating in the game.
        :param flop: The first three community cards (list of Card objects).
        :param turn: The fourth community card (list of one Card object).
        :param river: The fifth community card (list of one Card object).
        """
        self.players = []
        self.flop = None
        self.turn = None
        self.river = None
        self.deck = Deck()
        self.handEquities = None
    
    def getHandEquities(self) -> dict[str: float]:
        """
        Returns the calculated hand equities for all players.

        :return: A dictionary of player names and their respective equity percentages.
        """
        return(self.handEquities)
    
    def addPlayers(self, amnt: int = 1) -> None:
        """
        Adds the specified number of players to the simulation.

        :param amnt: The number of players to add (default is 1).
        """
        assert len(self.players) + amnt <= 10, "MAX AMOUNT OF PLAYERS ALREADY REACHED (10)."

        for _ in range(amnt):
            self.players.append(Player("Player "+str(len(self.players)+1)))

    def removePlayers(self, amnt: int = 1) -> None:
        """
        Removes the specified number of players from the simulation.

        :param amnt: The number of players to remove (default is 1).
        """
        assert len(self.players) - amnt >= 0, "NOT ENOUGH PLAYERS TO REMOVE."
        
        for _ in range(amnt):
            self.players.pop()
    
    def defineHole(self, id: int, hole: list[Card]) -> None:
        """
        Assigns hole cards to a player by their ID.

        :param id: The player ID to assign hole cards to.
        :param hole: A list of two Card objects representing the player's hole cards.
        """
        assert isinstance(hole, list) and all(isinstance(card, Card) for card in hole), "HOLE IS NOT A LIST OF TWO CARDS."
        assert len(hole) == 2, "TWO CARDS NOT GIVEN."
        assert not hole[0].equals(hole[1]), "BOTH CARDS ARE THE SAME."
        assert Player.contains(self.players, "Player "+str(id)), "Player "+str(id)+" DOES NOT EXIST."
        
        index = Player.index(self.players, "Player "+str(id))
        self.players[index].clearHole()
        self.players[index].assignHole(hole[0])
        self.players[index].assignHole(hole[1])

    def clearHole(self, id: int) -> None:
        """
        Clears the hole cards of a player by their ID.

        :param id: The player ID whose hole cards should be cleared.
        """
        assert Player.contains(self.players, "Player "+str(id)), "Player "+str(id)+" DOES NOT EXIST."

        index = Player.index(self.players, "Player "+str(id))
        self.players[index].clearHole()
    
    def defineDeck(self, deck: Deck) -> None:
        """
        Defines the deck to be used in the simulation.

        :param deck: The Deck object to be used in the simulation.
        """
        assert isinstance(deck, Deck), "DECK INPUT IS OF INVALID TYPE."
        assert deck.getDepth() >= 2*len(self.players) + 8, "DECK IS TOO SMALL, REQUIRES AT LEAST "+str(2*len(self.players) + 8)+" CARDS."

        self.deck = deck

    def defineBoard(self, board: list[Card]) -> None:
        """
        Defines the community board cards (flop, turn, river).

        :param board: A list of 3-5 Card objects representing the community cards.
        """
        assert isinstance(board, list) and all(isinstance(card, Card) for card in board), "BOARD IS NOT A LIST OF 3-5 CARDS."
        assert len(board) >= 3 and len(board) <= 5

        self.flop = board[:3]
        self.turn = ([board[3]] if len(board) > 3 else None)
        self.river = ([board[4]] if len(board) > 4 else None)
    
    def calculateHandEquity(self, trials: int = 1000) -> dict[str: float]:
        """
        Calculates the hand equity for each player based on simulations.

        :param trials: The number of trials (default is 1000).
        :return: A dictionary of player names and their respective equity percentages.
        """
        assert isinstance(trials, int) and trials > 0, "TRIALS INPUT IS NOT A POSITIVE INTEGER."
        assert self.deck.getDepth() >= 2*len(self.players) + 8, "DECK IS TOO SMALL, REQUIRES AT LEAST "+str(2*len(self.players) + 8)+" CARDS."
        assert len(self.players) > 0, "NO PLAYERS ADDED"

        tempDeck = copy.deepcopy(self.deck)

        equityDict = {}
        for player in self.players:
            equityDict[player.getName()] = 0
            tempHole = player.showHole()
            if len(tempHole) > 0:
                # assert tempDeck.contains(tempHole[0]) and tempDeck.contains(tempHole[1]), "INVALID DECK."
                tempDeck.remove(tempHole[0])
                tempDeck.remove(tempHole[1])
        equityDict["CHOP"] = 0

        burns = 0

        if self.flop:
            for card in self.flop:
                # assert tempDeck.contains(card), "INVALID DECK."
                tempDeck.remove(card)
            burns += 1
                
        if self.turn:
            # assert tempDeck.contains(self.turn[0]), "INVALID DECK."
            tempDeck.remove(self.turn[0])
            burns += 1

        if self.river:
            # assert tempDeck.contains(self.river[0]), "INVALID DECK."
            tempDeck.remove(self.river[0])
            burns += 1
        
        
        for _ in range(trials):
            trialDeck = copy.deepcopy(tempDeck)
            trialDeck.shuffle()
            trialPlayers = copy.deepcopy(self.players)
            
            for player in trialPlayers:
                if len(player.showHole()) == 0:
                    player.assignHole(trialDeck.draw())
                    player.assignHole(trialDeck.draw())
            
            for n in range(burns):
                trialDeck.burn()
            
            summary = Simulation.runSim(len(trialPlayers), trialDeck, trialPlayers, self.flop, self.turn, self.river)
            winners = summary.getWinners()
            
            if len(winners) == len(trialPlayers): 
                equityDict["CHOP"] += 1/trials
            else:
                for winner in winners:
                    equityDict[winner.getName()] += 1/trials
        
        self.handEquities = equityDict
        return(equityDict)

    def toString(self) -> str:
        """
        Returns a string representation of the current simulation state.

        :return: A formatted string showing the community cards, players' hands, 
                 and their equity percentages.
        """
        message = ""
        message += "____________________\n"
        
        board = (self.flop or []) + (self.turn or []) + (self.river or [])
        message += "Board Cards: \n"
        message += Card.sequenceToString(board)
        message += "\n____________________\n"

        if self.handEquities:
            for player in self.players:
                message += player.getName() + " | " + Card.sequenceToString(player.showHole()) + " | " + str(self.handEquities[player.getName()]*100) + "%\n"
            message += "Chop | " + str(self.handEquities["CHOP"]*100) + "%\n"
            message += "____________________\n"

        else:
            for player in self.players:
                message += player.getName() + " | " + Card.sequenceToString(player.showHole()) + "\n"
            message += "____________________\n"
        
        return(message)
    
    @staticmethod
    def generateRange(range: list[str]) ->  list[list[Self]]:
        """
        Generates all possible hands from a given hand range.

        :param range: A list of strings representing the hand range (e.g., ["AsKs", "AcKc"]).
        :return: A list of all possible combinations of hands based on the specified range.
        """
        assert isinstance(range, list) and all(isinstance(hand, str) for hand in range), "INPUT RANGE IS NOT A LIST OF STRINGS."
        assert all((len(hand) == 3 and hand[2] in {'s', 'o'}) or (len(hand) == 2 and hand[0] == hand[1]) for hand in range), "ONE OR MORE HANDS IS OF INVALID FORMAT."
        assert all(hand[0] in list(Card.ranks.values()) and hand[1] in list(Card.ranks.values()) for hand in range), "ONE OR MORE HANDS IS OF INVALID FORMAT."

        enumerations = []
        for hand in range:
            cases = []
            if len(hand) == 2:
                for pair in combinations(list(Card.suits.keys()), 2):
                    cases.append((hand[0]+pair[0], hand[1]+pair[1]))
            elif hand[2] == 's':
                for suit in list(Card.suits.keys()):
                    cases.append((hand[0]+suit, hand[1]+suit))
            elif hand[2] == 'o':
                for pair in permutations(list(Card.suits.keys()), 2):
                    cases.append((hand[0]+pair[0], hand[1]+pair[1]))
            enumerations += cases
        return(Card.generateSetofSets(enumerations))
    
    @staticmethod
    def calculateRangeEquity(*args: list[list[Card]], trials: int = 1000, customDeck: Deck = Deck(), customBoard: list[Card] = None) ->  tuple[dict[str: float], str]:
        """
        Calculates the equity for each range in a multi-way poker hand simulation.

        It iterates through all combinations of the hands from the given ranges and runs 
        simulations to determine the equity for each range based on the community cards (flop, turn, river).

        :param args: A list of ranges (each range is a list of hands, with each hand being a list of Card objects).
        :param trials: The number of trials to run in the simulation (default is 1000).
        :param customDeck: A custom deck to be used for the simulation (default is a standard deck).
        :param customBoard: A custom board (community cards) to be used for the simulation (default is None).
        :return: A tuple containing a dictionary of range equities and a string summary of the results.
        """
        assert len(args) > 0, "NO RANGES GIVEN."
        assert all(isinstance(range, list) and all(isinstance(hand, list) and all(isinstance(card, Card) for card in hand) for hand in range) for range in args), "INPUT RANGES ARE OF INVALID TYPES."
        assert all(all((len(hand) == 2) for hand in range) for range in args)
        assert all(all(not hand[0].equals(hand[1]) for hand in range) for range in args)

        rangeEquities = {}
        for i in builtins.range(len(args)):
            rangeEquities["Range "+str(i+1)] = 0
        rangeEquities["CHOP"] = 0
        
        solver = EquitySolver()
        solver.addPlayers(len(args))
        if customBoard:
            solver.defineBoard(customBoard)
        if customDeck:
            solver.defineDeck(customDeck)
        
        totalPerms = sum(1 for _ in product(*args))
        for permutation in product(*args):
            for i, hand in enumerate(permutation):
                solver.defineHole(i+1, hand)
            handEquities = solver.calculateHandEquity(trials)

            for (key1, value1), (key2, value2) in zip(rangeEquities.items(), handEquities.items()):
                rangeEquities[key1] += value2/totalPerms
        
        message = "____________________\nBoardCards: \n"
        if customBoard:
            message += Card.sequenceToString(customBoard)
        message += "\n____________________\n"
        for range, equity in rangeEquities.items():
            message += range + " | " + str(rangeEquities[range]*100) + "%\n"
        message += "____________________\n"
        
        return(rangeEquities, message)
        
        







            










