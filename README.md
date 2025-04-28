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


