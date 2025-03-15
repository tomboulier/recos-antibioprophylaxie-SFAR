#!/bin/bash

# Script de démarrage simple pour l'application Antibioprophylaxie SFAR
# Démarre à la fois le backend FastAPI et le frontend Vue.js

# Couleurs pour les messages
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Démarrage de l'application Antibioprophylaxie SFAR${NC}"

# Chemin absolu du projet
PROJECT_PATH=$(pwd)

# S'assurer que la base de données est initialisée avant de démarrer l'API
echo -e "${YELLOW}Initialisation de la base de données...${NC}"
cd "$PROJECT_PATH/backend" && python -m scripts.init_db

# Démarrer le backend en arrière-plan
echo -e "${BLUE}Démarrage du backend...${NC}"
cd "$PROJECT_PATH/backend" && \
python -m uvicorn infrastructure.api.main:app --reload --host 0.0.0.0 --port 8000 > "$PROJECT_PATH/backend.log" 2>&1 &
BACKEND_PID=$!

# Attendre un peu pour que le backend démarre
sleep 3

# Démarrer le frontend en arrière-plan
echo -e "${BLUE}Démarrage du frontend...${NC}"
cd "$PROJECT_PATH/frontend" && \
npm run dev > "$PROJECT_PATH/frontend.log" 2>&1 &
FRONTEND_PID=$!

# Enregistrer les PIDs pour pouvoir arrêter proprement
echo $BACKEND_PID > "$PROJECT_PATH/.backend.pid"
echo $FRONTEND_PID > "$PROJECT_PATH/.frontend.pid"

echo -e "${GREEN}Application démarrée avec succès !${NC}"
echo -e "${GREEN}Frontend: http://localhost:5173${NC}"
echo -e "${GREEN}Backend API: http://localhost:8000${NC}"
echo -e "${GREEN}Documentation API: http://localhost:8000/docs${NC}"
echo -e ""
echo -e "Logs du backend: ${BLUE}tail -f $PROJECT_PATH/backend.log${NC}"
echo -e "Logs du frontend: ${BLUE}tail -f $PROJECT_PATH/frontend.log${NC}"
echo -e "Pour arrêter l'application: ${BLUE}$PROJECT_PATH/arreter.sh${NC}"
