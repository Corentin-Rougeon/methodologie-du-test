import pytest
from src.Ex1 import Song

@pytest.fixture
def song():
    return Song()

def test_phrase(song):
    assert "3 kilomètres à pied, ¸ca use, ¸ca use," == song.phrase1(3)
    assert "1 kilomètre à pied, ¸ca use, ¸ca use," == song.phrase1(1)
    assert "20000000 kilomètres à pied, ¸ca use, ¸ca use," == song.phrase1(20_000_000)

def test_phrase2(song):
    assert "1 kilomètre à pied, ¸ca use, ¸ca use," == song.phrase1(1)
    assert "10 kilomètres à pied, ¸ca use, ¸ca use," == song.phrase1(10)
    assert "2000000 kilomètres à pied, ¸ca use, ¸ca use," == song.phrase1(2_000_000)

def test_song(song):
    expected = """1 kilomètre à pied, ¸ca use, ¸ca use,
1 kilomètre à pied, ca use les souliers.

2 kilomètres à pied, ¸ca use, ¸ca use,
2 kilomètres à pied, ca use les souliers."""

    assert expected == song.sing(2)

    expected = """1 kilomètre à pied, ¸ca use, ¸ca use,
1 kilomètre à pied, ca use les souliers.

2 kilomètres à pied, ¸ca use, ¸ca use,
2 kilomètres à pied, ca use les souliers.

3 kilomètres à pied, ¸ca use, ¸ca use,
3 kilomètres à pied, ca use les souliers."""

    assert expected == song.sing(3)

def test_song_minus(song):
    assert "" == song.sing(-1)