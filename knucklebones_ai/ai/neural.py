import torch
from torch import nn

from knucklebones_ai.game.board import Board
from knucklebones_ai.game.state import Player, State


def tensorify_board(board: Board):
    return torch.asarray(board._data, dtype=torch.float32) / 3


def tensorify_state(state: State):
    if state.player in (Player.PLAYER_ROLL, Player.OPPONENT_ROLL):
        raise ValueError(f"Cannot tensorify a state with player: {state.player}")

    player_tensor = tensorify_board(state.player_board)
    opponent_tensor = tensorify_board(state.opponent_board)

    if state.player == Player.OPPONENT:
        player_tensor, opponent_tensor = opponent_tensor, player_tensor

    roll_tensor = torch.zeros(6, dtype=torch.float32)
    roll_tensor[state.roll - 1] = 1

    return torch.cat((player_tensor.flatten(), opponent_tensor.flatten(), roll_tensor))


class KnucklebonesNet(nn.Module):
    def __init__(self):
        super().__init__()

        self.features = nn.Sequential(
            nn.Linear(48, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
        )

    def forward(self, x):
        return self.features(x)