"""My implementation for Codingame Ultimate TicTacToe."""
from __future__ import annotations
from abc import ABC, abstractmethod
import datetime
from functools import lru_cache
from math import log
from random import randrange, shuffle
import sys

# RAND_INDEX = 0
# RANDOM_MOVES = [
#     randrange(0, 1000) for _ in range(1000)
# ]
# def get_randomint(max_val):
#     global RAND_INDEX
#     res = (RANDOM_MOVES[RAND_INDEX])%max_val
#     RAND_INDEX += 1
#     if RAND_INDEX > 999:
#         shuffle(RANDOM_MOVES)
#         RAND_INDEX = 0
#     return res

MOVES = [
    0b000000001,
    0b000000010,
    0b000000100,
    0b000001000,
    0b000010000,
    0b000100000,
    0b001000000,
    0b010000000,
    0b100000000,
]
WINS = [
    0b111000000,
    0b000111000,
    0b000000111,

    0b100100100,
    0b010010010,
    0b001001001,

    0b100010001,
    0b001010100,
]
SMALL_TO_BIG = {
    0b000000001: 8,
    0b000000010: 7,
    0b000000100: 6,
    0b000001000: 5,
    0b000010000: 4,
    0b000100000: 3,
    0b001000000: 2,
    0b010000000: 1,
    0b100000000: 0,
}
BIG_TO_SMALL = {
    8: 0b000000001,
    7: 0b000000010,
    6: 0b000000100,
    5: 0b000001000,
    4: 0b000010000,
    3: 0b000100000,
    2: 0b001000000,
    1: 0b010000000,
    0: 0b100000000,
}
ACTION_TO_STRING = {
    (0, 0b100000000): "0 0",
    (0, 0b010000000): "0 1",
    (0, 0b001000000): "0 2",
    (0, 0b000100000): "1 0",
    (0, 0b000010000): "1 1",
    (0, 0b000001000): "1 2",
    (0, 0b000000100): "2 0",
    (0, 0b000000010): "2 1",
    (0, 0b000000001): "2 2",

    (1, 0b100000000): "0 3",
    (1, 0b010000000): "0 4",
    (1, 0b001000000): "0 5",
    (1, 0b000100000): "1 3",
    (1, 0b000010000): "1 4",
    (1, 0b000001000): "1 5",
    (1, 0b000000100): "2 3",
    (1, 0b000000010): "2 4",
    (1, 0b000000001): "2 5",

    (2, 0b100000000): "0 6",
    (2, 0b010000000): "0 7",
    (2, 0b001000000): "0 8",
    (2, 0b000100000): "1 6",
    (2, 0b000010000): "1 7",
    (2, 0b000001000): "1 8",
    (2, 0b000000100): "2 6",
    (2, 0b000000010): "2 7",
    (2, 0b000000001): "2 8",

    (3, 0b100000000): "3 0",
    (3, 0b010000000): "3 1",
    (3, 0b001000000): "3 2",
    (3, 0b000100000): "4 0",
    (3, 0b000010000): "4 1",
    (3, 0b000001000): "4 2",
    (3, 0b000000100): "5 0",
    (3, 0b000000010): "5 1",
    (3, 0b000000001): "5 2",

    (4, 0b100000000): "3 3",
    (4, 0b010000000): "3 4",
    (4, 0b001000000): "3 5",
    (4, 0b000100000): "4 3",
    (4, 0b000010000): "4 4",
    (4, 0b000001000): "4 5",
    (4, 0b000000100): "5 3",
    (4, 0b000000010): "5 4",
    (4, 0b000000001): "5 5",

    (5, 0b100000000): "3 6",
    (5, 0b010000000): "3 7",
    (5, 0b001000000): "3 8",
    (5, 0b000100000): "4 6",
    (5, 0b000010000): "4 7",
    (5, 0b000001000): "4 8",
    (5, 0b000000100): "5 6",
    (5, 0b000000010): "5 7",
    (5, 0b000000001): "5 8",

    (6, 0b100000000): "6 0",
    (6, 0b010000000): "6 1",
    (6, 0b001000000): "6 2",
    (6, 0b000100000): "7 0",
    (6, 0b000010000): "7 1",
    (6, 0b000001000): "7 2",
    (6, 0b000000100): "8 0",
    (6, 0b000000010): "8 1",
    (6, 0b000000001): "8 2",

    (7, 0b100000000): "6 3",
    (7, 0b010000000): "6 4",
    (7, 0b001000000): "6 5",
    (7, 0b000100000): "7 3",
    (7, 0b000010000): "7 4",
    (7, 0b000001000): "7 5",
    (7, 0b000000100): "8 3",
    (7, 0b000000010): "8 4",
    (7, 0b000000001): "8 5",

    (8, 0b100000000): "6 6",
    (8, 0b010000000): "6 7",
    (8, 0b001000000): "6 8",
    (8, 0b000100000): "7 6",
    (8, 0b000010000): "7 7",
    (8, 0b000001000): "7 8",
    (8, 0b000000100): "8 6",
    (8, 0b000000010): "8 7",
    (8, 0b000000001): "8 8",
}
STRING_TO_ACTION = {
    "0 0": (0, 0b100000000),
    "0 1": (0, 0b010000000),
    "0 2": (0, 0b001000000),
    "1 0": (0, 0b000100000),
    "1 1": (0, 0b000010000),
    "1 2": (0, 0b000001000),
    "2 0": (0, 0b000000100),
    "2 1": (0, 0b000000010),
    "2 2": (0, 0b000000001),

    "0 3": (1, 0b100000000),
    "0 4": (1, 0b010000000),
    "0 5": (1, 0b001000000),
    "1 3": (1, 0b000100000),
    "1 4": (1, 0b000010000),
    "1 5": (1, 0b000001000),
    "2 3": (1, 0b000000100),
    "2 4": (1, 0b000000010),
    "2 5": (1, 0b000000001),

    "0 6": (2, 0b100000000),
    "0 7": (2, 0b010000000),
    "0 8": (2, 0b001000000),
    "1 6": (2, 0b000100000),
    "1 7": (2, 0b000010000),
    "1 8": (2, 0b000001000),
    "2 6": (2, 0b000000100),
    "2 7": (2, 0b000000010),
    "2 8": (2, 0b000000001),

    "3 0": (3, 0b100000000),
    "3 1": (3, 0b010000000),
    "3 2": (3, 0b001000000),
    "4 0": (3, 0b000100000),
    "4 1": (3, 0b000010000),
    "4 2": (3, 0b000001000),
    "5 0": (3, 0b000000100),
    "5 1": (3, 0b000000010),
    "5 2": (3, 0b000000001),

    "3 3": (4, 0b100000000),
    "3 4": (4, 0b010000000),
    "3 5": (4, 0b001000000),
    "4 3": (4, 0b000100000),
    "4 4": (4, 0b000010000),
    "4 5": (4, 0b000001000),
    "5 3": (4, 0b000000100),
    "5 4": (4, 0b000000010),
    "5 5": (4, 0b000000001),

    "3 6": (5, 0b100000000),
    "3 7": (5, 0b010000000),
    "3 8": (5, 0b001000000),
    "4 6": (5, 0b000100000),
    "4 7": (5, 0b000010000),
    "4 8": (5, 0b000001000),
    "5 6": (5, 0b000000100),
    "5 7": (5, 0b000000010),
    "5 8": (5, 0b000000001),

    "6 0": (6, 0b100000000),
    "6 1": (6, 0b010000000),
    "6 2": (6, 0b001000000),
    "7 0": (6, 0b000100000),
    "7 1": (6, 0b000010000),
    "7 2": (6, 0b000001000),
    "8 0": (6, 0b000000100),
    "8 1": (6, 0b000000010),
    "8 2": (6, 0b000000001),

    "6 3": (7, 0b100000000),
    "6 4": (7, 0b010000000),
    "6 5": (7, 0b001000000),
    "7 3": (7, 0b000100000),
    "7 4": (7, 0b000010000),
    "7 5": (7, 0b000001000),
    "8 3": (7, 0b000000100),
    "8 4": (7, 0b000000010),
    "8 5": (7, 0b000000001),

    "6 6": (8, 0b100000000),
    "6 7": (8, 0b010000000),
    "6 8": (8, 0b001000000),
    "7 6": (8, 0b000100000),
    "7 7": (8, 0b000010000),
    "7 8": (8, 0b000001000),
    "8 6": (8, 0b000000100),
    "8 7": (8, 0b000000010),
    "8 8": (8, 0b000000001),
}
@lru_cache
def won(board):
    """Returns lambda to determine win."""
    return lambda move: not move & board
