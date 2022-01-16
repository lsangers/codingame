"""Tests fro my new bot classes as they do not work as expected at the moment :)"""
from ..new_bot import UltimateBoard, get_valid_actions, has_won
import numpy as np

def test_get_valid_actions():
    """Test get_valid_actions"""
    #moves when only 1 spot free
    moves = get_valid_actions(0b011111111)
    assert len(moves) == 1
    assert moves[0] & 0b100000000

    moves = get_valid_actions(0b101111111)
    assert len(moves) == 1
    assert moves[0] & 0b010000000

    moves = get_valid_actions(0b110111111)
    assert len(moves) == 1
    assert moves[0] & 0b001000000

    moves = get_valid_actions(0b111011111)
    assert len(moves) == 1
    assert moves[0] & 0b000100000

    moves = get_valid_actions(0b111101111)
    assert len(moves) == 1
    assert moves[0] & 0b000010000

    moves = get_valid_actions(0b111110111)
    assert len(moves) == 1
    assert moves[0] & 0b000001000

    moves = get_valid_actions(0b111111011)
    assert len(moves) == 1
    assert moves[0] & 0b000000100

    moves = get_valid_actions(0b111111101)
    assert len(moves) == 1
    assert moves[0] & 0b000000010

    moves = get_valid_actions(0b111111110)
    assert len(moves) == 1
    assert moves[0] & 0b000000001

    #moves on an empty board
    moves = get_valid_actions(0b000000000)
    assert len(moves) == 9

    #few other options
    moves = get_valid_actions(0b000011111)
    assert len(moves) == 4
    moves = get_valid_actions(0b101010101)
    assert len(moves) == 4
    moves = get_valid_actions(0b010101010)
    assert len(moves) == 5

def test_has_won():
    """Test has_won"""
    win = has_won(0b001010100)
    assert win is True
    
    loss = has_won(0b101000101)
    assert loss is False

def test_monte_carlo_play():
    """Test the play method of the Monte Carlo Node class."""

    #empty board with player_1 moving
    board = UltimateBoard(False, (0, 0b100000000))
    
    board._grid_player_1 = np.array([435, 334,  69, 210, 100, 220, 241, 377, 184])
    board._grid_player_2 = np.array([ 76, 177, 442, 301, 411, 291, 270, 134, 326])

    board._player_1 = 299
    board._player_2 = 112

    board._move = (0, 0b100000000)

    actions = board.get_valid_actions()

    assert actions == 0



