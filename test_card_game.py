"""Pytest automation for module card_game.

There are test functions for each class found in card_game.

    Typical usage:

        pytest -v test_card_game.py --cov

    Author: Jeff Reagen
    Date: 1/13/2021
"""

import pytest
import card_game


@pytest.fixture
def card(rank, suit):
    """Returns a card object based on arguments."""
    return card_game.Card(rank, suit)


@pytest.mark.parametrize("rank, suit, expected_value", [
    (2, "Clubs", 8),
    (2, "Hearts", 6),
    (2,"Diamonds", 4),
    (2, "Spades", 2),
])
def test_card_value(rank, suit, expected_value):
    """Tests the computation of a given cards value."""
    my_card = card_game.Card(rank, suit)
    assert my_card.card_value == expected_value


@pytest.mark.parametrize("rank, suit, expected_value", [
    (2, "Clubs", "2 of Clubs"),
    (2, "Hearts", "2 of Hearts"),
    (2,"Diamonds", "2 of Diamonds"),
    (2, "Spades", "2 of Spades"),
    (13,"Spades", "King of Spades"),
])
def test_card__str__(rank, suit, expected_value):
    """Test the cards overloaded __str__ operator"""
    my_card = card_game.Card(rank, suit)
    assert str(my_card) == expected_value


@pytest.mark.parametrize("first_card, second_card, result", [
    ([2, "Hearts"], [3, "Hearts"], True),
    ([14, "Spades"], [14, "Clubs"], True),
    ([5, "Diamonds"], [4, "Hearts"], True),
    ([6, "Diamonds"], [13, "Spades"], False),
])
def test_card__gt__(first_card, second_card, result):
    """Test the cards overloaded __gt__ operator"""
    card_low = card_game.Card(first_card[0], first_card[1])
    card_high = card_game.Card(second_card[0], second_card[1])
    assert (card_high > card_low) == result

@pytest.fixture
def deck():
    """Returns a standard, un-shuffled deck of playing cards."""
    return card_game.Deck()


def test_deck(deck):
    """Verify that the deck contains fifty two cards"""
    assert len(deck.the_deck) == 52


def test_deal(deck):
    """Verify that the deal method returns the top card from the deck."""
    # get a copy of the top card
    # make sure deal delivers top card of deck
    card_count = len(deck.the_deck)
    top_card = deck.the_deck[0]
    dealt_card = deck.deal()
    assert (top_card == dealt_card) == (len(deck.the_deck) == (card_count - 1))


def test_shuffle(deck):
    """Verify that cards in deck get re-arranged."""
    # make an actual copy of the original deck
    initial_deck = list(deck.the_deck)
    deck.shuffle()
    assert initial_deck != deck.the_deck


def test_sort(deck):
    """Confirm that deck gets sorted in the expected order."""
    deck.sort()
    # deck should now be arranged by Spades, Diamonds, Hearts, Clubs with face
    # value for each suit in ascending order
    prev_card = None
    while deck.the_deck:
        if prev_card is None:
            prev_card = deck.the_deck.pop(0)
        else:
            next_card = deck.the_deck.pop(0)
            if next_card > prev_card:
                prev_card = next_card
            else:
                # found out of order card
                break

    assert len(deck.the_deck) == 0


@pytest.fixture
def player():
    """Returns a Player object."""

    name_id = 1
    return card_game.Player(name_id)


def test_player_name(player):
    """Verify player name created properly."""
    assert player.name == "Player 1"


def test_player_add_card(player):
    """Confirm a card is added to players cards and card value calculated properly."""
    new_card = card_game.Card(14, "Clubs")
    assert (len(player.cards) == 1) == (player.score == 56
                                        )


@pytest.mark.parametrize("player_count", [0, 1, 3, 100])
def test_card_game_player_failure(player_count):
    """Confirm that an exception is raised if number of players is incorrect."""
    with pytest.raises(ValueError):
        card_game.CardGame(player_count)


@pytest.mark.parametrize("player_count", [2])
def test_card_game_player_success(player_count):
    """Verify that the number of game players is created successfully"""
    new_game = card_game.CardGame(player_count)
    assert len(new_game.players) == 2


@pytest.fixture
def game():
    """Returns a CardGame object."""
    players = 2
    deck_sorted = True
    return card_game.CardGame(players, deck_sorted)


def test_play_card_game(game):
    """Verify each player gets three or more cards."""
    game.play_card_game()
    assert (len(game.players[0].cards) >= 3) == (len(game.players[1].cards) >= 3)


def test_show_winner(game):
    """Confirm that the expected winner wins the game.

    Note. Deck must be sorted for this test to work properly.
    """
    # Assumes sorted deck
    game.play_card_game()
    assert game.show_winner() == "Player 2"


def test_main_success(monkeypatch):
    """Confirm game is played properly when number of players is two."""
    monkeypatch.setattr("sys.argv", ["card_game.py", "2"])
    assert card_game.main() == 0


def test_main_sort_option(monkeypatch):
    """Confirm game plays properly when deck sort option is specified."""
    monkeypatch.setattr("sys.argv", ["card_game.py", "--sort", "2"])
    assert card_game.main() == 0


def test_main_failure(monkeypatch):
    """Confirm game doesn't play when invalid number players specified."""
    monkeypatch.setattr("sys.argv", ["card_game.py", "4"])
    assert card_game.main() != 0
