from axelrod.action import Action, actions_to_str
from axelrod.player import Player

C, D = Action.C, Action.D


class GA_Strategy(Player):
    """
    A player starts by cooperating and then mimics the previous action of the
    opponent.

    This strategy was referred to as the *'simplest'* strategy submitted to
    Axelrod's first tournament. It came first.

    Note that the code for this strategy is written in a fairly verbose
    way. This is done so that it can serve as an example strategy for
    those who might be new to Python.

    Names:

    - Rapoport's strategy: [Axelrod1980]_
    - TitForTat: [Axelrod1980]_
    """

    # These are various properties for the strategy
    name = 'GA Strategy'
    classifier = {
        'memory_depth': 3,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False,
        'bit_string' : [0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0,
                        1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0]
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
            # can be changed to implement another strategy
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