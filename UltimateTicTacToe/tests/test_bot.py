"""Tests fro my bot classes as they do not work as expected at the moment :)"""
from ..bot import Action

def test_action():
    """Test the Action class"""
    action = Action(4, 7, 2)

    assert action.tuple() == (2, 4, 7)
