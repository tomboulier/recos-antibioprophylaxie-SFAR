# Benchmark Antibioprophylaxie SFAR

> Jeu de questions standardisé pour évaluer tout système (RAG, MCP, chatbot, LLM)
> sur les recommandations d'antibioprophylaxie chirurgicale (RFE SFAR 2024).
>
> **Source** : RFE SFAR 2024 (V2.0 du 22/05/2024)
> **Périmètre** : Chirurgie orthopédique programmée + Traumatologie (47 interventions)
> **Auteur initial** : Claude (à valider/corriger par un médecin)
> **Date** : 2026-03-11

## Format des réponses attendues

Pour les questions ouvertes, la réponse attendue suit le format :

```
Molecule | Dose initiale | Réinjection
```

Ou bien :
- `Pas d'ABP recommandée`
- `Hors périmètre` (question ne portant pas sur l'ortho/trauma)

Pour les QCM, une seule réponse correcte sauf mention contraire.

---

## Questions ouvertes

### Q01 — Protocole standard PTH

- **type** : open
- **difficulté** : facile
- **catégorie** : protocole-standard
- **question** : Quelle antibioprophylaxie recommandez-vous pour une prothèse totale de hanche ?
- **réponse** : Céfazoline | 2g IVL | 1g si durée > 4h, puis toutes les 4h jusqu'à fin de chirurgie
- **source** : ortho-prog-mi-prothese-hanche-genou

### Q02 — Pas d'ABP arthroscopie diagnostique

- **type** : open
- **difficulté** : facile
- **catégorie** : pas-abp
- **question** : Faut-il prescrire une antibioprophylaxie pour une arthroscopie diagnostique du genou sans mise en place de matériel ?
- **réponse** : Pas d'ABP recommandée
- **source** : ortho-prog-mi-arthroscopie-sans-materiel

### Q03 — Allergie PTH

- **type** : open
- **difficulté** : moyen
- **catégorie** : allergie
- **question** : Un patient allergique aux bêtalactamines doit bénéficier d'une prothèse de hanche. Quelle antibioprophylaxie en première intention ?
- **réponse** : Clindamycine | 900mg IVL
- **source** : ortho-prog-mi-prothese-hanche-genou

### Q04 — Allergie PTH voie antérieure

- **type** : open
- **difficulté** : difficile
- **catégorie** : allergie-note
- **question** : Pour une prothèse de hanche par voie antérieure chez un patient allergique aux bêtalactamines, faut-il préférer la clindamycine ou la vancomycine ?
- **réponse** : Vancomycine | 20 mg/kg IVL (ou Teicoplanine 12 mg/kg IVL) - préférer la vancomycine ou la teicoplanine à la clindamycine pour cette voie d'abord
- **source** : ortho-prog-mi-prothese-hanche-genou (note)

### Q05 — Fracture ouverte Gustilo 2-3

- **type** : open
- **difficulté** : moyen
- **catégorie** : protocole-standard
- **question** : Quelle antibioprophylaxie pour une fracture ouverte de jambe Gustilo 2 ?
- **réponse** : Amoxicilline/Clavulanate | 2g IVL | 1g si durée > 2h, puis toutes les 2h jusqu'à fin de chirurgie
- **source** : trauma-fracture-ouverte-gustilo-2-3

### Q06 — Fracture fermée fixateur externe

- **type** : open
- **difficulté** : facile
- **catégorie** : pas-abp
- **question** : Faut-il une antibioprophylaxie pour la pose d'un fixateur externe sur une fracture fermée ?
- **réponse** : Pas d'ABP recommandée
- **source** : trauma-fracture-fermee-fixateur-externe

### Q07 — Rachis instrumenté 1 temps

- **type** : open
- **difficulté** : moyen
- **catégorie** : protocole-standard
- **question** : Quelle antibioprophylaxie pour une arthrodèse lombaire instrumentée en un temps ?
- **réponse** : Céfazoline | 2g IVL | 1g si durée > 4h, puis toutes les 4h jusqu'à fin de chirurgie
- **source** : ortho-prog-rachis-instrumentee-1-temps

### Q08 — Rachis sans matériel

- **type** : open
- **difficulté** : facile
- **catégorie** : pas-abp
- **question** : Faut-il une antibioprophylaxie pour une chirurgie du rachis sans pose de matériel (par ex. hernie discale) ?
- **réponse** : Pas d'ABP recommandée
- **source** : ortho-prog-rachis-sans-materiel

### Q09 — Morsure

- **type** : open
- **difficulté** : moyen
- **catégorie** : protocole-standard
- **question** : Quelle antibioprophylaxie pour le parage chirurgical d'une morsure ?
- **réponse** : Amoxicilline/Clavulanate | 2g IVL | 1g si durée > 2h, puis toutes les 2h jusqu'à fin de chirurgie
- **source** : trauma-morsure

### Q10 — Traumatisme complexe main

- **type** : open
- **difficulté** : moyen
- **catégorie** : protocole-standard
- **question** : Quelle antibioprophylaxie pour un écrasement complexe de la main nécessitant une chirurgie de plus de 2 heures ?
- **réponse** : Amoxicilline/Clavulanate | 2g IVL | 1g si durée > 2h, puis toutes les 2h jusqu'à fin de chirurgie
- **source** : trauma-main-complexe

### Q11 — Hors périmètre

- **type** : open
- **difficulté** : piège
- **catégorie** : hors-perimetre
- **question** : Quelle antibioprophylaxie pour une cholécystectomie par coelioscopie ?
- **réponse** : Hors périmètre
- **source** : aucune (chirurgie digestive, hors ortho/trauma)

### Q12 — Réinjection

- **type** : open
- **difficulté** : moyen
- **catégorie** : reinjection
- **question** : Une prothèse de genou dure 5 heures. Quand faut-il réinjecter l'antibioprophylaxie et à quelle dose ?
- **réponse** : Réinjection de 1g de Céfazoline à H+4, puis toutes les 4h jusqu'à fin de chirurgie
- **source** : ortho-prog-mi-prothese-hanche-genou

### Q13 — Plaie tellurique

- **type** : open
- **difficulté** : moyen
- **catégorie** : protocole-standard
- **question** : Quelle antibioprophylaxie pour une plaie de cuisse par accident agricole, susceptible d'être contaminée par des germes telluriques ?
- **réponse** : Amoxicilline/Clavulanate | 2g IVL | 1g si durée > 2h, puis toutes les 2h jusqu'à fin de chirurgie
- **source** : trauma-plaie-contaminee

### Q14 — Plaie simple parties molles

- **type** : open
- **difficulté** : facile
- **catégorie** : pas-abp
- **question** : Faut-il une antibioprophylaxie pour le parage d'une plaie simple du mollet ?
- **réponse** : Pas d'ABP recommandée
- **source** : trauma-plaie-simple

### Q15 — Allergie Gustilo 2-3

- **type** : open
- **difficulté** : difficile
- **catégorie** : allergie
- **question** : Un patient allergique aux pénicillines présente une fracture ouverte Gustilo 3. Quelle antibioprophylaxie ?
- **réponse** : Clindamycine + Gentamicine | 900mg IV + 6-7 mg/kg
- **source** : trauma-fracture-ouverte-gustilo-2-3

---

## QCM

### Q16 — Molécule PTG (QCM)

- **type** : qcm
- **difficulté** : facile
- **catégorie** : protocole-standard
- **question** : Quelle molécule est recommandée en première intention pour l'antibioprophylaxie d'une prothèse totale de genou ?
- **choix** :
  - A. Amoxicilline/Clavulanate
  - B. Céfazoline
  - C. Clindamycine
  - D. Vancomycine
- **réponse** : B
- **source** : ortho-prog-mi-prothese-hanche-genou

### Q17 — Dose Céfazoline (QCM)

- **type** : qcm
- **difficulté** : facile
- **catégorie** : posologie
- **question** : Quelle est la dose initiale de Céfazoline recommandée en antibioprophylaxie en chirurgie orthopédique ?
- **choix** :
  - A. 1g IVL
  - B. 2g IVL
  - C. 3g IVL
  - D. 20 mg/kg IVL
- **réponse** : B
- **source** : ortho-prog-mi-prothese-hanche-genou

### Q18 — Pas d'ABP (QCM)

- **type** : qcm
- **difficulté** : facile
- **catégorie** : pas-abp
- **question** : Parmi ces interventions, laquelle ne nécessite PAS d'antibioprophylaxie ?
- **choix** :
  - A. Prothèse d'épaule
  - B. Arthrodèse lombaire instrumentée
  - C. Ablation de matériel d'ostéosynthèse du fémur
  - D. Arthroscopie du genou avec pose d'ancre
- **réponse** : C
- **source** : ortho-prog-mi-ablation-materiel

### Q19 — Allergie bêtalactamines (QCM)

- **type** : qcm
- **difficulté** : moyen
- **catégorie** : allergie
- **question** : En cas d'allergie aux bêtalactamines, quelle est l'alternative de première intention pour l'antibioprophylaxie d'une prothèse de hanche ?
- **choix** :
  - A. Gentamicine
  - B. Vancomycine
  - C. Clindamycine
  - D. Métronidazole
- **réponse** : C
- **source** : ortho-prog-mi-prothese-hanche-genou

### Q20 — Gustilo classification (QCM)

- **type** : qcm
- **difficulté** : moyen
- **catégorie** : protocole-standard
- **question** : À partir de quel stade de Gustilo la molécule d'antibioprophylaxie change-t-elle (passage de la Céfazoline à l'Amoxicilline/Clavulanate) ?
- **choix** :
  - A. Gustilo 1
  - B. Gustilo 2
  - C. Gustilo 3
  - D. Pas de changement, c'est toujours la Céfazoline
