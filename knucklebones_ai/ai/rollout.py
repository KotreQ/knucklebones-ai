from knucklebones_ai.game.state import State
import random


def do_random_rollout(state: State) -> float:
    while not state.is_finished():
        action = random.choice(state.get_actions())
        state = state.transition(action)

    points = state.get_points()
    if points > 0:
        return 1
    elif points < 0:
        return -1
    else:
        return 0
