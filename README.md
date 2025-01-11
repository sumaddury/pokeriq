# PokerIQ ♠♥♦♣
![License](https://img.shields.io/badge/license-Apache%202.0-blue)
![Version](https://img.shields.io/badge/version-0.1.0-blue)
***
A micro-library intended for studying [No Limit Texas Hold'Em (NLH)](https://thelodgepokerclub.com/no-limit-texas-holdem-rules-beginners-guide/), written in pure Python. 

The library provides classes and tools for toy games, simulations, and inductive equity calculations. It is intended for approximation and ease-of-use, rather than a replacement for more rigorous [GTO](https://blog.gtowizard.com/what-is-gto-in-poker/) study.
***
## Overview
_No Limit Hold'Em is the most popular variant of poker, allowing for uncapped betting across multiple streets which creates a more complex layer of strategy. The goal of this package is to provide the basic tools needed to understand NLH inductively. It includes six main classes that work together to allow for custom simulation and equity calculation:_
1. **Card**: Provides functionality for individual cards, including several generation mechanisms.
2. **Hand**: Performs made hand strength calculations and comparison
3. **Player**: Encapsulates information about individual players (stack, hole, made hand, etc.).
4. **Deck**: Provides functionality for a deck (burn, draw, deal, shuffle, etc.)
5. **Simulation**: Encapsulates all information about a given trial, running the board out, assessing winners, etc.
6. **EquitySolver**: The main equity calculation mechanism. Provides functionality for both hand and range equity calculation for up to 10 players on any street.

To get started, read the short tutorial notebook.
***
## Instalation


