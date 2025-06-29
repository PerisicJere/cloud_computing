import pytest

from cloud_computing.assingment1.bowling import Game


@pytest.fixture
def game():
    game = Game()
    yield game


def roll_many(game: Game, times: int, pins: int):
    for _ in range(times):
        game.roll(pins)


def test_gutter_game(game: Game):
    roll_many(game, 20, 0)
    assert game.score() == 0


def test_all_ones(game: Game):
    roll_many(game, 20, 1)
    assert game.score() == 20


def test_spare(game: Game):
    game.roll(5)
    game.roll(5)
    game.roll(3)
    roll_many(game, 17, 0)
    assert game.score() == 16


def test_strike(game: Game):
    game.roll(10)
    game.roll(3)
    roll_many(game, 16, 0)
    assert game.score() == 13
