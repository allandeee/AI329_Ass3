from axelrod.action import Action, actions_to_str
from axelrod.player import Player

C, D = Action.C, Action.D


class Allan_Dominguez(Player):
    """
    This strategy used Genetic Algorithms to generate its strategy.
    The strategy is in the form a bit string (classifiers['bit_string']),
    which then utilises memory depth of 3 by default.

    This class is callable, can memory depth can be changed (also changing
    the bit string). Look at Allan_Dominguez_IPD_test.py to see how this is done

    Names:

    - Rapoport's strategy: [Axelrod1980]_
    - TitForTat: [Axelrod1980]_
    """

    # These are various properties for the strategy
    name = 'Allan Dominguez GA Strategy'
    classifier = {
        'memory_depth': 3,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False,
        'bit_string' : [1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1,
                        0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0]

    }

    def strategy(self, opponent: Player) -> Action:
        """This is the actual strategy"""
        k = self.classifier['memory_depth']
        strat = self.classifier['bit_string']
        # First move
        if not self.history:
            return C
        opp_hist = actions_to_str(opponent.history[-k:])
        my_hist = actions_to_str(self.history[-k:])
        history_string = ''.join([''.join(t) for t in zip(my_hist, opp_hist)])
        if len(self.history) < k:
            if opponent.history[-1] == D:
                return D
            return C

        pairs = ['CC', 'CD', 'DC', 'DD']
        vals = []
        for c1, c2 in zip(history_string[0::2], history_string[1::2]):
            pair = c1 + c2
            vals.append(pairs.index(pair))
        i = 0
        ith = 0
        while i < k:
            ith += vals[i] * 4 ** (k - (i + 1))
            i += 1

        act = strat[ith]
        if act == 1:
            return C
        return D