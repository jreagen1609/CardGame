#!/usr/bin/env python3
"""This module supports a two player card game.

Two players are dealt three cards alternating back and forth.
The player with the higher score wns the game.
By default, the game builds a deck and then shuffles
the deck. The deck is not sorted.

Assumptions associated with design:
    1. Standard 52 card playing deck
    2. Two players per game
    3. Values for face cards: Jack = 11, Queen = 12, King = 13, Ace = 14
    4. Values associates with card suits: Spades = 1, Diamonds = 2, Hearts = 3, Clubs = 4
    5. The deck is not sorted by default.
    6. Sorting of the deck is by suit, followed by rank
    7. Exceptions vs error values. For the most part returning an error code was used
       instead of an exception because the code bodies were very short. It is
       an easy exercise to replace error codes with exceptions if that was
       desired.0000

    Typical usage example:

    game = CardGame()
    game.play_the_game()
    game.show_winner()

Game developed and unit tested using the following environment:
    macOS Big Sur, version 11.1
    Python3, version 3.9.1
    PyCharm 2020.3
    Pytest, version 6.2.1
    Pycov, version 5.3.1

    Author: Jeff Reagen
    Date: 1/13/2021

"""

import argparse
import random
from operator import attrgetter


class Card:
    """Class Card is used to represent a playing card.

    Each card represents a card from a standard 52 card deck.
    Numeric cards e.g. 2-10 have a rank corresponding to the card number.
    Face cards, e.g. Jack, Queen, King, Ace have values 11, 12, 13, and 14 respectively.

    The four card suits have different values. Spades are worth 1, Diamonds are 2,
    Hearts are 3, and Clubs are 4.

    Card value is determined by multiplying card rank by card suit

    """

    # Dictionary for simple suit to value lookup
    suit_values = {"Spades" : 1, "Diamonds" : 2, "Hearts" : 3, "Clubs" : 4}

    # Dictionary for rank to face card lookup
    face_value = {
        11: "Jack",
        12: "Queen",
        13: "King",
        14: "Ace",
    }

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.suit_sort = Card.suit_values[self.suit]

    @property
    def card_value(self):
        """Property returning value associated with the card.

        Card value is computed based on rank of card
        and the suit.

        Args:
            None
        Returns:
            int representing value of card
        Raises:
            None
        """

        # compute card score.
        # Could have done this during init as well since card value doesn't change
        return self.rank * self.suit_values[self.suit]

    def __str__(self):
        """Returns rank and suit of card as a string.

        Args:
            None
        Returns:
            String representing card. For example, Ace of Spades.
        Raises:
            None
        """

        if self.rank in Card.face_value:
            face = Card.face_value[self.rank]
        else:
            face = self.rank
        return "%s of %s" % (face, self.suit)

    def __gt__(self, other):
        """Determine if one card is ranked higher than another based on rank and suit.

        Args:
            other: the second card to compare
        Returns:
            bool - true if 2 cards have the same suit and the first card
                   is greater than the second.
                 - true if both cards have different suits, and the first suit
                   ranks higher than the second
            bool - false otherwise.
        """

        if self.suit == other.suit:
            return_value = bool(self.rank > other.rank)
        else:
            return_value = bool(Card.suit_values[self.suit] > Card.suit_values[other.suit])
        return return_value


class Deck:
    """Class Deck represents a standard deck of fifty two cards.

    The Deck class contains various methods to shuffle and sort the deck.
    A deal method returns the top card on the deck.
    """

    suits = ["Spades", "Diamonds", "Hearts", "Clubs"]

    def __init__(self):
        self.the_deck = list()
        for suit in Deck.suits:
            for rank in range(2, 15):
                new_card = Card(rank, suit)
                self.the_deck.append(new_card)

    def shuffle(self):
        """Method shuffle causes the deck to be shuffled.

        The shuffle method mixes the card in the deck
        in a random order.

        Args:
            None
        Returns:
            None. Deck is shuffled in place.
        Raises:
            None
        """
        random.shuffle(self.the_deck)


    def sort(self):
        """Method sort() sorts the deck in ascending order.

        The sort is based on the card rank and then the value associated
        with the card suit. For example, if the deck contains
        (Spades,2), (Diamonds,5), (Spades, King), (Hearts,3), (Clubs,Ace)

        then the sort() method will reorganize the deck such
        that the new order is:
        (Spades,2), (Spades,King), (Diamonds,5), (Hearts,3), (Clubs,Ace)

        Args:
            None

        Returns:
            None. Deck is sorted in place

        Raises:
            None

        """

        self.the_deck.sort(key=attrgetter('rank'))
        self.the_deck.sort(key=attrgetter('suit_sort'))
        # self.show_deck()

    def deal(self):
        """Method Deal() returns the top card from the deck.

        Args:
            None

        Returns:
            next card from top of deck

            None if deck is empty

        Raises:
            None
        """

        # validate there are cards left to deal
        if self.the_deck:
            return self.the_deck.pop(0)  # return next card from top of deck
        return None

    def show_deck(self):
        """Print each card from the deck.

        Intended for debug use only to verify deck
        is in expected order e.g. shuffled or sorted.
        """
        for card in self.the_deck:
            print(card)


