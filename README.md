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
