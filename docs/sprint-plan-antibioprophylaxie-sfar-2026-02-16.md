# Sprint Plan : Antibioprophylaxie SFAR

**Date :** 2026-02-16
**Scrum Master :** Thomas Boulier (assisté par Claude)
**Niveau de projet :** 2

**Documents de référence :**
- PRD : docs/prd-antibioprophylaxie-sfar-2026-02-15.md
- Architecture : docs/architecture-antibioprophylaxie-sfar-2026-02-16.md
- UX Design : docs/ux-design-antibioprophylaxie-sfar-2026-02-16.md

---

## Résumé

| Métrique | Valeur |
|----------|--------|
| Stories | 19 |
| Points totaux | 78 |
| Milestones | 3 |
| Rythme | Pas de sprints chronométrés — story par story, au rythme du porteur de projet |

**Mode opératoire :** Claude Code fait le développement, Thomas supervise et valide. Tout est tracé sur GitHub (issues, milestones, project board) via `gh` CLI.

**Objectif :** V1 complète avant le congrès SFAR (septembre 2026).

---

## Inventaire des stories

### Milestone 1 : Structuration des données (EPIC-001)

> **Objectif :** Extraire les données du PDF RFE 2024 en formats exploitables (JSON + Excel), validés cliniquement.
>
> **Livrable :** `data/rfe.json` + `data/rfe.xlsx` complets et validés.
>
> **Approche :** Itérative — on commence par un tableau pilote (une spécialité), on se met d'accord sur le format, puis on itère sur les autres.

---

#### S-001 : Init projet — repo GitHub, structure, CI, CONTRIBUTING.md

**Epic :** EPIC-001
**Priorité :** Must Have
**Points :** 3

**User Story :**
En tant que développeur (humain ou IA),
je veux un repo GitHub initialisé avec la structure du projet, la CI et un guide de contribution,
afin de pouvoir contribuer efficacement dès le départ.

**Critères d'acceptation :**
- [ ] Repo GitHub public créé avec `gh`
- [ ] Structure de dossiers conforme à l'architecture (`app/`, `data/`, `tests/`, etc.)
- [ ] `pyproject.toml` avec les dépendances (FastAPI, uvicorn, pytest, ruff, etc.)
- [ ] `CONTRIBUTING.md` universel (humains + IAs) : conventions de code, git flow, conventional commits, principes (KISS, YAGNI), comment lancer le projet
- [ ] `CLAUDE.md` avec instructions spécifiques Claude Code (réfère au CONTRIBUTING.md)
- [ ] `.github/workflows/ci.yml` : lint (ruff) + tests (pytest) sur push/PR
- [ ] `README.md` minimal (description du projet, statut, liens vers la doc)
- [ ] Milestones et labels créés sur GitHub avec `gh`
- [ ] Issues créées pour toutes les stories avec `gh`

**Notes techniques :**
- Utiliser `uv` comme gestionnaire de paquets
- Pre-commit hooks : ruff check + ruff format
- Labels GitHub : `epic:data`, `epic:webapp`, `epic:ia`, `priority:must`, `priority:should`, `priority:could`

**Dépendances :** Aucune

---

#### S-002 : Extraire le 1er tableau (pilote) en JSON

**Epic :** EPIC-001
**Priorité :** Must Have
**Points :** 5

**User Story :**
En tant que développeur,
je veux extraire les données d'un premier tableau du PDF RFE (une spécialité) en JSON structuré,
afin de valider le format de données avec le clinicien avant d'itérer sur les autres.

**Critères d'acceptation :**
- [ ] Un fichier `data/rfe.json` avec la structure définie dans l'architecture (modèle Intervention, Protocole, AlternativeAllergie)
- [ ] Au moins une spécialité complète (suggestion : Orthopédie — tableau bien structuré)
- [ ] Chaque intervention contient : molécule, posologie, timing, réinjection, durée, alternative allergie, source (page + tableau)
- [ ] Les cas "pas d'ABP recommandée" sont gérés
- [ ] Validation Pydantic du JSON (script de validation)

