from .card import Card
from .made_hand import Hand
from typing import Self

# player.py
# This file contains a class for representing a poker player.
# It handles player actions, such as placing bets, updating their chip stack, 
# assigning hole cards, identifying the player's hand, and determining the winner among a list of players.

class Player:
    def __init__(self, name: str, chipStack: int | float = 200) -> Self:
        """
        Initializes a player with a name and an optional chip stack amount.

        :param name: The name of the player (string).
        :param chipStack: The initial chip stack (positive number, default is 200).
        """
        assert isinstance(name, str), "INPUT NAME IS NOT A STRING."
        assert (isinstance(chipStack, int) or isinstance(chipStack, float)) and chipStack > 0, "INPUT CHIPSTACK IS NOT A POSITIVE NUMBER."
        
        self.name = name
        self.stack = chipStack
        self.hole = []
        self.currentBet = 0
        
    def bet(self, amount: int | float) -> None:
        """
        Deducts the specified amount from the player's stack to place a bet.

        :param amount: The amount to bet (positive number).
        """
        assert (isinstance(amount, int) or isinstance(amount, float)) and amount > 0, "INPUT AMOUNT IS NOT A POSITIVE NUMBER."
        assert amount <= self.stack, "NOT ENOUGH CHIPS."
        self.stack -= amount
    
    def getCurrentBet(self) -> int:
        """
        Retrieves the current bet made by the player in the ongoing round.

        :returns: The current bet amount (integer).
        """
        return(self.currentBet)

    def updateCurrentBet(self, bet: int | float) -> None:
        """
        Updates the player's current bet.

        :param bet: The new bet amount (positive number).
        """
        assert (isinstance(bet, int) or isinstance(bet, float)) and bet > 0, "INPUT BET IS NOT A POSITIVE NUMBER."
        
        self.currentBet = bet

    def augment(self, add: int | float) -> None:
        """
        Adds a specified amount to the player's chip stack.

        :param add: The amount to add (positive number).
        """
        assert (isinstance(add, int) or isinstance(add, float)) and add > 0, "INPUT ADD-ON IS NOT A POSITIVE NUMBER."

        self.stack += add

    def clearHole(self) -> None:
        """
        Clears the player's hole cards and resets their current bet.

        :returns: None
        """
        self.hole = []
        self.currentBet = 0
    
    def assignHole(self, dealtCard: Card) -> None:
        """
        Assigns a card to the player's hole cards, ensuring the player only has two cards and the cards are not duplicates.

        :param dealtCard: The card to assign to the hole (Card object).
        """
        assert len(self.hole) < 2, "HOLE CARDS MAXIMUM ALREADY REACHED (2)."
        assert isinstance(dealtCard, Card), "INPUT CARD IS OF INVALID TYPE."
        assert len(self.hole) == 0 or not dealtCard.equals(self.hole[0]), "BOTH HOLE CARDS WOULD BE THE SAME."

        self.hole.append(dealtCard)
    
    def identifyHand(self, board: list[Card]) -> None:
        """
        Assigns a hand to the player based on their hole cards and the community board.

        :param board: A list of Card objects representing the community board (5 cards).
        """
        assert isinstance(board, list) and all(isinstance(card, Card) for card in board), "INPUT BOARD IS NOT A LIST OF CARDS."
        assert len(board) == 5, "FULL BOARD NOT PROVIDED (5)."

        self.hand = Hand(board, self.hole)
    
    def getHand(self) -> Hand:
        """
        Retrieves the player's hand object.

        :returns: The player's hand (Hand object).
        """
        return(self.hand)
    
    def showHole(self) -> list[Card]:
        """
        Shows the player's hole cards.

        :returns: A list of the player's hole cards (Card objects).
        """
        return(self.hole)
    
    def getName(self) -> str:
        """
        Retrieves the player's name.

        :returns: The player's name (string).
        """
        return(self.name)
    
    def getStack(self) -> int:
        """
        Retrieves the player's current chip stack.

        :returns: The player's chip stack (integer).
        """
        return(self.stack)
    
    @staticmethod
    def contains(players: list[Self], name: str) -> bool:
        """
        Checks if a player with the given name exists in the list of players.

        :param players: A list of Player objects.
        :param name: The name of the player to search for (string).
        :returns: True if the player is in the list, False otherwise.
        """
        assert isinstance(players, list) and all(isinstance(player, Player) for player in players), "INPUT PLAYERS IS NOT A LIST OF PLAYERS."
        assert isinstance(name, str), "INPUT NAME IS NOT A STRING."

        for player in players:
            if player.getName() == name:
                return(True)
        return(False)
    
    @staticmethod
    def index(players: list[Self], name: str) -> int | None:
        """
        Finds the index of a player with the given name in the list of players.

        :param players: A list of Player objects.
        :param name: The name of the player to search for (string).
        :returns: The index of the player, or None if not found.
        """
        assert isinstance(players, list) and all(isinstance(player, Player) for player in players), "INPUT PLAYERS IS NOT A LIST OF PLAYERS."
        assert isinstance(name, str), "INPUT NAME IS NOT A STRING."

        for i, player in enumerate(players):
            if player.getName() == name:
                return(i)
        return(None)

    @staticmethod
    def winner(players: list[Self]) -> list[Self]:
        """
        Determines the winner(s) among a list of players based on their hands.

        :param players: A list of Player objects.
        :returns: A list of Player objects representing the winner(s).
        """
        assert isinstance(players, list) and all(isinstance(player, Player) for player in players), "INPUT PLAYERS IS NOT A LIST OF PLAYERS."
        
        top = [players[0]]
        for player in players[1:]:
            comparison = player.getHand().compareTo(top[0].getHand())
            if comparison == -1:
                top = [player]
            elif comparison == 0:
                top.append(player)
        return(top)
        


    


