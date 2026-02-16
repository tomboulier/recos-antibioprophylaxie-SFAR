# Architecture : Antibioprophylaxie SFAR

**Date :** 2026-02-16
**Architecte :** Thomas Boulier (assisté par Claude)
**Version :** 1.0

**Documents de référence :**
- PRD : docs/prd-antibioprophylaxie-sfar-2026-02-15.md
- UX Design : docs/ux-design-antibioprophylaxie-sfar-2026-02-16.md
- Recherche : docs/research-reglementaire-academique-technique-2026-02-15.md

---

## 1. Drivers architecturaux

Les exigences qui influencent le plus les choix d'architecture :

| # | Driver | Exigence | Impact architectural |
|---|--------|----------|---------------------|
| 1 | **Performance recherche** | NFR-001 : < 200ms | Données en mémoire, pas de requête réseau pour la recherche |
| 2 | **Budget minimal** | NFR-010 : < 20€/mois | Hébergement léger, pas de DB managée, pas de services payants |
| 3 | **Zéro authentification** | NFR-004 | Pas de sessions, pas de tokens, pas de table users |
| 4 | **Pas de données de santé** | NFR-003 | Hébergement standard, pas de HDS |
| 5 | **3 niveaux de structuration** | FR-009 | L'archi supporte RAG PDF + RAG Excel + MCP côte à côte |
| 6 | **API REST + MCP** | FR-010, FR-011 | Deux interfaces d'accès aux mêmes données |
| 7 | **Dev solo** | Contexte projet | Stack simple, un seul langage, déploiement simple |

---

## 2. Architecture haut niveau

### Pattern : Monolithe modulaire

Un seul serveur FastAPI qui sert tout : les pages HTML, l'API REST, le chatbot, et le serveur MCP.

```
                    ┌─────────────────────────────┐
                    │        Navigateur            │
                    │  (mobile ou desktop)         │
                    └──────────┬──────────────────┘
                               │ HTTPS
                    ┌──────────▼──────────────────┐
                    │        FastAPI               │
                    │                              │
                    │  ┌──────────────────────┐    │
                    │  │  Pages HTML          │    │ ← Jinja2 + HTMX
                    │  │  (Accueil, Protocole,│    │
                    │  │   Spécialité, Chat)  │    │
                    │  └──────────────────────┘    │
                    │                              │
                    │  ┌──────────────────────┐    │
                    │  │  API REST (/api/v1/) │    │ ← Endpoints JSON
                    │  └──────────────────────┘    │
                    │                              │
                    │  ┌──────────────────────┐    │
                    │  │  Chatbot (/chat/)    │    │ ← Appel LLM API
                    │  └──────────────────────┘    │
                    │                              │
                    │  ┌──────────────────────┐    │
                    │  │  Couche données      │    │ ← JSON en mémoire
                    │  │  (DataService)       │    │
                    │  └──────────────────────┘    │
                    └─────────────────────────────┘

                    ┌─────────────────────────────┐
                    │  Serveur MCP (processus      │ ← Même données,
                    │  séparé ou même serveur)     │   protocole MCP
                    └─────────────────────────────┘

    Données sources :
    ┌──────────┐  ┌──────────┐  ┌──────────┐
    │ data/    │  │ data/    │  │ data/    │
    │ rfe.json │  │ rfe.xlsx │  │ rfe.pdf  │
    └──────────┘  └──────────┘  └──────────┘
```

### Justification

- **Monolithe** car : dev solo, ~12-20 stories, pas besoin de microservices, déploiement unique, un seul processus à monitorer.
- **Modulaire** car : séparation claire entre pages, API, chatbot, données. Chaque module est un routeur FastAPI indépendant. Facile à extraire en service séparé si besoin en V2.
- **MCP séparé** car : le protocole MCP utilise stdio/SSE, incompatible avec le serveur HTTP. C'est un processus séparé qui accède aux mêmes fichiers JSON.

---

## 3. Stack technique

### Backend : Python 3.12+ / FastAPI