- **réponse** : B
- **source** : trauma-fracture-ouverte-gustilo-1, trauma-fracture-ouverte-gustilo-2-3

### Q21 — Réinjection Amox/Clav (QCM)

- **type** : qcm
- **difficulté** : moyen
- **catégorie** : reinjection
- **question** : À quel intervalle doit-on réinjecter l'Amoxicilline/Clavulanate en antibioprophylaxie ?
- **choix** :
  - A. Toutes les 2h
  - B. Toutes les 4h
  - C. Toutes les 6h
  - D. Pas de réinjection
- **réponse** : A
- **source** : trauma-fracture-ouverte-gustilo-2-3

### Q22 — Plaie main tellurique (QCM)

- **type** : qcm
- **difficulté** : difficile
- **catégorie** : pas-abp
- **question** : Un patient se présente avec une plaie de la main par accident de jardinage, susceptible de contamination tellurique. Quelle est la recommandation ?
- **choix** :
  - A. Céfazoline 2g IVL
  - B. Amoxicilline/Clavulanate 2g IVL
  - C. Pas d'ABP recommandée
  - D. Clindamycine 900mg IVL
- **réponse** : C
- **source** : trauma-main-plaie-contaminee

### Q23 — Allergie trauma complexe main (QCM)

- **type** : qcm
- **difficulté** : difficile
- **catégorie** : allergie
- **question** : Quelle est l'alternative en cas d'allergie aux pénicillines pour un traumatisme complexe de la main (écrasement) ?
- **choix** :
  - A. Clindamycine seule
  - B. Vancomycine seule
  - C. Céfazoline + Gentamicine
  - D. Clindamycine + Gentamicine
- **réponse** : C
- **source** : trauma-main-complexe

### Q24 — Piège hors périmètre (QCM)

- **type** : qcm
- **difficulté** : piège
- **catégorie** : hors-perimetre
- **question** : Quelle antibioprophylaxie pour une appendicectomie ?
- **choix** :
  - A. Céfazoline 2g IVL
  - B. Amoxicilline/Clavulanate 2g IVL
  - C. Pas d'ABP recommandée
  - D. Hors périmètre de ces recommandations
- **réponse** : D
- **source** : aucune (chirurgie digestive)

### Q25 — Distinction matériel / sans matériel (QCM)

- **type** : qcm
- **difficulté** : moyen
- **catégorie** : protocole-standard
- **question** : Deux patients doivent bénéficier d'une arthroscopie de genou : l'un avec mise en place d'une ancre, l'autre sans matériel. Quelle est la bonne conduite ?
- **choix** :
  - A. ABP pour les deux
  - B. ABP uniquement pour celui avec matériel
  - C. Pas d'ABP pour les deux
  - D. ABP uniquement pour celui sans matériel
- **réponse** : B
- **source** : ortho-prog-mi-arthroscopie-avec-materiel, ortho-prog-mi-arthroscopie-sans-materiel
