from itertools import product
from collections import namedtuple



Action = namedtuple('Action', ['x_coord', 'y_coord'])
Board = namedtuple('Board', ['winner', 'actions'])
def get_winner(board):
    for index in range(3):
            #rows
        if board[index][0] > 0 \
                    and board[index][0] == board[index][1] \
                    and board[index][0] == board[index][2]:
                return board[index][0]

            #cols
        if board[0][index] > 0 \
                    and board[0][index] == board[1][index] \
                    and board[0][index] == board[2][index]:
                return board[0][index]

        #diagonals
    if board[0][0] > 0 \
                and board[0][0] == board[1][1] \
                and board[0][0] == board[2][2]:
            return board[0][0]
    if board[2][0] > 0 \
                and board[2][0] == board[1][1] \
                and board[2][0] == board[0][2]:
            return board[2][0]

    return 0
def get_actions(board):
    valid_actions = []
    for y_coord in range(3):
        for x_coord in range(3):
            if board[y_coord][x_coord] == 0:
                valid_actions.append(Action(x_coord, y_coord))

    return valid_actions

NORMAL_BOARDS = {
    grid: Board(winner := get_winner(grid), get_actions(grid) if winner == 0 else []) for grid in product(product([0, 1, 2], repeat = 3), repeat = 3)
}

print(NORMAL_BOARDS)

