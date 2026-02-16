# Product Requirements Document : Antibioprophylaxie SFAR

**Date :** 2026-02-15
**Auteur :** Thomas Boulier
**Version :** 1.0
**Type de projet :** Application web (web-app)
**Niveau de projet :** 2
**Statut :** Brouillon

---

## Vue d'ensemble

Ce document définit les exigences fonctionnelles et non-fonctionnelles du projet Antibioprophylaxie SFAR. Il sert de référence pour ce qui sera développé et assure la traçabilité des exigences jusqu'à l'implémentation.

**Documents liés :**
- Product Brief : docs/product-brief-antibioprophylaxie-sfar-2026-02-15.md
- Recherche : docs/research-reglementaire-academique-technique-2026-02-15.md

---

## Résumé exécutif

Ce projet vise à créer une plateforme web unifiée et open-source en trois couches pour l'antibioprophylaxie chirurgicale, basée sur les RFE SFAR 2024 :

1. **Webapp responsive** : recherche instantanée et navigation par arborescence dans les recommandations
2. **Module IA / Chatbot** : questions en langage naturel avec sourçage systématique des réponses
3. **API REST + serveur MCP** : accès programmatique open-source aux recommandations

Le projet comporte une **dimension recherche** : comparer plusieurs niveaux de structuration des données (RAG sur PDF brut, RAG sur Excel, MCP sur API JSON) pour évaluer la fiabilité des réponses d'un LLM sur des recommandations médicales. L'objectif est une publication scientifique sur cette comparaison.

Un **chantier transverse** de structuration des données du PDF de 91 pages en formats exploitables est le prérequis à l'ensemble.

---

## Objectifs

### Objectifs business

1. **V1 complète avant le congrès SFAR (septembre 2026)** : webapp + module IA + API/MCP, le tout fonctionnel et démontrable
2. **Soumission d'une publication scientifique** : fin 2026, si le projet est mené à bien (comparaison multi-niveaux de structuration des données pour un LLM sur des recommandations médicales)

### Métriques de succès

- Temps de recherche d'une antibioprophylaxie : < 5 secondes (vs. plusieurs minutes avec le PDF)
- Taux d'hallucination du chatbot IA : à mesurer et publier (objectif : < 5% sur un jeu de questions de test)
- Couverture des données : 100% des interventions listées dans la RFE structurées en base
- Feedback qualitatif positif des collègues anesthésistes et du groupe numérique SFAR
- Au moins 1 démonstration au congrès SFAR septembre 2026

---

## Exigences fonctionnelles

Les exigences fonctionnelles (FRs) définissent **ce que** le système fait. Chaque exigence est priorisée selon la méthode MoSCoW :
- **Must Have** : indispensable pour le MVP, le projet échoue sans
- **Should Have** : important mais contournable
- **Could Have** : souhaitable, on saute si le temps manque

---

### FR-001 : Extraction et modélisation des données du PDF

**Priorité :** Must Have

**Description :**
Les tableaux du PDF RFE antibioprophylaxie 2024 (91 pages) sont extraits et structurés en base de données, couvrant : spécialité chirurgicale, type d'intervention, antibiotique recommandé, posologie, timing d'administration, réinjection, alternative en cas d'allergie.

**Critères d'acceptation :**
- [ ] 100% des interventions listées dans la RFE sont présentes en base
- [ ] Chaque entrée contient : molécule, posologie, timing, réinjection, alternative allergie
- [ ] Chaque entrée est liée à sa source exacte (page, tableau du PDF)
- [ ] Les données sont validées manuellement par un clinicien

**Dépendances :** Aucune

---

### FR-002 : Recommandations générales structurées

**Priorité :** Should Have

**Description :**
Les recommandations narratives transverses (timing général, patients obèses, insuffisance rénale, durée de prolongation, etc.) sont aussi structurées et accessibles.

**Critères d'acceptation :**
- [ ] Les recommandations générales sont stockées et interrogeables
- [ ] Lien vers la source exacte dans le PDF

**Dépendances :** FR-001

---

### FR-003 : Recherche instantanée (type-ahead)

**Priorité :** Must Have

**Description :**
Une barre de recherche centrale permet de taper des mots-clés. Les résultats se mettent à jour en temps réel à chaque frappe (type-ahead), affichant les interventions correspondantes avec leur protocole.

**Critères d'acceptation :**
- [ ] Résultats visibles en < 200ms après chaque frappe
- [ ] Recherche textuelle sur les noms d'interventions et spécialités
- [ ] Résultats pertinents dès 2-3 caractères saisis

