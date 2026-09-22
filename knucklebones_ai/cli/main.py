import os
import subprocess as sp
import shlex
import time

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
            cmd = input("Enter command: ").strip()
        except EOFError:
            cmd = "exit"

        try:
            cmd = shlex.split(cmd)
        except ValueError as e:
            print(f"Invalid command syntax: {e}")
            wait_for_key()
            continue

        match cmd:
            case ("exit",):
                print("\nExiting...")
                finished = True

            case ("new",):
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

            case ("clear",):
                game = None

            case ("debug",):
                wait_for_key()

            case ("do", _):
                if game is None:
                    print("No game started")
                    wait_for_key()
                    continue

                try:
                    choice = int(cmd[1])
                except ValueError:
                    print(f"Invalid argument: {cmd[1]}")
                    wait_for_key()
                    continue

                actions = {action.value: action for action in game.get_actions()}
                try:
                    action = actions[choice]
                except KeyError:
                    print(f"No action with value: {choice}")
                    wait_for_key()
                    continue

                game = game.transition(action)
            
            case _:
                print("Unknown command")
                time.sleep(1)