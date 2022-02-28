import numpy as np
from enum import Enum

# object that describes prisoner bot

from dataclasses import dataclass

class Action(Enum):
    COOPERATE = 0
    DEFECT = 1

# the first probability represents probability of cooperating when starting a turn in this state
# the remaining probabilities represent transition probabilities (4x number of states for each payoff matrix)

@dataclass
class PrisonerConfig:
    transitions: list[list[float]] # States x (4*States)
    actions: list[float]
    num_states: int
    matrix_size: int = 4

    @staticmethod
    def create_from_file(file_path: str):
        transitions = []
        actions = []

        with open(file_path, 'r') as f:
            for line in f:
                action_prob, transition_probs = PrisonerConfig.parse_from_line(line)
                transitions.append(transition_probs)
                actions.append(action_prob)

        # check some invariants
        n_states = len(transitions)
        for action, transition in zip(actions, transitions):
            assert(n_states*PrisonerConfig.matrix_size == len(transition))

            # assert coop probs are probs
            assert(0 <= action <= 1)
            for i in range(PrisonerConfig.matrix_size):

                # assert transition probs are a distribution
                assert(sum(transition[i*n_states: (i+1)*n_states]) == 1)

        return PrisonerConfig(transitions, actions, n_states)
    
    # get list of probabilities for state
    @staticmethod
    def parse_from_line(line: str) -> tuple[float, list[float]]:
        nums_text = line.rstrip('\n').split(' ')
        nums = [float(n) for n in nums_text]
        return nums[0], nums[1:]



class Prisoner:

    def __init__(self, f: str) -> None:
        # self.matrix_size = 4 # 4 for 2x2 payoff matrix
        self.config = PrisonerConfig.create_from_file(f)
        self.curr_state = 0

    def transition(self, self_action: Action, other_action: Action) -> None:
        trans_idx = self._get_idx_from_actions(self_action, other_action)
        trans_probs = self.config.transitions[self.curr_state][trans_idx*self.config.num_states:(trans_idx + 1)*self.config.num_states]
        self.curr_state = np.random.choice(self.config.num_states, p=trans_probs)

    def reset_state(self):
        self.curr_state = 0
        
    def act(self) -> Action:
        return self._act(np.random.rand())

    def _act(self, rand: float) -> Action:
        if rand > self.config.actions[self.curr_state]:
            return Action.DEFECT
        
        return Action.COOPERATE

    def _get_idx_from_actions(self, self_action: Action, other_action: Action) -> int:
        int_self_action = self_action.value
        int_other_action = other_action.value
        int_payoff_index = (int_self_action * len(Action)) + int_other_action
        return int_payoff_index

if __name__ == '__main__':
    p = Prisoner('my_config.txt')
    print(p)

    
    