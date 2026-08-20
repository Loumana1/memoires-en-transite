# Backlog

Deux fichiers, et c'est tout.

| Fichier | Contenu | Règle |
|---------|---------|-------|
| [`Q&A.md`](./Q&A.md) | Tout ce qui est **ambigu, incomplet ou contradictoire**. Une question par sujet, avec ce que dit Simon, ce que fait le patch, les options, et l'impact. | L'IA **ne code pas** ce qui dépend d'une question encore ouverte. Elle demande. |
| [`TO DO.md`](./TO%20DO.md) | Tout ce qui est **clair** : les bugs, et les demandes sur lesquelles Simon et l'implémentation sont d'accord. | L'IA n'y pioche que si Loumana le demande. |

---

## Le cycle

```text
document reçu de Simon
        │
        ├── clair, ou bug constaté ─────────────→ TO DO.md
        │
        └── ambigu, ou contredit le patch ─────→ Q&A.md
                                                    │
                                    réponse écrite  │
                                                    ▼
                            TO DO.md   ou   décision figée dans Zones/ ou Matiere/
```

Une question répondue **quitte** `Q&A.md`. Un `Q&A.md` qui grossit sans jamais se vider veut dire qu'on code sans avoir tranché — c'est précisément ce qu'on veut éviter.

---

## Pourquoi ce fichier existe

Les documents reçus jusqu'ici mélangent trois choses : des intentions artistiques claires, des comportements ambigus, et des règles qui contredisent directement ce qui est déjà implémenté et validé à l'oreille. Tant que les trois arrivent mélangés, chaque nouvelle implémentation casse quelque chose qui marchait.

Le tri se fait **avant** de coder, ici, et pas à l'oreille trois semaines plus tard.

Le document source reste intact dans [`../Sources/`](../Sources/) : on ne le corrige pas, on le lit et on en extrait des questions.
