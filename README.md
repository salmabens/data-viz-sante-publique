# Installation et Lancement du Projet
1. Cloner le dépôt

Clonez ce projet sur votre machine locale en exécutant la commande suivante :
   ```bash
   git clone https://github.com/hmnthy/mosef_app.git
   cd mosef_app
   ```
2. Installation de Docker
   
Si Docker n'est pas encore installé sur votre machine, suivez ces étapes pour l'installer :
   ```bash
   sudo apt update
   sudo apt install docker.io
   ```
3. Construction de l'image Docker
   
Accédez au répertoire cloné, puis construisez l'image Docker en exécutant la commande suivante :
   ```bash
   docker build -t webapp:latest .
   ```
4. Lancer le conteneur

Exécutez l'application dans un conteneur Docker avec cette commande :
   ```bash
   docker run -p 9090:9090 webapp
   ```
