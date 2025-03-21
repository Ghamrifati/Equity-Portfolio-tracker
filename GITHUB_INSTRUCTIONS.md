# Instructions pour pousser le projet vers GitHub

Ce document explique comment utiliser les scripts fournis pour pousser votre projet local vers GitHub.

## Prérequis

1. Avoir Git installé sur votre ordinateur
   - Windows: Téléchargez et installez depuis [git-scm.com](https://git-scm.com/downloads)
   - macOS: Installez via Homebrew avec `brew install git` ou téléchargez depuis [git-scm.com](https://git-scm.com/downloads)
   - Linux: Utilisez votre gestionnaire de paquets (ex: `sudo apt install git` pour Ubuntu/Debian)

2. Avoir un compte GitHub et un dépôt créé
   - Le dépôt est déjà configuré: https://github.com/Ghamrifati/equity-portfolio-tracker.git

## Utilisation des scripts

### Pour Windows (PowerShell)

1. Ouvrez PowerShell dans le répertoire du projet
2. Exécutez le script:
   ```
   .\push_to_github.ps1
   ```
3. Si vous rencontrez une erreur de politique d'exécution, exécutez d'abord:
   ```
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```
   Puis réexécutez le script.

### Pour macOS/Linux (Bash)

1. Ouvrez un terminal dans le répertoire du projet
2. Rendez le script exécutable (uniquement la première fois):
   ```
   chmod +x push_to_github.sh
   ```
3. Exécutez le script:
   ```
   ./push_to_github.sh
   ```

## Que font ces scripts?

Les scripts effectuent les opérations suivantes:

1. Vérifient si Git est installé
2. Initialisent un dépôt Git local si nécessaire
3. Configurent le dépôt distant (GitHub)
4. Ajoutent tous les fichiers au suivi Git
5. Créent un commit avec votre message
6. Gèrent intelligemment l'envoi des modifications vers GitHub:
   - Si le dépôt distant est vide, les modifications sont envoyées directement
   - Si le dépôt distant contient déjà des commits, trois options sont proposées:
     * Récupérer les modifications distantes et les fusionner (git pull)
     * Forcer l'envoi des modifications locales (écrase les modifications distantes)
     * Annuler l'opération

### Gestion des conflits

Si le dépôt distant contient des modifications qui ne sont pas présentes localement, les scripts vous offrent plusieurs options:

1. **Option 1: Pull puis Push** - Cette option récupère d'abord les modifications distantes et les fusionne avec vos modifications locales avant de les pousser. C'est l'option la plus sûre si vous travaillez en équipe.

2. **Option 2: Force Push** - Cette option écrase les modifications distantes avec vos modifications locales. Utilisez cette option avec précaution, car elle peut entraîner la perte de modifications distantes.

3. **Option 3: Annuler** - Cette option annule l'opération sans envoyer vos modifications.

## Authentification GitHub

Lors de la première utilisation, Git vous demandera vos identifiants GitHub:

- **Méthode recommandée**: Configurez l'authentification par clé SSH ou un token d'accès personnel
- **Alternative**: Entrez votre nom d'utilisateur et mot de passe GitHub (si l'authentification par mot de passe est encore activée)

Pour plus d'informations sur l'authentification GitHub, consultez:
[Authentification GitHub](https://docs.github.com/fr/authentication)

## Fichiers exclus du suivi Git

Un fichier `.gitignore` a été créé pour exclure certains fichiers du suivi Git:
- Environnements virtuels (.venv, venv)
- Fichiers de cache Python (__pycache__, .pyc)
- Fichiers de configuration locaux (.env)
- Fichiers système (.DS_Store, Thumbs.db)
- Fichiers d'IDE (.vscode, .idea)

Si vous souhaitez exclure d'autres fichiers, modifiez le fichier `.gitignore`.
