# Product Brief : Antibioprophylaxie SFAR

**Date :** 2026-02-15
**Auteur :** Thomas Boulier
**Version :** 1.0
**Type de projet :** Application web (web-app)
**Niveau de projet :** 2 (Medium, 5-15 stories)

---

## Résumé exécutif

Ce projet vise à créer une application web unifiée et open-source permettant aux anesthésistes-réanimateurs de retrouver instantanément la bonne antibioprophylaxie au bloc opératoire, en s'appuyant sur les Recommandations Formalisées d'Experts (RFE) de la SFAR 2024. Au-delà de l'outil clinique, le projet comporte une dimension recherche : intégrer un accès IA (MCP, RAG, ou comparaison des deux) aux recommandations, évaluer la fiabilité des réponses, et publier les résultats. Il s'agit aussi d'un projet vitrine pour le groupe numérique de la SFAR et d'un support pédagogique pour la numérisation des recommandations médicales.

---

## Problème à résoudre

### Le problème

Aujourd'hui, pour trouver la bonne antibioprophylaxie pour une intervention chirurgicale, un anesthésiste doit : aller sur internet, chercher "atb rfe sfar 2024" sur Google, cliquer sur le lien de la SFAR, télécharger un PDF de 91 pages, l'ouvrir, faire Ctrl+F, trier parmi des dizaines de résultats pour trouver la bonne page. Par exemple, chercher "prothèse" donne 35 résultats ; il faut affiner avec "hanche" pour tomber sur céfazoline en page 73.

En pratique, les médecins contournent le problème en imprimant les pages pertinentes par spécialité (ex. : pages 72 à 77 pour l'orthopédie) et les affichent en salle. Les protocoles locaux (adaptés à l'écologie bactérienne locale, en lien avec l'infectiologie) sont eux aussi au format Word/PDF imprimé. C'est fonctionnel, mais archaïque.

### Pourquoi maintenant ?

Trois facteurs convergent :

1. **L'arrivée des LLMs en médecine** : les modèles de langage débarquent dans le monde médical, mais sans garde-fous. Les sociétés savantes comme la SFAR ont un rôle à jouer pour que leurs recommandations soient accessibles de manière fiable aux outils d'IA, plutôt que de laisser les éditeurs logiciels développer ces outils sans expertise médicale.

2. **Le contexte académique** : le porteur du projet vise un poste hospitalo-universitaire en santé numérique (section 46.04 CNU — informatique, biostatistiques et santé numérique). Ce projet constitue une démonstration d'expertise IA appliquée à la médecine, avec un potentiel de publication.

3. **Le groupe numérique SFAR** : des discussions sont en cours sur la numérisation des RFE. Cette RFE sur l'antibioprophylaxie est un excellent premier cas d'usage concret.

### Impact si on ne fait rien

Ce n'est pas un drame clinique — les médecins continuent avec leurs PDF et feuilles imprimées. Mais c'est un symptôme d'une résignation collective face à des outils inadaptés. Le risque plus large est que les LLMs en médecine se développent *sans* l'implication des sociétés savantes, avec des données non structurées et un risque d'hallucinations sur des informations critiques (dosages d'antibiotiques, indications, contre-indications).

---

## Public cible

### Utilisateurs principaux

**Anesthésistes-réanimateurs** (praticiens hospitaliers, internes, IADE) — au bloc opératoire (sur téléphone ou PC de la station d'anesthésie) et en consultation pré-anesthésique. Peu technophiles en général, ils ont besoin d'un outil qui fonctionne immédiatement, sans friction.

### Utilisateurs secondaires

- **Groupe numérique SFAR** : interlocuteurs techniques, early adopters, relais institutionnel. Plus à l'aise avec la technologie, intéressés par la démarche de numérisation des RFE.
- **Éditeurs logiciels et développeurs** : consommateurs de l'API/MCP open-source pour intégrer les recommandations officielles dans leurs outils (DPI, systèmes d'aide à la décision, assistants IA).
- **Infectiologues** (à la marge) : potentiellement impliqués pour les protocoles locaux dans une version future.

