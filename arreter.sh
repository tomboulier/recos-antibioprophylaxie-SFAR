#!/bin/bash

# Script d'arrêt pour l'application Antibioprophylaxie SFAR

# Couleurs pour les messages
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

PROJECT_PATH=$(pwd)

echo -e "${RED}Arrêt de l'application Antibioprophylaxie SFAR...${NC}"

# Arrêter le backend
if [ -f "$PROJECT_PATH/.backend.pid" ]; then
    BACKEND_PID=$(cat "$PROJECT_PATH/.backend.pid")
    if ps -p $BACKEND_PID > /dev/null; then
        echo "Arrêt du backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        rm "$PROJECT_PATH/.backend.pid"
    else
        echo "Le processus backend n'est pas en cours d'exécution."
    fi
else
    echo "Aucun fichier PID trouvé pour le backend."
fi

# Arrêter le frontend
if [ -f "$PROJECT_PATH/.frontend.pid" ]; then
    FRONTEND_PID=$(cat "$PROJECT_PATH/.frontend.pid")
    if ps -p $FRONTEND_PID > /dev/null; then
        echo "Arrêt du frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        rm "$PROJECT_PATH/.frontend.pid"
    else
        echo "Le processus frontend n'est pas en cours d'exécution."
    fi
else
    echo "Aucun fichier PID trouvé pour le frontend."
fi

# Tuer tous les processus uvicorn et vite qui pourraient être restés en cours d'exécution
echo "Nettoyage des processus restants..."
pkill -f uvicorn || true
pkill -f vite || true

echo -e "${GREEN}Application arrêtée avec succès !${NC}"
