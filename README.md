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
