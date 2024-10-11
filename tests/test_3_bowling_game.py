from src.bowling_game import Game
import pytest

@pytest.fixture
def bowling():
    return Game()



def test_valid1(bowling):
    bowling.roll(5)

    assert bowling.score() == 5

def test_valid2(bowling):
    bowling.roll(2)
    bowling.roll(4)

    assert bowling.score() == 6

def test_valid3(bowling):
    bowling.roll(6)
    bowling.roll(4)
    bowling.roll(4)
    bowling.roll(4)

    assert bowling.score() == 22

def test_valid4(bowling):
    bowling.roll(10)
    bowling.roll(4)
    bowling.roll(4)
    bowling.roll(4)

    assert bowling.score() == 30

def test_full_score(bowling):
    for i in range(0,12):
        bowling.roll(10)

    assert bowling.score() == 300

def test_invalid(bowling):
    with pytest.raises(ValueError):
        bowling.roll(11)

    with pytest.raises(ValueError):
        bowling.roll(4)
        bowling.roll(7)