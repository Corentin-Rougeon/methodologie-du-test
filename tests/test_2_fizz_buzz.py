import sys

import pytest
from src.Ex2 import FizzBuzz


@pytest.fixture
def fizzbuzz():
    return FizzBuzz()


def test_fizzbuzz(fizzbuzz):
    assert fizzbuzz.fibu(15) == "FizzBuzz"

    assert fizzbuzz.fibu(9) == "Fizz"

    assert fizzbuzz.fibu(13) == ""

    assert fizzbuzz.fibu(-25) == "Buzz"

    assert fizzbuzz.fibu(sys.maxsize * 2 + 1) == "FizzBuzz"

    assert fizzbuzz.fibu(-sys.maxsize * 2 - 1) == "FizzBuzz"


def test_loop(fizzbuzz):
    expected = """1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz"""

    assert fizzbuzz.loop(15) == expected
