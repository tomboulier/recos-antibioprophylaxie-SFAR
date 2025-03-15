FROM python:3.11-slim

WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code source
COPY . .

# Créer un script d'initialisation pour la base de données
RUN echo '#!/bin/bash\n\
set -e\n\
python -m infrastructure.database.db_initializer\n\
exec "$@"' > /entrypoint.sh \
    && chmod +x /entrypoint.sh

# Exposer le port sur lequel FastAPI s'exécute
EXPOSE 8000

# Utiliser le script d'initialisation comme point d'entrée
ENTRYPOINT ["/entrypoint.sh"]


# Commande pour démarrer l'application
CMD ["uvicorn", "infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