VALID_ACTIONS = {
    board: list(filter(won(board), MOVES))
    for board in range(0b000000000, 0b1000000000)
}
@lru_cache
def to_big(index):
    """Returns lambda to translate small to big move."""
    return lambda action: (index, action)

TRANSLATED_VALID_ACTIONS = {
    index: {
        board: list(map(to_big(index), VALID_ACTIONS[board]))
        for board in range(0b000000000, 0b1000000000)
    } for index in range(9)
}

def win(state):
    """Returns whether state is a win."""
    return lambda win: ((win & state) == win)
HAS_WON = {
    state: any(map(win(state), WINS))
    for state in range(0b000000000, 0b1000000000)
}
IS_TERMINAL = {
    player_1: {
        player_2: HAS_WON[player_1] \
            or HAS_WON[player_2] \
            or (player_1 | player_2) == 0b111111111
        for player_2 in range(0b000000000, 0b1000000000)
    }
    for player_1 in range(0b000000000, 0b1000000000)
}

C = 1.41
@lru_cache
def calculate_utc(score: int, visited_count: int, parent_visited_count: int) -> float:
    """Return the UTC value of this node.
    Based on: https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
    Section Exploration and exploitation.

    """
    visited_count = visited_count if visited_count else 1
    return (score/visited_count) \
            + C * (log(parent_visited_count)/visited_count)**.5

