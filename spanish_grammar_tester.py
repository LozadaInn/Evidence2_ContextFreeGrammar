#INSTALL NLTK IN CMD
#!pip install nltk

import nltk
from nltk import CFG
from nltk.parse import ChartParser

# Gramática desambiguada: PP solo se adjunta a NP
spanish_grammar_unambiguous = CFG.fromstring(r"""
S       -> NP VP
NP      -> Det N NP_Cont
NP_Cont -> PP NP_Cont
NP_Cont ->
VP      -> V NP
PP      -> P NP
Det     -> 'el' | 'la' | 'un' | 'una'
N       -> 'hombre' | 'mujer' | 'niño' | 'parque' | 'telescopio'
V       -> 'vio' | 'amó' | 'encontró'
P       -> 'con' | 'en' | 'a'
""")

parser = ChartParser(spanish_grammar_unambiguous)

test_sentences = [
    "El hombre vio la mujer con el telescopio",
    "La mujer encontró un niño en el parque",
    "El niño encontró el telescopio en el parque",
]

for sentence in test_sentences:
    tokens = sentence.lower().split()
    trees = list(parser.parse(tokens))
    print(f"'{sentence}' genera {len(trees)} árbol(es):")
    for tree in trees:
        tree.pretty_print()