**Notes techniques :**
- Extraction manuelle ou semi-automatique depuis le PDF (Claude peut lire le PDF et extraire)
- Le format JSON est celui défini dans l'architecture (section 5)
- Créer un script `scripts/validate_data.py` qui charge le JSON et valide avec Pydantic

**Dépendances :** S-001

---

#### S-003 : Créer l'export Excel du 1er tableau

**Epic :** EPIC-001
**Priorité :** Must Have
**Points :** 2

**User Story :**
En tant que chercheur,
je veux un export Excel des données du premier tableau,
afin de disposer du niveau 2 de structuration pour l'étude comparative RAG.

**Critères d'acceptation :**
- [ ] Fichier `data/rfe.xlsx` généré à partir du JSON
- [ ] Une feuille par spécialité, colonnes : intervention, molécule, posologie, timing, réinjection, durée, allergie, source
- [ ] Script reproductible (`scripts/json_to_excel.py`)

**Notes techniques :**
- Utiliser openpyxl pour la génération
- Le format Excel doit ressembler aux tableaux du PDF original (pour le niveau 2 du RAG)

**Dépendances :** S-002

---

#### S-004 : Extraire les tableaux restants en JSON

**Epic :** EPIC-001
**Priorité :** Must Have
**Points :** 5

**User Story :**
En tant que développeur,
je veux extraire toutes les spécialités restantes du PDF en JSON,
afin d'avoir une couverture à 100% des interventions de la RFE.

**Critères d'acceptation :**
- [ ] Toutes les spécialités de la RFE sont présentes dans `data/rfe.json`
- [ ] 100% des interventions listées dans les tableaux du PDF
- [ ] Validation Pydantic réussie sur l'ensemble
- [ ] Validation clinique par Thomas (spécialité par spécialité)

**Notes techniques :**
- Itérer spécialité par spécialité
- Le format est stabilisé depuis S-002
- Thomas valide au fur et à mesure

**Dépendances :** S-002 (format validé)

---

#### S-005 : Compléter l'export Excel pour toutes les spécialités

**Epic :** EPIC-001
**Priorité :** Must Have
**Points :** 2

**User Story :**
En tant que chercheur,
je veux l'export Excel complet de toutes les spécialités,
afin de disposer du dataset complet pour le RAG niveau 2.

**Critères d'acceptation :**
- [ ] `data/rfe.xlsx` contient toutes les spécialités
- [ ] Généré automatiquement par `scripts/json_to_excel.py`

**Dépendances :** S-004

---

#### S-006 : Structurer les recommandations générales

**Epic :** EPIC-001
**Priorité :** Should Have
**Points :** 3

**User Story :**
En tant qu'anesthésiste,
je veux accéder aux recommandations générales transverses (timing, obésité, insuffisance rénale, etc.),
afin de compléter l'information des protocoles par intervention.

**Critères d'acceptation :**
- [ ] Section `recommandations_generales` dans `data/rfe.json`
- [ ] Au minimum : timing d'administration, patient obèse, insuffisance rénale, durée de prolongation
- [ ] Lien source (page PDF) pour chaque recommandation

**Dépendances :** S-002 (format JSON stabilisé)

---

### Milestone 2 : Webapp + API REST (EPIC-002)

> **Objectif :** Webapp responsive fonctionnelle avec recherche instantanée, navigation par arborescence, et API REST publique.
>
> **Livrable :** Application déployée sur le NAS, consultable par les collègues.

---

#### S-007 : Backend FastAPI — modèles Pydantic, chargement JSON, config

**Epic :** EPIC-002
**Priorité :** Must Have
**Points :** 3

**User Story :**
En tant que développeur,
je veux le squelette FastAPI fonctionnel qui charge les données JSON au démarrage,
afin de servir de base à l'API et aux pages web.

