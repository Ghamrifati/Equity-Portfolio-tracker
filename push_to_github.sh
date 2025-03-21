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

# Vérifier si le dépôt distant existe et contient des commits
if git ls-remote --heads origin $BRANCH &> /dev/null; then
    echo -e "${YELLOW}Le dépôt distant contient déjà des commits.${NC}"
    echo -e "${YELLOW}Options disponibles:${NC}"
    echo -e "${GREEN}1. Récupérer les modifications distantes et fusionner (git pull)${NC}"
    echo -e "${RED}2. Forcer l'envoi des modifications locales (écrase les modifications distantes)${NC}"
    echo -e "${GREEN}3. Annuler l'opération${NC}"
    
    read -p "Entrez votre choix (1, 2 ou 3): " CHOICE
    
    case $CHOICE in
        1)
            echo -e "${YELLOW}Récupération et fusion des modifications distantes...${NC}"
            git pull origin $BRANCH
            if [ $? -ne 0 ]; then
                echo -e "${RED}Erreur lors de la récupération des modifications. Résolvez les conflits avant de continuer.${NC}"
                exit 1
            fi
            
            echo -e "${YELLOW}Envoi des modifications vers GitHub...${NC}"
            git push -u origin $BRANCH
            ;;
        2)
            echo -e "${RED}ATTENTION: Vous allez écraser les modifications distantes!${NC}"
            read -p "Êtes-vous sûr? (o/n): " CONFIRM
            if [ "$CONFIRM" = "o" ] || [ "$CONFIRM" = "O" ]; then
                echo -e "${YELLOW}Envoi forcé des modifications vers GitHub...${NC}"
                git push -u origin $BRANCH --force
            else
                echo -e "${GREEN}Opération annulée.${NC}"
                exit 0
            fi
            ;;
        3)
            echo -e "${GREEN}Opération annulée.${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Choix non valide. Opération annulée.${NC}"
            exit 1
            ;;
    esac
else
    # Pousser les modifications vers GitHub (premier push)
    echo -e "${YELLOW}Envoi des modifications vers GitHub...${NC}"
    git push -u origin $BRANCH
fi

# Vérifier le résultat
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Les modifications ont été envoyées avec succès vers GitHub!${NC}"
    echo -e "${GREEN}URL du dépôt: $REPO_URL${NC}"
else
    echo -e "${RED}Une erreur s'est produite lors de l'envoi des modifications.${NC}"
    echo -e "${RED}Vérifiez vos identifiants GitHub et votre connexion internet.${NC}"
fi