| Choix | Technologie | Justification |
|-------|-------------|---------------|
| **Langage** | Python 3.12+ | Confort du développeur, écosystème IA (LangChain, Anthropic SDK), écosystème data science |
| **Framework** | FastAPI | Rapide, async natif, auto-documentation OpenAPI, typage Pydantic |
| **Templates** | Jinja2 | Intégré à FastAPI, simple, pas de build step |
| **Interactivité** | HTMX | Requêtes AJAX déclaratives en HTML, pas de JS à écrire pour le type-ahead et le chat |
| **Serveur** | Uvicorn | Serveur ASGI performant, standard pour FastAPI |

**Trade-off :** On choisit HTMX plutôt qu'un SPA (React/Vue) car :
- ✓ Un seul langage (Python), pas de toolchain JS (npm, webpack, etc.)
- ✓ Pas de build step frontend
- ✓ Rendu serveur = bon SEO, temps de chargement initial rapide
- ✗ Moins flexible pour des interactions complexes (mais nos 5 écrans sont simples)

### Frontend : HTML + HTMX + CSS

| Choix | Technologie | Justification |
|-------|-------------|---------------|
| **Markup** | HTML5 sémantique | Via templates Jinja2 |
| **Interactivité** | HTMX 2.x | Type-ahead, chat, navigation sans rechargement complet |
| **Style** | CSS vanilla (custom properties) | Design tokens en variables CSS, pas besoin de Tailwind pour 5 écrans |
| **Icônes** | Lucide Icons (SVG) | Léger, accessible, open-source |

### Données : fichiers JSON

| Choix | Technologie | Justification |
|-------|-------------|---------------|
| **Stockage** | Fichiers JSON dans `data/` | ~200-300 interventions, lecture seule, ultra-rapide en mémoire |
| **Accès** | Chargé en RAM au démarrage | Recherche en mémoire < 1ms, zéro latence réseau |
| **Recherche** | Recherche textuelle Python (difflib/rapidfuzz) | Fuzzy matching pour tolérer les fautes de frappe |

**Trade-off :** JSON plutôt que SQLite/PostgreSQL car :
- ✓ Zéro dépendance, zéro configuration, zéro coût
- ✓ Versionnable dans Git (on voit les diffs des données)
- ✓ ~200 entrées tiennent en quelques Ko en RAM
- ✗ Pas de requêtes SQL complexes (pas besoin en V1)
- ✗ Migration vers SQLite facile si V2 nécessite du CRUD

### IA / LLM

| Choix | Technologie | Justification |
|-------|-------------|---------------|
| **LLM principal** | Mistral AI | Francophone, français, open-source, impliqué dans le projet PARTAGES (LLM santé national financé France 2030). Cohérent avec le positionnement recherche et souveraineté numérique. |
| **SDK** | mistralai (Python SDK) | Intégration simple avec FastAPI |
| **LLMs secondaires** | Claude (Anthropic), GPT-4 (OpenAI) | Pour l'étude comparative multi-modèles |
| **RAG** | LangChain (ou LlamaIndex) | Pour les niveaux 1 et 2 (RAG sur PDF et Excel) |
| **Vector store** | ChromaDB (embarqué) | Gratuit, embarqué, pas de service externe |
| **MCP** | mcp (Python SDK officiel Anthropic) | SDK standard pour les serveurs MCP |