**Critères d'acceptation :**
- [ ] `app/main.py` démarre avec Uvicorn
- [ ] Modèles Pydantic dans `app/data/models.py` (conformes à l'architecture)
- [ ] `app/data/loader.py` charge `data/rfe.json` en mémoire au démarrage
- [ ] Endpoint `/api/v1/health` fonctionnel
- [ ] Tests unitaires pour le loader et les modèles
- [ ] Configuration via variables d'environnement (`.env`)

**Dépendances :** S-002 (au moins les données pilote)

---

#### S-008 : API REST — endpoints interventions, spécialités

**Epic :** EPIC-002
**Priorité :** Must Have
**Points :** 5

**User Story :**
En tant que développeur externe,
je veux une API REST documentée pour interroger les recommandations,
afin d'intégrer les données dans mes propres outils.

**Critères d'acceptation :**
- [ ] `GET /api/v1/interventions` — liste (+ filtre `?q=` et `?specialite=`)
- [ ] `GET /api/v1/interventions/{id}` — détail
- [ ] `GET /api/v1/specialites` — liste avec nombre d'interventions
- [ ] `GET /api/v1/specialites/{id}` — détail avec interventions
- [ ] `GET /api/v1/recommandations` — recommandations générales
- [ ] Documentation Swagger auto-générée sur `/docs`
- [ ] Tests d'intégration pour chaque endpoint
- [ ] Réponses JSON conformes aux schémas Pydantic

**Dépendances :** S-007

---

#### S-009 : Recherche fuzzy type-ahead

**Epic :** EPIC-002
**Priorité :** Must Have
**Points :** 5

**User Story :**
En tant qu'anesthésiste,
je veux taper quelques lettres et voir les résultats apparaître instantanément,
afin de trouver le bon protocole en moins de 5 secondes.

**Critères d'acceptation :**
- [ ] Recherche fuzzy (tolère les fautes de frappe) dans `app/data/search.py`
- [ ] Résultats < 200ms (NFR-001)
- [ ] Recherche sur : nom d'intervention, spécialité, molécule
- [ ] Endpoint HTMX `GET /htmx/search?q=xxx` retournant un fragment HTML
- [ ] Résultats pertinents dès 2-3 caractères
- [ ] Tests unitaires sur la recherche (cas normaux + fuzzy + aucun résultat)

**Notes techniques :**
- Utiliser `rapidfuzz` ou `difflib` pour le fuzzy matching
- Debounce côté client (HTMX `hx-trigger="keyup changed delay:100ms"`)

**Dépendances :** S-007

---

#### S-010 : Layout de base — templates Jinja2, header, footer, CSS tokens

**Epic :** EPIC-002
**Priorité :** Must Have
**Points :** 3

**User Story :**
En tant qu'utilisateur,
je veux une interface sobre et professionnelle, cohérente sur tous les écrans,
afin de consulter l'outil avec confiance.

**Critères d'acceptation :**
- [ ] Template `base.html` : header, main, footer (disclaimer)
- [ ] CSS : design tokens (couleurs SFAR, typographie, espacement) en variables CSS
- [ ] HTMX inclus (`htmx.min.js`)
- [ ] Responsive : mobile-first, breakpoints 768px / 1024px
- [ ] Footer disclaimer permanent : "Outil de consultation · Ne remplace pas le jugement clinique · Source : RFE SFAR 2024"
- [ ] Navigation : logo + liens (Rechercher, Parcourir, Chat)

**Notes techniques :**
- Couleurs SFAR : `#273466` (primaire), `#0cc9bf` (accent), `#f15c40` (warning/allergie)
- Cf. design tokens dans le document UX

**Dépendances :** Aucune (peut être fait en parallèle de S-007)

---

#### S-011 : Écran d'accueil — recherche + grille spécialités

**Epic :** EPIC-002
**Priorité :** Must Have
**Points :** 5

**User Story :**
En tant qu'anesthésiste,
je veux arriver sur l'app et pouvoir immédiatement chercher ou parcourir les spécialités,
afin d'accéder au protocole le plus vite possible.

**Critères d'acceptation :**
- [ ] Barre de recherche en autofocus (héros de la page)
- [ ] Résultats type-ahead sous la barre (overlay HTMX)
- [ ] Grille des spécialités visible sous la recherche (cartes cliquables)
- [ ] Desktop : grille 4 colonnes ; Mobile : liste verticale
- [ ] Navigation clavier : flèches dans les résultats + Enter pour sélectionner

**Dépendances :** S-009, S-010

---

#### S-012 : Écran protocole — détail intervention

**Epic :** EPIC-002
**Priorité :** Must Have
**Points :** 3

**User Story :**
En tant qu'anesthésiste au bloc,
je veux voir le protocole complet d'une intervention de manière claire et scannable,
afin de confirmer la molécule et la posologie en 2 secondes.

**Critères d'acceptation :**
- [ ] URL propre : `/protocole/{id}`
- [ ] Composant ProtocolCard : molécule en gros, tableau label/valeur
- [ ] Bloc allergie visuellement distinct (fond orangé, bordure warning)
- [ ] Source cliquable (page PDF, tableau)
- [ ] Breadcrumb : Spécialité > Intervention
- [ ] Responsive : blocs côte à côte (desktop) / empilés (mobile)

**Dépendances :** S-007, S-010

---

#### S-013 : Écran spécialité — liste + toggle "tout déplier"

**Epic :** EPIC-002
**Priorité :** Must Have
**Points :** 3

**User Story :**
En tant qu'anesthésiste,
je veux voir toutes les interventions d'une spécialité avec leur aperçu,
afin de trouver le bon protocole même sans connaître le nom exact.

**Critères d'acceptation :**
- [ ] URL propre : `/specialite/{id}`
- [ ] Liste des interventions avec aperçu (molécule principale)
- [ ] Bouton "Tout déplier" / "Tout replier" : affiche les protocoles complets inline
- [ ] Filtre local optionnel
- [ ] Chaque intervention cliquable → écran protocole

**Dépendances :** S-007, S-010, S-012 (réutilise ProtocolCard)

---

#### S-014 : Dockerfile + déploiement NAS

**Epic :** EPIC-002
**Priorité :** Must Have
**Points :** 3

**User Story :**
En tant que porteur de projet,
je veux déployer l'app sur mon NAS via Docker,
afin de la tester et la montrer à mes collègues sans coût d'hébergement.

**Critères d'acceptation :**
- [ ] `Dockerfile` multi-stage (build + runtime)
- [ ] `docker-compose.yml` pour le déploiement local/NAS
- [ ] L'app démarre et fonctionne dans le conteneur
- [ ] Documentation dans le README : comment déployer sur un NAS
- [ ] Health check Docker configuré

**Notes techniques :**
- Image de base : `python:3.12-slim`
- Port exposé : 8000
- Variables d'env pour la config (port, log level, etc.)

**Dépendances :** S-007 + au moins un écran fonctionnel

---

### Milestone 3 : Module IA + MCP (EPIC-003)

> **Objectif :** Chatbot IA intégré avec sourçage, serveur MCP, et infrastructure pour l'étude comparative.
>
> **Livrable :** Chatbot fonctionnel + serveur MCP + données d'évaluation pour la publication.

---

#### S-015 : Interface chatbot — écran chat, bulles, HTMX

**Epic :** EPIC-003
**Priorité :** Must Have
**Points :** 5

**User Story :**
En tant qu'anesthésiste,
je veux poser une question en langage naturel et recevoir une réponse formatée,
afin d'obtenir un protocole sans connaître le nom exact de l'intervention.

**Critères d'acceptation :**
- [ ] Écran chat accessible via bouton 💬
- [ ] Bulles user (droite) et IA (gauche)
- [ ] Input en bas, toujours visible
- [ ] Indicateur de chargement pendant la réponse
- [ ] Mobile : plein écran ; Desktop : à définir (plein écran ou panneau latéral)
- [ ] Message d'accueil avec exemples de questions
- [ ] Historique de conversation (session navigateur)

**Dépendances :** S-010

---

#### S-016 : Intégration LLM niveau 3 (tool use) — réponses sourcées

**Epic :** EPIC-003
**Priorité :** Must Have
**Points :** 8

**User Story :**
En tant qu'anesthésiste,
je veux que le chatbot me réponde avec le bon protocole ET cite sa source exacte,
afin d'avoir confiance dans la réponse.

**Critères d'acceptation :**
- [ ] Appel API Claude avec tool use (les outils de recherche dans les données)
- [ ] System prompt structuré (cf. architecture section 8)
- [ ] 100% des réponses incluent une source (page, tableau)
- [ ] "Je ne sais pas" si hors périmètre (pas d'hallucination)
- [ ] Réponse formatée avec carte protocole intégrée (réutilise le composant)
- [ ] Streaming SSE pour affichage progressif
- [ ] Rate limiting : 10 req/min par IP
- [ ] Temps de réponse < 10s (NFR-002)
- [ ] Tests : questions in-scope, hors-scope, ambiguës

**Notes techniques :**
- Utiliser le SDK Anthropic Python
- Les tools correspondent aux fonctions de `app/data/search.py`
- Clé API en variable d'environnement

**Dépendances :** S-008, S-015

---

#### S-017 : Serveur MCP

**Epic :** EPIC-003
**Priorité :** Must Have
**Points :** 5

**User Story :**
En tant que développeur ou utilisateur de Claude Desktop,
je veux connecter un client MCP au serveur pour interroger les recommandations,
afin d'intégrer les données dans mon workflow IA.

**Critères d'acceptation :**
- [ ] Serveur MCP fonctionnel (`mcp_server/server.py`)
- [ ] Outils : `search_interventions`, `get_intervention`, `list_specialites`, `get_specialite`, `get_recommandations_generales`
- [ ] Connectable depuis Claude Desktop
- [ ] Documentation d'intégration dans le README
- [ ] Tests unitaires des outils MCP

**Notes techniques :**
- SDK : `mcp` (Python SDK officiel Anthropic)
- Processus séparé, lit les mêmes fichiers `data/rfe.json`

**Dépendances :** S-007

---

#### S-018 : RAG niveau 1 (PDF) + niveau 2 (Excel)

**Epic :** EPIC-003
**Priorité :** Must Have
**Points :** 5

**User Story :**
En tant que chercheur,
je veux implémenter les approches RAG sur PDF brut et Excel,
afin de comparer leur fiabilité avec l'approche MCP structurée.

**Critères d'acceptation :**
- [ ] RAG niveau 1 : PDF → chunking → embeddings → ChromaDB → contexte → LLM
- [ ] RAG niveau 2 : Excel → chunking → embeddings → ChromaDB → contexte → LLM
- [ ] Les deux approches répondent aux mêmes questions que le niveau 3
- [ ] Résultats enregistrés pour comparaison

**Notes techniques :**
- LangChain ou LlamaIndex pour le pipeline RAG
- ChromaDB embarqué (pas de service externe)
- Les embeddings peuvent utiliser l'API Anthropic ou un modèle local

**Dépendances :** S-005 (Excel complet), S-016 (niveau 3 fonctionnel)

---

#### S-019 : Jeu de questions + évaluation comparative

**Epic :** EPIC-003
**Priorité :** Must Have
**Points :** 5

**User Story :**
En tant que chercheur,
je veux évaluer les 3 niveaux de structuration sur un jeu de questions standardisé,
afin de mesurer l'impact de la structuration sur la fiabilité des réponses.

**Critères d'acceptation :**
- [ ] Jeu de 30-50 questions standardisé dans `research/questions.json`
- [ ] Script d'évaluation automatique (`research/evaluate.py`)
- [ ] Résultats par niveau : taux de réponses correctes, hallucinations, "je ne sais pas"
- [ ] Export des résultats en CSV/JSON dans `research/results/`
- [ ] Les réponses de référence (ground truth) sont validées par un clinicien

**Notes techniques :**
- Questions : mix de questions directes ("ATB pour PTH ?"), ambiguës ("je mets quoi pour la hanche ?"), hors périmètre ("dosage de Doliprane ?")
- Évaluation : comparaison automatique + validation clinicien

**Dépendances :** S-016, S-018

---

## Traçabilité

### Epics → Stories

| Epic | Nom | Stories | Points |
|------|-----|---------|--------|
| EPIC-001 | Structuration des données | S-001 à S-006 | 20 |
| EPIC-002 | Webapp + API REST | S-007 à S-014 | 30 |
| EPIC-003 | Module IA + MCP | S-015 à S-019 | 28 |
| **Total** | | **19 stories** | **78 points** |

### FRs → Stories

| FR | Nom | Stories |
|----|-----|---------|
| FR-001 | Extraction données PDF | S-002, S-003, S-004, S-005 |
| FR-002 | Recommandations générales | S-006 |
| FR-003 | Recherche instantanée | S-009, S-011 |
| FR-004 | Navigation arborescence | S-011, S-013 |
| FR-005 | Affichage protocole | S-012 |
| FR-006 | Disclaimer médical | S-010 |
| FR-007 | Chatbot | S-015, S-016 |
| FR-008 | Sourçage réponses IA | S-016 |
| FR-009 | Comparaison 3 niveaux | S-018, S-019 |
| FR-010 | API REST | S-008 |
| FR-011 | Serveur MCP | S-017 |
| FR-012 | Open-source + docs | S-001 |

### NFRs → Stories

| NFR | Nom | Stories |
|-----|-----|---------|
| NFR-001 | < 200ms recherche | S-009 |
| NFR-002 | < 10s chatbot | S-016 |
| NFR-003 | Pas de données santé | Transversal (aucun champ patient) |
| NFR-004 | Pas d'auth | Transversal (aucune route protégée) |
| NFR-005 | Disponibilité 99% | S-014 |
| NFR-006 | Design responsive | S-010 |
| NFR-007 | Accessibilité > 80 | S-010 |
| NFR-008 | Code documenté | S-001 |
| NFR-009 | Mise à jour données | S-002 (format JSON séparé) |
| NFR-010 | < 20€/mois | S-014 (NAS), architecture globale |

---

## Risques

**Élevé :**
- Qualité de l'extraction PDF → Mitigation : extraction tableau par tableau, validation clinique systématique
- Hallucinations du chatbot → Mitigation : tool use (pas de génération libre), tests rigoureux

**Moyen :**
- Performance du RAG sur PDF brut (niveau 1) → Mitigation : c'est précisément ce qu'on mesure
- Coût API LLM si usage intensif → Mitigation : routage Haiku/Sonnet, rate limiting

**Faible :**
- Disponibilité du NAS → Mitigation : migration Docker vers le cloud triviale
- Compatibilité navigateurs → Mitigation : HTMX fonctionne partout, pas de JS exotique

---

## Definition of Done

Pour qu'une story soit considérée comme terminée :
- [ ] Code implémenté et poussé sur une branche `feat/xxx`
- [ ] Tests écrits et passants (coverage > 80% sur la logique métier)
- [ ] Lint (ruff) passant
- [ ] PR créée via `gh pr create`
- [ ] CI verte
- [ ] Critères d'acceptation validés
- [ ] Mergée dans `main`

---

## Prochaines étapes

1. **Commencer par S-001** : `gh repo create`, structure, CI, CONTRIBUTING.md
2. Puis **S-002** : extraire le premier tableau en JSON (pilote)
3. Avancer story par story, au rythme du porteur de projet

Lancer `/bmad:dev-story S-001` pour commencer l'implémentation.

---

*Généré par BMAD Method v6 — Scrum Master*
*Date : 2026-02-16*
