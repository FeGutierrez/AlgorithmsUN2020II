# -----------------
# User Instructions
# 
# Modify our scrabble program to accept blank tiles and score 
# them appropriately. You can do this in whatever manner you 
# wish as long as you match the given test cases.

# NEW: Import statements.
from collections import defaultdict
from string import ascii_lowercase, ascii_uppercase
from itertools import product

# UPDATED: Removed '_' =0 and instead added keys for each lowercase letter (blank), where each value = 0.
PUNTOS = dict(A=1, B=3, C=3, D=2, E=1, F=4, G=2, H=4, I=1, J=8, K=5, L=1, M=3, N=1, O=1, P=3, Q=10, R=1, S=1, T=1, U=1, V=4, W=4, X=8, Y=4, Z=10)
puntos = defaultdict(int)
for l in ascii_lowercase: puntos[l]
PUNTOS.update(puntos)

def bonus_template(quadrant):
    return mirror(map(mirror, quadrant.split()))

def mirror(secuencia): return secuencia + secuencia[-2::-1]

SCRABBLE = bonus_template("""
|||||||||
|3..:...3
|.2...;..
|..2...:.
|:..2...:
|....2...
|.;...;..
|..:...:.
|3..:...*
""")

WWF = bonus_template("""
|||||||||
|...3..;.
|..:..2..
|.:..:...
|3..;...2
|..:...:.
|.2...3..
|;...:...
|...:...*
""")

BONUS = WWF

DW, TW, DL, TL = '23:;'   

def removed(letras, a_remover):
    for L in a_remover:
        letras = letras.replace(L, '', 1)
    return letras

def prefijos(palabra):
    "A list of the initial sequences of a word, not including the complete word."
    return [palabra[:i] for i in range(len(palabra))]
           
def transpuesta(matriz):
    return map(list, zip(*matriz))

def readwordlist(filename):
    wordset = set(file(filename).read().upper().split())
    prefixset = set(p for word in wordset for p in prefijos(word))
    return wordset, prefixset

PALABRAS, PREFIJOS = readwordlist('words4k.txt')

class anchor(set):
    "An anchor is where a new word can be placed; has a set of allowable letters."

# UPDATED: Letters include UPPERCASE and lowercase (representing blanks).
LETTERS = list(ascii_uppercase + ascii_lowercase)

ANY = anchor(LETTERS) # The anchor that can be any letter

def es_letra(sq):
    return isinstance(sq, str) and sq in LETTERS

def es_vacio(sq):
    return sq  == '.' or sq == '*' or isinstance(sq, set) 

# UPDATED: Convert prefixes to uppercase before running check.
def anadir_sufijos(hand, pre, inicio, fila, resultados, anchored=True):
    i = inicio + len(pre)
    PRE = pre.upper()
    if PRE in PALABRAS and anchored and not es_letra(fila[i]):
        resultados.add((inicio, pre))
    if PRE in PREFIJOS:
        sq = fila[i]
        if es_letra(sq):
            anadir_sufijos(hand, pre + sq, inicio, fila, resultados)
        elif es_vacio(sq):
            possibilities = sq if isinstance(sq, set) else ANY
            for L in hand:
                if L in possibilities:
                    anadir_sufijos(hand.replace(L, '', 1), pre + L, inicio, fila, resultados)
    return resultados

def prefijo_valido(i, fila):
    s = i
    while es_letra(fila[s - 1]): s -= 1
    if s < i: ## There is a prefix
        return ''.join(fila[s:i]), i - s
    while es_vacio(fila[s - 1]) and not isinstance(fila[s - 1], set): s -= 1
    return ('', i-s)

prev_hand, prev_results = '', set()

def hallar_prefijos(mano, pre='', resultados=None):
    global prev_hand, prev_results
    if mano == prev_hand: return prev_results
    if resultados is None: resultados = set()
    if pre == '': prev_hand, prev_results = mano, resultados
    PRE = pre.upper()
    if PRE in PALABRAS or PRE in PREFIJOS: resultados.add(pre)
    if PRE in PREFIJOS:
        for L in mano:
            hallar_prefijos(mano.replace(L, '', 1), pre + L, resultados)
    return resultados

def jugadas_por_fila(mano, fila):
    results = set()
    hands = get_hands(mano)
    for h in hands:
        for (i, sq) in enumerate(fila[1:-1], 1):
            if isinstance(sq, set):
                pre, maxsize = prefijo_valido(i, fila)
                start = i - len(pre)
                anadir_sufijos(h, pre, start, fila, results, anchored=False)
                for pre in hallar_prefijos(h):
                    if len(pre) <= maxsize:
                        start = i - len(pre)
                        anadir_sufijos(removed(h, pre), pre, start, fila, results, anchored=False)
    return results

