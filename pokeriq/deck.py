from Card import Card
from typing import Self
import random
import copy

# deck.py
# This file contains a class representing a deck of playing cards.
# It provides methods for shuffling, drawing, adding/removing cards, and dealing cards for poker games.

class Deck:
    def __init__(self, cardStack: list[Card] = None) -> Self:
        """
        Initializes the deck with a list of Card objects, either provided or by creating a standard 52-card deck.
        
        :param cardStack: An optional list of Card objects to initialize the deck with.
        """
        if cardStack:
            assert isinstance(cardStack, list) and all(isinstance(card, Card) for card in cardStack), "INPUT CARDSTACK IS NOT A LIST OF CARDS."

            self.cards = copy.deepcopy(cardStack)
        else:
            self.cards = []
            for i in list(Card.suits.keys()):
                for k in list(Card.ranks.keys()):
                    self.cards.append(Card(i, k))
    
    def shuffle(self) -> None:
        """
        Shuffles the deck of cards multiple times.
        """
        random.shuffle(self.cards)
        random.shuffle(self.cards)
        random.shuffle(self.cards)
    
    def contains(self, card: Card) -> bool:
        """
        Checks if the deck contains a specific card.
        
        :param card: A Card object to check for presence in the deck.
        :return: True if the card is in the deck, False otherwise.
        """
        assert isinstance(card, Card), "INPUT IS OF INVALID TYPE."

        return(Card.contains(self.cards, card))

    def getCards(self) -> list[Card]:
        """
        Returns the list of cards currently in the deck.
        
        :return: A list of Card objects in the deck.
        """
        return(self.cards)
    
    def getDepth(self) -> int:
        """
        Returns the number of cards remaining in the deck.
        
        :return: The number of cards in the deck.
        """
        return(len(self.cards))

    def remove(self, card: Card) -> bool:
        """
        Removes a specific card from the deck.
        
        :param card: A Card object to remove from the deck.
        :return: True if the card was removed, False if the card was not found.
        """
        assert isinstance(card, Card), "INPUT IS OF INVALID TYPE."

        for c in self.cards:
            if c.equals(card):
                self.cards.remove(c)
                return(True)
        return(False)
    
    def add(self, card: Card) -> None:
        """
        Adds a specific card to the deck.
        
        :param card: A Card object to add to the deck.
        """
        assert isinstance(card, Card), "INPUT IS OF INVALID TYPE."

        self.cards.append(card)

    def draw(self) -> Card:
        """
        Draws the top card from the deck.
        
        :return: A Card object drawn from the top of the deck.
        """
        return(self.cards.pop(0))

    def burn(self) -> None:
        """
        Burns (removes) the top card of the deck.
        """
        self.cards.pop(0)

    def dealFlop(self) -> list[Card]:
        """
        Deals the flop in a poker game (3 cards).
        
        :return: A list of 3 Card objects for the flop.
        """
        self.burn()
        return([self.draw(), self.draw(), self.draw()])

    def dealTurnRiver(self) -> list[Card]:
        """
        Deals the turn or river card in a poker game (1 card).
        
        :return: A list of 1 Card object for the turn or river.
        """
        self.burn()
        return([self.draw()])

    def reset(self, cardStack: list[Card] = None) -> None:
        """
        Resets the deck, either with a new card stack or by recreating a standard 52-card deck.
        
        :param cardStack: An optional list of Card objects to reset the deck with.
        """
        if cardStack:
            assert isinstance(cardStack, list) and all(isinstance(card, Card) for card in cardStack), "INPUT CARDSTACK IS NOT A LIST OF CARDS."

            self.cards = cardStack
        else:
            self.cards.clear()
            for i in list(Card.suits.keys()):
                for k in list(Card.ranks.keys()):
                    self.cards.append(Card(i, k))
    
    

