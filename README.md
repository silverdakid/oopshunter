# OopsHunter - Application Web de détection de fuites de données

## Contexte du Projet

Il est important de noter que **OopsHunter est un projet universitaire** réalisé en groupe dans le cadre d'un projet de première année à Telecom Nancy. L'application a été développée en équipe, et les tâches ont été réparties entre les membres.

Ma contribution personnelle s'est concentrée sur les aspects suivants :

*   **Système d'authentification** : Mise en place de la logique de connexion et de la protection des routes.
*   **Logique d'analyse et rapports** : Développement du lien entre le backend et le frontend pour le traitement des analyses et l'affichage des rapports de fuites de données.
*   **Base de données** : Participation à la conception et à l'intégration de la base de données.
*   **Correctifs divers** : Application de multiples corrections sur l'ensemble du projet pour en assurer la stabilité.

---

OopsHunter est une application web conçue pour aider les entreprises à détecter les fuites de données sensibles au sein de leurs documents. Les utilisateurs peuvent téléverser des fichiers de divers formats (tels que `.pdf`, `.xlsx`, `.txt`, `.docx`) et obtenir en un clic des rapports d'analyse détaillés.

Le nom "OopsHunter" vient de l'idée de "chasser" (Hunter) les erreurs humaines ("Oops") qui mènent à la divulgation involontaire d'informations confidentielles.

## Fonctionnalités

*   **Analyse de documents** : Détecte une variété de données sensibles comme les numéros de carte bancaire, de téléphone, les adresses e-mail, etc.
*   **Rapports détaillés** : Génère des rapports clairs indiquant le type de données qui ont fuité et les données exactes concernées.
*   **Historique des analyses** : Conserve un historique de toutes les analyses effectuées pour un suivi aisé.
*   **Gestion des documents** : Permet de visualiser, filtrer, ajouter et supprimer les documents téléversés.
*   **Panneau d'administration** : Une section est dédiée à la gestion des informations des employés (utilisateurs), avec la possibilité de calculer un score de risque de fuite de données pour chacun.

## Explications Techniques

### Backend

L'application est développée avec le framework **Flask** en Python. La structure du projet est organisée en **Blueprints** pour séparer logiquement les différentes fonctionnalités (authentification, gestion des documents, analyses, etc.). Les requêtes à la base de données sont isolées dans un répertoire `queries/` et utilisent le module `sqlite3`.

Un système d'authentification simple basé sur les sessions Flask et un décorateur `@login_required` sécurise l'accès aux différentes parties de l'application.

### Base de Données

Nous utilisons **SQLite** comme système de gestion de base de données. Le schéma a été conçu pour être flexible, notamment grâce à une table `DATA_TYPE` qui permet d'ajouter de nouveaux types de données à rechercher (via des expressions régulières ou des mots-clés) sans avoir à modifier le code source de l'application.

### Algorithmes de Détection

Pour "chasser" les données sensibles, OopsHunter combine plusieurs techniques :

*   **Recherche par mots-clés** : Recherche des chaînes de caractères connues (noms, prénoms, etc.).
*   **Expressions Régulières** : Pour identifier des formats de données spécifiques comme les e-mails, IBAN, ou numéros de sécurité sociale.
*   **Bibliothèques spécialisées** :
    *   `phonenumbers` pour la détection et la validation de numéros de téléphone.
    *   L'algorithme de **Luhn** pour valider la syntaxe des numéros de carte bancaire.
*   **OCR** : La bibliothèque `pytesseract` est utilisée pour extraire le texte des fichiers PDF non lisibles nativement.

### Frontend

L'interface utilisateur est construite en **HTML** et stylisée avec le framework **Bootstrap** pour une expérience utilisateur simple et efficace.

## Comment exécuter le projet

### 1. Prérequis

*   Python 3.x
*   Pip
*   SQLite3
*   Tesseract OCR : Suivez la [documentation officielle](https://tesseract-ocr.github.io/tessdoc/Installation.html) pour l'installer sur votre système.

### 2. Installation

Clonez ce dépôt et naviguez dans le répertoire du projet :

```bash
git clone https://github.com/silverdakid/oopshunter.git
cd oopshunter
```

Créez et activez un environnement virtuel :

```bash
python -m venv venv
source venv/bin/activate
```
*Sur Windows, utilisez `venv\Scripts\activate`.*

Installez les dépendances nécessaires :

```bash
pip install -r requirements.txt
```

### 3. Base de données

Un fichier de base de données `oopshunter.db` est fourni pour les tests. Si vous devez (ré)initialiser la base de données, vous pouvez utiliser le fichier `backup.sql` avec la commande suivante :

```bash
sqlite3 oopshunter.db < bdd/backup.sql
```

### 4. Lancement de l'application

Lancez l'application avec Flask :

```bash
flask --app index run
```

L'application sera alors accessible à l'adresse [http://127.0.0.1:5000](http://127.0.0.1:5000).

### 5. Utilisation

Une fois l'application lancée, vous pouvez vous connecter avec les comptes de test suivants :

*   **Compte 1 :**
    *   **Email** : `antoine.delacroix@gmail.com`
    *   **Mot de passe** : `password`
*   **Compte 2 :**
    *   **Email** : `marie.dubois@gmail.com`
    *   **Mot de passe** : `securepass`

Vous pourrez ensuite :
1.  Ajouter un document à analyser.
2.  Cliquer sur le bouton "Analyze" pour lancer la détection.
3.  Consulter le résultat de l'analyse.
4.  Voir l'historique des analyses précédentes.
5.  Accéder à la partie administration pour gérer les comptes et les types de données sensibles.
