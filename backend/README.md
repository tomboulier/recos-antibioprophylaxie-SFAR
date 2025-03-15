# Backend Antibioprophylaxie SFAR

Ce package contient le backend de l'application Antibioprophylaxie SFAR.

Le backend est développé en Python avec FastAPI et suit les principes de l'architecture hexagonale (Clean Architecture).

## Structure du projet

```
backend/
├── domaine/             # Couche domaine - logique métier (en français)
├── application/         # Couche application - cas d'utilisation
├── infrastructure/      # Couche infrastructure - adaptateurs techniques
├── presentation/        # Couche présentation - interface API
├── tests/               # Tests unitaires et d'intégration
└── pyproject.toml       # Configuration du package
```

## Installation

Voir le README principal à la racine du projet.
