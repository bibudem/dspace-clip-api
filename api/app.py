# Importations de modules
from clip_client_crud import ClientCrud
from docarray import Document
from fastapi import FastAPI, Query, HTTPException, Path
from urllib.parse import urlparse
import os
import json
import grpc
from grpc_health.v1 import health_pb2, health_pb2_grpc

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
    # Vérification de l'état du serveur gRPC
    if not check_grpc_server_status(grpc_server):
        # Gérer l'erreur de connexion au serveur CLIP
        raise HTTPException(status_code=500, detail="Le serveur CLIP est indisponible. Veuillez réessayer plus tard.")
    else:
        try:
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
                "idClip": result.id,
                "id": result.tags.get('itemid', ''),
                "uuid": result.tags.get('itemid', ''),
                "name": result.tags.get('itemName', ''),
                "handle": result.tags.get('itemHandle', ''),
                "_embedded": {
                    "image": {
                        "id": result.tags.get('itemid', ''),
                        "uuid": result.tags.get('itemid', ''),
                        "Score": cosine_value,
                        "name": image_name
                    }
                }
            }

            if 'collectionId' in result.tags:
                item["_embedded"]["scope"] = result.tags['collectionId']

            content["_embedded"]["searchResult"]["_embedded"]["_embedded"]["indexableObject"].append(item)
    except Exception as e:
       raise HTTPException(status_code=400, detail="Une erreur inattendue s'est produite. Veuillez réessayer.")

@app.post("/{id}")
async def indexation(
    id: int = Path(..., title="ID de l'image"),
    collectionId: str = Query(None),
    url: str = Query(None),
    uuid: str = Query(None),
    name: str = Query(None),
    handle: str = Query(None)
):
    # Vérification de l'état du serveur gRPC
    if not check_grpc_server_status(grpc_server):
        # Gérer l'erreur de connexion au serveur CLIP
        raise HTTPException(status_code=500, detail="Le serveur CLIP est indisponible. Veuillez réessayer plus tard.")
    else:
        try:
            if not url:
                raise HTTPException(status_code=400, detail="Veuillez fournir un URL.")

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
           raise HTTPException(status_code=400, detail="Une erreur inattendue s'est produite. Veuillez réessayer.")
