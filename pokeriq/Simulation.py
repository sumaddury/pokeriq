from Card import Card
from Hand import Hand
from Player import Player
from Deck import Deck
from typing import Self

# Simulation.py
# This file contains a class for running a poker hand simulation.
# It handles the dealing of cards, assigning hands to players, 
# and determining the winners based on the community cards (flop, turn, river).

class Simulation:
    def __init__(self, flop: list[Card], turn: list[Card], river: list[Card], players: list[Player]) -> Self:
        """
        Initializes a simulation with community cards (flop, turn, river) and players.
        It also identifies the players' hands and determines the winners.

        :param flop: The first three community cards (list of Card objects).
        :param turn: The fourth community card (list of one Card object).
        :param river: The fifth community card (list of one Card object).
        :param players: The list of Player objects participating in the hand.
        """
        assert isinstance(flop, list) and all(isinstance(card, Card) for card in flop) and len(flop) == 3, "INVALID FLOP PROVIDED."
        assert isinstance(turn, list) and all(isinstance(card, Card) for card in turn) and len(turn) == 1, "INVALID TURN PROVIDED."
        assert isinstance(river, list) and all(isinstance(card, Card) for card in river) and len(river) == 1, "INVALID RIVER PROVIDED."
        assert isinstance(players, list) and all(isinstance(player, Player) for player in players), "INVALID PLAYER LIST PROVIDED."

        self.flop = flop
        self.turn = turn
        self.river = river
        self.board = self.flop+self.turn+self.river
        self.players = players
        for player in self.players:
            player.identifyHand(self.board)
        self.winners = Player.winner(self.players)
        self.highHand = self.winners[0].getHand().toString()
    
    def toString(self) -> str:
        """
        Returns a summary of the simulation, including community cards, player hands, and winners.

        :returns: A string representation of the simulation.
        """
        message = ""
        message += "SIM SUMMARY"+"\n"
        message += "____________________"+"\n"
        message += "FLOP"+"\n"
        message += Card.sequenceToString(self.flop)+"\n"
        message += "____________________"+"\n"
        message += "TURN"+"\n"
        message += Card.sequenceToString(self.flop+self.turn)+"\n"
        message += "____________________"+"\n"
        message += "RIVER"+"\n"
        message += Card.sequenceToString(self.flop+self.turn+self.river)+"\n"
        message += "____________________"+"\n"
        for player in self.players:
            message += player.getName()+": "+Card.sequenceToString(player.showHole())+" | "+player.getHand().toString()+"\n"
        message += "____________________"+"\n"
        message += "Winners: "
        for player in self.winners:
            message += player.getName() + " | "
        message += "\nWinning Hand: "+self.highHand
        return(message)
    
    def getBoard(self) -> list[Card]:
        """
        Retrieves the community cards (flop, turn, and river) of the simulation.

        :returns: A list of all community cards (Card objects).
        """
        return(self.board)
    
    def getPlayers(self) -> list[Player]:
        """
        Retrieves the list of players in the simulation.

        :returns: A list of Player objects.
        """
        return(self.players)
    
    def getWinners(self) -> list[Player]:
        """
        Retrieves the list of players who won the hand.

        :returns: A list of Player objects representing the winners.
        """
        return(self.winners)
    
    def getHighHand(self) -> str:
        """
        Retrieves the high hand (the winning hand) in string format.

        :returns: The winning hand as a string.
        """
        return(self.highHand)

    @staticmethod
    def runSim(playerCount: int, customDeck: Deck = Deck(), customPlayers: list[Player] = None, customFlop: list[Card] = None, customTurn: list[Card] = None, customRiver: list[Card] = None) -> Self:
        """
        Runs a simulation by creating a deck and dealing cards to players. 
        It allows customization for the number of players, deck, and community cards.

        :param playerCount: The number of players in the simulation (1-10).
        :param customDeck: An optional custom Deck object.
        :param customPlayers: An optional list of custom Player objects.
        :param customFlop: An optional custom flop (list of 3 Card objects).
        :param customTurn: An optional custom turn (1 Card object).
        :param customRiver: An optional custom river (1 Card object).
        :returns: A Simulation object representing the hand.
        """
        assert isinstance(playerCount, int) and playerCount > 0 and playerCount <= 10, "INPUT PC IS NOT AN INTEGER ON [1,10]."
        assert isinstance(customDeck, Deck), "INPUT DECK IS OF INVALID TYPE."
        assert not customPlayers or isinstance(customPlayers, list) and all(isinstance(player, Player) for player in customPlayers), "INVALID PLAYER LIST PROVIDED."
        assert not customFlop or isinstance(customFlop, list) and all(isinstance(card, Card) for card in customFlop) and len(customFlop) == 3, "INVALID FLOP PROVIDED."
        assert not customTurn or isinstance(customTurn, list) and all(isinstance(card, Card) for card in customTurn) and len(customTurn) == 1, "INVALID TURN PROVIDED."
        assert not customRiver or isinstance(customRiver, list) and all(isinstance(card, Card) for card in customRiver) and len(customRiver) == 1, "INVALID RIVER PROVIDED."

        message = ""
        deck = customDeck
        deck.shuffle()

        if customPlayers:
            players = customPlayers

        else:
            players = [Player("Player "+str(i+1)) for i in range(playerCount)]
            for player in players:
                player.assignHole(deck.draw())

            for player in players:
                player.assignHole(deck.draw())
        
        if customFlop:
            flop = customFlop
            
            if customTurn:
                turn = customTurn

                if customRiver:
                    river = customRiver
                
                else:
                    river = deck.dealTurnRiver()

            else:
                turn = deck.dealTurnRiver()
                river = deck.dealTurnRiver()
        else:
            flop = deck.dealFlop()
            turn = deck.dealTurnRiver()
            river = deck.dealTurnRiver()

        return(Simulation(flop, turn, river, players))
