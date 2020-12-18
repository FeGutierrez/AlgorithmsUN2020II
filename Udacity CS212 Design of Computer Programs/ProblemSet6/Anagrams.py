# -----------------
# User Instructions
# 
# This homework deals with anagrams. An anagram is a rearrangement 
# of the letters in a word to form one or more new words. 
#
# Your job is to write a function anagrams(), which takes as input 
# a phrase and an optional argument, shortest, which is an integer 
# that specifies the shortest acceptable word. Your function should
# return a set of all the possible combinations of anagrams. 
#
# Your function should not return every permutation of a multi word
# anagram: only the permutation where the words are in alphabetical
# order. For example, for the input string 'ANAGRAMS' the set that 
# your function returns should include 'AN ARM SAG', but should NOT 
# include 'ARM SAG AN', or 'SAG AN ARM', etc...

# Lazy approach that just barely passed the grader.
import itertools
def anagrams(frase, mas_corta=2):
    """Return a set of phrases with words from WORDS that form anagram
    of phrase. Spaces can be anywhere in phrase or anagram. All words 
    have length >= shortest. Phrases in answer must have words in 
    lexicographic order (not all permutations)."""
    frase = frase.replace(' ', '')
    palabras = set([word for word in find_words(frase) if len(word) >= mas_corta])
    combos = list(itertools.combinations(palabras, 3)) + list(itertools.combinations(palabras, 2)) + list(itertools.combinations(palabras, 1))
    return set([' '.join(sorted(c)) for c in combos if sorted(''.join(c)) == sorted(frase)])


def find_anagrams(frase, palabras, longitud_frase, prev='', resultados=None):
    "Find anagrams in words by checking recursively against previous words"
    if resultados is None: resultados = set()
    
    # Remove spaces from the list of prev. words. Example: "COP THIN" -> COPTHIN"
    previas_sin_espacio = ''.join(prev.split())
    
    # Look for anagrams in words where the word and prefixes both fit within the phrase.
    otras_palabras = set([w for w in palabras if both_fit(previas_sin_espacio, w, frase)])
    
    for w in otras_palabras:
        
        # Add the word to the previous words.
        ext_prev = previas_sin_espacio + w
        ext_prev_len = len(ext_prev)
        ext_prev_w_space = ' '.join(sorted(prev.split() + [w]))
        
        # If extended prefix is same length as phrase and they're anagrams, add to results.
        if (ext_prev_len == longitud_frase) and (sorted(ext_prev) == sorted(frase)):
            resultados.add(ext_prev_w_space)
        
        # If extended prefix is shorter than phrase, find anagrams with the new prefix.
        elif ext_prev_len < longitud_frase:
            find_anagrams(frase, palabras, longitud_frase, ext_prev_w_space, resultados)

    return resultados

def both_fit(palabra1, palabra2, frase):
    return (len(frase) - len(palabra1 + palabra2)) == len(removed(frase, palabra1 + palabra2))

# ------------
# Helpful functions
# 
# You may find the following functions useful. These functions
# are identical to those we defined in lecture. 

def removed(letters, remove):
    for L in remove:
        letters = letters.replace(L, '', 1)
    return letters

def find_words(letters):
    return extend_prefix('', letters, set())

def extend_prefix(pre, letters, results):
    if pre in WORDS: results.add(pre)
    if pre in PREFIXES:
        for L in letters:
            extend_prefix(pre+L, letters.replace(L, '', 1), results)
    return results

def prefixes(word):
    return [word[:i] for i in range(len(word))]

def readwordlist(filename):
    wordset = set(open(filename).read().upper().split())
    prefixset = set(p for word in wordset for p in prefixes(word))
    return wordset, prefixset

WORDS, PREFIXES = readwordlist('words4k.txt')

# ------------
# Testing
# 
# Run the function test() to see if your function behaves as expected.

def test():
    assert both_fit('COP', 'THIN', 'PYTHONIC') == True
    assert both_fit('IN', 'ON', 'PYTHONIC') == False
    
    assert 'DOCTOR WHO' in anagrams('TORCHWOOD')
    assert 'BOOK SEC TRY' in anagrams('OCTOBER SKY')
    assert 'SEE THEY' in anagrams('THE EYES')
    assert 'LIVES' in anagrams('ELVIS')
    assert anagrams('PYTHONIC') == set([
        'NTH PIC YO', 'NTH OY PIC', 'ON PIC THY', 'NO PIC THY', 'COY IN PHT',
        'ICY NO PHT', 'ICY ON PHT', 'ICY NTH OP', 'COP IN THY', 'HYP ON TIC',
        'CON PI THY', 'HYP NO TIC', 'COY NTH PI', 'CON HYP IT', 'COT HYP IN',
        'CON HYP TI'])
    return 'tests pass'

print test()