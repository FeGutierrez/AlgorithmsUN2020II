# -----------------
# User Instructions
# 
# In this problem, you will use a faster version of Pwin, which we will call
# Pwin2, that takes a state as input but ignores whether it is player 1 or 
# player 2 who starts. This will reduce the number of computations to about 
# half. You will define a function, Pwin3, which will be called by Pwin2.
#
# Pwin3 will only take me, you, and pending as input and will return the 
# probability of winning. 
#
# Keep in mind that the probability that I win from a position is always
# (1 - probability that my opponent wins).


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
            cache[args] = resultado = f(*args)
            return resultado
        except TypeError:
            # some element of args refuses to be a dict key
            return f(args)
    _f.cache = cache
    return _f

objetivo = 40

def roll(estado, d):
    """Apply the roll action to a state (and a die roll d) to yield a new state:
    If d is 1, get 1 point (losing any accumulated 'pending' points),
    and it is the other player's turn. If d > 1, add d to 'pending' points."""
    (yo, tu, pendiente) = estado
    if d == 1:
        return (tu, yo+1, 0) # pig out; other player's turn
    else:
        return (yo, tu, pendiente+d)  # accumulate die roll in pending

def hold(estado):
    """Apply the hold action to a state to yield a new state:
    Reap the 'pending' points and it becomes the other player's turn."""
    (me, you, pending) = estado
    return (you, me+pending, 0)

def Q_pig(estado, accion, Pwin):  
    "The expected value of choosing action in state."
    if accion == 'hold':
        return 1 - Pwin(hold(estado))
    if accion == 'roll':
        return (1 - Pwin(roll(estado, 1))
                + sum(Pwin(roll(estado, d)) for d in (2, 3, 4, 5, 6))) / 6.
    raise ValueError

def pig_actions(estado):
    "The legal actions from a state."
    _, _, pending = estado
    return ['roll', 'hold'] if pending else ['roll']


def Pwin2(estado):
   """The utility of a state; here just the probability that an optimal player
   whose turn it is to move can win from the current state."""
   return Pwin3(estado[1:]) # Remove the first argument, p, leaving me, you, and pending.

@memo
def Pwin3(estado):
    """The utility of a state; here just the probability that an optimal player
    whose turn it is to move can win from the current state."""
    # Assumes opponent also plays with optimal strategy.
    yo, tu, pendiente = estado
    if yo + pendiente >= objetivo:
        return 1
    elif tu >= objetivo:
        return 0
    else:
        return max(Q_pig(estado, accion, Pwin3)
                   for accion in pig_actions(estado))   

def test():
    epsilon = 0.0001 # used to make sure that floating point errors don't cause test() to fail
    assert objetivo == 40
    assert len(Pwin3.cache) <= 50000
    assert Pwin2((0, 42, 25, 0)) == 1
    assert Pwin2((1, 12, 43, 0)) == 0
    assert Pwin2((0, 34, 42, 1)) == 0
    assert abs(Pwin2((0, 25, 32, 8)) - 0.736357188272) <= epsilon
    assert abs(Pwin2((0, 19, 35, 4)) - 0.493173612834) <= epsilon
    return 'tests pass'

print test()