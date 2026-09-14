import os
import subprocess as sp

from knucklebones_ai.game.board import Board
from knucklebones_ai.game.state import Player, State
from .board_utils import display_state


def clear_console():
    sp.run("cls" if os.name == "nt" else "clear")


def wait_for_key():
    print("Press ENTER to continue")
    input()


def run_cli():
    finished = False
    game = None

    while not finished:
        clear_console()
        if game is not None:
            display_state(game)
        else:
            print("No game loaded.")
        print("")

        try:
            command = input("Enter command: ").strip()
        except EOFError:
            command = "exit"

        match command:
            case "exit":
                print("\nExiting...")
                finished = True

            case "new":
                match input("Who is the starting player? player or opponent (p/o): ").strip().lower():
                    case "p":
                        player = Player.PLAYER_ROLL
                    case "o":
                        player = Player.OPPONENT_ROLL
                    case _:
                        print("Invalid value")
                        wait_for_key()
                        continue

                game = State(player, 0, Board(), Board())

            case "debug":
                wait_for_key()
            
            case _:
                print("Unknown command")