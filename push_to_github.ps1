# Script PowerShell pour pousser les fichiers locaux vers GitHub
# Auteur: Claude
# Date: 20/03/2025

# Configuration
$repoUrl = "https://github.com/Ghamrifati/equity-portfolio-tracker.git"
$branch = "main"  # ou "master" selon la branche par défaut

# Vérifier si Git est installé
try {
    $gitVersion = git --version
    Write-Host "Git est installé: $gitVersion"
} catch {
    Write-Host "Erreur: Git n'est pas installé ou n'est pas dans le PATH." -ForegroundColor Red
    Write-Host "Veuillez installer Git depuis https://git-scm.com/downloads" -ForegroundColor Red
    exit 1
}

# Vérifier si le répertoire est déjà un dépôt Git
if (-not (Test-Path -Path ".git")) {
    Write-Host "Initialisation du dépôt Git local..." -ForegroundColor Yellow
    git init
    
    Write-Host "Ajout du dépôt distant..." -ForegroundColor Yellow
    git remote add origin $repoUrl
} else {
    Write-Host "Le répertoire est déjà un dépôt Git." -ForegroundColor Green
    
    # Vérifier si le remote origin existe déjà
    $remoteExists = git remote -v | Select-String -Pattern "origin"
    if (-not $remoteExists) {
        Write-Host "Ajout du dépôt distant..." -ForegroundColor Yellow
        git remote add origin $repoUrl
    } else {
        Write-Host "Le dépôt distant est déjà configuré." -ForegroundColor Green
    }
}

# Ajouter tous les fichiers
Write-Host "Ajout de tous les fichiers au suivi Git..." -ForegroundColor Yellow
git add .

# Demander un message de commit
$commitMessage = Read-Host "Entrez un message de commit (ou appuyez sur Entrée pour utiliser 'Mise à jour du projet')"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Mise à jour du projet"
}

# Créer un commit
Write-Host "Création d'un commit avec le message: '$commitMessage'..." -ForegroundColor Yellow
git commit -m $commitMessage

# Vérifier si le dépôt distant existe et contient des commits
$remoteExists = git ls-remote --heads origin $branch 2>$null
if ($remoteExists) {
    Write-Host "Le dépôt distant contient déjà des commits." -ForegroundColor Yellow
    Write-Host "Options disponibles:" -ForegroundColor Yellow
    Write-Host "1. Récupérer les modifications distantes et fusionner (git pull)" -ForegroundColor Cyan
    Write-Host "2. Forcer l'envoi des modifications locales (écrase les modifications distantes)" -ForegroundColor Red
    Write-Host "3. Annuler l'opération" -ForegroundColor Green
    
    $choice = Read-Host "Entrez votre choix (1, 2 ou 3)"
    
    switch ($choice) {
        "1" {
            Write-Host "Récupération et fusion des modifications distantes..." -ForegroundColor Yellow
            git pull origin $branch
            if ($LASTEXITCODE -ne 0) {
                Write-Host "Erreur lors de la récupération des modifications. Résolvez les conflits avant de continuer." -ForegroundColor Red
                exit 1
            }
            
            Write-Host "Envoi des modifications vers GitHub..." -ForegroundColor Yellow
            git push -u origin $branch
        }
        "2" {
            Write-Host "ATTENTION: Vous allez écraser les modifications distantes!" -ForegroundColor Red
            $confirm = Read-Host "Êtes-vous sûr? (o/n)"
            if ($confirm -eq "o" -or $confirm -eq "O") {
                Write-Host "Envoi forcé des modifications vers GitHub..." -ForegroundColor Yellow
                git push -u origin $branch --force
            } else {
                Write-Host "Opération annulée." -ForegroundColor Green
                exit 0
            }
        }
        "3" {
            Write-Host "Opération annulée." -ForegroundColor Green
            exit 0
        }
        default {
            Write-Host "Choix non valide. Opération annulée." -ForegroundColor Red
            exit 1
        }
    }
} else {
    # Pousser les modifications vers GitHub (premier push)
    Write-Host "Envoi des modifications vers GitHub..." -ForegroundColor Yellow
    git push -u origin $branch
}

# Vérifier le résultat
if ($LASTEXITCODE -eq 0) {
    Write-Host "Les modifications ont été envoyées avec succès vers GitHub!" -ForegroundColor Green
    Write-Host "URL du dépôt: $repoUrl" -ForegroundColor Green
} else {
    Write-Host "Une erreur s'est produite lors de l'envoi des modifications." -ForegroundColor Red
    Write-Host "Vérifiez vos identifiants GitHub et votre connexion internet." -ForegroundColor Red
}