**Dépendances :** FR-001

---

### FR-004 : Navigation par arborescence

**Priorité :** Must Have

**Description :**
Navigation alternative par spécialité chirurgicale → type d'intervention → protocole. Permet de parcourir sans connaître le nom exact.

**Critères d'acceptation :**
- [ ] Arborescence complète couvrant toutes les spécialités de la RFE
- [ ] Navigation en 2-3 clics maximum jusqu'au protocole
- [ ] Compatible mobile (menu accordéon ou similaire)

**Dépendances :** FR-001

---

### FR-005 : Affichage complet du protocole

**Priorité :** Must Have

**Description :**
Pour chaque intervention, affichage clair et complet du protocole : molécule, posologie, timing, réinjection, alternative allergie, et lien vers la source (page PDF).

**Critères d'acceptation :**
- [ ] Toutes les informations du protocole visibles sans scroll excessif
- [ ] Source exacte (page, tableau) affichée et cliquable
- [ ] Lisible sur écran de téléphone et sur écran d'ordinateur

**Dépendances :** FR-001

---

### FR-006 : Disclaimer médical

**Priorité :** Must Have

**Description :**
Un disclaimer clair est affiché, indiquant que l'outil est un support de consultation et de recherche, ne se substituant pas au jugement clinique.

**Critères d'acceptation :**
- [ ] Disclaimer visible au premier accès
- [ ] Accessible depuis n'importe quelle page (footer ou lien permanent)

**Dépendances :** Aucune

---

### FR-007 : Chatbot en langage naturel

**Priorité :** Must Have

**Description :**
Un chatbot intégré à la webapp permet de poser des questions en langage naturel (ex : "je mets quoi sur une PTH ?"). Le chatbot répond en s'appuyant sur les données structurées.

**Critères d'acceptation :**
- [ ] Le chatbot comprend les questions en français, y compris le jargon médical courant
- [ ] Temps de réponse < 10 secondes
- [ ] Interface de chat intégrée à la webapp (pas un outil externe)

**Dépendances :** FR-001

---

### FR-008 : Sourçage systématique des réponses IA

**Priorité :** Must Have

**Description :**
Chaque réponse du chatbot cite la source exacte (page PDF, tableau) dont elle est tirée. Si le chatbot ne trouve pas la réponse, il le dit explicitement ("je ne sais pas") plutôt que d'inventer.

**Critères d'acceptation :**
- [ ] 100% des réponses incluent une référence à la source
- [ ] Le chatbot dit "je ne sais pas" quand la question est hors périmètre des RFE
- [ ] Pas de fabrication de citations ou de dosages

**Dépendances :** FR-007

---

### FR-009 : Comparaison multi-niveaux de structuration (volet recherche)

**Priorité :** Must Have

**Description :**
Le module IA implémente trois niveaux progressifs d'accès aux données pour le volet publication :
1. RAG sur le PDF brut (effort minimal de structuration)
2. RAG sur un fichier Excel extrait des tableaux (effort intermédiaire)
3. MCP sur API avec données JSON structurées (effort maximal)

La question de recherche est : quel niveau de structuration faut-il pour obtenir des réponses fiables d'un LLM sur des recommandations médicales ?

**Critères d'acceptation :**
- [ ] Les trois approches sont implémentées et fonctionnelles
- [ ] Un jeu de questions standardisé (30-50 questions) est défini
- [ ] Les résultats de chaque approche sont enregistrés pour analyse comparative

**Dépendances :** FR-001, FR-007

---

### FR-010 : API REST en lecture seule

**Priorité :** Must Have

**Description :**
Une API REST publique (GET uniquement) permet d'interroger les recommandations de manière programmatique. Pas d'authentification requise.

**Critères d'acceptation :**
- [ ] Endpoints pour recherche par mot-clé, par spécialité, par intervention
- [ ] Réponses au format JSON, documentées
- [ ] Accessible sans authentification

**Note d'architecture :** L'architecture doit anticiper l'extensibilité vers CRUD pour la V2 (protocoles locaux, adaptation à l'écologie bactérienne locale).

**Dépendances :** FR-001

---

### FR-011 : Serveur MCP

**Priorité :** Must Have

**Description :**
Un serveur MCP expose les recommandations structurées pour intégration avec les LLMs. Les outils (tools) MCP permettent d'interroger les données de la même manière que l'API REST.

