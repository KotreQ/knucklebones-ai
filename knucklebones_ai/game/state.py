from enum import Enum
from dataclasses import dataclass
from .board import Board


class Player(Enum):
    PLAYER_ROLL = 0
    PLAYER = 1
    OPPONENT_ROLL = 2
    OPPONENT = 3


@dataclass(frozen=True, slots=True)
class Action:
    player: Player
    value: int


class State:
    def __init__(self, player: Player, roll: int, player_board: Board, opponent_board: Board):
        self.player = player
        self.roll = roll    # [1,6] if dice already rolled, 0 otherwise
        self.player_board = player_board
        self.opponent_board = opponent_board

    def get_actions(self) -> list[Action]:
        if self.player in (Player.PLAYER_ROLL, Player.OPPONENT_ROLL):
            return [Action(self.player, val) for val in range(1, 7)]
        else:
            board = self.player_board if self.player == Player.PLAYER else self.opponent_board
            return [Action(self.player, col) for col in range(3) if board.is_col_available(col)]

    def transition(self, action: Action) -> State:
        assert action.player == self.player

        new_player = Player(self.player.value + 1 % len(Player))

        if self.player in (Player.PLAYER_ROLL, Player.OPPONENT_ROLL):
            new_roll = action.value
            return State(new_player, new_roll, self.player_board.copy(), self.opponent_board.copy())

        if self.player == Player.PLAYER:
            new_player_board = self.player_board.place_die(action.value, self.roll)
            new_opponent_board = self.opponent_board.remove_dice(action.value, self.roll)
        else:
            new_opponent_board = self.opponent_board.place_die(action.value, self.roll)
            new_player_board = self.player_board.remove_dice(action.value, self.roll)

        return State(new_player, 0, new_player_board, new_opponent_board)

    def get_points(self) -> int:
        return self.player_board.get_points() - self.opponent_board.get_points()

    def is_finished(self) -> bool:
        return self.player_board.is_full() or self.opponent_board.is_full()
