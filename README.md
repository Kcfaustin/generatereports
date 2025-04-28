Bot Telegram de Gestion de Tâches
Ce projet est un bot Telegram écrit en Python qui permet à un utilisateur autorisé d'ajouter des tâches à une feuille Google Sheets. Le bot extrait les tâches et les dates des messages, les formate, et les ajoute à une feuille Google Sheets avec une case à cocher, la date et la description de la tâche.

Fonctionnalités

Gestion des tâches : Envoyez un message au bot pour ajouter une tâche à une feuille Google Sheets.
Extraction de dates : Extrait automatiquement les dates au format jj/mm/aaaa des messages ou utilise la date actuelle si aucune date n'est fournie.
Autorisation : Seule une personne spécifique (définie par AUTHORIZED_USER_ID) peut interagir avec le bot.
Intégration Google Sheets : Ajoute les tâches à une feuille Google Sheets avec une case à cocher, la date et le texte de la tâche.
Configuration sécurisée : Utilise des variables d'environnement pour stocker les données sensibles comme les jetons API et les identifiants.

Prérequis

Python 3.8+ : Assurez-vous que Python est installé sur votre système.
Jeton Telegram : Obtenez un jeton via @BotFather sur Telegram.
Projet Google Cloud : Configurez un projet Google Cloud avec l'API Google Sheets activée et un compte de service avec des identifiants.
Feuille Google Sheets : Créez une feuille Google Sheets et partagez-la avec l'adresse e-mail du compte de service (provenant de credentials.json).
ID utilisateur Telegram : Obtenez votre ID Telegram via @userinfobot.

Installation

Cloner le dépôt :
git clone https://github.com/Kcfaustin/generatereports.git
cd generatereports


Installer les dépendances :Créez un environnement virtuel (facultatif) et installez les packages Python requis :
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
pip install -r requirements.txt


Configurer les variables d'environnement :Créez un fichier .env à la racine du projet ou définissez les variables d'environnement directement :
BOT_TOKEN=votre_jeton_bot
SPREADSHEET_ID=votre_id_feuille
AUTHORIZED_USER_ID=votre_id_telegram
GOOGLE_CREDENTIALS='{"type": "service_account", ...}'


Remplacez votre_jeton_bot par le jeton obtenu via @BotFather.
Remplacez votre_id_feuille par l'ID de votre feuille Google Sheets (trouvé dans l'URL : https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit).
Remplacez votre_id_telegram par votre ID Telegram.
Copiez le contenu JSON complet de credentials.json (du compte de service Google Cloud) dans GOOGLE_CREDENTIALS.


Exécuter le bot localement :
python reportsheet.py

Le bot démarre et affiche Bot démarré.... Testez-le en envoyant /start ou un message de tâche (par exemple, J'ai fait du sport 24/04/2025) à votre bot Telegram.


Structure du projet

reportsheet.py : Script principal du bot gérant les messages Telegram et l'intégration Google Sheets.
requirements.txt : Liste les dépendances Python.
Procfile : Spécifie la commande pour exécuter le bot lors du déploiement (par exemple, worker: python reportsheet.py).
.gitignore : Exclut les fichiers sensibles comme .env et credentials.json.
.env (non versionné) : Stocke les variables d'environnement pour les tests locaux.

Déploiement
Pour exécuter le bot 24/7, déployez-le sur une plateforme cloud. Les plateformes gratuites recommandées incluent :
Deta Space (Gratuit)

Installez l'outil CLI Deta :curl -fsSL https://get.deta.dev/space-cli.sh | sh


Connectez-vous :deta login


Définissez les variables d'environnement :deta env set BOT_TOKEN votre_jeton_bot
deta env set SPREADSHEET_ID votre_id_feuille
deta env set AUTHORIZED_USER_ID votre_id_telegram
deta env set GOOGLE_CREDENTIALS '{"type": "service_account", ...}'


Déployez :deta new
deta deploy


Vérifiez les logs :deta logs



Autres plateformes

Fly.io : Niveau gratuit avec 256 Mo de RAM et 3 Go de stockage (nécessite une carte bancaire).
Cyclic : Gratuit pour jusqu'à 10 000 requêtes API/mois.
Replit + UptimeRobot : Gratuit mais moins sécurisé pour les données sensibles.

Consultez les instructions détaillées de déploiement dans la section Déploiement ou la documentation de la plateforme.
Recommandations de sécurité

Utilisez des variables d'environnement : Ne codez jamais en dur les données sensibles (BOT_TOKEN, SPREADSHEET_ID, AUTHORIZED_USER_ID, GOOGLE_CREDENTIALS) dans le code.
Dépôt privé : Hébergez votre code dans un dépôt GitHub privé pour éviter toute exposition.
Permissions Google Sheets : Partagez la feuille Google Sheets uniquement avec l'adresse e-mail du compte de service de credentials.json.
Surveillez les logs : Vérifiez régulièrement les logs de votre plateforme d'hébergement pour détecter les erreurs ou les tentatives d'accès non autorisées.
Sécurisez GOOGLE_CREDENTIALS : Stockez le contenu JSON de credentials.json comme variable d'environnement plutôt que d'inclure le fichier dans le dépôt.

Utilisation

Démarrez le bot en envoyant /start à votre bot Telegram.
Envoyez un message de tâche, par exemple, J'ai fait du sport 24/04/2025 ou J'ai couru.
Le bot extrait la date (si fournie) ou utilise la date actuelle.
La tâche est formatée (par exemple, Fait du sport) et ajoutée à la feuille Google Sheets avec une case à cocher.


Le bot répond avec une confirmation, par exemple, Tâche ajoutée : Fait du sport (24/04/2025).

Dépannage

Le bot ne répond pas :
Vérifiez les logs de votre plateforme d'hébergement pour identifier les erreurs.
Assurez-vous que BOT_TOKEN est correct et que le bot est en ligne.
Vérifiez que les variables d'environnement sont correctement définies.


Erreurs Google Sheets :
Confirmez que le compte de service a un accès en écriture à la feuille Google Sheets.
Vérifiez que SPREADSHEET_ID et GOOGLE_CREDENTIALS sont valides.


Accès non autorisé :
Assurez-vous que AUTHORIZED_USER_ID correspond à votre ID Telegram.


Tests locaux :
Utilisez un fichier .env avec python-dotenv pour les tests locaux :pip install python-dotenv

Mettez à jour reportsheet.py pour charger .env :from dotenv import load_dotenv
load_dotenv()





Contribution
Les contributions sont les bienvenues ! Veuillez soumettre une pull request ou ouvrir une issue sur le dépôt.
Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
