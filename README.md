# Antibioprophylaxie SFAR

Webapp de consultation des recommandations d'antibioprophylaxie chirurgicale, basée sur les **RFE SFAR 2024** (Recommandations Formalisées d'Experts de la Société Française d'Anesthésie et de Réanimation).

## Objectifs

- **Recherche instantanée** : trouver le bon protocole en quelques secondes (fuzzy search)
- **Navigation par spécialité** : parcourir les interventions par spécialité chirurgicale
- **Chatbot IA** : poser une question en langage naturel, obtenir une réponse sourcée
- **API REST publique** : intégrer les données dans d'autres outils
- **Serveur MCP** : connecter un client LLM (Claude Desktop, etc.) aux données structurées
- **Volet recherche** : comparaison RAG vs MCP pour une publication scientifique

## Stack technique

Python 3.12 · FastAPI · Jinja2 · HTMX · CSS vanilla · Mistral AI · MCP

## Démo en ligne

**https://recos-antibioprophylaxie-sfar.onrender.com**

> Hébergé sur Render (free tier). Premier chargement ~30s si l'app était en veille.

## Statut

En cours de développement. Voir la [documentation projet](docs/) pour les détails.

## Installation rapide

```bash
# Prérequis : Python 3.12+, uv (https://docs.astral.sh/uv/)
git clone git@github.com:tomboulier/recos-antibioprophylaxie-SFAR.git
cd recos-antibioprophylaxie-SFAR
uv sync --extra dev
uv run pytest
```

## Lancer le serveur

```bash
uv run uvicorn app.main:app --reload
```

Le serveur démarre sur http://localhost:8000. Les données de `data/rfe.json` (47 interventions, 2 spécialités) sont chargées en mémoire au démarrage.

### Endpoints disponibles

| Endpoint | Description |
|----------|-------------|
| `GET /` | Page d'accueil (Jinja2 + HTMX) |
| `GET /api/v1/health` | Health check avec statistiques (nb spécialités, nb interventions) |
| `GET /docs` | Documentation Swagger UI (générée automatiquement par FastAPI) |
| `GET /redoc` | Documentation ReDoc |

### Exemple : health check

```bash
curl http://localhost:8000/api/v1/health
```

```json
{
  "status": "ok",
  "version": "0.1.0",
  "data_version": "RFE SFAR 2024",
  "specialites": 2,
  "interventions": 47
}
```

### Configuration

Variables d'environnement (optionnelles) :

| Variable | Défaut | Description |
|----------|--------|-------------|
| `DEBUG` | `false` | Mode debug |
| `DATA_PATH` | `data/rfe.json` | Chemin vers le fichier de données |

## Déploiement Render

L'app est déployée sur **[https://recos-antibioprophylaxie-sfar.onrender.com](https://recos-antibioprophylaxie-sfar.onrender.com)**.

Pour déployer votre propre instance sur [Render](https://render.com) :

### Déploiement automatique (via render.yaml)

1. Forker ou connecter ce repo sur [dashboard.render.com](https://dashboard.render.com)
2. Cliquer **"New → Blueprint"** et sélectionner ce repo
3. Render détecte automatiquement `render.yaml` et configure le service

### Déploiement manuel

1. **New → Web Service** sur Render
2. Connecter le repo GitHub
3. Renseigner :
   - **Runtime :** Python 3
   - **Build command :** `pip install uv && uv sync`
   - **Start command :** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path :** `/api/v1/health`
4. Ajouter les variables d'environnement :
   - `PYTHON_VERSION` = `3.12.0`
   - `DEBUG` = `false`
5. Laisser les autres options par défaut (Free plan)

> **Note :** Le free tier se met en veille après 15 min d'inactivité (premier chargement ~30s). Suffisant pour les démos.

## Documentation

| Document | Description |
|----------|-------------|
| [PRD](docs/prd-antibioprophylaxie-sfar-2026-02-15.md) | Exigences fonctionnelles et non-fonctionnelles |
| [Architecture](docs/architecture-antibioprophylaxie-sfar-2026-02-16.md) | Stack, structure, modèle de données, API |
| [UX Design](docs/ux-design-antibioprophylaxie-sfar-2026-02-16.md) | Wireframes, flows, design tokens |
| [Sprint Plan](docs/sprint-plan-antibioprophylaxie-sfar-2026-02-16.md) | Stories, estimations, milestones |
| [CONTRIBUTING](CONTRIBUTING.md) | Guide de contribution (humains + IAs) |

## Historique

Ce projet a connu deux prototypes exploratoires, conservés en branches d'archive :
- `archive/prototype-v1-windsurf` — Premier prototype (Windsurf, mars 2025)
- `archive/prototype-v2-mcp` — Prototype MCP (février 2025)

## Licence

[MIT](LICENSE)

## Avertissement

Cet outil est un aide-mémoire de consultation. Il ne remplace pas le jugement clinique. Source : RFE SFAR 2024.
