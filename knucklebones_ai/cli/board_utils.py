import numpy as np

from knucklebones_ai.game.board import Board
from knucklebones_ai.game.state import State


def display_board(board: Board, *, reversed: bool = False):
    board_tiles = np.zeros((3, 3), np.uint8)

    for col in range(3):
        idx = 0
        for val, count in enumerate(board._data[col, 1:], start=1):
            for _ in range(count):
                board_tiles[col][idx] = val
                idx += 1

    separator = "-" * 13

    print(separator)
    for row in (range(3) if not reversed else range(2, -1, -1)):
        row_dice = (str(val) if val > 0 else " " for val in board_tiles[:, row])
        print("| " + " | ".join(row_dice) + " |")
    print(separator)


def display_state(state: State):
    print(f"Current player: {state.player.name}")
    if state.roll != 0:
        print(f"Dice value: {state.roll}")
    print("")
    print("Board:")
    display_board(state.opponent_board, reversed=True)
    print("")
    display_board(state.player_board)
    print("")
    print(f"Available actions: {[a.value for a in state.get_actions()]}")
