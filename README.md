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

### Creation d'environement et installation des dependance

Il est recommandé d’utiliser un environement virtuel.Et d'installer les dépendances.

#### Création d’un environement virtuel
Pour créer un environemment de taper la commande suivante dans le terminal

```bash
python -m venv venv
```
##### Activation de l’environnement
Pour activer l'environement une installer de taper cette commande selon votre type de pc :

Windows :
```bash
venv\Scripts\activate
```
---

Mac / Linux :
```bash
source venv/bin/activate
```
---
Une fois activé, le nom de l’environnement (venv) apparaît généralement dans le terminal, ce qui indique que toutes les installations de packages se feront uniquement dans cet environnement isolé, protégeant ainsi votre système et vos autres projets.

### Installation des packages nécessaires
Installer des packages selon le type de projets a faire dans le cas de se projets j'ai installer pandas, pymongo, et python-dotenv.


##### Pandas (lecture et transformation des CSV)
Pandas elle permet de  manipuler et analyser des données tabulaires de manière rapide et efficace.
```bash
pip install pandas
```
Vérifier l’installation :

```bash
python -c "import pandas as pd; print(pd.__version__)"
```
##### PyMongo (connexion à MongoDB)
pymongo : bibliothèque Python pour connecter et manipuler des bases de données MongoDB directement depuis Python.
```bash
pip install pymongo==4.7.2
```
Vérifier :
```bash
python -c "import pymongo; print(pymongo.__version__)"
```
##### Python Dotenv (gestion des variables d’environnement)
python-dotenv : bibliothèque Python pour gérer facilement les variables d’environnement depuis un fichier .env, sécurisant ainsi les informations sensibles et les configurations du projet.
```bash
pip install python-dotenv==1.0.1
```
Vérifier :

```bash
pip show python-dotenv
```

### Fichier requirements.txt

Créer un fichier `requirements.txt` .
Apres avoir installer les packages dans le terminal taper cette commande 
```bash 
pip freeze > requirements.txt
```
Elle va créer le fichier requirement et on retrouvera c'est information a l'intérieur 
```
pandas
pymongo==4.7.2
python-dotenv==1.0.1
```
Une fois le fichier créer 
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

 Aucune installation locale n’est nécessaire si Docker est utilisé.

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


## git Hub 
 deux branch sont créer un main et l'autre no-pandas 
 dans main j'utilise pandas dans no-pandas je n'utilise pas pandas pour changer de branch 
 ```bash 
 git checkout (suivi du nom de la branch )
 ```

# 4 Déroulement 
Projet 

```text
Projet
│
├─ script/                            # Dossier script du projet
│     ├─ automate.py                  #Fichier automate elle execute en même temps le test du fichier csv et  apres migration et test comparaison
│     ├─dictionnaire.py               #Définitions et mappings des champs
│     ├─test.py                       #Test fichier Csv avant migration 
│     ├─migration.py                  #Mirgartion csv vers mongodb
│     ├─testmigration.py              #Test apres migration
│     └─ testcomapre.py               #Test de comparaison entre csv et mongodb
├─ data/                              #Dossier contenant la data
│  └─ healthcare_dataset.csv          #le fichier csv
├─test/                               #Dossier Crud 
│     ├─create.py                     #Create permet de créer des contenu
│     ├─update.py                     #Update mettre a jour les contenu
│     └─delete.py                     #Delete supprimer les contenu
├─docker-compoase.yml                 #Configuration Docker Compose
├─dockerfile                          #Fichier Docker pour l’image du projet
├─ .env                               #Variables d’environnement local
├─ .env.docker                        #Variables d’environnement pour docker
└─ requirements.txt                   #Liste des dépendances Python
```
## Création du fichier `.env`

Créer un fichier `.env` à la racine du projet se fichier permettra d'avoir des variable pour les script retrouver un exemple dans le projet et ou voici un exemple.
---
MONGO_USER=votre nom 
MONGO_PASSWORD=votre mot passe 
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DB_NAME=votre nom de la base
MONGO_COLLECTION= votre nom de collection 
CSV_FILE=data/healthcare_dataset.csv
---
## Script
Dans le dossier **script** elle est composé de:
   1.Automate.py: Elle permet une fois éxécuter de lancer en simultanément le fichier test.py , testmigration.py et testcompare.py
   2.dictionnaire.py : Il permet de générer dynamiquement la structure attendue d’un fichier CSV
   3.test.py : vérifie la conformité des colonnes, des types de données, des valeurs manquantes, des doublons et la validité des âges avant toute migration vers la base de données.
   4.migration.py : Permet de vers la migration vers mongodb
   5.testmigration.py : vérifie l’intégrité des documents stockés (présence des champs attendus, types de données, valeurs manquantes, doublons et validité des âges) afin de garantir la conformité des données après migration.
   6.testcompare.oy:  compare les données sources et les données migrées (structure, nombre de lignes, colonnes et contenu détaillé) afin de valider l’intégrité complète de la migration.

Pour éxécuter les script il faut que l'environement est activé une fois activé on peux lancer le script avec la commande 
```bash 
python script/nom_ du_script.py
```
Pour la partie  automate.py elle permet de lancer les script en mm temps au lieu de faire individuel elle a pour but de faire le script test , testmigration, testcompoare 
```bash 
python script/nom_ du_script.py
```
## Crud
Pour le crud elle se trouve dans le dossier test, elle contient 

## Docker
### Creation D'environement .env.docker 
Créer un fichier `.env.docker` à la racine du projet. Ce fichier permet de définir les variables d’environnement utilisées par les services Docker
---
MONGO_USER=votre nom 
MONGO_PASSWORD=votre mot passe 
MONGO_HOST=mongo
MONGO_PORT=27017
MONGO_DB_NAME=votre nom de la base
MONGO_COLLECTION= votre nom de collection 
CSV_FILE=data/healthcare_dataset.csv
---
### Déroulement Docker
Creation de **dockerfile**.Le Dockerfile permet de construire l’image Docker de l’application Python.
**Docker Compose** coordonne la base MongoDB et le script de migration pour exécuter le projet dans un environnement conteneurisé.
Une fois créer les fichier dockerfile et docker-compose.ymml pour réaliser le projet voici les commande:

Perme de créer le volume 
```bash
docker volume create mongo_data
```
Permet de véerifier si le volume est bien créer 
```bash
docker volume ls
```
Lancement d'installation et execution du container 
```bash
docker-compose up -d --build
```
Lancement du projet dans docker ne pas pas oublier de remplacer -u **** par votre nom et -p **** par votre mot passe renseigné dans votre .env.docker
```bash
docker exec -it mongodb_docker mongosh -u **** -p ****
```
test sur docker 
vérification de tables 
```bash
show dbs
```
Vérification de la table  
```bash
test> use healthcare
```
Vérification des collection 
```bash
test> show collections
```
Vérification des collection 
```bash
test> db.getCollectionNames().
```
test de la collection 
```bash
db.ma_collection.find().limit(5)
```
en cas de bug cette commande permet de voir
Vérifier que le conteneur est actif :
```bash
docker ps
```