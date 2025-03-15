# Application de Recommandations d'Antibioprophylaxie SFAR

Une application web et mobile pour aider les anesthésistes à trouver la bonne antibioprophylaxie selon les recommandations de la Société Française d'Anesthésie et de Réanimation (SFAR).

## Présentation

Cette application a pour objectif de faciliter l'accès et la consultation des recommandations officielles de la SFAR concernant l'antibioprophylaxie en chirurgie et médecine interventionnelle. Elle permet aux anesthésistes et autres professionnels de santé de trouver rapidement les protocoles d'antibioprophylaxie adaptés à chaque type d'intervention chirurgicale.

## Architecture

Le projet suit les principes de la Clean Architecture (Architecture Hexagonale) :

- **Domaine** : Le cœur métier de l'application, contenant les entités et règles métier sans dépendances extérieures
- **Application** : Les cas d'utilisation orchestrant les opérations métier
- **Infrastructure** : Les adaptateurs techniques pour la persistance et l'API
- **Présentation** : L'interface utilisateur

### Technologies utilisées

- **Backend** : Python avec FastAPI
- **Frontend** : React Native Web avec TypeScript
- **Base de données** : SQLite (développement) / PostgreSQL (production)
- **Documentation** : MkDocs Material

## Structure du projet

```
antibioprophylaxie-sfar/
├── backend/                 # Backend Python avec FastAPI
│   ├── domaine/             # Cœur métier (en français)
│   ├── application/         # Cas d'utilisation
│   ├── infrastructure/      # Adaptateurs techniques
│   └── presentation/        # Interface API
├── frontend/                # Frontend React Native Web
│   ├── src/
│   ├── ios/
│   ├── android/
│   └── web/
└── docs/                    # Documentation
```

## Installation

Instructions pour l'installation à venir...

## Développement

Instructions pour le développement à venir...

## Licence

Ce projet est développé à des fins éducatives et de recherche.

## Références

- Recommandations Formalisées d'Experts - SFAR
