# PokerIQ ♠♥♦♣
___
A micro-library intended for studying [No Limit Texas Hold'Em (NLH)](https://thelodgepokerclub.com/no-limit-texas-holdem-rules-beginners-guide/), written in pure Python. 

The library provides classes and tools for toy games, simulations, and inductive equity calculations. It is intended for approximation and ease-of-use, rather than a replacement for more rigorous [GTO](https://blog.gtowizard.com/what-is-gto-in-poker/) study.
___
## Overview
_No Limit Hold'Em is the most popular variant of poker, allowing for uncapped betting across multiple streets which creates a more complex layer of strategy. The goal of this package is to provide the basic tools needed to understand NLH inductively. It includes six main classes that allow for custom simulation and [equity](https://upswingpoker.com/equity/) calculation:_
1. `Card`: Provides functionality for individual cards, including several generation mechanisms.
2. `Hand`: Performs made hand strength calculations and comparison.
3. `Player`: Encapsulates information about individual players (stack, hole, made hand, etc.).
4. `Deck`: Provides functionality for a deck (burn, draw, deal, shuffle, etc.).
5. `Simulation`: Encapsulates all information about a given trial, running the board out, assessing winners, etc.
6. `EquitySolver`: The main equity calculation mechanism. Hand and range equity, EV, fold equity calculation.

Generate a few ranges and a custom board if desired with the utilities provided by the `Card` class.
```python
  myRange = [Card.generateSet(('9s', '9h'))]
  standardThreeBet = EquitySolver.generateRange(['AA', 'KK', 'QQ', 'AKs', 'AKo', 'JJ',
                                                'TT', '99', 'AQs', 'AQo', 'AJs', 'AJo',
                                                 'ATs', 'ATo', 'KQs', 'KQo'])
  board = Card.generateSet(('Ah', '9c', '5c'))
```

Initialize an `EquitySolver` and input the ranges and board to approximate equity.
```python
  equities, message = EquitySolver.calculateRangeEquity(myRange, standardThreeBet,
                                                        trials=10000, customBoard=board)
  print(message)
```
```
  ____________________
  BoardCards:
  ♥A ♣9 ♣5
  ____________________
  Range 1 | 84.11034482757842%
  Range 2 | 10.833620689654694%
  CHOP | 5.0560344827581485%
  ____________________
```

For more detailed instruction on how to use the library, refer to the [short tutorial notebook](https://github.com/sumaddury/pokeriq/blob/main/tutorial.ipynb).
___
## Setup
Install via `pip`:
```bash
  pip install git+https://github.com/sumaddury/pokeriq.git
```
Or install from source:
```bash
  git clone https://github.com/sumaddury/pokeriq.git
  cd pokeriq
  pip install .
```
Finally, import the required classes!
```python
  from pokeriq import Card, Hand, Deck, Player, Simulation, EquitySolver
```
___
## Features
|           | Implementation                                                                                                                                                                                                                                                   | Supported Params                                    |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| **Hand Equity**       | Randomizes over some n trials.<br>• All inputs are first removed from the deck<br>• All-way chops are recorded as ties<br>• Chops between a subset of the players count as a win<br>• For players with unspecified hands, a random hand from the deck is drawn on each trial | PC: 1-10<br>Streets: Any<br>Custom deck: ✅                |
| **Range Equity**      | Enumerates over all possible hand combinations between ranges exactly n trials each.<br>• Above rules apply<br>• Exact card collisions are not an issue<br>• Does NOT account for blockers                                                                                                                         | PC: Any<br>Streets: Any<br>Range Size: Any<br>Custom deck: ✅ |
| **Semi-Bluff EV**      | Calculates EV based on showdown equity, player count, pot bet, and fold equity per player. Uses deduction                                                                                                                        | PC: Any<br>Streets: Any<br> |
| **Fold Equity Calculation**      | Calculates necessary average fold equity to break even based on showdown equity, player count, and pot bet. Uses root-finding.                                                                                                                       | PC: Any<br>Streets: Any<br> |
| **Custom Simulation** | Non-dealt streets are dealt, and winners are assessed.                                                                                                                                                                                                           | PC: Varies<br>Streets: Any<br>Custom deck: ✅              |
___
## Repo Structure
Top:
1. [`tutorial.ipynb`](https://github.com/sumaddury/pokeriq/blob/main/tutorial.ipynb): Short tutorial for PokerIQ functionality.
2. [`tests.ipynb`](https://github.com/sumaddury/pokeriq/blob/main/tests.ipynb): Few tests to ensure sanity and stability. Credits to PokerAI for solver references.
   
In `pokeriq` directory:
1. [`card.py`](https://github.com/sumaddury/pokeriq/blob/main/pokeriq/card.py): Contains `Card` class functionality.
2. [`deck.py`](https://github.com/sumaddury/pokeriq/blob/main/pokeriq/deck.py): Contains `Deck` class functionality.
3. [`made_hand.py`](https://github.com/sumaddury/pokeriq/blob/main/pokeriq/made_hand.py): Contains `Hand` class functionality.
4. [`player.py`](https://github.com/sumaddury/pokeriq/blob/main/pokeriq/player.py): Contains `Player` class functionality.
5. [`runout_simulation.py`](https://github.com/sumaddury/pokeriq/blob/main/pokeriq/runout_simulation.py): Contains `Simulation` class functionality.
6. [`equity_tools.py`](https://github.com/sumaddury/pokeriq/blob/main/pokeriq/equity_tools.py): Contains `EquitySolver` class functionality.
___