### Besoins des utilisateurs

1. **Trouver instantanément le bon ATB** pour une intervention donnée — en tapant quelques lettres ou en naviguant par spécialité, obtenir la recommandation complète (molécule, posologie, timing, réinjection, alternative en cas d'allergie) avec la source exacte (page, tableau).
2. **Expérimenter l'IA sur des données médicales structurées** — évaluer si un LLM branché sur les RFE via MCP/RAG donne des réponses fiables, mesurables, publiables. Pouvoir poser des questions en langage naturel ("je mets quoi sur une PTH ?") et obtenir une réponse sourcée ou un "je ne sais pas" honnête.
3. **Accéder aux recommandations de manière programmatique** — via une API REST ou un serveur MCP, permettre à d'autres outils (éditeurs logiciels, LLMs, applications tierces) d'interroger les recommandations officielles de manière fiable et traçable.

---

## Vue d'ensemble de la solution

### Solution proposée

Une plateforme unifiée en trois couches, fusionnant les deux dépôts existants :

- **Couche 1 — Webapp responsive** : une interface web épurée avec une barre de recherche centrale. À chaque frappe, les résultats se mettent à jour en temps réel (type-ahead). Navigation alternative par arborescence (spécialité → type d'intervention → protocole). Design responsive pour usage au bloc (téléphone, tablette, PC).

- **Couche 2 — Module IA** : un chatbot intégré à la webapp permettant de poser des questions en langage naturel. Le chatbot s'appuie sur les données structurées (pas directement sur le PDF) et fournit systématiquement la source de sa réponse. S'il ne trouve pas la réponse, il le dit clairement et peut suggérer l'intervention la plus proche.

- **Couche 3 — API et MCP open-source** : le backend est un produit en soi. Une API REST et un serveur MCP permettent à des services tiers (éditeurs logiciels, autres LLMs) d'interroger les recommandations. Le tout est open-source et documenté pour favoriser l'adoption.

**Chantier transverse** : structuration des données du PDF de 91 pages en base de données exploitable (extraction, validation, modélisation).

### Fonctionnalités clés

- Recherche instantanée par mots-clés avec mise à jour en temps réel (type-ahead)
- Navigation par arborescence (spécialité → intervention)
- Affichage complet du protocole : molécule, posologie, timing, réinjection, alternative allergie
- Traçabilité : lien vers la source exacte (page du PDF, tableau d'origine)
- Chatbot IA avec recherche augmentée et sourçage des réponses
- API REST pour accès programmatique aux recommandations
- Serveur MCP pour intégration avec les LLMs
- Projet open-source (GitHub)

### Proposition de valeur

Ce n'est pas juste "un PDF en ligne avec un meilleur moteur de recherche". C'est une donnée médicale structurée, fiable, traçable, accessible en 2 secondes au bloc — et consommable par des machines (API, MCP). C'est la démonstration qu'une société savante peut structurer ses recommandations pour l'ère de l'IA, plutôt que de subir les interprétations approximatives des LLMs sur des PDF.

---

## Objectifs

### Objectifs concrets

- **V1 fonctionnelle avant le congrès SFAR (septembre 2026)** : webapp avec recherche instantanée + navigation par arborescence, déployée et démontrable
- **Module IA opérationnel** : chatbot avec recherche augmentée, capable de répondre aux questions d'ATB avec sourçage, à présenter au groupe numérique SFAR
- **API/MCP documentée et open-source** : publiée sur GitHub, utilisable par des tiers
- **Soumission d'une publication** : article décrivant la démarche de numérisation des RFE et l'évaluation de la fiabilité d'un LLM branché sur des recommandations structurées

### Métriques de succès

- Temps de recherche d'une antibioprophylaxie : < 5 secondes (vs. plusieurs minutes avec le PDF)
- Taux d'hallucination du chatbot IA : à mesurer et publier (objectif : < 5% sur un jeu de questions de test)
- Couverture des données : 100% des interventions listées dans la RFE structurées en base
- Feedback qualitatif positif des collègues anesthésistes et du groupe numérique SFAR
- Au moins 1 démonstration au congrès SFAR septembre 2026

### Valeur attendue

- **Pédagogique** : apprentissage personnel (spec-driven development, architecture logicielle, IA en médecine) et support de formation pour d'autres
- **Académique** : publication scientifique, renforcement du dossier HU (section 46.04 CNU)
- **Politique/institutionnelle** : positionnement de la SFAR dans le débat sur l'IA en médecine, démonstration que les sociétés savantes peuvent structurer leurs recommandations pour l'ère numérique

---

## Périmètre

### Dans le périmètre (V1)

- Structuration des données du PDF RFE antibioprophylaxie 2024 en base de données
- Webapp responsive avec recherche instantanée (type-ahead)
- Navigation par arborescence (spécialité → intervention)
- API REST pour accès programmatique (lecture seule — GET)
- Serveur MCP pour intégration LLM
- Module chatbot IA avec sourçage des réponses et capacité à dire "je ne sais pas"
- Traçabilité : référence à la source exacte (page PDF, tableau)
- Projet open-source sur GitHub
- Documentation technique et utilisateur

### Hors périmètre (V1)

- **Application mobile native** (iOS/Android) — un autre projet est en cours côté SFAR
- **Gestion des utilisateurs / authentification** — l'outil doit être accessible sans compte, sans friction
- **Autres RFE** que l'antibioprophylaxie — cette RFE est le point de départ, les autres suivront éventuellement
- **Hébergement certifié HDS** — pas de données de santé hébergées, uniquement des recommandations publiques
- **Intégration directe avec les DPI** — c'est l'API libre d'accès qui sert de point d'intégration

### Considérations futures (V2+)

- **Protocoles locaux** : personnalisation par établissement (CRUD complet — Create, Update), possiblement avec authentification légère
- **Export Excel** des recommandations (format demandé par les médecins)
- **Extension à d'autres RFE** de la SFAR et d'autres sociétés savantes
- **Évaluation réglementaire** : clarifier le statut de dispositif médical / logiciel d'aide à la décision (à investiguer via `/bmad:research`)

---

## Parties prenantes

- **Thomas Boulier (Porteur de projet / Développeur)** — Influence haute. Anesthésiste-réanimateur et ingénieur/chercheur. Concepteur, développeur principal, et premier utilisateur.
- **Groupe Numérique SFAR** — Influence haute. Cible de démonstration prioritaire, interlocuteurs sur la numérisation des RFE. Relais vers le reste de l'institution.
- **SFAR (Comité des référentiels / CA)** — Influence moyenne (indirecte). Partie prenante institutionnelle, accessible via le groupe numérique si le projet convainc.
- **Collègues anesthésistes du service** — Influence moyenne. Utilisateurs finaux, source de retours terrain et de validation de l'ergonomie.

---

## Contraintes et hypothèses

### Contraintes

- **Développeur solo** : Thomas est seul sur le développement, avec un temps limité (activité clinique + recherche en parallèle)
- **Budget quasi-nul** : pas de budget dédié ; hébergement et éventuels coûts d'API LLM à minimiser (solutions gratuites/open-source privilégiées)
- **Deadline congrès SFAR** : septembre 2026, pour une démonstration fonctionnelle
- **Données source complexes** : un PDF de 91 pages avec des tableaux à structurer — travail d'extraction et de modélisation significatif
- **Open-source obligatoire** : le code doit être public et réutilisable
- **Stack technique libre** : pas de contrainte imposée, ouverture à l'apprentissage de nouvelles technologies

### Hypothèses

- Les données des RFE SFAR sont publiques et librement réutilisables (recommandations de société savante, pas de restriction de propriété intellectuelle connue)
- Les utilisateurs ont accès à un navigateur web moderne (pas besoin d'installation)
- Un LLM peut répondre correctement aux questions d'antibioprophylaxie si on lui fournit des données structurées — hypothèse à valider (c'est le cœur du volet recherche)
- Le statut réglementaire (dispositif médical / logiciel d'aide à la décision) ne bloque pas un projet de recherche open-source — à confirmer

---

## Critères de succès

- L'outil est utilisable en conditions réelles au bloc opératoire (responsive, rapide, sans authentification)
- Un anesthésiste trouve la bonne antibioprophylaxie en moins de 5 secondes
- Le chatbot IA donne des réponses sourcées et correctes, ou dit explicitement "je ne sais pas"
- Le groupe numérique SFAR est convaincu par la démonstration
- Le projet est démontré au congrès SFAR septembre 2026
- Une publication scientifique est soumise (évaluation de la fiabilité du LLM sur les RFE)
- Le code est open-source, documenté, et réutilisable par d'autres (RFE ou éditeurs)

---

## Planning et jalons

### Objectif de lancement

**Septembre 2026** — Congrès annuel de la SFAR : démonstration d'une V1 fonctionnelle.

### Jalons clés

- **Phase 1 — Spécification et architecture** (février-mars 2026) : product brief, PRD, architecture technique
- **Phase 2 — Données structurées** (mars-avril 2026) : extraction et modélisation des données du PDF, validation de la base de données
- **Phase 3 — Webapp V1** (avril-juin 2026) : recherche instantanée, navigation par arborescence, API REST
- **Phase 4 — Module IA** (juin-août 2026) : chatbot avec recherche augmentée (MCP et/ou RAG), évaluation de la fiabilité
- **Phase 5 — Finalisation** (août-septembre 2026) : tests utilisateurs, corrections, préparation de la démo congrès, rédaction de l'article

---

## Risques et mitigation

- **Risque : Extraction des données du PDF trop complexe**
  - **Probabilité :** Moyenne
  - **Mitigation :** Commencer tôt par l'extraction ; utiliser des outils semi-automatiques (LLM pour aider à structurer les tableaux) ; valider manuellement chaque tableau

- **Risque : Temps de développement insuffisant (projet solo + activité clinique)**
  - **Probabilité :** Haute
  - **Mitigation :** Prioriser strictement (V1 minimale d'abord) ; utiliser des outils de productivité (Claude Code, spec-driven development) ; accepter de réduire le périmètre si nécessaire

- **Risque : Taux d'hallucination du LLM trop élevé pour un usage clinique**
  - **Probabilité :** Moyenne
  - **Mitigation :** C'est précisément l'objet de la recherche — mesurer et publier les résultats quel qu'ils soient ; privilégier l'approche "je ne sais pas" plutôt que de deviner ; comparer MCP vs RAG

- **Risque : Statut réglementaire flou (dispositif médical / aide à la décision)**
  - **Probabilité :** Faible à moyenne
  - **Mitigation :** Investiguer tôt (via `/bmad:research`) ; se positionner comme outil de recherche et de consultation, pas comme dispositif médical ; ajouter les disclaimers appropriés

- **Risque : Manque d'adhésion du groupe numérique SFAR**
  - **Probabilité :** Moyenne
  - **Mitigation :** Impliquer le groupe tôt ; montrer des résultats concrets régulièrement ; aligner le projet avec leurs discussions en cours sur la numérisation des RFE

- **Risque : Propriété intellectuelle des RFE**
  - **Probabilité :** Faible
  - **Mitigation :** Vérifier les conditions d'utilisation des RFE SFAR ; le projet vise à promouvoir les recommandations (pas à les commercialiser)

---

## Prochaines étapes

1. Créer le Product Requirements Document (PRD) — `/prd`
2. Investiguer le statut réglementaire (dispositif médical) — `/bmad:research`
3. Créer le design UX (optionnel) — `/bmad:create-ux-design`

---

**Ce document a été créé avec la méthode BMAD v6 — Phase 1 (Analyse)**

*Pour continuer : lancer `/workflow-status` pour voir la progression et le prochain workflow recommandé.*