class MonteCarloNode(ABC):
    """Base class for a Monte Carlo Tree Search state"""

    def __init__(self, parent:MonteCarloNode = None) -> None:
        self.visited_count = 1
        self.score = 0
        self._last_utc_calc_visit_count = -5
        self._last_child_calc_visit_count = -5
        self._utc = 0
        self.parent = parent
        self.unvisited_actions = []
        self.sorted_actions = []
        self.children = {}

    @property
    def utc(self) -> float:
        """Return hopefully cached UTC."""
        if self._last_utc_calc_visit_count < self.visited_count:
            self._last_utc_calc_visit_count = self.visited_count
            self._utc = calculate_utc(self.score, self.visited_count, self.parent.visited_count)
        return self._utc

    def select_leaf(self) -> MonteCarloNode:
        """Select a Leaf Node for the next iterations.
        Note: if fully expanded is recursive!

        """
        if not self.children:
            self.expand()
            if not self.unvisited_actions:
                return self
            shuffle(self.unvisited_actions)

        if self.unvisited_actions:
            self.sorted_actions.insert(0, self.unvisited_actions.pop())
            return self.children[self.sorted_actions[0]]
        return self.children[self.sorted_actions[0]].select_leaf()

    @abstractmethod
    def expand(self):
        """Create all Child Nodes."""

    @abstractmethod
    def simulate(self) -> bool:
        """Complete one playout."""

    def backpropagate(self, winning:bool, turn_counter: int) -> None:
        """Use the result of the simulation to update information
        in the Nodes on the from the Child Node to the root Node.

        """
        self.visited_count += 1
        if winning:
            self.score += 1 + 1/turn_counter
        else:
            self.score -= 1 + 1/turn_counter
        if self.parent:
            if self.parent.parent:
                self.parent.backpropagate(not winning, turn_counter)
            if self.sorted_actions:
                self.update_sorted_actions()

    def update_sorted_actions(self):
        """Update the sorted list of actions"""
        utc = self.utc
        sorted_actions = self.parent.sorted_actions
        tmp_move = sorted_actions[0]
        for pos in range(1, len(sorted_actions)):
            if self.parent.children[sorted_actions[pos]].utc > utc:
                sorted_actions[pos-1] = sorted_actions[pos]
            else:
                if pos > 1:
                    sorted_actions[pos-1] = tmp_move
                else:
                    sorted_actions[0] = tmp_move
                break


    def run(self, run_time: float) -> None:
        """Run simulations until we run out of run_time"""
        # count = 0
        begin = datetime.datetime.now()
        while (datetime.datetime.now() - begin).total_seconds() < run_time:
            self.select_leaf().simulate()
        #     count += 1
        # print(str(count), file=sys.stderr, flush = True)


