# CLAUDE.md — Instructions pour Claude Code

Ce fichier contient les instructions spécifiques à Claude Code pour ce projet.
Pour les conventions générales, voir [CONTRIBUTING.md](CONTRIBUTING.md).

## Contexte du projet

Webapp de consultation des recommandations d'antibioprophylaxie chirurgicale (RFE SFAR 2024).
- **Stack :** Python 3.12 / FastAPI / Jinja2 / HTMX / CSS vanilla / JSON statique
- **Architecture :** Monolithe modulaire (voir `docs/architecture-*.md`)
- **Gestionnaire de paquets :** `uv` (pas pip)
- **Linter/formatter :** `ruff` (pas black, pas flake8)

## Commandes essentielles

```bash
uv sync --extra dev          # Installer les dépendances
uv run pytest                # Lancer les tests
uv run pytest --cov=app      # Tests + couverture
uv run ruff check app/ tests/  # Lint
uv run ruff format app/ tests/ # Format
uv run uvicorn app.main:app --reload  # Serveur dev
```

## Conventions de code

- Conventional commits obligatoires : `type(scope): description`
- Branches : `feat/xxx`, `fix/xxx`, `docs/xxx` depuis `main`
- PRs via `gh pr create`, merge via `gh pr merge --squash`
- KISS, YAGNI, SOLID pragmatique
- Docstrings Google-style sur les fonctions publiques
- Tests pytest obligatoires pour toute logique métier (coverage >= 80%)

## Structure

```
app/data/     → Modèles Pydantic, chargement JSON, recherche fuzzy
app/api/      → API REST /api/v1/
app/chat/     → Chatbot (appel LLM, prompts)
app/web/      → Pages HTML (Jinja2 + HTMX)
app/templates/ → Templates Jinja2
app/static/   → CSS, JS (HTMX uniquement), images
data/         → Données sources (rfe.json, rfe.xlsx, rfe.pdf)
mcp_server/   → Serveur MCP (processus séparé)
research/     → Évaluation comparative (RAG vs MCP)
tests/        → Tests pytest
scripts/      → Scripts utilitaires
```

## Données

- Source de vérité : `data/rfe.json`
- Chargé en RAM au démarrage de FastAPI
- ~200-300 interventions, lecture seule
- Pas de base de données en V1

## Workflow GitHub

- Utiliser `gh` pour tout : issues, PRs, milestones, labels
- Ne jamais push directement sur `main` sans PR
- La CI doit passer avant merge (ruff + pytest)

## Ce qu'il ne faut PAS faire

- Ne pas ajouter de dépendances sans justification
- Ne pas créer de fichiers inutiles (pas de Makefile, pas de tox.ini)
- Ne pas sur-architecturer (pas d'interfaces abstraites, pas de factory pattern)
- Ne pas commiter de secrets (.env, clés API)
- Ne pas modifier les branches `archive/*`
