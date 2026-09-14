import os
import subprocess as sp


def clear_console():
    sp.run("cls" if os.name == "nt" else "clear")


def run_cli():
    finished = False
    game = None

    while not finished:
        clear_console()
        if game is not None:
            game.display()
        else:
            print("No game loaded.")
        command = input("Enter command: ").strip()

        match command:
            case "exit":
                print("Exiting...")
                finished = True

            # case "new":

            case "debug":
                print("Press ENTER to continue")
                input()
            
            case _:
                print("Unknown command")