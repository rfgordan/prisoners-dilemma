from Prisoner import *
from Logger import *
import numpy as np

class GameConfig:
    rounds = 100
    noise = 0.1 # with probability 0.1, observe random action

    # payoff for our_action x their_action
    payoff_matrix = [
        [2, 0],
        [3, 1]
    ]

class Game:
    def __init__(
        self,
        p1: Prisoner,
        p2: Prisoner,
        config: GameConfig,
        logger: PDLogger
    ) -> None:
        self.p1 = p1
        self.p2 = p2
        self.config = config
        self.payoff_p1 = 0
        self.payoff_p2 = 0
        self.logger = logger

        self._check_payoff_matrix()

    def run_game(self):
        for _ in range(self.config.rounds):
            self._run_round()
    
    def _run_round(self):
        p1_act = self.p1.act()
        p2_act = self.p2.act()

        # record payoffs for round
        self.payoff_p1 += self._get_payoff(p1_act, p2_act)
        self.payoff_p2 += self._get_payoff(p2_act, p1_act)

        # switch act for certain noise
        p1_act_noised = self._perturb_act(p1_act)
        p2_act_noised = self._perturb_act(p2_act)

        # transition prisoners to next state
        self.p1.transition(p1_act, p2_act_noised)
        self.p2.transition(p2_act, p1_act_noised)

        # log current state
        self.logger.log_round(self.payoff_p1, self.payoff_p2, self.p1.curr_state, self.p2.curr_state)
        print('p1 score:', self.payoff_p1, ' p2 score:' , self.payoff_p2 , ' p1 state:' , self.p1.curr_state , ' p2 state:' , self.p2.curr_state)

    def _get_payoff(self, self_act: Action, other_act: Action) -> int:
        return self.config.payoff_matrix[self_act.value][other_act.value]

    def _perturb_act(self, act: Action) -> Action:
        if np.random.rand() > self.config.noise:
            return act
        
        return np.random.choice(Action)

    def _check_payoff_matrix(self):
        assert(len(self.config.payoff_matrix) == len(Action))
        assert(len(self.config.payoff_matrix[0]) == len(Action))


class GameFactory:

    @staticmethod
    def create_game(
        p1_path: str,
        p2_path: str,
        results_path: str,
    ) -> Game:

        p1 = Prisoner(p1_path)
        p2 = Prisoner(p2_path)
        config = GameConfig()
        logger = PDLogger("my_game", results_path)

        return Game(p1, p2, config, logger)

if __name__ == '__main__':
    g = GameFactory.create_game('data/tit_for_tat.txt', 'data/tit_for_tat.txt', 'data')
    g.run_game()
    g.logger.write_data()
