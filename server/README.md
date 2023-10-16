# dspace-clip-api / Dossier server

Ce dossier contient des fichiers de configuration pour exécuter un serveur clip-as-service et Ann lite.

La description de chaque configuration se trouve en commentaires dans les fichiers.

## Pour exécuter un serveur

# Instructions pour Exécuter le Fichier Flow

Ce fichier `flow.yml` contient les configurations pour le flux de travail. Voici les étapes pour l'exécuter :

1. **Installer les Dépendances**

Assurez-vous d'installer les dépendances nécessaires en exécutant les commandes suivantes :

      pip install clip_server
      pip install annlite


2. **Exécution du Fichier Flow**

Utilisez la commande suivante pour exécuter le fichier flow et démarer clip-as-service:

python -m clip_server flow.yml


3. **Accès au Serveur**

Une fois le flux exécuté avec succès, le serveur sera accessible via différents protocoles (gRPC, HTTP, WebSocket) aux ports spécifiés.

Par exemple, pour accéder au serveur gRPC, utilisez l'URL : `grpc://localhost:51000`.

N'hésitez pas à explorer le contenu du fichier `flow.yaml` pour plus de détails sur les configurations spécifiques.
