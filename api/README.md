# dspace-clip-api / Dossier api


# API d'Indexation et Recherche d'Images

Cette API permet l'indexation et la recherche d'images à l'aide du serveur CLIP.

## Démarrage de l'API FastAPI

Pour lancer l'API FastAPI, suivez ces simples :

1. **Assurez-vous d'être dans le répertoire de votre application où se trouve le fichier `app.py`.**

2. **Exécutez la commande suivante dans votre terminal :**

   ```bash
   uvicorn app:app --reload
   ```

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

#### Endpoint : `GET /index`

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
curl -X GET "http://localhost:8000/index?collectionId=_plage&id=0001&uuid=0001&name=Paysage%20ensoleill%C3%A9%20sur%20la%20plage&url=../utils/img/IMG_0505.jpeg" -H 'accept: application/json'

curl -X GET "http://localhost:8000/index?collectionId=_plage&id=0002&uuid=0002&name=Coquillages%20et%20coquillages%20sur%20le%20sable&url=../utils/img/IMG_0734.jpeg" -H 'accept: application/json'

curl -X GET "http://localhost:8000/index?collectionId=_plage&id=0003&uuid=0003&name=Surf%20sous%20les%20vagues%20de%20l%27Atlantique&url=../utils/img/IMG_0777.jpeg" -H 'accept: application/json'

curl -X GET "http://localhost:8000/index?collectionId=_soleil&id=0004&uuid=0004&name=Coucher%20de%20soleil%20sur%20l%27oc%C3%A9an&url=../utils/img/IMG_0963.jpeg" -H 'accept: application/json'

curl -X GET "http://localhost:8000/index?collectionId=_soleil&id=0006&uuid=0006&name=Famille%20construisant%20un%20ch%C3%A2teau%20de%20sable&handle=_handle_exemple&url=../utils/img/IMG_1682.jpeg" -H 'accept: application/json'
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

## Configuration

La configuration de l'API est gérée via le fichier `config.json` situé dans le répertoire `utils/config/`. Vous pouvez spécifier l'URL du serveur CLIP et définir la limite de résultats à retourner.


Dans le fichier `config.json`, vous pouvez ajuster les valeurs selon vos besoins. Cela offre une flexibilité totale pour configurer l'API en fonction de votre environnement et de vos préférences.

