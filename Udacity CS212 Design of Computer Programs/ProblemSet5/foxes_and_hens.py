# -----------------
# User Instructions
# 
# This problem deals with the one-player game foxes_and_hens. This 
# game is played with a deck of cards in which each card is labelled
# as a hen 'H', or a fox 'F'. 
# 
# A player will flip over a random card. If that card is a hen, it is
# added to the yard. If it is a fox, all of the hens currently in the
# yard are removed.
#
# Before drawing a card, the player has the choice of two actions, 
# 'gather' or 'wait'. If the player gathers, she collects all the hens
# in the yard and adds them to her score. The drawn card is discarded.
# If the player waits, she sees the next card. 
#
# Your job is to define two functions. The first is do(action, state), 
# where action is either 'gather' or 'wait' and state is a tuple of 
# (score, yard, cards). This function should return a new state with 
# one less card and the yard and score properly updated.
#
# The second function you define, strategy(state), should return an 
# action based on the state. This strategy should average at least 
# 1.5 more points than the take5 strategy.

import random

def foxes_and_hens(estrategia, zorros=7, gallinas=45):
    """Play the game of foxes and hens."""
    # A state is a tuple of (score-so-far, number-of-hens-in-yard, deck-of-cards)
    estado = (puntaje, campo, cartas) = (0, 0, 'Z' * zorros + 'G' * gallinas)
    while cartas:
        accion = estrategia(estado)
        estado = (puntaje, campo, cartas) = do(accion, estado)
    return puntaje + campo

def do(accion, estado):
    "Apply action to state, returning a new state."
    # Make sure you always use up one card.
    #
    puntaje, campo, cartas = estado
    
    # Choose a card at random and remove it from the deck.
    card = random.choice(cartas)
    cartas = cartas.replace(card, '', 1)
	
	# Harvest the yard points and clear the yard.
    if accion == 'gather':
        return (puntaje+campo, 0, cartas)
    
    # If fox, clear the yard. If hen, add 1 to the yard.
    elif accion == 'wait':
        return (puntaje, 0, cartas) if card == 'Z' else (puntaje, campo+1, cartas)
        
    else:
        raise Exception("Invalid action")
    
def take5(estado):
    "A strategy that waits until there are 5 hens in yard, then gathers."
    (puntaje, campo, cartas) = estado
    if campo < 5:
        return 'wait'
    else:
        return 'gather'

def average_score(estrategia, N=1000):
    return sum(foxes_and_hens(estrategia) for _ in range(N)) / float(N)

def superior(A, B=take5):
    "Does strategy A have a higher average score than B, by more than 1.5 point?"
    print "A:", average_score(A)
    print "B:", average_score(B)
    return average_score(A) - average_score(B) > 1.5

def strategy(estado):
    (score, yard, cartas) = estado
    zorros = cartas.count('Z') + 0.0
    gallinas = cartas.count('G') + 0.0
    
    # Wait until there's more than 3 hens or when the prob of pulling a fox is < 35%.
    if yard < 3 and zorros/(zorros + gallinas) < 0.35:
        return 'wait'
    else:
        return 'gather'
    

def test():
    gather = do('gather', (4, 5, 'Z'*4 + 'G'*10))
    assert (gather == (9, 0, 'Z'*3 + 'G'*10) or
            gather == (9, 0, 'Z'*4 + 'G'*9))
    
    wait = do('wait', (10, 3, 'ZZGG'))
    assert (wait == (10, 4, 'ZZG') or
            wait == (10, 0, 'ZGG'))
    
    assert superior(strategy)
    return 'tests pass'

print test()   


