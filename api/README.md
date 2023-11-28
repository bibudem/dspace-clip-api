# dspace-clip-api / Dossier api


# API d'Indexation et Recherche d'Images

Cette API permet l'indexation, la recherche, la mise à jour et la suppression d'images à l'aide du modèle CLIP.

## Démarrage de l'API FastAPI

1. **Démarrer le serveur CLIP :**
   - Assurez-vous d'être dans le répertoire du serveur où se trouve le fichier `flow_api.yml`.
   - Exécutez la commande suivante dans votre terminal : `python -m clip_server flow_api.yml`

2. **Lancer l'API FastAPI :**
   - Assurez-vous d'être dans le répertoire de l'application où se trouve le fichier `app.py`.
   - Exécutez la commande suivante dans votre terminal : `uvicorn app:app --reload`

   L'option `--reload` permet un rechargement automatique de l'API lors de la modification du code. Veillez à laisser le terminal ouvert pendant l'utilisation de l'API.

## Accès à l'API

Une fois l'API démarrée, vous avez deux options pour accéder à la documentation interactive et explorer les fonctionnalités :

1. **Swagger - Interface Interactive :**
   - Ouvrez votre navigateur et visitez l'URL [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

2. **ReDoc - Documentation Visuelle :**
   - Accédez à l'interface ReDoc en visitant l'URL [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

## Utilisation de l'API

Une fois l'API démarrée, vous pouvez utiliser les points de terminaison définis dans votre application FastAPI, tels que `/search` et `/index`. Consultez la section "Fonctionnalités" dans le fichier README pour des exemples d'appels CURL.

## Arrêt de l'API

Pour arrêter l'API, vous pouvez interrompre le processus en cours d'exécution. Dans le terminal, utilisez la combinaison de touches `Ctrl + C`. Assurez-vous de faire cela dans le terminal où vous avez lancé l'API.


## Fonctionnalités

### Indexation d'Images

#### Endpoint : `POST /{id}`

Cette route permet d'indexer une image en spécifiant les paramètres suivants :

- `collectionId` : ID de la collection (optionnel)
- `id` : ID de l'objet (optionnel)
- `uuid` : UUID de l'objet (optionnel)
- `name` : Nom de l'objet (optionnel)
- `handle` : Handle de l'objet (optionnel)
- `url` : URL de l'image (obligatoire)

L'indexation est effectuée en extrayant les informations pertinentes de l'URL de l'image et en les associant à l'objet.

Exemple d'appel CURL :

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"itemId\": \"0505\",\"uuid\": \"10505\", \"itemHandle\": \"12345/0505\", \"itemName\": \"Raiatea depuis un motu\", \"collectionId\": \"exemples\", \"url\": \"../utils/img/IMG_0505.jpeg\"}" http://localhost:8000/0505

curl -X POST -H "Content-Type: application/json" -d "{\"itemId\": \"0734\",\"uuid\": \"10734\", \"itemHandle\": \"12345/0734\", \"itemName\": \"Raiatea depuis un motu\", \"collectionId\": \"exemples\", \"url\": \"../utils/img/IMG_0734.jpeg\"}" http://localhost:8000/0734

curl -X POST -H "Content-Type: application/json" -d "{\"itemId\": \"0777\",\"uuid\": \"10777\", \"itemHandle\": \"12345/0777\", \"itemName\": \"Raiatea depuis un motu\", \"collectionId\": \"exemples2\", \"url\": \"../utils/img/IMG_0777.jpeg\"}" http://localhost:8000/0777

curl -X POST -H "Content-Type: application/json" -d "{\"itemId\": \"2015\",\"uuid\": \"12015\", \"itemHandle\": \"12345/2015\", \"itemName\": \"Raiatea depuis un motu\", \"collectionId\": \"exemples2\", \"url\": \"../utils/img/IMG_2015.jpeg\"}" http://localhost:8000/2015
```

### Recherche d'Images

#### Endpoint : `GET /search`

Cette route permet de rechercher des images en spécifiant les paramètres suivants :

- `query` : Requête de recherche (optionnel)
- `url` : URL de l'image à rechercher (optionnel)
- `scope` : Champ de recherche (optionnel)
- `size` : Nombre de résultats à retourner (par défaut : 10)

L'API retourne les résultats sous forme de JSON contenant les informations pertinentes sur les images correspondant à la requête.

Exemple d'appel CURL :

```bash
curl -X GET "http://localhost:8000/search?query=paysage&size=5" -H "accept: application/json"

```
### Suppression

#### Endpoint: `DELETE /{itemId}`
Cette route vous permet de supprimer une index d'une image en spécifiant l'itemId dans l'URL.

Exemple d'appel CURL :

```bash
curl -X DELETE "http://localhost:8000/votre_item_id" -H "accept: application/json"
```
### Mise à jour
#### Endpoint: `PUT /update`
Cette route vous permet de mettre à jour un index d'une image en fournissant les informations mises à jour à l'aide du modèle Image.

Exemple d'appel CURL :
```bash
curl -X PUT "http://localhost:8000/update" -H "accept: application/json" -H "Content-Type: application/json" -d '{"itemId": "votre_item_id", "uuid": "votre_uuid", "itemHandle": "votre_handle", "itemName": "votre_nom", "collectionId": "votre_collection_id", "url": "votre_url_mise_a_jour"}'
```


## Configuration

La configuration de l'API est gérée via le fichier `config.json` situé dans le répertoire `utils/config/`. Vous pouvez spécifier l'URL du serveur CLIP et définir la limite de résultats à retourner.


Dans le fichier `config.json`, vous pouvez ajuster les valeurs selon vos besoins. Cela offre une flexibilité totale pour configurer l'API en fonction de votre environnement et de vos préférences.