**Critères d'acceptation :**
- [ ] Serveur MCP fonctionnel et connectable depuis un client MCP standard
- [ ] Outils définis pour recherche par intervention, par spécialité
- [ ] Documentation d'intégration

**Dépendances :** FR-001

---

### FR-012 : Documentation et open-source

**Priorité :** Must Have

**Description :**
Le code est publié sur GitHub, avec documentation technique (installation, contribution) et documentation utilisateur (API, MCP).

**Critères d'acceptation :**
- [ ] Repository GitHub public
- [ ] README avec instructions d'installation et d'utilisation
- [ ] Documentation API (OpenAPI/Swagger ou équivalent)

**Dépendances :** Aucune

---

## Exigences non-fonctionnelles

Les exigences non-fonctionnelles (NFRs) définissent **comment** le système se comporte — qualité, performance, contraintes.

---

### NFR-001 : Temps de réponse webapp

**Priorité :** Must Have

**Description :**
La recherche textuelle et la navigation par arborescence répondent en < 200ms. Le chargement initial de la page est < 2 secondes sur une connexion 4G.

**Critère :** Temps mesuré sur un téléphone mobile en 4G

**Justification :** Au bloc opératoire, l'outil ne sera utilisé que s'il est plus rapide que le PDF.

---

### NFR-002 : Temps de réponse chatbot IA

**Priorité :** Should Have

**Description :**
Le chatbot répond en < 10 secondes. Un indicateur de chargement est affiché pendant le traitement.

**Critère :** 95% des réponses en < 10s

**Justification :** L'IA est plus lente par nature, mais un feedback visuel rend l'attente acceptable.

---

### NFR-003 : Pas de données de santé

**Priorité :** Must Have

**Description :**
L'application ne collecte, ne stocke et ne traite aucune donnée de santé personnelle. Seules les recommandations publiques de la SFAR sont hébergées.

**Critère :** Aucun champ de saisie de données patient ; aucune donnée personnelle en base

**Justification :** Pas de nécessité d'hébergement HDS, pas de RGPD santé. Simplifie considérablement l'architecture et le réglementaire.

---

### NFR-004 : Pas d'authentification (V1)

**Priorité :** Must Have

**Description :**
L'outil est accessible sans compte, sans login, sans friction. Accès direct à la recherche.

**Critère :** Aucune page de connexion ; accès immédiat

**Justification :** Les anesthésistes au bloc ne créeront pas de compte. Zéro friction = adoption.

---

### NFR-005 : Disponibilité standard

**Priorité :** Should Have

**Description :**
L'application vise 99% de disponibilité (~3,5 jours de downtime toléré par an). Pas d'engagement formel de disponibilité — ce n'est pas un outil critique, le PDF existe toujours en secours.

**Critère :** 99% d'uptime mesuré mensuellement

**Justification :** Projet solo, budget minimal. Un hébergement standard suffit.

---

### NFR-006 : Design responsive

**Priorité :** Must Have

