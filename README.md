# Migration de données médicales vers MongoDB (NoSQL)

---
# Sommaire
1. [Introduction](#1-Introduction)
   - [Contexte](#Contexte)
   - [Objectif technique](#Objectif-technique)
2. [Outils et technologies](#outils-et-technologies)
3. [Installation et configuration](#2-Installatio-et-configuration)
   - [MongoDB](#mongodb)
   - [Python](#python)
   - [Docker](#docker)
   - [Variables d’environnement](#Variables-d-environnement)
4. [Déroulement](#4-deroulement)
   -[Script](#script)
   -[Crud](#crud)
   -[Docker](#docker)
---

# 1 Introduction

## Contexte

Ce projet a pour objectif de migrer des données médicales initialement stockées au format **CSV** vers une base de données **MongoDB (NoSQL)**.

L’entreprise dispose de plusieurs fichiers CSV contenant des informations médicales (patients, consultations, traitements, etc.) et souhaite :

- Centraliser l’ensemble des données dans une base unique
- Structurer les informations pour une meilleure exploitation
- Optimiser les performances d’accès aux données
- Automatiser le processus d’import
- Garantir la reproductibilité du projet grâce à Docker

Cette migration permet de passer d’un stockage statique (CSV) à une base de données flexible, évolutive et adaptée aux besoins métier.

---

## Objectif technique

Le projet repose sur plusieurs étapes techniques :

- Lecture et analyse des fichiers CSV
- Nettoyage et transformation des données
- Reconstruction des relations métier (liaisons patients, actes médicaux, etc.)
- Insertion des documents dans MongoDB
- Mise en place d’un environnement isolé et reproductible avec Docker

L’objectif est d’obtenir une base MongoDB cohérente, structurée et prête à être exploitée.

---

# 2 Outils et technologies

Le projet s’appuie sur les technologies suivantes :

- **MongoDB** — Base de données NoSQL orientée document
- **Python** — Traitement, transformation et import des données
- **Pandas** — Manipulation des fichiers CSV
- **PyMongo** — Connexion Python ↔ MongoDB
- **Docker** — Conteneurisation de l’environnement
- **MongoDB Compass** — Interface graphique pour visualiser les données

---

# 3 Installation et configuration

Cette section décrit les prérequis nécessaires pour exécuter la migration ainsi que la configuration de l’environnement.

---
## Python
Python est utilisé pour lire, transformer et insérer les données dans MongoDB.

### Installation Python
Télécharger Python depuis le site officiel :

https://www.python.org/downloads/

Vérifier l’installation :

```bash
python --version
```

ou

```bash
python3 --version
```

---

### Installation des dépendances

Il est recommandé d’utiliser un environnement virtuel.

#### Création d’un environnement virtuel

```bash
python -m venv venv
```

#### Activation de l’environnement

Windows :

```bash
venv\Scripts\activate
```

Mac / Linux :

```bash
source venv/bin/activate
```

---

### Installation des packages nécessaires

#### Pandas (lecture et transformation des CSV)

```bash
pip install pandas
```

Vérifier l’installation :

```bash
python -c "import pandas as pd; print(pd.__version__)"
```

---

#### PyMongo (connexion à MongoDB)

```bash
pip install pymongo==4.7.2
```

Vérifier :

```bash
python -c "import pymongo; print(pymongo.__version__)"
```

---

#### Python Dotenv (gestion des variables d’environnement)

```bash
pip install python-dotenv==1.0.1
```

Vérifier :

```bash
pip show python-dotenv
```

---

### Fichier requirements.txt

Créer un fichier `requirements.txt` :

```
pandas
pymongo==4.7.2
python-dotenv==1.0.1
```

Installer toutes les dépendances :

```bash
pip install -r requirements.txt
```

---

## MongoDB

MongoDB est la base de données utilisée pour stocker les données médicales après transformation.

Dans ce projet, MongoDB est exécuté via **Docker**, ce qui permet :

- Une installation simplifiée
- Une isolation complète de l’environnement
- Une reproductibilité sur n’importe quelle machine
- Une suppression facile sans impact système

👉 Aucune installation locale n’est nécessaire si Docker est utilisé.

### Installation locale (optionnelle)

Si vous souhaitez installer MongoDB en local :

1. Télécharger MongoDB Community Edition :  
   https://www.mongodb.com/try/download/community

2. Installer selon votre système d’exploitation

3. Vérifier l’installation :

```bash
mongod --version
```

### MongoDB Compass

Pour visualiser les données de manière graphique, installer **MongoDB Compass** :

https://www.mongodb.com/try/download/compass

---





## Docker

Docker permet de lancer MongoDB dans un conteneur isolé.
apres avoir installer docker creer le fichier dockerfile puis docker-compose.yml puis de executer les commande suivante
### Vérifier l’installation
```bash
docker --version 
```

```bash
docker volume create mongo_data
```
```bash
docker volume create csv_data
```
```bash
docker volume ls
```
```bash
docker-compose up -d
```
```bash
docker exec -it mongodb_docker mongosh -u Noel974 -p Emm@nuel974
```
test sur docker 
```bash
show dbs
```
```bash
test> use healthcare_db
```

```bash
db.ma_collection.find().limit(5)
```


Vérifier que le conteneur est actif :

```bash
docker ps
```

## git Hub 
 deux branch sont créer un main et l'autre no-pandas 
 dans main j'utilise pandas dans no-pandas je n'utilise pas pandas pour changer de branch 
 ```bash 
 git checkout (suivi du nom de la branch )
 ```

# 4 Déroulement

## Script
Pour les script il faut que l'environement est activé une fois activé on peux lancer le script avec la commande 
```bash 
python script/nom_ du_script.py
```
Dans le script il un fichier automate.py elle permet de lancer les script en mm temps au lieu de faire individuel elle a pour but de faire le script test , testmigration, testcompoare 
```bash 
python script/nom_ du_script.py
```
## Crud
Pour le crud elle se trouve dans le dossier test, elle contient 
## Docker

1. Lecture des fichiers CSV avec Pandas  
3. Transformation en dictionnaires Python  
4. Insertion des documents dans MongoDB  
5. Vérification via MongoDB Compass  

---

## Structure recommandée du projet

```
project/
│
├── data/                 # Fichiers CSV
├── src/                  # Scripts Python
├── .env                  # Variables d’environnement
├── requirements.txt
└── README.md
```

---

---

## Configuration des variables d’environnement (.env)

Afin de sécuriser les informations sensibles (identifiants, mot de passe, URI MongoDB), la connexion à MongoDB est configurée via un fichier `.env`.

Cette méthode permet :

- De ne pas exposer les identifiants dans le code source
- De faciliter la configuration selon l’environnement (développement, production)
- D’améliorer la sécurité du projet

---

### Création du fichier `.env`

Créer un fichier `.env` à la racine du projet :
Description des variables

MONGO_URI : Chaîne de connexion à MongoDB

MONGO_DB_NAME : Nom de la base de données cible

MONGO_COLLECTION : Nom de la collection dans laquelle les documents seront insérés


Le projet est maintenant prêt à être exécuté dans un environnement propre, isolé et reproductible.
 Dans le dossier test on retrouvera tous les test Crud d'ou un fichier Create.py, un udapte.py et delete.py
