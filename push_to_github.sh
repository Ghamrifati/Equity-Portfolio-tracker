#!/bin/bash
# Script Bash pour pousser les fichiers locaux vers GitHub
# Auteur: Claude
# Date: 20/03/2025

# Configuration
REPO_URL="https://github.com/Ghamrifati/equity-portfolio-tracker.git"
BRANCH="main"  # ou "master" selon la branche par défaut

# Définir les couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Vérifier si Git est installé
if ! command -v git &> /dev/null; then
    echo -e "${RED}Erreur: Git n'est pas installé ou n'est pas dans le PATH.${NC}"
    echo -e "${RED}Veuillez installer Git avec votre gestionnaire de paquets.${NC}"
    exit 1
else
    echo -e "${GREEN}Git est installé: $(git --version)${NC}"
fi

# Vérifier si le répertoire est déjà un dépôt Git
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Initialisation du dépôt Git local...${NC}"
    git init
    
    echo -e "${YELLOW}Ajout du dépôt distant...${NC}"
    git remote add origin $REPO_URL
else
    echo -e "${GREEN}Le répertoire est déjà un dépôt Git.${NC}"
    
    # Vérifier si le remote origin existe déjà
    if ! git remote -v | grep -q "origin"; then
        echo -e "${YELLOW}Ajout du dépôt distant...${NC}"
        git remote add origin $REPO_URL
    else
        echo -e "${GREEN}Le dépôt distant est déjà configuré.${NC}"
    fi
fi

# Ajouter tous les fichiers
echo -e "${YELLOW}Ajout de tous les fichiers au suivi Git...${NC}"
git add .

# Demander un message de commit
echo -e "${YELLOW}Entrez un message de commit (ou appuyez sur Entrée pour utiliser 'Mise à jour du projet'):${NC}"
read COMMIT_MESSAGE
if [ -z "$COMMIT_MESSAGE" ]; then
    COMMIT_MESSAGE="Mise à jour du projet"
fi

# Créer un commit
echo -e "${YELLOW}Création d'un commit avec le message: '$COMMIT_MESSAGE'...${NC}"
git commit -m "$COMMIT_MESSAGE"

# Pousser les modifications vers GitHub
echo -e "${YELLOW}Envoi des modifications vers GitHub...${NC}"
git push -u origin $BRANCH

# Vérifier le résultat
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Les modifications ont été envoyées avec succès vers GitHub!${NC}"
    echo -e "${GREEN}URL du dépôt: $REPO_URL${NC}"
else
    echo -e "${RED}Une erreur s'est produite lors de l'envoi des modifications.${NC}"
    echo -e "${RED}Vérifiez vos identifiants GitHub et votre connexion internet.${NC}"
fi
