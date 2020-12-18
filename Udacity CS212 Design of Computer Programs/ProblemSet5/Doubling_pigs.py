# -----------------
# User Instructions
# 
# In this problem, we introduce doubling to the game of pig. 
# At any point in the game, a player (let's say player A) can
# offer to 'double' the game. Player B then has to decide to 
# 'accept', in which case the game is played through as normal,
# but it is now worth two points, or 'decline,' in which case
# player B immediately loses and player A wins one point. 
#
# Your job is to write two functions. The first, pig_actions_d,
# takes a state (p, me, you, pending, double), as input and 
# returns all of the legal actions.
# 
# The second, strategy_d, is a strategy function which takes a
# state as input and returns one of the possible actions. This
# strategy needs to beat hold_20_d in order for you to be
# marked correct. Happy pigging!

import random
from functools import update_wrapper

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args refuses to be a dict key
            return f(args)
    _f.cache = cache
    return _f


@memo
def Pwin(yo, tu, pendiente):
    """The utility of a state; here just the probability that an optimal player
    whose turn it is to move can win from the current state."""
    # Assumes opponent also plays with optimal strategy.
    if yo + pendiente >= objetivo:
        return 1
    elif tu >= objetivo:
        return 0
    else:
        Proll = (1 - Pwin(tu, yo + 1, 0) +
                 sum(Pwin(yo, tu, pendiente + d)
            for d in (2,3,4,5,6))) / 6.
        
        return (Proll if not pendiente else
                max(Proll, 1 - Pwin(tu, yo + pendiente, 0)))

def pig_actions_d(estado):
    """The legal actions from a state. Usually, ["roll", "hold"].
    Exceptions: If double is "double", can only "accept" or "decline".
    Can't "hold" if pending is 0.
    If double is 1, can "double" (in addition to other moves).
    (If double > 1, cannot "double").
    """
    # state is like before, but with one more component, double,
    # which is 1 or 2 to denote the value of the game, or 'double'
    # for the moment at which one player has doubled and is waiting
    # for the other to accept or decline
    (p, yo, tu, pendiente, double) = estado
    actions = ['roll']
    if pendiente > 0:        actions += ['hold']
    if double == 1:        actions += ['double']
    if double == 'double': actions  = ['accept', 'decline']
    return actions


def strategy_d(estado):
    (p, yo, tu, pendiente, double) = estado

    # Double only when player has a 75% chance of winning via optimal strategy.
    if double == 1 and Pwin(yo, tu, pendiente) > 0.75:
        return 'double'
    
    # Accept a double only when opponent has a 75% chance of winning via optimal strategy.
    elif double == 'double':
        return 'accept' if Pwin(tu, yo, pendiente) > 0.75 else 'decline'
    
    # Hold at 20 pending strategy.
    elif (pendiente >= 20 or yo + pendiente >= objetivo):
        return 'hold'
    
    else:
        return 'roll'

## You can use the code below, but don't need to modify it.

def hold_20_d(estado):
    "Hold at 20 pending.  Always accept; never double."
    (p, me, you, pending, double) = estado
    return ('accept' if double == 'double' else
            'hold' if (pending >= 20 or me + pending >= objetivo) else
            'roll')
    
def clueless_d(estado):
    return random.choice(pig_actions_d(estado))

def dierolls():
    "Generate die rolls."
    while True:
        yield random.randint(1, 6)

def play_pig_d(A, B, dierolls=dierolls()):
    """Play a game of pig between two players, represented by their strategies.
    Each time through the main loop we ask the current player for one decision,
    which must be 'hold' or 'roll', and we update the state accordingly.
    When one player's score exceeds the goal, return that player."""
    estrategias = [A, B]
    estado = (0, 0, 0, 0, 1)
    while True:
        (p, yo, tu, pendiente, double) = estado
        if yo >= objetivo:
            return estrategias[p], double
        elif tu >= objetivo:
            return estrategias[otra[p]], double
        else:
            action = estrategias[p](estado)
            estado = do(action, estado, dierolls)

## No more roll() and hold(); instead, do:

def do(accion, estado, dierolls):
    """Return the state that results from doing action in state.
     If action is not legal, return a state where the opponent wins.
    Can use dierolls if needed."""
    (p, yo, tu, pendiente, double) = estado
    if accion not in pig_actions_d(estado):
        return (otra[p], objetivo, 0, 0, double)
    elif accion == 'roll':
        d = next(dierolls)
        if d == 1:
            return (otra[p], tu, yo + 1, 0, double) # pig out; other player's turn
        else:
            return (p, yo, tu, pendiente+d, double)  # accumulate die in pending
    elif accion == 'hold':
        return (otra[p], tu, yo + pendiente, 0, double)
    elif accion == 'double':
        return (otra[p], tu, yo, pendiente, 'double')
    elif accion == 'decline':
        return (otra[p], objetivo, 0, 0, 1)
    elif accion == 'accept':
        return (otra[p], tu, yo, pendiente, 2)

objetivo = 40
otra = {1:0, 0:1}

def strategy_compare(A, B, N=1000):
    """Takes two strategies, A and B, as input and returns the percentage
    of points won by strategy A."""
    A_points, B_points = 0, 0
    for i in range(N):
        if i % 2 == 0:  # take turns with who goes first
            ganador, puntajes = play_pig_d(A, B)
        else: 
            ganador, puntajes = play_pig_d(B, A)
        if ganador.__name__ == A.__name__:
            A_points += puntajes
        else: B_points += puntajes
    A_percent = 100*A_points / float(A_points + B_points)
    print 'In %s games of pig, strategy %s took %s percent of the points against %s.' % (N, A.__name__, A_percent, B.__name__)
    return A_percent
    
def test():
    assert set(pig_actions_d((0, 2, 3, 0, 1)))          == set(['roll', 'double'])
    assert set(pig_actions_d((1, 20, 30, 5, 2)))        == set(['hold', 'roll']) 
    assert set(pig_actions_d((0, 5, 5, 5, 1)))          == set(['roll', 'hold', 'double'])
    assert set(pig_actions_d((1, 10, 15, 6, 'double'))) == set(['accept', 'decline']) 
    assert strategy_compare(strategy_d, hold_20_d) > 60 # must win 60% of the points      
    return 'test passes'

print test()