class Player:
    """Class Player represents a game player.

    The class keeps track of the players hand,
    allows a card to be added to the hand,
    and computes the score associated with
    the players hand.
    """

    def __init__(self, name):

        self.name = "Player " + str(name)
        self.cards = list()
        self.player_score = 0

    def add_card(self, new_card):
        """Adds a card to the players hand.

        After adding the card to the existing hand,
        add_card() updates the players score.

            Args:
                 new_card: int representing the player name
            Returns:
                None
            Raises:
                None
        """

        self.cards.append(new_card)
        self.player_score += new_card.card_value

    @property
    def score(self):
        """Retrieves the score associated with the players cards.

        Implemented as a property to make comparing the score
        of two players easier to read and understand.

            Args:
                None
            Returns:
                int representing the player score
            Raises:
                None
        """
        return self.player_score

    def __gt__(self, other):
        """Overloaded greater than operator simplifies comparison of players scores.

        Increases program readability.

            Args:
                other: player class to be compared against
            Returns:
                bool - True if self > other, otherwise False
        """
        return self.player_score > other.player_score


class CardGame:
    """A class representing a two player card game using a standard deck.

    Typical usage:
        new_game = CardGame()
        new_game.play_the_game()
        new_game.show_winner()
    """

    GAME_PLAYERS_REQUIRED = 2

    def __init__ (self, num_players=2, sort_deck=False, cards_per_player=3):
        """Creates class object based on specified parameters.

        This function is designed with flexibility to expand or
        create different games. For example, instead of two players,
        the game could be changed to five players. If the number of players
        does change, then some work will need to be done on the error checking
        associated with the player count. Another example is the number of
        cards dealt which could be changed from three to something
        larger like 10.

            Args:
                num_players: number of players in the game
                sort_deck: bool indicating whether or not to sort deck
                cards_per_player: number of cards to deal to each player
            Returns:
                CardGame object
            Raises:
                ValueError: if number of layers is no GAME_PLAYERS_REQUIRED.
        """
        self.players = list()
        self.num_players = num_players
        self.sort_deck = sort_deck
        self.cards_per_player = cards_per_player
        if self.num_players != CardGame.GAME_PLAYERS_REQUIRED:
            raise ValueError("Incorrect player count specified.")

        # instantiate players
        for player_name in range(1, self.num_players+1):
            self.players.append(Player(player_name))

    def play_card_game(self):
        """Method play_card_game creates a deck and deals the cards to players.

        The deck is created and then shuffled. Optionally, the deck will be sorted
        if the CardGame object was created with the sort option set to True.

        play_card_method defaults to dealing three cards to each player, from
        the top of the deck alternating between players one card per deal.

            Args:
                None
            Returns:
                None
            Raises:
                None
        """

        deck = Deck()
        deck.shuffle()
        if self.sort_deck:
            deck.sort()  # sort based on rank and suit

        # deal cards to players in round robin fashion.
        current_player = 0
        cards_to_deal = self.num_players * self.cards_per_player
        while cards_to_deal > 0:
            next_card = deck.deal()
            if next_card is None:   # no mre cards left in deck
                break
            self.players[current_player].add_card(next_card)
            current_player = (current_player + 1) % self.num_players
            cards_to_deal -= 1

    def show_winner(self):
        """Determines winner of the game.


        The winner is considered the player with the highest score.

        Args:
            None
        Returns:
            Player - object represent winning player
        Raises:
            None
        """

        winner = self.players.pop(0)
        while self.players:
            compare = self.players.pop(0)
            if compare > winner:
                winner = compare
        return winner.name


def main(args=None):
    """The top level function which sets the game environment up for play.

    The purpose of this function is to isolate the __main__ body of the program
    so that importing of the module by some other module does not cause main
    to get executed.

    Args:
        None
    Returns:
        None
    Raises:
        None
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("num_players", help="enter number of game players", type=int)
    parser.add_argument("-s", "--sort", action="store_true", default=False,
                        help="enables sorting of the card deck")
    args = parser.parse_args()

    try:
        game = CardGame(args.num_players, args.sort)
    except ValueError as exception:
        print("Game over. %s\n\n" % exception)
    else:
        game.play_card_game()
        print("%s wins!" % (game.show_winner()))
        return 0


# main program starts here
if __name__ == "__main__":
    main()
