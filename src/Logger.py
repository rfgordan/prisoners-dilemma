import pandas as pd
import os

class PDLogger:
    def __init__(self, name: str, out_path: str) -> None:
        self.data = {
            'prisoner1_payoff' : [],
            'prisoner2_payoff' : [],
            'prisoner1_state' : [],
            'prisoner2_state' : []
        }

        self.out_path = out_path
        self.name = name

    def log_round(self, p1_payoff, p2_payoff, p1_state, p2_state):
        self.data['prisoner1_payoff'].append(p1_payoff)
        self.data['prisoner2_payoff'].append(p2_payoff)
        self.data['prisoner1_state'].append(p1_state)
        self.data['prisoner2_state'].append(p2_state)

    def write_data(self):
        df = pd.DataFrame(self.data)
        p = os.path.join(self.out_path, self.name + '.csv')
        df.to_csv(p, index=False)