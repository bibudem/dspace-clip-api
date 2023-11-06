# Importations de modules
from clip_client import Client
from docarray import Document
from fastapi import FastAPI, Query,Request, HTTPException
from fastapi.responses import JSONResponse
from urllib.parse import urlparse
import os
import requests
import time
import json

# Initialisation de FastAPI
app = FastAPI()

# Lecture des configurations depuis le fichier JSON
with open('../utils/config/config.json') as config_file:
    config = json.load(config_file)

# Initialisation du client CLIP
client = Client(config['clip_server'])
limit = config['limit']

# Route principale de l'API
@app.get("/")
async def read_root():
    return {"projet": "dspace-clip-api"}

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

@app.get("/index")
async def indexation(
    collectionId: str = Query(None),
    url: str = Query(None),
    id: str = Query(None),
    uuid: str = Query(None),
    name: str = Query(None),
    handle: str = Query(None)
):
    try:
        if not url:
            raise HTTPException(status_code=400, detail="Veuillez fournir une URL.")

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

        return {"indexation": "réalisée", "file_name": file_name}
    except Exception as e:
        # Vous pouvez traiter l'exception ici, par exemple, la journaliser ou renvoyer un message d'erreur personnalisé.
        return {"error": str(e)}



