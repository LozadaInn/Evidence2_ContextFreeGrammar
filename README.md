# Evidence 2 - Generating and Cleaning a Restricted Context Free Grammar.
**Iñaki Salvador Pérez Lozada - A01278252**

## Disclaimer
I used ChatGPT and Monica IA mainly for consulting but also to correct code syntax and translation.

## Description
The language that I chose is Spanish, one of the most widely spoken languages in the world. Spanish is a Romance language that evolved from Latin, characterized by a relatively flexible word order and rich use of articles, prepositions, and verb conjugations.

In this project, a subset of the Spanish language will be modeled, specifically focusing on simple noun phrases and verb phrases, to limit the scope and ensure the grammar remains manageable for analysis and parsing.

### The basic structure analyzed consists of:
- **Noun Phrases (NP)**
- **Verb Phrases (VP)**
- **Prepositional Phrases (PP)**

### The goal is to recognize simple sentences like:
- "El hombre vio a la mujer."
- "La niña encontró el telescopio en el parque."

This subset captures essential Spanish syntactic constructions but avoids complex structures such as subordinate clauses or advanced verb conjugations, making it ideal for a first step in syntax analysis.

## Models

### Initial Grammar (Ambiguous)
The initial grammar that models simple Spanish sentences is the following:

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


### Problem: Ambiguity
This grammar is ambiguous because for sentences like:

"El hombre vio a la mujer con el telescopio."

it is unclear if the prepositional phrase "con el telescopio" modifies "la mujer" (i.e., the woman with the telescope) or the action "vio" (i.e., he saw using the telescope).

There are two possible parse trees for such sentences, which is unacceptable for LL(1) parsing. Additionally, left recursion in NP and VP productions prevents direct LL(1) parsing.

---------------------------------------------------------
# Analysis and Elimination of Ambiguity

## Introduction

The original grammar is ambiguous because it allows more than one parse tree for certain sentences, creating confusion about which phrase a prepositional phrase (PP) modifies. For example, the sentence:

**"El hombre vio a la mujer con el telescopio."**

has two possible interpretations:

- **Interpretation 1:** The man saw the woman who had the telescope.
- **Interpretation 2:** The man used the telescope to see the woman.

## Modified Grammar

To eliminate this ambiguity, the grammar is restructured by explicitly defining optional modifiers for noun and verb phrases separately:

S → NP VP  
NP → Det N NP_Mod  
NP_Mod → PP | ε  
VP → V NP VP_Mod  
VP_Mod → PP | ε  
PP → P NP  
Det → "el" | "la" | "un" | "una"  
N → "hombre" | "mujer" | "niño" | "telescopio" | "parque"  
V → "vio" | "amó" | "encontró"  
P → "con" | "en" | "a"

In this revised grammar, the modifiers are clearly attached to either noun phrases (NP_Mod) or verb phrases (VP_Mod), thus eliminating structural ambiguity.

## Elimination of Left Recursion

The original grammar also contains left recursion, specifically in the rules:

NP → NP PP  
VP → VP PP

Left recursion is problematic for LL(1) parsers because it can lead to infinite loops during parsing. To solve this, we apply standard techniques to eliminate left recursion, converting it to right recursion using additional non-terminal symbols:

NP → Det N NP_Tail  
NP_Tail → PP NP_Tail | ε  

VP → V NP VP_Tail  
VP_Tail → PP VP_Tail | ε

This restructuring ensures that the grammar is suitable for LL(1) parsing, as it no longer contains left-recursive productions.

## Parse Trees Before and After Grammar Modification

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

```
S
├── NP
│   ├── Det ("el")
│   └── N ("hombre")
└── VP
    ├── V ("vio")
    ├── NP
    │   ├── Det ("la")
    │   └── N ("mujer")
    └── VP_Tail
        ├── PP
        │   ├── P ("con")
        │   └── NP
        │       ├── Det ("el")
        │       └── N ("telescopio")
        └── ε
```

This parse tree clearly shows that the prepositional phrase "con el telescopio" modifies the verb phrase ("vio"), removing ambiguity entirely.


Summary of Improvements

With these modifications, our grammar now meets essential LL(1) parsing criteria:

No Ambiguity: Each sentence has exactly one parse tree.
No Left Recursion: Eliminated to ensure compatibility with LL(1) parsers.
Explicit Modifiers: Clearly distinguishes noun and verb modifiers.
This revised grammar serves as a solid foundation for accurate and efficient parsing of simple Spanish sentences.
