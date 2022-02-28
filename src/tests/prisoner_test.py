from unittest import TestCase
import unittest
from Prisoner import Prisoner, Action, PrisonerConfig

class PrisonerTests(TestCase):
    def setUp(self) -> None:
        self.test_prisoner = Prisoner('data/test_config_2states.txt')
    
    def test_start_state(self):
        self.test_prisoner.reset_state()
        self.assertTrue(self.test_prisoner.curr_state == 0)

    # should be deterministic for test
    def test_transition_coop_coop(self):
        self.test_prisoner.reset_state()
        self.test_prisoner.transition(Action.COOPERATE, Action.COOPERATE)
        self.assertTrue(self.test_prisoner.curr_state == 0)

    def test_transition_def_def(self):
        self.test_prisoner.reset_state()
        self.test_prisoner.transition(Action.DEFECT, Action.DEFECT)
        self.assertTrue(self.test_prisoner.curr_state == 1)

if __name__ == '__main__':
    unittest.main()
    