# Bienvenue sur DataViz Santé Publique 

# Introduction

Notre plateforme offre une exploration détaillée des données actualisées de 2015 à 2022, fournies par l’Assurance Maladie, couvrant un large éventail de pathologies, traitements chroniques et épisodes de soins. Conçue pour répondre aux besoins des mutuelles, professionnels de santé et acteurs engagés dans la gestion des soins et dépenses de santé, elle vous aide à prendre des décisions éclairées.


# Installation et Lancement du Projet
1. Cloner le dépôt

Clonez ce projet sur votre machine en exécutant la commande suivante :
   ```bash
   git clone https://github.com/salmabens/data-viz-sante-publique.git
   ```

Une fois le dépôt cloné, accédez au répertoire du projet :
   ```bash
   cd data-viz-sante-publique
   ```
2. Installation de Docker
   
Si Docker n'est pas encore installé sur votre machine, suivez ces étapes pour l'installer :
   ```bash
   sudo apt update
   sudo apt install docker.io
   ```
3. Construction de l'image Docker
   
Construisez l'image Docker en exécutant la commande suivante :
   ```bash
   docker build -t webapp:latest .
   ```
4. Lancer le conteneur

Exécutez l'application dans un conteneur Docker avec cette commande :
   ```bash
   docker run -p 5007:5007 webapp
   ```
