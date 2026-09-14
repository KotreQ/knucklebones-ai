from enum import Enum, auto
from dataclasses import dataclass
from .board import Board


class Player(Enum):
    PLAYER_ROLL = auto()
    PLAYER = auto()
    OPPONENT_ROLL = auto()
    OPPONENT = auto()


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
        ...

    def transition(self, action: Action) -> State:
        ...

    def get_points(self) -> int:
        return self.player_board.get_points() - self.opponent_board.get_points()

    def is_finished(self) -> bool:
        return self.player_board.is_full() or self.opponent_board.is_full()