**Pourquoi Mistral en principal :**
- Modèle français, entreprise française — aligné avec le positionnement institutionnel SFAR
- Impliqué dans le projet [PARTAGES](https://www.health-data-hub.fr/actualites/democratiser-lia-generative-en-sante-letat-travers-france-2030-selectionne-le-projet) (Health Data Hub + Mistral + AP-HP + universités) : LLM open-source dédié à la santé, financé France 2030
- Open-source (poids disponibles) → possibilité de déploiement local sur le NAS à terme
- Bon rapport qualité/prix sur le français
- L'étude comparative testera aussi Claude et GPT-4 pour la publication

**Pour la comparaison (FR-009) — 3 niveaux × N modèles :**

| Niveau | Approche | Données | Outil |
|--------|----------|---------|-------|
| 1 | RAG sur PDF brut | `data/rfe.pdf` | LangChain + PyPDF + ChromaDB |
| 2 | RAG sur Excel | `data/rfe.xlsx` | LangChain + Excel loader + ChromaDB |
| 3 | MCP sur API JSON | `data/rfe.json` → API REST | Serveur MCP + tool use |

Chaque niveau sera testé avec Mistral, Claude et GPT-4 pour une matrice complète (3 niveaux × 3 modèles = 9 conditions).

### Infrastructure

| Choix | Technologie | Justification |
|-------|-------------|---------------|
| **Hébergement** | À choisir : Fly.io, Railway, Render, ou Hetzner VPS | Détail ci-dessous |
| **Conteneur** | Docker | Déploiement reproductible, standard |
| **CI/CD** | GitHub Actions | Gratuit pour les repos publics, intégré à GitHub |
| **Domaine** | Optionnel (sous-domaine gratuit du provider) | Domaine custom en V2 si besoin |

**Options d'hébergement :**

| Option | Coût | Cold starts | Maintenance | Recommandation |
|--------|------|-------------|-------------|----------------|
| **Fly.io** | 0-5€/mois | Oui (gratuit) | Faible | Bon compromis |
| **Railway** | 0-5€/mois | Non (hobby) | Très faible | DX excellent |
| **Render** | 0-7€/mois | Oui (gratuit) | Faible | Simple |
| **Hetzner VPS** | ~4€/mois | Non | Moyenne | Meilleur perf/prix |

**Stratégie de déploiement en 2 phases :**

1. **Phase dev/test : NAS personnel** — Docker sur le NAS, accès via tunnel (Cloudflare Tunnel ou Tailscale). Zéro coût, idéal pour le développement, les tests et les premières démos aux collègues.
2. **Phase production : hébergement cloud** — Le même Dockerfile déployé sur Railway, Fly.io, Hetzner VPS, ou un serveur SFAR si soutien institutionnel. Migration = `docker push` + `docker pull`. Coût estimé : 5-15€/mois.

---

## 4. Structure du projet

```
recos-antibioprophylaxie-SFAR/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Point d'entrée FastAPI
│   ├── config.py               # Configuration (env vars)
│   │
│   ├── data/                   # Couche données
│   │   ├── __init__.py
│   │   ├── models.py           # Modèles Pydantic (Intervention, Protocole, etc.)
│   │   ├── loader.py           # Chargement JSON → mémoire
│   │   └── search.py           # Recherche fuzzy
│   │
│   ├── api/                    # API REST
│   │   ├── __init__.py
│   │   ├── router.py           # Routeur /api/v1/
│   │   └── schemas.py          # Schémas de réponse API
│   │
│   ├── chat/                   # Module chatbot
│   │   ├── __init__.py
│   │   ├── router.py           # Routes /chat/
│   │   ├── llm.py              # Abstraction appel LLM
│   │   └── prompts.py          # System prompts
│   │
│   ├── web/                    # Pages HTML
│   │   ├── __init__.py
│   │   └── router.py           # Routes / (pages Jinja2)
│   │
│   ├── templates/              # Templates Jinja2
│   │   ├── base.html           # Layout commun (header, footer, disclaimer)
│   │   ├── index.html          # Accueil (recherche + spécialités)
│   │   ├── specialty.html      # Vue spécialité
│   │   ├── protocol.html       # Détail protocole
│   │   ├── chat.html           # Interface chatbot
│   │   └── partials/           # Fragments HTMX
│   │       ├── search_results.html
│   │       ├── protocol_card.html
│   │       └── chat_message.html
│   │
│   └── static/                 # Fichiers statiques
│       ├── css/
│       │   └── style.css       # Design tokens + styles
│       ├── js/
│       │   └── htmx.min.js     # HTMX (seul JS externe)
│       └── img/
│
├── data/                       # Données sources
│   ├── rfe.json                # Données structurées (source de vérité)
│   ├── rfe.xlsx                # Export Excel (pour RAG niveau 2)
│   └── rfe.pdf                 # PDF original (pour RAG niveau 1)
│
├── mcp_server/                 # Serveur MCP (processus séparé)
│   ├── __init__.py
│   ├── server.py               # Point d'entrée MCP
│   └── tools.py                # Outils MCP (search, get_protocol, etc.)
│
├── research/                   # Scripts du volet recherche
│   ├── evaluate.py             # Évaluation comparative
│   ├── questions.json          # Jeu de questions standardisé
│   └── results/                # Résultats des évaluations
│
├── tests/                      # Tests
│   ├── test_data.py
│   ├── test_api.py
│   ├── test_search.py
│   └── test_chat.py
│
├── Dockerfile
├── pyproject.toml              # Dépendances (uv/pip)
├── CLAUDE.md                   # Instructions pour Claude Code
├── README.md
└── .github/
    └── workflows/
        └── ci.yml              # GitHub Actions CI/CD
```

---

## 5. Modèle de données

### Entités principales

Les données sont en lecture seule (V1). Le JSON est la source de vérité.

```python
# app/data/models.py

from pydantic import BaseModel

class Protocole(BaseModel):
    """Protocole d'antibioprophylaxie pour une intervention."""
    molecule: str                    # Ex: "Céfazoline"
    posologie: str                   # Ex: "2g IV"
    timing: str                      # Ex: "30 min avant incision"
    reinjection: str | None          # Ex: "1g toutes les 4h"
    duree: str                       # Ex: "Dose unique" ou "24h"

class AlternativeAllergie(BaseModel):
    """Alternative en cas d'allergie."""
    molecule: str                    # Ex: "Clindamycine"
    posologie: str                   # Ex: "900mg IV"
    reinjection: str | None          # Ex: "600mg toutes les 6h"

class Intervention(BaseModel):
    """Une intervention chirurgicale avec son protocole d'ABP."""
    id: str                          # Ex: "ortho-pth"
    nom: str                         # Ex: "Prothèse totale de hanche (PTH)"
    specialite: str                  # Ex: "Orthopédie"
    protocole: Protocole
    alternative_allergie: AlternativeAllergie | None
    pas_d_abp: bool = False          # True si "pas d'ABP recommandée"
    source_page: int                 # Page du PDF
    source_tableau: str              # Ex: "Tableau 12"
    notes: str | None                # Notes spécifiques

class Specialite(BaseModel):
    """Une spécialité chirurgicale."""
    id: str                          # Ex: "orthopedie"
    nom: str                         # Ex: "Orthopédie"
    interventions: list[Intervention]

class RecommandationGenerale(BaseModel):
    """Recommandation narrative transverse (FR-002)."""
    id: str
    titre: str                       # Ex: "Patient obèse"
    contenu: str                     # Texte de la recommandation
    source_page: int
```

### Format JSON (`data/rfe.json`)

```json
{
  "version": "RFE SFAR 2024",
  "date_extraction": "2026-XX-XX",
  "specialites": [
    {
      "id": "orthopedie",
      "nom": "Orthopédie",
      "interventions": [
        {
          "id": "ortho-pth",
          "nom": "Prothèse totale de hanche (PTH)",
          "specialite": "Orthopédie",
          "protocole": {
            "molecule": "Céfazoline",
            "posologie": "2g IV",
            "timing": "30 min avant incision",
            "reinjection": "1g toutes les 4h",
            "duree": "Dose unique"
          },
          "alternative_allergie": {
            "molecule": "Clindamycine",
            "posologie": "900mg IV",
            "reinjection": "600mg toutes les 6h"
          },
          "pas_d_abp": false,
          "source_page": 73,
          "source_tableau": "Tableau 12",
          "notes": null
        }
      ]
    }
  ],
  "recommandations_generales": [
    {
      "id": "timing-general",
      "titre": "Timing d'administration",
      "contenu": "L'antibioprophylaxie doit être administrée...",
      "source_page": 15
    }
  ]
}
```

### Flux de données

```
Au démarrage du serveur :
  data/rfe.json → loader.py → RAM (list[Specialite])
                                    ↓
                              Utilisé par :
                              ├── search.py (recherche fuzzy)
                              ├── api/router.py (endpoints JSON)
                              ├── web/router.py (pages HTML)
                              └── chat/llm.py (contexte pour le LLM)
```

---

## 6. API REST

### Endpoints

Tous les endpoints sont en lecture seule (GET), sans authentification (NFR-004), et renvoient du JSON.

```
GET /api/v1/interventions
    → Liste toutes les interventions
    Query params : ?q=hanche (recherche textuelle)
                   ?specialite=orthopedie (filtre par spécialité)
    Réponse : [{ id, nom, specialite, protocole, ... }]

GET /api/v1/interventions/{id}
    → Détail d'une intervention
    Réponse : { id, nom, specialite, protocole, alternative_allergie, source_page, ... }

GET /api/v1/specialites
    → Liste toutes les spécialités avec le nombre d'interventions
    Réponse : [{ id, nom, nombre_interventions }]

GET /api/v1/specialites/{id}
    → Détail d'une spécialité avec toutes ses interventions
    Réponse : { id, nom, interventions: [...] }

GET /api/v1/recommandations
    → Liste les recommandations générales (FR-002)
    Réponse : [{ id, titre, contenu, source_page }]

POST /api/v1/chat
    → Envoie une question au chatbot
    Body : { "question": "je mets quoi sur une PTH ?" }
    Réponse : { "reponse": "...", "sources": [...], "intervention_ids": [...] }

GET /api/v1/health
    → Health check
    Réponse : { "status": "ok", "version": "1.0", "data_version": "RFE SFAR 2024" }
```

**Documentation :** FastAPI génère automatiquement le Swagger UI sur `/docs` et le schéma OpenAPI sur `/openapi.json`. Ça couvre FR-012 (documentation API) gratuitement.

### HTMX endpoints (pages web)

Les pages HTML sont servies par le routeur web, et les fragments HTMX par des endpoints dédiés :

```
GET /                           → Page d'accueil
GET /specialite/{id}            → Vue spécialité
GET /protocole/{id}             → Détail protocole
GET /chat                       → Interface chatbot

GET /htmx/search?q=hanche      → Fragment HTML : résultats de recherche
POST /htmx/chat                 → Fragment HTML : bulle de réponse chatbot
GET /htmx/protocol-card/{id}    → Fragment HTML : carte protocole
```

---

## 7. Serveur MCP

Le serveur MCP expose les mêmes données que l'API REST, mais via le protocole MCP (stdio ou SSE) pour intégration avec des clients LLM (Claude Desktop, etc.).

### Outils MCP

```python
# mcp_server/tools.py

@mcp.tool()
def search_interventions(query: str) -> list[dict]:
    """Recherche des interventions par mot-clé."""

@mcp.tool()
def get_intervention(id: str) -> dict:
    """Retourne le protocole complet d'une intervention."""

@mcp.tool()
def list_specialites() -> list[dict]:
    """Liste toutes les spécialités chirurgicales."""

@mcp.tool()
def get_specialite(id: str) -> dict:
    """Retourne toutes les interventions d'une spécialité."""

@mcp.tool()
def get_recommandations_generales() -> list[dict]:
    """Retourne les recommandations générales transverses."""
```

### Architecture MCP

Le serveur MCP est un **processus séparé** qui lit les mêmes fichiers `data/rfe.json`. Il ne dépend pas de FastAPI.

```
Client MCP (Claude Desktop, etc.)
    ↕ stdio ou SSE
Serveur MCP (mcp_server/server.py)
    ↓ lecture
data/rfe.json
```

---

## 8. Module chatbot

### Architecture du chatbot

```
Question utilisateur
    ↓
Sélection du niveau (1, 2, ou 3) pour la recherche
    ↓
┌─────────────────────────────────────────────────┐
│ Niveau 1 : RAG sur PDF                          │
│   PyPDF → chunks → ChromaDB → contexte → LLM   │
│                                                  │
│ Niveau 2 : RAG sur Excel                        │
│   openpyxl → chunks → ChromaDB → contexte → LLM│
│                                                  │
│ Niveau 3 : MCP / Tool use                       │
│   Question → LLM → appels API structurés →      │
│   données exactes → LLM → réponse formatée      │
└─────────────────────────────────────────────────┘
    ↓
Réponse formatée + sources
```

### System prompt du chatbot (niveau 3 — production)

```
Tu es un assistant spécialisé dans l'antibioprophylaxie chirurgicale,
basé sur les RFE SFAR 2024.

Règles :
- Réponds UNIQUEMENT à partir des données fournies
- Cite TOUJOURS la source (page, tableau)
- Si tu ne trouves pas l'information, dis "Je n'ai pas trouvé cette
  information dans les RFE SFAR 2024."
- Ne fabrique JAMAIS de dosages ou de citations
- Formate les réponses de manière claire : molécule, posologie,
  timing, réinjection, alternative allergie
```

### Coût LLM estimé

- Mistral Small pour les questions simples : ~0.001€/requête
- Mistral Large pour les questions complexes : ~0.008€/requête
- Budget 10€/mois ≈ 1250 requêtes Large ou 10 000 requêtes Small
- Stratégie : router les questions simples vers Small, les complexes vers Large
- À terme (si PARTAGES livre un modèle santé open-source) : déploiement local sur le NAS = coût zéro

---

## 9. Couverture des NFRs

### NFR-001 : Temps de réponse webapp (< 200ms)

**Solution :**
- Données JSON chargées en RAM au démarrage (~quelques Ko)
- Recherche fuzzy en Python sur données en mémoire : < 5ms
- HTMX renvoie des fragments HTML légers (pas de SPA qui télécharge tout)
- CSS et HTMX servis en cache avec headers appropriés

**Validation :** Mesurer le temps de réponse des endpoints `/htmx/search` en staging.

### NFR-002 : Temps de réponse chatbot (< 10s)

**Solution :**
- Indicateur de chargement affiché immédiatement (HTMX `hx-indicator`)
- Appel API Claude en streaming (SSE) pour afficher la réponse au fur et à mesure
- Routage intelligent : questions simples → Haiku (< 3s), complexes → Sonnet (< 8s)

**Validation :** Mesurer le p95 du temps de réponse en production.

### NFR-003 : Pas de données de santé

**Solution :**
- Aucun champ de saisie patient dans l'application
- Seules les recommandations publiques SFAR sont stockées
- Le chatbot ne stocke pas l'historique des conversations côté serveur (session navigateur uniquement)
- Pas de cookies de tracking, pas d'analytics personnalisées

### NFR-004 : Pas d'authentification

**Solution :**
- Aucune route protégée, aucun middleware d'auth
- API REST publique, pas de clé API
- Pas de table users en base

### NFR-005 : Disponibilité 99%

**Solution :**
- Déploiement Docker simple, redémarrage automatique
- Health check `/api/v1/health` pour le monitoring
- Si Fly.io/Railway : auto-restart en cas de crash
- Si VPS : systemd + watchdog

### NFR-006 : Design responsive (375px → 1920px)

**Solution :**
- CSS mobile-first avec media queries (breakpoints : 768px, 1024px)
- Design tokens en variables CSS (cf. UX design)
- Templates Jinja2 avec layout responsive
- Test sur Chrome DevTools (mobile + desktop)

### NFR-007 : Accessibilité (Lighthouse > 80)

**Solution :**
- HTML5 sémantique (`<header>`, `<main>`, `<nav>`, `<footer>`)
- Attributs ARIA sur les composants interactifs (recherche, chat)
- Contraste vérifié (cf. design tokens UX)
- Navigation clavier (Tab, Enter, Escape)
- Cibles tactiles minimum 44px

### NFR-008 : Code open-source et documenté

**Solution :**
- Repository GitHub public
- README avec instructions d'installation (< 15 min)
- `CLAUDE.md` avec conventions de développement
- Documentation API auto-générée (Swagger/OpenAPI)
- Docstrings sur les fonctions publiques

### NFR-009 : Mise à jour des données sans redéploiement

**Solution :**
- Les données sont dans `data/rfe.json`, séparées du code
- Pour mettre à jour : modifier le JSON, redémarrer le serveur (ou endpoint de rechargement)
- Le JSON est versionné dans Git → on voit l'historique des modifications
- En V2, possibilité d'ajouter un endpoint admin pour éditer les données (CRUD)

### NFR-010 : Hébergement < 20€/mois

**Budget prévisionnel :**

| Poste | Coût mensuel |
|-------|-------------|
| Hébergement (Railway/Fly.io/VPS) | 0-7€ |
| API Claude (chatbot) | 5-10€ |
| Domaine (optionnel) | 0-1€ |
| **Total** | **5-18€** |

---

## 10. Sécurité

Même sans authentification ni données sensibles, les bonnes pratiques s'appliquent :

**En transit :**
- HTTPS obligatoire (fourni par l'hébergeur)
- Headers de sécurité : `X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy`

**Validation des entrées :**
- Recherche : sanitization des paramètres de requête (Pydantic)
- Chat : la question utilisateur est passée au LLM dans un prompt structuré (pas d'injection directe)
- API : validation Pydantic sur tous les paramètres

**Protection contre les abus :**
- Rate limiting sur `/api/v1/chat` (coûteux en appels LLM) : 10 req/min par IP
- Rate limiting léger sur l'API REST : 100 req/min par IP
- Pas de rate limiting sur les pages HTML (consultation libre)

**Clé API LLM :**
- Stockée en variable d'environnement, jamais dans le code
- `.env` dans le `.gitignore`

---

## 11. Conventions de développement

### Git flow

- **Branche principale :** `main` (toujours déployable)
- **Branches de travail :** `feat/xxx`, `fix/xxx`, `docs/xxx`
- **Pas de branche develop** (overkill pour un dev solo)
- Workflow : créer une branche → commits → PR via `gh pr create` → merge dans main

### Conventional commits

Format : `type(scope): description`

```
feat(search): add fuzzy matching for interventions
fix(chat): handle timeout on LLM API call
docs(readme): add installation instructions
refactor(data): extract search logic into dedicated module
test(api): add tests for /api/v1/interventions endpoint
chore(ci): add GitHub Actions workflow
```

Types autorisés : `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`, `perf`

### Workflow GitHub

```bash
# Créer une branche
git checkout -b feat/search-typeahead

# Développer, commiter (conventional commits)
git add -A
git commit -m "feat(search): implement type-ahead search"

# Pousser et créer une PR
gh pr create --title "feat(search): implement type-ahead" --body "..."

# Review (auto-merge pour le dev solo, CI doit passer)
gh pr merge --squash
```

### Principes de code

- **KISS** : la solution la plus simple qui fonctionne. 5 écrans, pas besoin d'abstractions complexes.
- **YAGNI** : pas de fonctionnalités "au cas où". On implémente ce qui est dans le sprint, pas plus.
- **SOLID** : appliqué avec pragmatisme. Séparation claire (data/api/chat/web), mais pas d'interfaces abstraites pour 3 classes.

### TDD / Stratégie de tests

- **Tests unitaires :** `pytest` sur la couche données (search, models) et la logique métier
- **Tests d'intégration :** `httpx` + `pytest` sur les endpoints FastAPI
- **Tests E2E :** optionnels, Playwright si le temps le permet
- **Couverture cible :** 80% sur la couche données et API, pas de couverture imposée sur les templates HTML
- **Règle :** écrire le test avant ou juste après le code. Les PRs sans tests sur la logique métier ne passent pas la CI.

### CI/CD (GitHub Actions)

```yaml
# .github/workflows/ci.yml
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv sync
      - run: uv run pytest --cov=app --cov-report=term-missing
      - run: uv run ruff check app/
      - run: uv run ruff format --check app/

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    # Déploiement automatique sur push to main
    # (config spécifique à l'hébergeur)
```

### Linting et formatting

- **Linter :** `ruff` (rapide, remplace flake8 + isort + pyupgrade)
- **Formatter :** `ruff format` (compatible Black)
- **Config :** dans `pyproject.toml`
- **Pre-commit hook :** `ruff check --fix && ruff format` avant chaque commit

### Docstrings

- Docstrings sur les fonctions publiques et les classes (Google style)
- Pas de docstrings sur les fonctions internes évidentes
- Les modèles Pydantic sont auto-documentés par leurs types et noms de champs

### Gestionnaire de paquets

- **uv** (par Astral, même équipe que ruff) : rapide, remplace pip + virtualenv
- Dépendances dans `pyproject.toml`
- Lock file : `uv.lock`

---

## 12. Traçabilité

### Exigences fonctionnelles → Composants

| FR | Nom | Composant(s) |
|----|-----|-------------|
| FR-001 | Extraction données PDF | `data/rfe.json` (fait manuellement) |
| FR-002 | Recommandations générales | `data/rfe.json` + `api/router.py` |
| FR-003 | Recherche instantanée | `data/search.py` + `web/router.py` + HTMX |
| FR-004 | Navigation arborescence | `web/router.py` + templates Jinja2 |
| FR-005 | Affichage protocole | `web/router.py` + `templates/protocol.html` |
| FR-006 | Disclaimer médical | `templates/base.html` (footer) |
| FR-007 | Chatbot | `chat/router.py` + `chat/llm.py` |
| FR-008 | Sourçage réponses IA | `chat/prompts.py` (system prompt) |
| FR-009 | Comparaison 3 niveaux | `research/` + `chat/llm.py` (3 stratégies) |
| FR-010 | API REST | `api/router.py` |
| FR-011 | Serveur MCP | `mcp_server/` |
| FR-012 | Open-source + docs | GitHub + README + `/docs` (Swagger) |

### NFRs → Solutions

| NFR | Nom | Solution |
|-----|-----|----------|
| NFR-001 | < 200ms recherche | JSON en RAM, recherche en mémoire |
| NFR-002 | < 10s chatbot | Streaming SSE, routage Haiku/Sonnet |
| NFR-003 | Pas de données santé | Aucun champ patient, pas de stockage |
| NFR-004 | Pas d'auth | Pas de middleware auth |
| NFR-005 | 99% dispo | Docker + auto-restart |
| NFR-006 | Responsive | CSS mobile-first + media queries |
| NFR-007 | Accessibilité > 80 | HTML sémantique + ARIA |
| NFR-008 | Open-source | GitHub public + README + Swagger |
| NFR-009 | Mise à jour données | JSON séparé du code |
| NFR-010 | < 20€/mois | Hébergement léger + Haiku par défaut |

### Trade-offs documentés

| Décision | On gagne | On perd | Justification |
|----------|----------|---------|---------------|
| Monolithe vs microservices | Simplicité, déploiement unique | Scaling indépendant | Dev solo, 12-20 stories |
| HTMX vs SPA (React/Vue) | Un seul langage, pas de build JS | Interactivité complexe | 5 écrans simples |
| JSON vs SQLite/PostgreSQL | Zéro config, versionnable Git | Requêtes SQL | ~200 entrées, lecture seule |
| ChromaDB embarqué vs Pinecone | Gratuit, pas de service externe | Scalabilité | Volume de données minime |
| Ruff vs Black+flake8 | Un seul outil, plus rapide | Moins configurable | Standard moderne Python |

---

## 13. Questions ouvertes

1. **Choix final de l'hébergeur** : à trancher au moment du premier déploiement (Railway vs Fly.io vs VPS)
2. **Modèle LLM pour l'étude comparative** : tester aussi GPT-4 et Mistral en plus de Claude ?
3. **Streaming des réponses chatbot** : SSE natif HTMX ou polling ? (SSE recommandé)
4. **PWA** : ajouter un manifest + service worker pour l'installation sur écran d'accueil ? (V2 possible)

---

## Prochaines étapes

1. **`/bmad:sprint-planning`** — Découper les epics en stories, estimer, planifier
2. **CLAUDE.md** — Créer le fichier de conventions pour Claude Code (basé sur la section 11)
3. **Développement** — Commencer par EPIC-001 (structuration des données)

---

*Généré par BMAD Method v6 — System Architect*
*Date : 2026-02-16*