**Description :**
L'interface s'affiche correctement sur ordinateur (station d'anesthésie) et sur téléphone. Fonctionne sur les navigateurs modernes (Chrome, Safari, Firefox, Edge — 2 dernières versions).

**Critère :** Interface testée et fonctionnelle de 375px (téléphone) à 1920px (écran bureau)

**Justification :** L'usage se fait autant sur le PC de la station d'anesthésie que sur le téléphone.

---

### NFR-007 : Accessibilité de base

**Priorité :** Could Have

**Description :**
Respect des bonnes pratiques d'accessibilité de base (contraste suffisant, navigation au clavier, balises sémantiques). Pas de certification WCAG complète visée.

**Critère :** Score Lighthouse accessibilité > 80

**Justification :** Les bonnes pratiques améliorent l'UX pour tous.

---

### NFR-008 : Code open-source et documenté

**Priorité :** Must Have

**Description :**
Le code est propre, documenté, et publiable sur GitHub. Un développeur externe doit pouvoir installer et faire tourner le projet localement en suivant le README.

**Critère :** Installation fonctionnelle en < 15 minutes en suivant la documentation

**Justification :** Open-source = vitrine. Si le groupe numérique SFAR ou des contributeurs veulent participer, le projet doit être abordable.

---

### NFR-009 : Mise à jour des données

**Priorité :** Should Have

**Description :**
La mise à jour des recommandations (si une nouvelle RFE sort) doit être réalisable sans refonte du code. Idéalement, modification des données en base ou remplacement d'un fichier source.

**Critère :** Mise à jour des données sans redéploiement du code applicatif

**Justification :** Les RFE sont mises à jour tous les 5-10 ans, mais la capacité de mise à jour est un argument de crédibilité.

---

### NFR-010 : Hébergement à coût minimal

**Priorité :** Must Have

**Description :**
L'hébergement et les coûts d'API LLM doivent rester minimaux (< 20€/mois en fonctionnement normal). Privilégier les tiers gratuits et les solutions open-source.

**Critère :** Coût mensuel total < 20€ hors pics de démo

**Justification :** Pas de budget dédié. Le projet doit être soutenable par un développeur solo sans financement.

---

## Epics

Les epics sont des regroupements logiques de fonctionnalités qui seront découpés en user stories lors du sprint planning (Phase 4).

---

### EPIC-001 : Structuration des données RFE

**Description :**
Extraire, modéliser et valider les données du PDF RFE antibioprophylaxie 2024 en formats exploitables (Excel, JSON/base de données).

**Exigences fonctionnelles :** FR-001, FR-002

**Estimation :** 3-5 stories

**Priorité :** Must Have

**Valeur business :** C'est le socle de tout le projet. Sans données structurées, pas de webapp, pas d'IA, pas d'API. C'est aussi le premier livrable du volet recherche (les différents niveaux de structuration : PDF brut → Excel → JSON).

---

### EPIC-002 : Webapp de consultation + API REST

**Description :**
Interface web responsive permettant la recherche instantanée et la navigation par arborescence dans les recommandations, avec affichage complet des protocoles, disclaimer médical, API REST backend et documentation open-source.

**Exigences fonctionnelles :** FR-003, FR-004, FR-005, FR-006, FR-010, FR-012

**Estimation :** 5-8 stories

**Priorité :** Must Have

**Valeur business :** L'outil clinique principal — ce que les anesthésistes utiliseront au quotidien. C'est le livrable le plus visible pour la démo au congrès SFAR. L'API REST est le backend naturel de la webapp.

---

### EPIC-003 : Module IA / Chatbot + serveur MCP

**Description :**
Chatbot intégré à la webapp, capable de répondre aux questions en langage naturel avec sourçage systématique. Implémente les trois niveaux de structuration (RAG PDF, RAG Excel, MCP API) pour le volet recherche comparatif. Le serveur MCP est une des approches d'accès aux données.

**Exigences fonctionnelles :** FR-007, FR-008, FR-009, FR-011

**Estimation :** 4-7 stories

**Priorité :** Must Have

**Valeur business :** Le cœur du volet recherche et la démonstration la plus marquante pour le congrès. La comparaison multi-niveaux est l'angle de publication original.

---

## User stories (haut niveau)

Les user stories détaillées seront créées lors du sprint planning (Phase 4).

---

## Personas

### Anesthésiste-réanimateur (utilisateur principal)

Praticien hospitalier, interne ou IADE, au bloc opératoire (sur téléphone ou PC de la station d'anesthésie) ou en consultation pré-anesthésique. Peu technophile en général, a besoin d'un outil qui fonctionne immédiatement, sans friction.

### Membre du groupe numérique SFAR (utilisateur secondaire)

Interlocuteur technique, early adopter, relais institutionnel. Plus à l'aise avec la technologie, intéressé par la démarche de numérisation des RFE.

### Éditeur logiciel / Développeur (utilisateur secondaire)

Consommateur de l'API/MCP open-source pour intégrer les recommandations officielles dans ses outils (DPI, systèmes d'aide à la décision, assistants IA).

---

## Flux utilisateurs clés

### Flux 1 : Recherche rapide au bloc

1. L'anesthésiste ouvre l'app sur son téléphone ou le PC
2. Tape quelques lettres dans la barre de recherche (ex : "hanche")
3. Les résultats apparaissent en temps réel
4. Clique sur l'intervention correspondante
5. Voit le protocole complet (molécule, posologie, timing, alternative allergie)

### Flux 2 : Navigation par spécialité

1. L'anesthésiste ouvre l'app
2. Navigue dans l'arborescence : Orthopédie → Prothèse totale de hanche
3. Voit le protocole complet

### Flux 3 : Question en langage naturel

1. L'anesthésiste ouvre le chatbot
2. Tape : "je mets quoi sur une PTH ?"
3. Le chatbot répond avec le protocole et la source exacte
4. Si hors périmètre : "je ne sais pas"

---

## Dépendances

### Dépendances internes

- Le PDF RFE antibioprophylaxie SFAR 2024 (91 pages) — source unique des données
- L'extraction et la structuration des données (EPIC-001) est un prérequis pour tout le reste

### Dépendances externes

- Un fournisseur d'API LLM (pour le module chatbot) — à choisir en Phase 3 (architecture)
- Un hébergement web (Vercel, Railway, ou équivalent) — à choisir en Phase 3

---

## Hypothèses

- Les données des RFE SFAR sont publiques et librement réutilisables (recommandations de société savante)
- Les utilisateurs ont accès à un navigateur web moderne
- Un LLM peut répondre correctement aux questions d'antibioprophylaxie si on lui fournit des données structurées — hypothèse à valider (c'est le cœur du volet recherche)
- Le statut réglementaire (dispositif médical / logiciel d'aide à la décision) ne bloque pas un projet de recherche open-source (cf. rapport de recherche)

---

## Hors périmètre (V1)

- **Application mobile native** (iOS/Android) — un autre projet est en cours côté SFAR
- **Gestion des utilisateurs / authentification** — l'outil doit être accessible sans compte
- **Autres RFE** que l'antibioprophylaxie — cette RFE est le point de départ
- **Hébergement certifié HDS** — pas de données de santé hébergées
- **Intégration directe avec les DPI** — c'est l'API libre d'accès qui sert de point d'intégration
- **Protocoles locaux** — prévu en V2, l'architecture anticipe l'extensibilité CRUD

---

## Questions ouvertes

- Propriété intellectuelle des RFE SFAR : vérifier les conditions d'utilisation exactes avec la SFAR
- Choix du/des modèles LLM pour le chatbot et l'étude comparative (à définir en Phase 3)
- Choix de la stack technique (à définir en Phase 3 — architecture)

---

## Parties prenantes

- **Thomas Boulier (Porteur de projet / Développeur)** — Influence haute. Anesthésiste-réanimateur et ingénieur/chercheur. Concepteur, développeur principal, et premier utilisateur.
- **Groupe Numérique SFAR** — Influence haute. Cible de démonstration prioritaire, interlocuteurs sur la numérisation des RFE.
- **SFAR (Comité des référentiels / CA)** — Influence moyenne (indirecte). Accessible via le groupe numérique si le projet convainc.
- **Collègues anesthésistes du service** — Influence moyenne. Utilisateurs finaux, source de retours terrain.

---

## Historique des révisions

| Version | Date | Auteur | Modifications |
|---------|------|--------|---------------|
| 1.0 | 2026-02-15 | Thomas Boulier | PRD initial |

---

## Prochaines étapes

### Phase 3 : Architecture

Lancer `/architecture` pour concevoir l'architecture technique en réponse à ces exigences :
- Stack technique
- Modèle de données
- Architecture des API
- Choix du/des LLMs
- Infrastructure d'hébergement

### Phase 4 : Sprint Planning

Après l'architecture, lancer `/sprint-planning` pour :
- Découper les epics en user stories détaillées
- Estimer la complexité
- Planifier les sprints
- Commencer le développement

---

## Annexe A : Matrice de traçabilité

| Epic | Nom | Exigences fonctionnelles | Stories estimées |
|------|-----|--------------------------|-----------------|
| EPIC-001 | Structuration des données RFE | FR-001, FR-002 | 3-5 |
| EPIC-002 | Webapp + API REST | FR-003, FR-004, FR-005, FR-006, FR-010, FR-012 | 5-8 |
| EPIC-003 | Module IA + MCP | FR-007, FR-008, FR-009, FR-011 | 4-7 |

---

## Annexe B : Résumé des priorités

### Exigences fonctionnelles (12 FRs)
- **Must Have :** 11 (FR-001, FR-003 à FR-012)
- **Should Have :** 1 (FR-002)
- **Could Have :** 0

### Exigences non-fonctionnelles (10 NFRs)
- **Must Have :** 5 (NFR-001, NFR-003, NFR-004, NFR-006, NFR-008, NFR-010)
- **Should Have :** 3 (NFR-002, NFR-005, NFR-009)
- **Could Have :** 1 (NFR-007)

### Epics (3)
- Toutes Must Have
- **Total stories estimées : 12-20**
- **Ordre de développement :** EPIC-001 → EPIC-002 → EPIC-003

---

**Ce document a été créé avec la méthode BMAD v6 — Phase 2 (Planification)**

*Pour continuer : lancer `/workflow-status` pour voir la progression et le prochain workflow recommandé.*
