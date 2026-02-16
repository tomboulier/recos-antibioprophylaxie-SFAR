# Guide de contribution

Ce guide s'adresse à tous les contributeurs, **humains comme IA** (Claude Code, GitHub Copilot, ou tout autre assistant).

## Prérequis

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (gestionnaire de paquets)
- [gh](https://cli.github.com/) (CLI GitHub)

## Installation

```bash
# Cloner le repo
gh repo clone tomboulier/recos-antibioprophylaxie-SFAR
cd recos-antibioprophylaxie-SFAR

# Installer les dépendances (dev)
uv sync --extra dev

# Installer les hooks pre-commit
uv run pre-commit install

# Lancer les tests
uv run pytest

# Lancer le serveur de développement
uv run uvicorn app.main:app --reload
```

## Git flow

- **Branche principale :** `main` (toujours déployable)
- **Branches de travail :** `feat/xxx`, `fix/xxx`, `docs/xxx`, `refactor/xxx`, `test/xxx`, `chore/xxx`
- Pas de branche `develop` (projet solo)

### Workflow

```bash
# 1. Créer une branche depuis main
git checkout main && git pull
git checkout -b feat/ma-feature

# 2. Développer + commiter (conventional commits, voir ci-dessous)
git add <fichiers>
git commit -m "feat(scope): description courte"

# 3. Pousser et créer une PR
git push -u origin feat/ma-feature
gh pr create --title "feat(scope): description" --body "Description détaillée"

# 4. Vérifier que la CI passe, puis merger
gh pr merge --squash
```

## Conventional commits

Chaque commit suit le format : `type(scope): description`

### Types autorisés

| Type | Usage |
|------|-------|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction de bug |
| `docs` | Documentation uniquement |
| `refactor` | Refactoring sans changement fonctionnel |
| `test` | Ajout ou modification de tests |
| `chore` | Maintenance (CI, dépendances, config) |
| `style` | Formatage, espaces, virgules (pas de changement de code) |
| `perf` | Amélioration de performance |

### Scopes courants

`data`, `api`, `search`, `chat`, `web`, `mcp`, `ci`, `docs`, `config`

### Exemples

```
feat(search): add fuzzy matching for interventions
fix(chat): handle timeout on LLM API call
docs(readme): add deployment instructions
test(api): add integration tests for /api/v1/interventions
chore(ci): update GitHub Actions workflow
```

## Style de code

### Principes

- **KISS** : la solution la plus simple qui fonctionne
- **YAGNI** : pas de fonctionnalités "au cas où"
- **SOLID** : appliqué avec pragmatisme (pas d'abstractions inutiles pour 5 écrans)

### Linting et formatage

On utilise [ruff](https://docs.astral.sh/ruff/) pour le linting ET le formatage.

```bash
# Vérifier
uv run ruff check app/ tests/
uv run ruff format --check app/ tests/

# Corriger automatiquement
uv run ruff check --fix app/ tests/
uv run ruff format app/ tests/
```

Le pre-commit hook lance automatiquement `ruff check --fix` et `ruff format` avant chaque commit.

### Docstrings

- Docstrings Google-style sur les fonctions et classes publiques
- Pas de docstrings sur les fonctions internes évidentes
- Les modèles Pydantic sont auto-documentés par leurs types

```python
def search_interventions(query: str, limit: int = 10) -> list[Intervention]:
    """Recherche des interventions par mot-clé avec fuzzy matching.

    Args:
        query: Texte de recherche (nom d'intervention, spécialité, molécule).
        limit: Nombre maximum de résultats.

    Returns:
        Liste d'interventions triées par pertinence.
    """
```

## Tests

```bash
# Lancer tous les tests
uv run pytest

# Avec couverture
uv run pytest --cov=app --cov-report=term-missing

# Un fichier spécifique
uv run pytest tests/test_search.py -v
```

### Règles

- Tests unitaires avec `pytest` sur la couche données et la logique métier
- Tests d'intégration avec `httpx` sur les endpoints FastAPI
- Couverture cible : **80%** sur `app/` (hors templates HTML)
- Les PRs sans tests sur la logique métier ne passent pas la CI

## Structure du projet

```
app/              # Code applicatif FastAPI
├── data/         # Modèles Pydantic, chargement JSON, recherche
├── api/          # API REST (/api/v1/)
├── chat/         # Module chatbot
├── web/          # Pages HTML (Jinja2)
├── templates/    # Templates Jinja2
└── static/       # CSS, JS (HTMX), images

data/             # Données sources (JSON, Excel, PDF)
mcp_server/       # Serveur MCP (processus séparé)
research/         # Scripts d'évaluation comparative
tests/            # Tests pytest
scripts/          # Scripts utilitaires
docs/             # Documentation projet (PRD, architecture, etc.)
```

## Pour les IAs (Claude Code, Copilot, etc.)

- Lire ce fichier ET le `CLAUDE.md` (ou équivalent) avant de contribuer
- Toujours vérifier que `uv run pytest` et `uv run ruff check` passent avant de proposer un commit
- Utiliser `gh` pour toutes les interactions GitHub (issues, PRs, milestones)
- Ne jamais commiter de secrets (`.env`, clés API) — vérifier le `.gitignore`
- Respecter les conventional commits sans exception
- En cas de doute sur une décision d'architecture, consulter `docs/architecture-*.md`

## Branches d'archive

Les branches `archive/prototype-v1-windsurf` et `archive/prototype-v2-mcp` contiennent les anciens prototypes du projet. Elles sont là pour référence historique — ne pas y pousser de code.

## Licence

MIT — voir [LICENSE](LICENSE).
