# -----------------
# User Instructions
# 
# In this problem, you will define a function, boggle_words(), 
# that takes a board as input and returns a set of words that
# can be made from the board according to the rules of Boggle.

import math

def boggle_words(tablero, longitud_minima=3):
    resultados = set()
    filas = size(tablero)
    for (i,sq) in enumerate(tablero):
        if sq != BORDE:
            find_boggle_words(tablero, filas, i, sq, longitud_minima, resultados)
    return resultados

def find_boggle_words(tablero, filas, i, pre, longitud_minima, resultados=None, visitados=set()):
    if resultados is None: resultados = set()
    if pre in PALABRAS and len(pre) >= longitud_minima:
        resultados.add(pre)
    if pre in PREFIJOS:
        ultimo = (i, tablero[i])
        visitados.add(ultimo)
        for nbr in vecinos(i, filas):
            if tablero[nbr] != BORDE and (nbr, tablero[nbr]) not in visitados:
                find_boggle_words(tablero, filas, nbr,
                                  pre + tablero[nbr], longitud_minima, resultados, visitados)
        visitados.remove(ultimo)

    return resultados

def test():
    b = Board('XXXX TEST XXXX XXXX')
    assert b == '|||||||XXXX||TEST||XXXX||XXXX|||||||'
    assert display(b) == """
||||||
|XXXX|
|TEST|
|XXXX|
|XXXX|
||||||""".strip()
    assert boggle_words(b) == set(['SET', 'SEX', 'TEST'])
    assert vecinos(20, 6) == (13, 14, 15, 19, 21, 25, 26, 27)
    assert len(boggle_words(Board('TPLER ORAIS METND DASEU NOWRB'))) == 317
    assert boggle_words(Board('PLAY THIS WORD GAME')) == set([
        'LID', 'SIR', 'OAR', 'LIS', 'RAG', 'SAL', 'RAM', 'RAW', 'SAY', 'RID', 
        'RIA', 'THO', 'HAY', 'MAR', 'HAS', 'AYS', 'PHI', 'OIL', 'MAW', 'THIS', 
        'LAY', 'RHO', 'PHT', 'PLAYS', 'ASIDE', 'ROM', 'RIDE', 'ROT', 'ROW', 'MAG', 
        'THIRD', 'WOT', 'MORE', 'WOG', 'WORE', 'SAID', 'MOR', 'SAIL', 'MOW', 'MOT', 
        'LAID', 'MOA', 'LAS', 'MOG', 'AGO', 'IDS', 'HAIR', 'GAME', 'REM', 'HOME', 
        'RED', 'WORD', 'WHA', 'WHO', 'WHOM', 'YID', 'DRAW', 'WAG', 'SRI', 'TOW', 
        'DRAG', 'YAH', 'WAR', 'MED', 'HIRE', 'TOWARDS', 'ORS', 'ALT', 'ORE', 'SIDE', 
        'ALP', 'ORA', 'TWA', 'ERS', 'TOR', 'TWO', 'AIS', 'AIR', 'AIL', 'ERA', 'TOM', 
        'AID', 'TOG', 'DIS', 'HIS', 'GAR', 'GAM', 'HID', 'HOG', 'PLAY', 'GOA', 'HOW', 
        'HOT', 'WARM', 'GOT', 'IRE', 'GOR', 'ARS', 'ARM', 'ARE', 'TOWARD', 'THROW'])    
    return 'tests pass'

    
def Board(texto):
    filas = texto.split()
    N = len(filas)
    filas = [BORDE * N] + filas + [BORDE * N]
    return ''.join(BORDE + fila + BORDE for fila in filas)

def size(board): return int(len(board)**0.5)

def vecinos(i, N):
    return (i-N-1, i-N, i-N+1, i-1, i+1, i+N-1, i+N, i+N+1)

BORDE = '|'

def display(tablero):
    N = size(tablero)
    return '\n'.join(tablero[i:i + N] for i in range(0, N ** 2, N))

# ------------
# Helpful functions
# 
# You may find the following functions useful. These functions
# are identical to those we defined in lecture. 

def prefixes(palabra):
    return [palabra[:i] for i in range(len(palabra))]

def readwordlist(filename):
    wordset = set(open(filename).read().upper().split())
    prefixset = set(p for word in wordset for p in prefixes(word))
    return wordset, prefixset

PALABRAS, PREFIJOS = readwordlist('words4k.txt')

b = Board('XXXX TEST XXXX XXXX')

print test()