# NEW FUNCTION
def get_hands(hand):
    letters = hand.replace('_', '')
    blanks = product(ascii_lowercase, repeat=hand.count('_'))
    return set([letters+''.join(b) for b in blanks])

def find_cross_word(board, i, j):
    sq = board[j][i]
    w = sq if es_letra(sq) else '.'
    for j2 in range(j, 0, -1):
        sq2 = board[j2-1][i]
        if es_letra(sq2): w = sq2 + w
        else: break
    for j3 in range(j+1, len(board)):
        sq3 = board[j3][i]
        if es_letra(sq3): w = w + sq3
        else: break
    return (j2, w)

def vecinos(tablero, i, j):
    return [tablero[j - 1][i], tablero[j + 1][i],
            tablero[j][i + 1], tablero[j][i - 1]]

def definir_anclajes(fila, j, tablero):
    for (i, sq) in enumerate(fila[1:-1], 1):
        neighborlist = (N,S,E,W) = vecinos(tablero, i, j)
        if sq == '*' or (es_vacio(sq) and any(map(es_letra, neighborlist))):
            if es_letra(N) or es_letra(S):
                (j2, w) = find_cross_word(tablero, i, j)

                fila[i] = anchor(L for L in LETTERS if w.replace('.', L.upper()) in PALABRAS)
            else: # Unrestricted empty square -- any letter will fit.
                fila[i] = ANY

def calcular_puntaje(tablero, pos, direccion, hand, palabra):
    "Return the total score for this play."
    total, crosstotal, word_mult = 0, 0, 1
    starti, startj = pos
    di, dj = direccion
    otra_direccion = DOWN if direccion == ACROSS else ACROSS
    for (n, L) in enumerate(palabra):
        i, j = starti + n*di, startj + n*dj
        sq = tablero[j][i]
        b = BONUS[j][i]
        word_mult *= (1 if es_letra(sq) else
                      3 if b == TW else 2 if b in (DW,'*') else 1)
        letter_mult = (1 if es_letra(sq) else
                       3 if b == TL else 2 if b == DL else 1)
        total += PUNTOS[L] * letter_mult
        if isinstance(sq, set) and sq is not ANY and direccion is not DOWN:
            crosstotal += puntaje_palabras_cruzadas(tablero, L, (i, j), otra_direccion)
    return crosstotal + word_mult * total
    
def puntaje_palabras_cruzadas(tablero, L, pos, direccion):
    "Return the score of a word made in the other direction from the main word."
    i, j = pos
    (j2, word) = find_cross_word(tablero, i, j)
    return calcular_puntaje(tablero, (i, j2), DOWN, L, word.replace('.', L))
  
ACROSS, DOWN = (1, 0), (0, 1) # Directions that words can go
   
def horizontal_plays(mano, board):
    "Find all horizontal plays -- (score, pos, word) pairs -- across all rows."
    results = set()
    for (j, row) in enumerate(board[1:-1], 1):
        definir_anclajes(row, j, board)
        for (i, word) in jugadas_por_fila(mano, row):
            score = calcular_puntaje(board, (i, j), ACROSS, mano, word)
            results.add((score, (i, j), word))
    return results


def all_plays(mano, tablero):
    jugadas_horizontales = horizontal_plays(mano, tablero)
    jugadas_verticales = horizontal_plays(mano, transpuesta(tablero))
    return (set((score, (i, j), ACROSS, w) for (score, (i, j), w) in jugadas_horizontales) |
            set((score, (i, j), DOWN, w) for (score, (j, i), w) in jugadas_verticales))
 
def hacer_jugada(jugada, tablero):
    (puntaje, (i, j), (di, dj), palabra) = jugada
    for (n, L) in enumerate(palabra):
        tablero[j + n * dj][i + n * di] = L
    return tablero

NOPLAY = None

def best_play(hand, tablero):
    jugadas = all_plays(hand, tablero)
    return sorted(jugadas)[-1] if jugadas else NOPLAY

def a_board():
    return map(list, ['|||||||||||||||||',
                      '|J............I.|',
                      '|A.....BE.C...D.|',
                      '|GUY....F.H...L.|',
                      '|||||||||||||||||'])

def test():
    def ok(hand, n, s, d, w):
        result = best_play(hand, a_board())
        test_case = result[:3] == (n, s, d) and result[-1].upper() == w.upper()
        print test_case
        return test_case
    assert ok('ABCEHKN', 64, (3, 2), (1, 0), 'BACKBENCH')
    assert ok('_BCEHKN', 62, (3, 2), (1, 0), 'BaCKBENCH')
    assert ok('__CEHKN', 61, (9, 1), (1, 0), 'KiCk')

print test()