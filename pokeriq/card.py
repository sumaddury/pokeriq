from typing import Self, Iterable

# card.py
# This file contains a class for representing a playing card with a suit and rank.
# It provides methods for comparing cards, converting cards to strings, and generating sets of cards.

class Card:

    suits = {'s':'♠', 'h':'♥', 'd':'♦', 'c':'♣'}
    ranks = {2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8',
            9:'9', 10:'T', 11:'J', 12:'Q', 13:'K', 14:'A'}

    def __init__(self, suit: str, rank: int) -> Self:
        """
        Initializes a card with a specified suit and rank.
        
        :param suit: A string representing the suit of the card ('s', 'h', 'd', or 'c').
        :param rank: An integer representing the rank of the card (2-14).
        """
        self.suit = suit
        self.rank = rank

    def getSuit(self) -> str:
        """
        Returns the suit of the card.
        
        :return: A string representing the suit ('s', 'h', 'd', or 'c').
        """
        return(self.suit)

    def getRank(self) -> int:
        """
        Returns the rank of the card.
        
        :return: An integer representing the rank (2-14).
        """
        return(self.rank)

    def toString(self) -> str:
        """
        Converts the card to a string representation.
        
        :return: A string combining the suit and rank (e.g., '♠A', '♥5').
        """
        return(Card.suits[self.suit]+Card.ranks[self.rank])
    
    def equals(self, card: Self) -> bool:
        """
        Compares the current card with another card to check for equality.
        
        :param card: Another Card object to compare with.
        :return: True if the two cards are equal (same suit and rank), False otherwise.
        """
        assert isinstance(card, Card), "CARD TO COMPARE TO IS OF INVALID TYPE."

        return(self.getRank() == card.getRank() and self.getSuit() == card.getSuit())

    @staticmethod
    def sequenceToString(sequence: list[Self]) -> str:
        """
        Converts a list of cards into a string representation.
        
        :param sequence: A list of Card objects.
        :return: A string representing all cards in the list.
        """
        assert isinstance(sequence, list) and all(isinstance(card, Card) for card in sequence), "INPUT IS NOT A LIST OF CARDS."
        
        message = ""
        for card in sequence:
            message+=" "+card.toString()
        return(message)
    
    @staticmethod
    def generateSet(sequence: Iterable[str]) -> list[Self]:
        """
        Generates a set of Card objects from a sequence of string representations.
        
        :param sequence: An iterable containing card strings (e.g., ['As', 'Kc']).
        :return: A list of Card objects generated from the input strings.
        """
        assert isinstance(sequence, Iterable) and all(isinstance(card, str) for card in sequence), "INPUT IS NOT A COLLECTION OF STRINGS."

        cards = []
        for card in sequence:
            cards.append(Card.generate(card))
        return(cards)
    
    @staticmethod
    def generateSetofSets(set: Iterable[Iterable[str]]) -> list[list[Self]]:
        """
        Generates a set of sets of Card objects from a collection of sequences of card strings.
        
        :param set: An iterable of iterables containing card strings.
        :return: A list of lists of Card objects.
        """
        assert isinstance(set, Iterable) and all(isinstance(sequence, Iterable) for sequence in set), "INPUT IS NOT A COLLECTION OF COLLECTIONS."
        
        output = []
        for sequence in set:
            output.append(Card.generateSet(sequence))
        return(output)
    
    @staticmethod
    def contains(cards: Iterable[Self], card: Self) -> bool:
        """
        Checks if a collection of cards contains a specific card.
        
        :param cards: An iterable collection of Card objects.
        :param card: A Card object to check for presence.
        :return: True if the card is in the collection, False otherwise.
        """
        assert isinstance(cards, Iterable) and all(isinstance(card, Card) for card in cards), "COLLECTION INPUT IS NOT AN ITERABLE OF CARDS."
        assert isinstance(card, Card), "CARD INPUT IS OF INVALID TYPE."

        for c in cards:
            if c.equals(card):
                return(True)
        return(False)
    
    @staticmethod
    def generate(card: str) -> Self:
        """
        Generates a Card object from a string representation.
        
        :param card: A string representing a card (e.g., 'As', 'Kc').
        :return: A Card object created from the input string.
        """
        assert isinstance(card, str), "INPUT IS NOT A STRING."
        assert len(card) == 2 and card[0] in list(Card.ranks.values()) and card[1] in list(Card.suits.keys()), "STRING IS INVALID."
        
        rank = list(Card.ranks.keys())[list(Card.ranks.values()).index(card[0])]
        suit = card[1]
        return(Card(suit, rank))
