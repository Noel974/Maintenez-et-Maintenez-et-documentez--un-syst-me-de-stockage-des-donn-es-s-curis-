# 📦 Migration de données médicales vers MongoDB (NoSQL)

---

#  Sommaire

1. Introduction  
2. Outils et technologies  
3. Installation  
4. Architecture du projet  
5. Processus de migration  
6. Déroulement détaillé de la migration  

---

# 1️ Introduction

## Contexte

Ce projet a pour objectif de migrer des données médicales stockées au format **CSV** vers une base de données **MongoDB (NoSQL)**.

L’entreprise dispose de plusieurs fichiers CSV contenant des informations médicales et souhaite :

- Centraliser les données
- Structurer les informations dans une base exploitable
- Automatiser le processus d’import
- Garantir la reproductibilité via Docker

---

## Objectif technique

- Lecture des fichiers CSV
- Transformation des données
- Reconstruction des relations métier
- Insertion dans MongoDB
- Conteneurisation complète avec Docker

---

#  Outils et technologies
