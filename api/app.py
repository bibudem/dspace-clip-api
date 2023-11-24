# Importations de modules
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from clip_client_crud import ClientCrud
from docarray import Document
from grpc_health.v1 import health_pb2, health_pb2_grpc
import os
import json
import grpc

# Une classe pour représenter une image à indexer
class Image(BaseModel):
    itemId: str
    uuid: str
    itemHandle: str
    itemName: str
    collectionId: str
    url: str

# Initialisation de FastAPI
app = FastAPI()

# Chargement de la configuration depuis le fichier JSON
with open('config/config.json') as config_file:
    config = json.load(config_file)

# Initialisation du client CLIP et autres paramètres
client = ClientCrud(config['clip_server'])
limit = config['limit']
grpc_server = config['grpc_server']

# Fonction pour vérifier l'état du serveur gRPC
def check_grpc_server_status(server_address):
    try:
        channel = grpc.insecure_channel(server_address)
        health_stub = health_pb2_grpc.HealthStub(channel)

        # Définir un délai court pour la réponse (1 seconde dans cet exemple)
        response = health_stub.Check(health_pb2.HealthCheckRequest(), timeout=1)

        # Si la réponse est "SERVING", le serveur gRPC est en cours d'exécution
        return response.status == health_pb2.HealthCheckResponse.SERVING

    except grpc.RpcError as e:
        # Une erreur peut se produire si le serveur n'est pas en cours d'exécution
        return False

# Appeler la méthode check_grpc_server_status lors du démarrage de l'application
@app.on_event("startup")
async def startup_event():
    if not check_grpc_server_status(grpc_server):
        # Gérer l'erreur de connexion au serveur CLIP
        raise HTTPException(status_code=500, detail="Le serveur CLIP est indisponible. Veuillez réessayer plus tard.")

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

    try:
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
            filter_add = {"collectionId": {"$eq": scope}} if scope else {}
            search_result = client.search([query], parameters={"filter": filter_add}, limit=size)
            results = search_result[0].matches
            search_object(results, content)

        # Recherche par URL
        if url:
            filter_add = {"collectionId": {"$eq": scope}} if scope else {}
            search_result = client.search([url], parameters={"filter": filter_add}, limit=size)
            results = search_result[0].matches
            search_object(results, content)

        return content

    except Exception as e:
        # Autres erreurs non liées à la connexion gRPC
        raise HTTPException(status_code=400, detail="Une erreur inattendue s'est produite. Veuillez réessayer.")

# Fonction de traitement des résultats de recherche
def search_object(results, content):
    try:
        for result in results:
            cosine_value = round(result.scores.get('cosine').value, 2)
            image_name = os.path.basename(result.uri) if result.uri else ''

            item = {
                "id": result.id,
                "url": result.uri,
                "itemId": result.tags.get('itemId', ''),
                "uuid": result.tags.get('uuid', ''),
                "itemName": result.tags.get('itemName', ''),
                "itemHandle": result.tags.get('itemHandle', ''),
                "collectionId": result.tags.get('collectionId', ''),
                "_embedded": {
                    "image": {
                        "id": result.id,
                        "score": cosine_value,
                        "name": result.tags.get('itemName', '')
                    }
                }
            }

            if 'collectionId' in result.tags:
                item["_embedded"]["scope"] = result.tags['collectionId']

            content["_embedded"]["searchResult"]["_embedded"]["_embedded"]["indexableObject"].append(item)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Une erreur inattendue s'est produite. Veuillez réessayer.")

# Ajout d'une image
@app.post("/{id}")
async def indexation(image: Image):
    try:
        if not image.url:
            raise HTTPException(status_code=400, detail="Veuillez fournir un URL.")

        # Création d'un document avec les balises associées
        document = Document(uri=image.url, id=image.itemId)
        document.tags['collectionId'] = str(image.collectionId) if image.collectionId else ''
        document.tags['itemId'] = str(image.itemId) if image.itemId else ''
        document.tags['uuid'] = str(image.uuid) if image.uuid else ''
        document.tags['itemHandle'] = str(image.itemHandle) if image.itemHandle else ''
        document.tags['itemName'] = str(image.itemName) if image.itemName else ''

        # Indexation du document
        client.index([document])

        return {"indexation": "réalisée", "url": image.url}

    except Exception as e:
        raise HTTPException(status_code=400, detail="Une erreur inattendue s'est produite. Veuillez réessayer.")

# Suppression d'une image
@app.delete("/{itemId}")
async def suppression(itemId):
    try:
        # Utilisation de la méthode delete du client pour supprimer l'élément
        client.delete(itemId)
        return f"Suppression de l'image {itemId} réussie"

    except Exception as e:
        # Capturez les exceptions spécifiques dont vous avez besoin (ajoutez des exceptions selon vos besoins)
        raise HTTPException(status_code=500, detail=f"Une erreur s'est produite lors de la suppression de l'image {itemId}")
