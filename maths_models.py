import numpy as np
from typing import Dict
 
class MarkovChain(object):

    def is_that_transtion_matrix(self, mt: Dict):
        assert (sum([sum(mt[key].values()) for key in mt.keys()]) == len(mt.keys()))


    def __init__(self, transition_prob: Dict):
        """
        Initialize the MarkovChain instance.
 
        Parameters
        ----------
        transition_prob: dict
            A dict object representing the transition 
            probabilities in Markov Chain. 
            Should be of the form: 
                {'state1': {'state1': 0.1, 'state2': 0.4}, 
                 'state2': {...}}
        """
        self.is_that_transtion_matrix(transition_prob)
        self.transition_prob = transition_prob
        self.states = list(transition_prob.keys())
    
    def next_state(self, current_state: str):
        """
        Returns the state of the random variable at the next time 
        instance.
 
        Parameters
        ----------
        current_state: str
            The current state of the system.
        """
        return np.random.choice(
            self.states, 
            p=[self.transition_prob[current_state][next_state] 
               for next_state in self.states]
        )
 
    def generate_states(self, current_state, no=10):
        """
        Generates the next states of the system.
 
        Parameters
        ----------
        current_state: str
            The state of the current random variable.
 
        no: int
            The number of future states to generate.
        """
        future_states = []
        for i in range(no):
            next_state = self.next_state(current_state)
            future_states.append(next_state)
            current_state = next_state
        return future_states