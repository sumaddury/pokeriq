from .card import Card
from typing import Self

# made_hand.py
# This file contains a class for evaluating poker hands and determining the best hand ranking.
# It provides methods for hand comparison, hand ranking, and determining hand strength.

class Hand:

    hands = ('ROYAL FLUSH',
            'STRAIGHT FLUSH',
            'FOUR OF A KIND',
            'FULL HOUSE',
            'FLUSH',
            'STRAIGHT',
            'THREE OF A KIND',
            'TWO PAIR',
            'ONE PAIR',
            'HIGH CARD')

    def __init__(self, board: list[Card], hole: list[Card]) -> Self:
        """
        Initializes a hand with the specified board and hole cards. The hand ranking and strength are determined
        based on the combination of both the board and hole cards.

        :param board: A list of `Card` objects representing the community cards on the board.
        :param hole: A list of `Card` objects representing the player's hole cards.
        """
        self.hand, self.strength = Hand.calculateHand(board, hole)

    def toString(self) -> str:
        """
        Returns a string representation of the hand, showing the hand's name (e.g., "ROYAL FLUSH").

        :returns: A string representing the hand's rank.
        """
        return(Hand.hands[self.hand])
    
    def getHand(self) -> int:
        """
        Returns the integer representation of the hand's rank.

        :returns: An integer representing the hand's rank (e.g., 0 for ROYAL FLUSH, 1 for STRAIGHT FLUSH).
        """
        return(self.hand)
    
    def getStrength(self) -> list[int]:
        """
        Returns a list of integers representing the strength of the hand, typically used for comparison
        against other hands.

        :returns: A list of integers representing the hand's strength (used in comparison).
        """
        return(self.strength)

    def compareTo(self, other: Self) -> int:
        """
        Compares the current hand to another hand to determine which one is stronger. If the hands are of
        equal rank, it compares the hand strengths to break the tie.

        :param other: The other `Hand` object to compare against.
        :returns: -1 if the current hand is weaker, 1 if stronger, or 0 if they are of equal strength.
        """
        if self.hand < other.hand:
            return(-1)
        elif self.hand > other.hand:
            return(1)
        else:
            for i in range(len(self.strength)):
                if self.strength[i] > other.getStrength()[i]:
                    return(-1)
                elif self.strength[i] < other.getStrength()[i]:
                    return(2)
            return(0)
    
    @staticmethod
    def calculateHand(board: list[Card], hole: list[Card]) -> tuple[int, list[int]]:
        """
        Calculates the hand rank and strength based on the given board and hole cards. It checks various
        possible hand types (e.g., Royal Flush, Full House, etc.) in order, returning the first valid hand found.

        :param board: A list of `Card` objects representing the community cards on the board.
        :param hole: A list of `Card` objects representing the player's hole cards.
        :returns: A tuple consisting of an integer representing the hand's rank and a list of integers
                  representing the hand's strength.
        """
        total = board+hole
        functions = [Hand.checkRoyalFlush, Hand.checkStraightFlush, Hand.checkFourKind, Hand.checkFullHouse, Hand.checkFlush, 
                Hand.checkStraight, Hand.checkThreeKind, Hand.checkTwoPair, Hand.checkOnePair, Hand.checkHighCard]
        for i in range(len(functions)):
            result = functions[i](total)
            if result != None:
                return(i, result)
        
    @staticmethod
    def checkHighCard(total: list[Card]) -> list[int] | None:
        """
        Checks for a High Card hand by finding the highest ranks in the total set of cards.

        :param total: A list of `Card` objects representing all cards available to the player (board + hole cards).
        :returns: A list of integer ranks of the highest cards, excluding the two smallest ranks. 
                  Returns `None` if no high card hand is found.
        """
        ranks = [card.getRank() for card in total]
        ranks.remove(min(ranks))
        ranks.remove(min(ranks))
        ranks.sort(reverse = True)
        return(ranks)

    @staticmethod
    def checkOnePair(total: list[Card]) -> list[int] | None:
        """
        Checks for a One Pair hand by finding a pair of matching ranks in the total set of cards.

        :param total: A list of `Card` objects representing all cards available to the player (board + hole cards).
        :returns: A list of integers where the first value is the pair's rank and the remaining values are 
                  the top 3 highest unpaired ranks. Returns `None` if no One Pair hand is found.
        """
        ranks = [card.getRank() for card in total]
        ranks.sort(reverse = True)
        pair = None
        for i in range(len(ranks)-1):
            if ranks[i] == ranks[i+1]:
                pair = ranks[i]
                break

        if pair == None:
            return(None)
        ranks.remove(pair)
        ranks.remove(pair)
        return([pair]+ranks[0:3])
    
    @staticmethod
    def checkTwoPair(total: list[Card]) -> list[int] | None:
        """
        Checks for a Two Pair hand by finding two distinct pairs of matching ranks in the total set of cards.

        :param total: A list of `Card` objects representing all cards available to the player (board + hole cards).
        :returns: A list of integers where the first two values are the ranks of the two pairs, followed by
                  the highest remaining rank. Returns `None` if no Two Pair hand is found.
        """
        ranks = [card.getRank() for card in total]
        ranks.sort(reverse = True)
        pairOne = None
        pairTwo = None
        for i in range(len(ranks)-1):
            if ranks[i] == ranks[i+1]:
                pairOne = ranks[i]

        if pairOne == None:
            return(None)
        ranks.remove(pairOne)
        ranks.remove(pairOne)

        for i in range(len(ranks)-1):
            if ranks[i] == ranks[i+1]:
                pairTwo = ranks[i]

        if pairTwo == None:
            return(None)
        ranks.remove(pairTwo)
        ranks.remove(pairTwo)
        return([pairOne, pairTwo]+[ranks[0]])

    @staticmethod
    def checkThreeKind(total: list[Card]) -> list[int] | None:
        """
        Checks for a Three of a Kind hand by finding three matching ranks in the total set of cards.

        :param total: A list of `Card` objects representing all cards available to the player (board + hole cards).
        :returns: A list of integers where the first value is the rank of the three of a kind and the 
                  remaining values are the top 2 highest unpaired ranks. Returns `None` if no Three of a Kind 
                  hand is found.
        """
        ranks = [card.getRank() for card in total]
        ranks.sort(reverse = True)
        triple = None
        for i in range(len(ranks)-2):
            if ranks[i] == ranks[i+1] == ranks[i+2]:
                triple = ranks[i]
                break

        if triple == None:
            return(None)
        ranks.remove(triple)
        ranks.remove(triple)
        ranks.remove(triple)
        return([triple]+ranks[0:2])

    @staticmethod
    def checkStraight(total: list[Card]) -> list[int] | None:
        """
        Checks for a Straight hand by finding five consecutive ranks in the total set of cards.

        :param total: A list of `Card` objects representing all cards available to the player (board + hole cards).
        :returns: A list of integers where the first value is the highest rank in the straight. Returns `None`
                  if no Straight hand is found.
        """
        ranks = [card.getRank() for card in total]
        if 14 in ranks:
            ranks.append(1)
        ranks = list(set(ranks))
        ranks.sort(reverse = True)
        strength = None

        for i in range(len(ranks)-4):
            if (ranks[i] == ranks[i+1] + 1) and (ranks[i+1] == ranks[i+2] + 1) and (ranks[i+2] == ranks[i+3] + 1) and (ranks[i+3] == ranks[i+4] + 1):
                strength = ranks[i]
                break
        
        if strength == None:
            return(None)
        return([strength])

    @staticmethod
    def checkFlush(total: list[Card]) -> list[int] | None:
        """
        Checks for a Flush hand by finding five cards of the same suit in the total set of cards.

        :param total: A list of `Card` objects representing all cards available to the player (board + hole cards).
        :returns: A list of integers representing the ranks of the top 5 flush cards, sorted in descending order.
                  Returns `None` if no Flush hand is found.
        """
        bySuit = {'s': [], 'h': [], 'd': [], 'c': []}
        for card in total:
            bySuit[card.getSuit()].append(card.getRank())
        for key, value in bySuit.items():
            if len(value) >= 5:
                return(sorted(value, reverse = True)[0:5])

        return(None)

    @staticmethod
    def checkFullHouse(total: list[Card]) -> list[int] | None:
        """
        Checks for a Full House hand by finding a three of a kind and a pair in the total set of cards.

        :param total: A list of `Card` objects representing all cards available to the player (board + hole cards).
        :returns: A list of integers where the first value is the three of a kind and the second value is the pair.
                  Returns `None` if no Full House hand is found.
        """
        ranks = [card.getRank() for card in total]
        ranks.sort(reverse = True)
        triple = None
        pair = None
        for i in range(len(ranks)-2):
            if ranks[i] == ranks[i+1] == ranks[i+2]:
                triple = ranks[i]
                break
        
        if triple == None:
            return(None)
        ranks.remove(triple)
        ranks.remove(triple)
        ranks.remove(triple)

        for i in range(len(ranks)-1):
            if ranks[i] == ranks[i+1]:
                pair = ranks[i]
                break

        if pair == None:
            return(None)
        return([triple, pair])

    @staticmethod
    def checkFourKind(total: list[Card]) -> list[int] | None:
        """
        Checks for a Four of a Kind hand by finding four matching ranks in the total set of cards.

        :param total: A list of `Card` objects representing all cards available to the player (board + hole cards).
        :returns: A list of integers where the first value is the rank of the four of a kind and the second value 
                  is the highest remaining rank. Returns `None` if no Four of a Kind hand is found.
        """
        ranks = [card.getRank() for card in total]
        ranks.sort(reverse = True)
        quad = None
        for i in range(len(ranks)-3):
            if ranks[i] == ranks[i+1] == ranks[i+2] == ranks[i+3]:
                quad = ranks[i]
        
        if quad == None:
            return(None)
        ranks.remove(quad)
        ranks.remove(quad)
        ranks.remove(quad)
        ranks.remove(quad)
        return([quad]+[ranks[0]])

    @staticmethod
    def checkStraightFlush(total: list[Card]) -> list[int] | None:
        """
        Checks for a Straight Flush hand by finding five consecutive cards of the same suit.

        :param total: A list of `Card` objects representing all cards available to the player (board + hole cards).
        :returns: A list of integers where the first value is the highest rank in the straight flush. Returns `None`
                  if no Straight Flush hand is found.
        """
        flushCond = Hand.checkFlush(total)
        if flushCond == None:
            return(None)
        if 14 in flushCond:
            flushCond.append(1)

        strength = None
        for i in range(len(flushCond)-4):
            if (flushCond[i] == flushCond[i+1] + 1) and (flushCond[i+1] == flushCond[i+2] + 1) and (flushCond[i+2] == flushCond[i+3] + 1) and (flushCond[i+3] == flushCond[i+4] + 1):
                strength = flushCond[i]
                break
        
        if strength == None:
            return(None)
        return([strength])

    @staticmethod
    def checkRoyalFlush(total: list[Card]) -> list[int] | None:
        """
        Checks for a Royal Flush hand, which is a Straight Flush starting with the Ace (rank 14).

        :param total: A list of `Card` objects representing all cards available to the player (board + hole cards).
        :returns: A list with a single value, 14, if a Royal Flush is found, or `None` if not.
        """
        if Hand.checkStraightFlush(total) == [14]:
            return([14])
        return(None)
    