class UltimateBoard(MonteCarloNode):
    """Class for Ultimate TicTacToe board."""
    def __init__(self,
            is_player_1: bool = False,
            move: tuple[int] = None,
            parent: UltimateBoard = None
        ) -> None:
        super().__init__(parent)

        self.is_player_1 = is_player_1
        if parent is None:
            self._grid_player_1 = [0b000000000 for _ in range(9)]
            self._grid_player_2 = [0b000000000 for _ in range(9)]
            self._player_1 = 0b000000000
            self._player_2 = 0b000000000
        else:
            self._grid_player_1 = parent._grid_player_1[:]
            self._grid_player_2 = parent._grid_player_2[:]
            self._player_1 = parent._player_1
            self._player_2 = parent._player_2

        self.move = move
        self.play()

    def get_valid_actions(self) -> list[tuple[int]]:
        """List of valid moves on this board."""
        valid_actions = []

        if self.move is not None:
            index = SMALL_TO_BIG[self.move[1]]
            if not IS_TERMINAL[self._grid_player_1[index]][self._grid_player_2[index]]:
                valid_actions = \
                    TRANSLATED_VALID_ACTIONS[index]\
                        [self._grid_player_1[index] | self._grid_player_2[index]]
        if not valid_actions:
            for playable_board in VALID_ACTIONS[self._player_1 | self._player_2]:
                index = SMALL_TO_BIG[playable_board]
                valid_actions.extend(
                    TRANSLATED_VALID_ACTIONS[index]\
                        [self._grid_player_1[index] | self._grid_player_2[index]]
                )

        return valid_actions

    def play(self) -> None:
        """Play a given move on this board."""

        if self.is_player_1:
            self._grid_player_1[self.move[0]] |= self.move[1]
            if HAS_WON[self._grid_player_1[self.move[0]]]:
                self._player_1 |= BIG_TO_SMALL[self.move[0]]
                self._grid_player_1[self.move[0]] = 0b111111111
                self._grid_player_2[self.move[0]] = 0b000000000

        else:
            self._grid_player_2[self.move[0]] |= self.move[1]
            if HAS_WON[self._grid_player_2[self.move[0]]]:
                self._player_2 |= BIG_TO_SMALL[self.move[0]]
                self._grid_player_1[self.move[0]] = 0b000000000
                self._grid_player_2[self.move[0]] = 0b111111111

    def expand(self):
        actions = self.get_valid_actions()

        for action in actions:
            action = action if isinstance(action, tuple) \
                else (SMALL_TO_BIG[self.move[1]], action)
            child_node = UltimateBoard(not self.is_player_1, action, self)
            self.unvisited_actions.append(action)
            self.children[action] = child_node

    def simulate(self):
        simulation_board = UltimateBoard(self.is_player_1, self.move, self.parent)
        turn_counter = 1
        while not IS_TERMINAL[self._player_1][self._player_2]:
            turn_counter += 1
            actions = simulation_board.get_valid_actions()
            if not actions:
                break
            simulation_board.move = actions[randrange(0, len(actions))]
            simulation_board.play()
            simulation_board.is_player_1 = not simulation_board.is_player_1

        self.backpropagate(
            HAS_WON[self._player_1] if self.is_player_1 \
                else HAS_WON[self._player_2],
            turn_counter
        )

    def print_move(self):
        """Print the best move to console.
        Note: They expect first the y coord then the x coord.
        """
        print(ACTION_TO_STRING[self.move])

def main():
    """Main"""
    #first turn
    opponent = input()
    valid_action_count = int(input())
    for _ in range(valid_action_count):
        _, valid_action_count = [int(j) for j in input().split()]

    root = None

    if opponent[0] == '-':
        root = UltimateBoard(True, (0, 0b100000000), None)
        root.run(.99)
        print("0 0")
    else:
        root = UltimateBoard(False, STRING_TO_ACTION[opponent], None)
        root.run(.99)
        root = root.children[root.sorted_actions[0]]
        root.parent = None
        root.print_move()


    #game loop
    while True:
        # opponent = input()
        # valid_action_count = int(input())
        # for _ in range(valid_action_count):
        #     _, _ = [int(j) for j in input().split()]

        if not root.children:
            root.expand()

        if not root.children:
            if HAS_WON[root._player_1]:
                print("player 1 has won")
            elif HAS_WON[root._player_2]:
                print("player 2 has won")
            else:
                print("draw")
            return

        # root = root.children[STRING_TO_ACTION[opponent]]
        root.run(.08)
        root = root.children[root.sorted_actions[0]]
        root.parent = None
        root.print_move()

# main()
