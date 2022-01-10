"""My implementation for Codingame Ultimate TicTacToe."""
#from copy import deepcopy

class Action:
    """Class for TicTacToe actions."""
    def __init__(self, x_coord, y_coord) -> None:
        self.x_coord = x_coord
        self.y_coord = y_coord

class NormalBoard:
    """Class for normal TicTacToe board."""
    def __init__(self) -> None:
        self.local_winner = 0
        self._grid = [[0 for _ in range(3)] for _ in range(3)]
        self._moves_count = 0
        self._current_player = 0

    @property.setter
    def current_player(self, current_player) -> None:
        self._current_player = current_player

    def get_valid_actions(self, base_x = 0, base_y = 0) -> list[Action]:
        """List of valid moves on this board."""
        if self.local_winner != 0:
            return []

        valid_actions = []
        for y_coord in range(3):
            for x_coord in range(3):
                if self._grid[y_coord][x_coord] == 0:
                    valid_actions.append(Action(base_x + x_coord, base_y + y_coord))
        return valid_actions

    def play(self, move: Action, *, localize=False) -> int:
        """Play a given move on this board."""
        x_coord = move.x_coord if not localize else move.x_coord % 3
        y_coord = move.y_coord if not localize else move.y_coord % 3
        if x_coord < 0 or x_coord >= 3 \
                or y_coord < 0 or y_coord >= 3 \
                or self._grid[y_coord][x_coord] != 0:
            raise InvalidMoveError(move, self._grid)

        self._grid[y_coord][x_coord] = self._current_player
        self._current_player = (self._current_player + 1) % 2
        self._moves_count += 1

        return self._update_winner()

    def _update_winner(self) -> int:
        """Return the id of the player that has won.
        Return -1 if the board has tied
        Return 0 otherwise
        """
        for index in range(3):
            #rows
            if self._grid[index][0] > 0 \
                    and self._grid[index][0] == self._grid[index][1] \
                    and self._grid[index][0] == self._grid[index][2]:
                self.local_winner = self._grid[index][0]
                return self.local_winner

            #cols
            if self._grid[0][index] > 0 \
                    and self._grid[0][index] == self._grid[1][index] \
                    and self._grid[0][index] == self._grid[2][index]:
                self.local_winner = self._grid[0][index]
                return self.local_winner

        #diagonals
        if self._grid[0][0] > 0 \
                and self._grid[0][0] == self._grid[1][1] \
                and self._grid[0][0] == self._grid[2][2]:
            self.local_winner = self._grid[0][0]
            return self.local_winner
        if self._grid[2][0] > 0 \
                and self._grid[2][0] == self._grid[1][1] \
                and self._grid[2][0] == self._grid[0][2]:
            self.local_winner = self._grid[2][0]
            return self.local_winner

        if self._moves_count > 8:
            self.local_winner = -1
            return self.local_winner
        return 0

class UltimateBoard:
    """Class for Ultimate TicTacToe board."""
    def __init__(self) -> None:
        self._grid = [[NormalBoard() for _ in range(3)] for _ in range(3)]
        self._done_board_count = 0
        self._current_player = 0

    def get_valid_actions(self, last_move: Action = None) -> list[Action]:
        """List of valid moves on this board."""
        valid_actions = []
        if last_move is not None:
            x_grid = last_move.x_coord / 3
            y_grid = last_move.y_coord / 3
            valid_actions.extend(self._grid[y_grid][x_grid].get_valid_actions(x_grid*3, y_grid*3))

        if not valid_actions:
            for y_coord, row in enumerate(self._grid):
                for x_coord, board in enumerate(row):
                    valid_actions.extend(board.get_valid_actions(x_coord, y_coord))

        return valid_actions

    def play(self, move: Action) -> int:
        """Play a given move on this board."""
        x_grid = move.x_coord / 3
        y_grid = move.y_coord / 3

        board = self._grid[y_grid][x_grid]
        board.current_player(self._current_player)
        self._current_player = (self._current_player + 1) % 2

        winner = board.play(move, localize = True)

        game_winner = 0
        if winner != 0:
            #someone won last board, so check whether game done
            self._done_board_count += 1
            game_winner = self._calc_winner()

        return game_winner

    def _calc_winner(self) -> int:
        """Return the id of the player that has won.
        Return -1 if the board has tied
        Return 0 otherwise
        """
        for index in range(3):
            #rows
            if self._grid[index][0].local_winner > 0 \
                    and self._grid[index][0].local_winner == self._grid[index][1].local_winner \
                    and self._grid[index][0].local_winner == self._grid[index][2].local_winner:
                return self._grid[index][0].local_winner

            #cols
            if self._grid[0][index].local_winner > 0 \
                    and self._grid[0][index].local_winner == self._grid[1][index].local_winner \
                    and self._grid[0][index].local_winner == self._grid[2][index].local_winner:
                return self._grid[0][index].local_winner

        #diagonals
        if self._grid[0][0] > 0 \
                and self._grid[0][0].local_winner == self._grid[1][1].local_winner \
                and self._grid[0][0].local_winner == self._grid[2][2].local_winner:
            return self._grid[0][0].local_winner
        if self._grid[2][0] > 0 \
                and self._grid[2][0].local_winner == self._grid[1][1].local_winner \
                and self._grid[2][0].local_winner == self._grid[0][2].local_winner:
            return self._grid[2][0].local_winner

        if self._done_board_count > 8:
            return -1
        return 0

# define Python user-defined exceptions
class InvalidMoveError(Exception):
    """Exception raised for Invalid moves."""

    def __init__(self, move: Action, board: NormalBoard) -> None:
        self.message = f"Cannot move to {move.x_coord}, {move.y_coord} on board {board}"
        super().__init__(self.message)
