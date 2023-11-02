# Importations de modules
from clip_client import Client
from docarray import Document
from fastapi import FastAPI, Query,Request, HTTPException
from fastapi.responses import JSONResponse
from configparser import ConfigParser
from urllib.parse import urlparse
import os
import requests
import time
import json

# Initialisation de FastAPI
app = FastAPI()

# Lecture des configurations depuis le fichier INI
config = ConfigParser()
config.read('../utils/config/config.ini')
client = Client(config['app']['CLIP_SERVER'])
limit = int(config['app']['LIMIT'])

# Route principale de l'API
@app.get("/")
async def read_root():
    return {"projet": "api-dspace-clip"}

# Route de recherche
@app.get("/search")
async def search(
    query: str = Query(None),
    url: str = Query(None),
    scope: str = Query(None),
    size: int = Query(10)
):
    # Vérification des paramètres
    if not query and not url:
        raise HTTPException(status_code=400, detail="Veuillez fournir une requête ou une URL d'image.")

    # Initialisation de la structure de réponse
    content = {
        "query": query,
        "url": url,
        "scope": scope,
        "_embedded": {
            "searchResult": {
                "_embedded": {
                    "_embedded": {
                        "indexableObject": []
                    }
                }
            }
        }
    }

    # Recherche par requête
    if query:
        if scope:
            filter_add = {"collectionId": {"$eq": scope}}
            search_result = client.search([query], parameters={"filter": filter_add}, limit=size)
        else:
            search_result = client.search([query], limit=size)
        results = search_result[0].matches
        search_object(results, content)

    # Recherche par URL
    if url:
        if scope:
            filter_add = {"collectionId": {"$eq": scope}}
            search_result = client.search([url], parameters={"filter": filter_add}, limit=size)
        else:
            search_result = client.search([url], limit=size)
        results = search_result[0].matches
        search_object(results, content)

    return content

# Fonction de traitement des résultats de recherche
def search_object(results, content):
    for result in results:
        cosine_value = round(result.scores.get('cosine').value, 2)
        image_name = os.path.basename(result.uri) if result.uri else ''

        item = {
            "id": result.id,
            "uuid": result.tags.get('itemid', ''),
            "name": result.tags.get('itemName', ''),
            "handle": result.tags.get('itemHandle', ''),
            "_embedded": {
                "image": {
                    "id": result.id,
                    "uuid": result.id,
                    "Score": cosine_value,
                    "name": image_name
                }
            }
        }

        if 'collectionId' in result.tags:
            item["_embedded"]["scope"] = result.tags['collectionId']

        content["_embedded"]["searchResult"]["_embedded"]["_embedded"]["indexableObject"].append(item)

# Route d'indexation d'images
@app.get("/index")
async def indexation(
    collectionId: str = Query(None),
    url: str = Query(None),
    id: str = Query(None),
    uuid: str = Query(None),
    name: str = Query(None),
    handle: str = Query(None)
):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']  # Liste des extensions d'images acceptées
    if url and any(url.endswith(ext) for ext in image_extensions):
        image_path = urlparse(url).path

        # Extraction du nom du dossier et du fichier
        folder_name, file_name = os.path.split(image_path)

        # Création d'un document avec les balises associées
        document = Document(uri=image_path)
        document.tags['collectionId'] = str(collectionId) if collectionId else ''
        document.tags['itemid'] = str(id) if id else ''
        document.tags['itemHandle'] = str(handle) if handle else ''
        document.tags['itemName'] = str(name) if name else ''
        document.tags['fileName'] = str(file_name) if file_name else ''

        # Indexation du document
        client.index([document])

        return {"index": "ok", "folder_name": folder_name, "file_name": file_name}

    raise HTTPException(status_code=400, detail="L'URL fournie n'a pas une extension d'image valide.")

# Route d'indexation à partir d'un fichier JSON
@app.get("/index_from_json")
async def index_from_json():
    content = {}
    indexed_objects = []  # Liste pour stocker les objets indexés
    try:
        # Ouverture et lecture du fichier JSON
        with open('exemple.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Enregistrement du temps de début
        start_time = time.time()

        for objet in data['objets']:
            collectionId = objet['collectionId']
            id = objet['id']
            uuid = objet['uuid']
            name = objet['name']
            url = objet['url']

            # Appel de la méthode d'indexation
            await indexation(collectionId=collectionId, url=url, id=id, uuid=uuid, name=name)

            # Ajout des informations de l'objet indexé à la liste
            indexed_objects.append({
                "collectionId": collectionId,
                "id": id,
                "uuid": uuid,
                "name": name,
                "url": url
            })

        # Enregistrement du temps de fin
        end_time = time.time()

        # Calcul de la durée d'exécution
        execution_time = end_time - start_time

        content["temps"] = f"Temps d'exécution : {execution_time} secondes"
        content["message"] = f'Indexation terminée pour {len(data["objets"])} objets.'
        content["indexed_objects"] = indexed_objects  # Ajout des objets indexés aux résultats

        return JSONResponse(content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur : {e}")
