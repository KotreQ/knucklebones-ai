import random

from knucklebones_ai.game.state import Player, State
from .rollout import do_random_rollout
from .ucb import calculate_ucb


class MctsNode:
    def __init__(self, state: State):
        self.state = state
        self.score = 0
        self.n = 0
        self.children: list[MctsNode] = []
    
    def is_expanded(self):
        return len(self.children) > 0

    def expand(self):
        assert not self.is_expanded()

        for action in self.state.get_actions():
            state = self.state.transition(action)
            node = MctsNode(state)
            self.children.append(node)

    def select_best_child(self) -> MctsNode:
        assert self.is_expanded()
        
        match self.state.player:
            case Player.PLAYER_ROLL | Player.OPPONENT_ROLL:
                return random.choice(self.children)

            case Player.PLAYER:
                node_eval = lambda node: calculate_ucb(node.score, node.n, self.n)

            case Player.OPPONENT:
                node_eval = lambda node: calculate_ucb(-node.score, node.n, self.n)

        return max(self.children, key=node_eval)

    def do_rollout(self) -> float:
        if self.n == 0:
            return self.do_random_rollout()

        if not self.is_expanded():
            self.expand()

            if not self.is_expanded():  # node is terminal - no children after trying to expand
                return self.do_random_rollout()

        child = self.select_best_child()
        value = child.do_rollout()
        self.score += value
        self.n += 1

    def do_random_rollout(self) -> float:
        value = do_random_rollout(self.state)
        self.score += value
        self.n += 1
        return value