"""My implementation for Codingame Ultimate TicTacToe."""
from __future__ import annotations
from abc import ABC, abstractmethod
import datetime
from functools import lru_cache
from math import log, sqrt
from random import choice, shuffle
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
VALID_ACTIONS_LEN = {
    board: len(actions)
    for board, actions in VALID_ACTIONS.items()
}
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

C = .6
@lru_cache
def calculate_utc(score: int, visited_count: int, parent_visited_count: int) -> float:
    """Return the UTC value of this node.
    Based on: https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
    Section Exploration and exploitation.

    """
    return (score/visited_count) \
            + C * sqrt(log(parent_visited_count)/visited_count)

def get_valid_actions(move, grid_player_1, grid_player_2, player_1, player_2) -> list[tuple[int, int]]:
    """List of valid moves on this board."""
    valid_actions = []

    if move is not None:
        index = SMALL_TO_BIG[move[1]]
        if not IS_TERMINAL[grid_player_1[index]][grid_player_2[index]]:
            valid_actions.extend(TRANSLATED_VALID_ACTIONS[index]\
                [grid_player_1[index] | grid_player_2[index]])

    if not valid_actions:
        for playable_board in VALID_ACTIONS[player_1 | player_2]:
            index = SMALL_TO_BIG[playable_board]
            valid_actions.extend(
                TRANSLATED_VALID_ACTIONS[index]\
                    [grid_player_1[index] | grid_player_2[index]]
            )

    return valid_actions

