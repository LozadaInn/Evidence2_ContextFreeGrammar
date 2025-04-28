# Evidence 2 – Generating and Cleaning a Restricted Context-Free Grammar  
**Iñaki Salvador Pérez Lozada – A01278252**

---

## Disclaimer
I used ChatGPT and Monica IA for consultation, code-syntax corrections, and translations.

---

## Description
The language I chose is **Spanish**, one of the most widely spoken languages in the world. Spanish is a Romance language that evolved from Latin, characterized by a relatively flexible word order and a rich system of articles, prepositions, and verb conjugations.

In this project we model a **subset** of Spanish—simple declarative sentences consisting of:

- **Noun Phrases (NP)**
- **Verb Phrases (VP)**
- **Prepositional Phrases (PP)**

The goal is to recognize sentences such as:  
> “El hombre vio a la mujer.”  
> “La niña encontró el telescopio en el parque.”

This subset captures essential Spanish syntax without subordinate clauses or advanced verb morphology, making it ideal for LL(1) parsing.

---

## Models

### Initial Grammar (Ambiguous)
```text
S    → NP VP

NP   → Det N
NP   → NP PP

VP   → V NP
VP   → VP PP

PP   → P NP

Det  → "el" | "la" | "un" | "una"
N    → "hombre" | "mujer" | "niño" | "telescopio" | "parque"
V    → "vio" | "amó" | "encontró"
P    → "con" | "en" | "a"
```

### Problem: Ambiguity
This grammar is ambiguous because for sentences like:

"El hombre vio a la mujer con el telescopio."

it is unclear if the prepositional phrase "con el telescopio" modifies "la mujer" (i.e., the woman with the telescope) or the action "vio" (i.e., he saw using the telescope).

There are two possible parse trees for such sentences, which is unacceptable for LL(1) parsing. Additionally, left recursion in NP and VP productions prevents direct LL(1) parsing.

---------------------------------------------------------
# Analysis and Elimination of Ambiguity

We decide that PPs only modify NPs.

Remove VP → VP PP.

Refactor NP → NP PP into a right-recursive tail:

```text
S        → NP VP

NP       → Det N NP_Tail
NP_Tail  → PP NP_Tail
NP_Tail  → ε

VP       → V NP

PP       → P NP

Det      → "el" | "la" | "un" | "una"
N        → "hombre" | "mujer" | "niño" | "telescopio" | "parque"
V        → "vio" | "amó" | "encontró"
P        → "con" | "en" | "a"
```

PP appears only in NP_Tail.

Now “con el telescopio” cannot attach to the VP.

## Elimination of Left Recursion

The original left-recursive rule NP → NP PP is gone.
We use:

```text
NP       → Det N NP_Tail
NP_Tail  → PP NP_Tail | ε
```

which is right-recursive. No left recursion remains—grammar is ready for LL(1).

Left recursion is problematic for LL(1) parsers because it can lead to infinite loops during parsing. To solve this, we apply standard techniques to eliminate left recursion, converting it to right recursion using additional non-terminal symbols:

This restructuring ensures that the grammar is suitable for LL(1) parsing, as it no longer contains left-recursive productions.

## Parse Trees Before and After Grammar Modification

To illustrate clearly the improvements made, we present parse trees for the sentence:

**"El hombre vio a la mujer con el telescopio."**

### Original Grammar (Ambiguous)

Two possible parse trees:

#### Interpretation 1 (NP attachment):
```
S
├── NP
│   ├── Det ("el")
│   └── N ("hombre")
└── VP
    ├── VP
    │   ├── V ("vio")
    │   └── NP
    │       ├── Det ("la")
    │       └── N ("mujer")
    └── PP
        ├── P ("con")
        └── NP
            ├── Det ("el")
            └── N ("telescopio")
```

### Interpretation 2 (VP attachment):

```
S
├── NP
│   ├── Det ("el")
│   └── N ("hombre")
└── VP
    ├── V ("vio")
    └── NP
        ├── NP
        │   ├── Det ("la")
        │   └── N ("mujer")
        └── PP
            ├── P ("con")
            └── NP
                ├── Det ("el")
                └── N ("telescopio")
```

### Modified Grammar (Unambiguous)

One clear parse tree, explicitly indicating attachment:

### Clear Interpretation (VP attachment example):

Only one tree—PP under NP:

```text
S
├─ NP
│  ├ Det(el)
│  ├ N(hombre)
│  └ NP_Tail
│     └ ε
└─ VP
   ├ V(vio)
   └ NP
      ├ Det(la)
      ├ N(mujer)
      └ NP_Tail
         ├ PP
         │  ├ P(con)
         │  └ NP
         │     ├ Det(el)
         │     └ N(telescopio)
         └ NP_Tail
            └ ε

```

This parse tree clearly shows that the prepositional phrase "con el telescopio" modifies the verb phrase ("vio"), removing ambiguity entirely.


Summary of Improvements

With these modifications, our grammar now meets essential LL(1) parsing criteria:

No Ambiguity: Each sentence has exactly one parse tree.
No Left Recursion: Eliminated to ensure compatibility with LL(1) parsers.
Explicit Modifiers: Clearly distinguishes noun and verb modifiers.
This revised grammar serves as a solid foundation for accurate and efficient parsing of simple Spanish sentences.

---

## Implementation

This is a simple python tester that uses NLTK and a ChartParser:

```python
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
```
### Run with

```shell
pip install nltk
python spanish_grammar_tester.py
```

### Accepted strings

```text
El hombre vio la mujer
El hombre vio la mujer con el telescopio
El niño encontró el telescopio en el parque
```

### Rejected strings

```text
Hombre vio el
La con mujer vio
El niño amó telescopio en
```
### LL(1) Parsing Example

For “El hombre vio la mujer con el telescopio” the parser returns 1 tree, showing that the grammar is deterministic with one lookahead.

### Analysis

**Before cleaning**

- Chomsky level: Type 2 (Context-Free), because productions have a single nonterminal on the left and a mix of terminals/nonterminals on the right.

- Ambiguity and left recursion prevented LL(1).

**After cleaning**

- Chomsky level: Still Type 2.

- Grammar is now unambiguous and LL(1).

**Time complexity**

- An LL(1) parser runs in O(n) time where n is the input length.

- Left-recursive or ambiguous grammars can cause backtracking or infinite loops.

## References:
- GeeksforGeeks. (2025a, January 27). Introduction of lexical analysis.GeeksforGeeks. https://www.geeksforgeeks.org/introduction-of-lexical-analysis/
- GeeksforGeeks. (2025b, January 28). Ambiguous grammar. GeeksforGeeks. https://www.geeksforgeeks.org/ambiguous-grammar/
- GeeksforGeeks. (2025c, April 2). Introduction to Syntax analysis in Compiler Design. GeeksforGeeks. https://www.geeksforgeeks.org/introduction-to-syntax-analysis-in-compiler-design/
- Grammars in prolog. (n.d.). https://www3.cs.stonybrook.edu/~warren/xsbbook/node10.html
