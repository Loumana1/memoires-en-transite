# Sources — documents reçus

Les documents de ce dossier sont conservés **tels quels**. On ne les corrige pas, on ne les met pas à jour.

**Ce ne sont pas des specs applicables.** Un document reçu se trie avant d'être implémenté :

| Ce qu'on y trouve | Où ça va |
|-------------------|----------|
| Une intention claire, ou un bug constaté | [`../Backlog/TO DO.md`](../Backlog/TO%20DO.md) |
| Un comportement ambigu, incomplet, ou qui contredit l'implémentation | [`../Backlog/Q&A.md`](../Backlog/Q&A.md) |
| Une décision tranchée sur le son d'une zone | [`../Zones/`](../Zones/) |
| Un vocabulaire d'attributs | [`../Matiere/Attributs.md`](../Matiere/Attributs.md) |

---

## Contenu

| Document | Auteur | Date | Périmètre | Tri fait |
|----------|--------|------|-----------|----------|
| [`Simon - Cortex et Cortex-Ambiance.md`](./Simon%20-%20Cortex%20et%20Cortex-Ambiance.md) | Simon Mahungu | août 2026 | Cortex et Cortex-Ambiance uniquement | oui, 20 août — 24 questions dans `Q&A.md` |
| [`Specifications_Pure_Data_Hippocampe.md`](./Specifications_Pure_Data_Hippocampe.md) | Simon Mahungu | août 2026 | Hippocampe (+ Hippocampe–Ambiance décrite, rejetée en V1) | oui, 21 août — §I `Q&A.md` ; Q26–Q28 fermées |
| [`Specifications_Pure_Data_Reconstruction_Reconstruction_Ambiance.md`](./Specifications_Pure_Data_Reconstruction_Reconstruction_Ambiance.md) | Simon Mahungu | août 2026 | Reconstruction + Reconstruction–Ambiance | oui, 21 août — §J `Q&A.md` ; Q29–Q37 ouvertes |

La **Boucle** n'a toujours **aucun** document source dédié. Voir [Q19](../Backlog/Q&A.md#q19).

Le guide Ableton de Simon du 15 août n'a jamais été transcrit ici. Ce qu'il en reste d'utile est dans [`../Matiere/Pipeline.md`](../Matiere/Pipeline.md) : il décrit la préparation des 4 masters, pas le fonctionnement du patch.

---

## Résumé du tri du 20 août

Le document de Simon est un vrai pas en avant : il donne pour la première fois un vocabulaire d'attributs nommé et des règles d'association explicites. Trois choses en ressortent.

**Ce qui est clair et acquis.** Deux fragments superposés par baffle de parole, un de chaque contexte géographique. Des niveaux de présence différents. Des ambiances sèches et continues, sans delay ni découpe. **Deux baffles d'ambiance globaux** (pas une ambiance par baffle de parole) — [Q25](../Backlog/Q&A.md#q25). Les deux baffles d'ambiance pas côte à côte. Le Cortex encore trop intelligible, à flouter davantage.

**Ce qui contredit directement l'implémentation.** La carte des 8 HP ([Q1](../Backlog/Q&A.md#q1)) : 6 baffles de parole et 2 d'ambiance chez Simon, contre 3 et 5 dans le patch. La durée des ambiances ([Q3](../Backlog/Q&A.md#q3)) : 30 s minimum contre des atomes de 2 s. Le rôle du piézo ([Q14](../Backlog/Q&A.md#q14)), qui fait l'inverse de ce qui est câblé. Et le mot « zone » qui ne désigne pas la même chose de part et d'autre ([Q2](../Backlog/Q&A.md#q2)).

**Ce qui est ambigu au point de ne pas être codable.** Les règles « à privilégier » sans dire quoi faire en cas d'échec ([Q7](../Backlog/Q&A.md#q7)). La table C2 qui n'est pas symétrique, donc dont le résultat dépend de l'ordre de tirage ([Q8](../Backlog/Q&A.md#q8)). Les tables C9 et C10 dont toutes les lignes donnent la même réponse, et qui ne discriminent donc rien ([Q12](../Backlog/Q&A.md#q12)). Et surtout : toutes les règles supposent une matière étiquetée Belgique / Congo qui n'existe pas encore ([Q4](../Backlog/Q&A.md#q4)).

Simon liste lui-même 8 points à confirmer au §6. Ils sont tous repris dans `Q&A.md`, avec 16 autres trouvés en confrontant le document au code.