class UltimateBoard():
    """Class for Ultimate TicTacToe board."""
    def __init__(self,
            is_player_1: bool = False,
            move: tuple[int, int] = None,
            parent: UltimateBoard = None
        ) -> None:
        self.visited_count = 1
        self.score = 0
        self.parent = parent
        self.unvisited_actions = []
        self.children = {}
        self.children_refs = []

        self.is_player_1 = is_player_1
        if parent is None:
            self.grid_player_1 = [0b000000000 for _ in range(9)]
            self.grid_player_2 = [0b000000000 for _ in range(9)]
            self.player_1 = 0b000000000
            self.player_2 = 0b000000000
        else:
            self.grid_player_1 = parent.grid_player_1[:]
            self.grid_player_2 = parent.grid_player_2[:]
            self.player_1 = parent.player_1
            self.player_2 = parent.player_2

        self.move = move
        if self.is_player_1:
            self.grid_player_1[self.move[0]] |= self.move[1]
            if HAS_WON[self.grid_player_1[self.move[0]]]:
                self.player_1 |= BIG_TO_SMALL[self.move[0]]

        else:
            self.grid_player_2[self.move[0]] |= self.move[1]
            if HAS_WON[self.grid_player_2[self.move[0]]]:
                self.player_2 |= BIG_TO_SMALL[self.move[0]]

    @property
    def utc(self) -> float:
        """Return hopefully cached UTC."""
        return calculate_utc(self.score, self.visited_count, self.parent.visited_count)
    @property
    def next_child(self) -> UltimateBoard:
        """Select the node with currently the highest utc value."""
        return max(self.children_refs, key=lambda child: child.utc)
    @property
    def best_child(self) -> UltimateBoard:
        """Select the node with currently the highest score per visit."""
        return max(self.children_refs, key=lambda child: child.visited_count)

    def get_valid_actions(self) -> list[tuple[int, int]]:
        """List of valid moves on this board."""
        valid_actions = []

        if self.move is not None:
            index = SMALL_TO_BIG[self.move[1]]
            if not IS_TERMINAL[self.grid_player_1[index]][self.grid_player_2[index]]:
                valid_actions.extend(TRANSLATED_VALID_ACTIONS[index]\
                        [self.grid_player_1[index] | self.grid_player_2[index]][:])

        if not valid_actions:
            for playable_board in VALID_ACTIONS[self.player_1 | self.player_2]:
                index = SMALL_TO_BIG[playable_board]
                valid_actions.extend(
                    TRANSLATED_VALID_ACTIONS[index]\
                        [self.grid_player_1[index] | self.grid_player_2[index]]
                )

        return valid_actions


    def run(self, run_time: float) -> None:
        """Run simulations until we run out of run_time"""
        count = 0
        begin = datetime.datetime.now()
        while (datetime.datetime.now() - begin).total_seconds() < run_time:
            #selection
            node = self
            while True:
                if not node.unvisited_actions and not node.children:
                    node.unvisited_actions.extend(node.get_valid_actions())
                    if not node.unvisited_actions:
                        break
                    shuffle(node.unvisited_actions)

                if node.unvisited_actions:
                    action = node.unvisited_actions.pop()
                    node.children[action] = UltimateBoard(not node.is_player_1, action, node)
                    node.children_refs.append(node.children[action])
                    node = node.children[action]
                    break
                node = node.next_child

            #simulation
            # simulation_board = UltimateBoard(node.is_player_1, node.move, node.parent)
            player_1_score = 0
            player_2_score = 0
            visits = 1
            depth = 0
            loc_grid_player_1 = node.grid_player_1[:]
            loc_grid_player_2 = node.grid_player_2[:]
            loc_player_1 = node.player_1
            loc_player_2 = node.player_2
            loc_is_player_1 = node.is_player_1
            big_move, small_move = last_move = node.move
            if loc_is_player_1:
                loc_grid_player_1[big_move] \
                    |= small_move
                if HAS_WON[loc_grid_player_1[big_move]]:
                    loc_player_1 |= BIG_TO_SMALL[big_move]
            else:
                loc_grid_player_2[big_move] \
                    |= small_move
                if HAS_WON[loc_grid_player_2[big_move]]:
                    loc_player_2 |= BIG_TO_SMALL[big_move]


            while not IS_TERMINAL[loc_player_1][loc_player_2]:
                depth += 1
                actions = get_valid_actions(
                    last_move,
                    loc_grid_player_1,
                    loc_grid_player_2,
                    loc_player_1,
                    loc_player_2
                )
                if not actions:
                    break
                big_move, small_move = last_move = choice(actions)
                # simulation_board.play()
                if loc_is_player_1:
                    loc_grid_player_1[big_move] \
                        |= small_move
                    if HAS_WON[loc_grid_player_1[big_move]]:
                        loc_player_1 |= BIG_TO_SMALL[big_move]
                else:
                    loc_grid_player_2[big_move] \
                        |= small_move
                    if HAS_WON[loc_grid_player_2[big_move]]:
                        loc_player_2 |= BIG_TO_SMALL[big_move]
                
                loc_is_player_1 = not loc_is_player_1

            if self.is_player_1 == loc_is_player_1:
                tmp = int(HAS_WON[loc_player_1] \
                            or VALID_ACTIONS_LEN[loc_player_1] < VALID_ACTIONS_LEN[loc_player_2] \
                        if loc_is_player_1 \
                        else HAS_WON[loc_player_2] \
                            or VALID_ACTIONS_LEN[loc_player_1] > VALID_ACTIONS_LEN[loc_player_2])
                player_1_score += tmp
                player_2_score += 1-tmp
            else:
                tmp = int(HAS_WON[loc_player_1] \
                        or VALID_ACTIONS_LEN[loc_player_1] < VALID_ACTIONS_LEN[loc_player_2] \
                    if not loc_is_player_1 \
                    else HAS_WON[loc_player_2] \
                        or VALID_ACTIONS_LEN[loc_player_1] > VALID_ACTIONS_LEN[loc_player_2])
                player_1_score += tmp
                player_2_score += 1-tmp

            #backpropagate
            while node.parent:
                node.visited_count += visits
                node.score += player_1_score if not node.is_player_1 else player_2_score
                node = node.parent


            count += 1
        print(str(count), file=sys.stderr, flush = True)

def main():
    """Main"""
    #first turn
    opponent = '-'#input()
    # valid_action_count = int(input())
    # for _ in range(valid_action_count):
    #     _, _ = [int(j) for j in input().split()]

    root = None

    if opponent[0] == '-':
        root = UltimateBoard(True, (4, 0b000010000), None)
        root.run(.99)
        print("4 4")
    else:
        root = UltimateBoard(False, STRING_TO_ACTION[opponent], None)
        root.run(.99)
        root = root.best_child
        root.parent = None
        print(ACTION_TO_STRING[root.move])


    #game loop
    while True:
        # opponent = input()
        # valid_action_count = int(input())
        # for _ in range(valid_action_count):
        #     _, _ = [int(j) for j in input().split()]

        if not root.children and not root.unvisited_actions:
            root.unvisited_actions.extend(root.get_valid_actions())

        if not root.children and not root.unvisited_actions:
            if HAS_WON[root.player_1]:
                print("player 1 has won")
            elif HAS_WON[root.player_2]:
                print("player 2 has won")
            else:
                print("draw")
            return

        # root = root.children[STRING_TO_ACTION[opponent]]
        root.run(.095)
        root = root.best_child
        root.parent = None
        print(ACTION_TO_STRING[root.move])

# main()
